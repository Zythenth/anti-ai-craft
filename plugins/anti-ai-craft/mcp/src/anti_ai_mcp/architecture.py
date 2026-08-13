from __future__ import annotations

from typing import Any

from .evidence import (
    CheckError,
    CheckResult,
    CheckStatus,
    Confidence,
    Evidence,
    EvidenceKind,
    Finding,
    Severity,
)
from .git import DiffMode, GitInspector
from .graph import GraphOverview, GraphProvider, GraphProviderError, GraphStatus
from .graph_evidence import GraphEvidenceNormalizer, relation_direction
from .impact import GraphImpactAnalyzer, ImpactCandidate


MAX_ARCHITECTURE_COMMUNITIES = 100
MAX_ARCHITECTURE_HOTSPOTS = 20
MAX_ARCHITECTURE_CROSS_EDGES = 100
MAX_CYCLE_CHECKS = 20
MAX_CYCLE_HOPS = 6


class ArchitectureService:
    def __init__(self, git_inspector: GitInspector, graph_provider: GraphProvider) -> None:
        self.git_inspector = git_inspector
        self.graph_provider = graph_provider
        self.impact_analyzer = GraphImpactAnalyzer(graph_provider)

    def inspect(self) -> CheckResult:
        status = self.graph_provider.get_status()
        normalizer = GraphEvidenceNormalizer(status)
        graph_metadata = normalizer.graph_metadata()
        graph_evidence = Evidence(EvidenceKind.FACT, "graph provider status", graph_metadata)
        if not normalizer.usable:
            manual = Evidence(EvidenceKind.MANUAL_REVIEW_REQUIRED, "graph provider", graph_metadata)
            return CheckResult(
                CheckStatus.MANUAL_REVIEW_REQUIRED,
                "Architecture cannot be inspected because graph evidence is unavailable.",
                findings=(
                    Finding(
                        "AA-ARCH-INSPECT-001",
                        "architecture",
                        Severity.MEDIUM,
                        Confidence.HIGH,
                        "No usable graph is available for architecture inspection.",
                        (manual,),
                        suggestion="Enable or rebuild Graphify before requesting structural architecture evidence.",
                    ),
                ),
                evidence=(graph_evidence, manual),
                metadata={"graph": graph_metadata, "warnings": normalizer.warnings()},
            )
        try:
            overview = self.graph_provider.get_overview(
                max_communities=MAX_ARCHITECTURE_COMMUNITIES,
                max_hotspots=MAX_ARCHITECTURE_HOTSPOTS,
                max_cross_edges=MAX_ARCHITECTURE_CROSS_EDGES,
            )
        except GraphProviderError as exc:
            return CheckResult(
                CheckStatus.ERROR,
                "Architecture graph overview failed.",
                evidence=(graph_evidence,),
                errors=(CheckError("AA-ARCH-GRAPH", str(exc)),),
            )
        metadata = self._overview_metadata(overview, normalizer)
        findings: tuple[Finding, ...] = ()
        if overview.truncated:
            limit_evidence = Evidence(EvidenceKind.FACT, "architecture limits", metadata["limits"])
            findings = (
                Finding(
                    "AA-ARCH-INSPECT-002",
                    "architecture",
                    Severity.LOW,
                    Confidence.HIGH,
                    "Architecture overview reached an explicit output limit.",
                    (limit_evidence,),
                    suggestion="Use Graphify directly to investigate an omitted community or relationship.",
                ),
            )
        result_status = (
            CheckStatus.WARNING
            if normalizer.non_fresh or overview.truncated
            else CheckStatus.PASS
        )
        return CheckResult(
            result_status,
            (
                f"Inspected {len(overview.communities)} graph community/communities and "
                f"{len(overview.cross_community_edges)} bounded cross-community relation(s)."
            ),
            findings=findings,
            evidence=(graph_evidence,),
            metadata=metadata,
        )

    def audit(
        self,
        *,
        mode: DiffMode = "combined",
        graph_status: GraphStatus | None = None,
    ) -> CheckResult:
        try:
            snapshot = self.git_inspector.snapshot(mode)
        except (RuntimeError, ValueError) as exc:
            return CheckResult(
                CheckStatus.ERROR,
                "Architecture audit could not inspect Git changes.",
                errors=(CheckError("AA-ARCH-GIT", str(exc)),),
            )
        status = graph_status or self.graph_provider.get_status()
        normalizer = GraphEvidenceNormalizer(status)
        changed_files = tuple(
            dict.fromkeys(
                endpoint
                for change in snapshot.files
                if change.status != "deleted"
                for endpoint in change.endpoints()
            )
        )
        analysis = self.impact_analyzer.analyze(
            changed_files,
            max_depth=2,
            include_tests=False,
            graph_status=status,
        )
        graph_metadata = normalizer.graph_metadata(
            truncated=analysis.truncated,
            coverage=analysis.coverage,
        )
        graph_evidence = Evidence(EvidenceKind.FACT, "graph provider status", graph_metadata)
        if not changed_files:
            return CheckResult(
                CheckStatus.NOT_APPLICABLE,
                "No changed files require architecture auditing.",
                evidence=(graph_evidence,),
                metadata={
                    "graph": graph_metadata,
                    "warnings": analysis.warnings,
                    "structural_delta": _delta_policy(),
                },
            )
        if not normalizer.usable:
            manual = Evidence(EvidenceKind.MANUAL_REVIEW_REQUIRED, "graph provider", graph_metadata)
            return CheckResult(
                CheckStatus.MANUAL_REVIEW_REQUIRED,
                "Architecture audit has Git facts but no usable structural graph evidence.",
                findings=(
                    Finding(
                        "AA-ARCH-001",
                        "architecture",
                        Severity.MEDIUM,
                        Confidence.HIGH,
                        "Structural architecture conclusions are unavailable for the current change.",
                        (manual,),
                        suggestion="Enable or rebuild Graphify, or review the architecture manually.",
                    ),
                ),
                evidence=(graph_evidence, manual),
                metadata={
                    "graph": graph_metadata,
                    "warnings": analysis.warnings,
                    "structural_delta": _delta_policy(),
                },
            )

        new_paths = {
            change.path
            for change in snapshot.files
            if change.status in {"added", "untracked"}
        }
        seeds = {node.id: node for node in analysis.changed_nodes}
        new_cross: list[ImpactCandidate] = []
        undetermined_cross: list[ImpactCandidate] = []
        ignored_containment = 0
        for candidate in analysis.candidates:
            if candidate.distance != 1:
                continue
            if candidate.path_edges and _is_containment(candidate.path_edges[0].relation):
                ignored_containment += 1
                continue
            seed = seeds.get(candidate.path[0])
            if (
                seed is None
                or seed.community is None
                or candidate.node.community is None
                or seed.community == candidate.node.community
            ):
                continue
            if seed.source_file in new_paths:
                new_cross.append(candidate)
            else:
                undetermined_cross.append(candidate)

        findings: list[Finding] = []
        if new_cross:
            evidence = tuple(
                normalizer.edge(
                    candidate.path_edges[0],
                    direction=relation_direction(status, candidate.path_edges[0], candidate.path[0]),
                    distance=1,
                    traversal_source=candidate.path[0],
                    traversal_target=candidate.path[1],
                )
                for candidate in new_cross[:MAX_ARCHITECTURE_CROSS_EDGES]
            )
            confidence = (
                Confidence.MEDIUM
                if normalizer.non_fresh
                or any(item.kind is not EvidenceKind.FACT for item in evidence)
                else Confidence.HIGH
            )
            findings.append(
                Finding(
                    "AA-ARCH-002",
                    "architecture",
                    Severity.MEDIUM,
                    confidence,
                    (
                        f"New file(s) introduce {len(new_cross)} observed relation(s) across graph communities. "
                        "A graph community is a structural cluster, not automatically an architecture boundary."
                    ),
                    evidence,
                    suggestion="Confirm that each new cross-community relation is intended and covered by validation.",
                )
            )

        cycle_evidence = self._new_directed_cycles(new_paths, analysis, normalizer)
        if cycle_evidence:
            findings.append(
                Finding(
                    "AA-ARCH-003",
                    "architecture",
                    Severity.HIGH,
                    (
                        Confidence.MEDIUM
                        if normalizer.non_fresh
                        or any(item.kind is not EvidenceKind.FACT for item in cycle_evidence)
                        else Confidence.HIGH
                    ),
                    f"{len(cycle_evidence)} bounded directed cycle(s) involve a newly added file.",
                    tuple(cycle_evidence),
                    suggestion="Remove the new cycle or document and test the required cyclic dependency.",
                )
            )

        try:
            overview = self.graph_provider.get_overview(
                max_communities=MAX_ARCHITECTURE_COMMUNITIES,
                max_hotspots=MAX_ARCHITECTURE_HOTSPOTS,
                max_cross_edges=MAX_ARCHITECTURE_CROSS_EDGES,
            )
        except GraphProviderError:
            overview = GraphOverview()
        changed_hotspots = [
            hotspot
            for hotspot in overview.hotspots
            if hotspot.node.source_file in changed_files
        ]
        if changed_hotspots:
            evidence = tuple(
                Evidence(
                    EvidenceKind.HEURISTIC,
                    "graph degree ranking",
                    {
                        "node": hotspot.node.to_dict(),
                        "degree": hotspot.degree,
                        "freshness": status.freshness.value,
                    },
                )
                for hotspot in changed_hotspots
            )
            findings.append(
                Finding(
                    "AA-ARCH-004",
                    "architecture",
                    Severity.LOW,
                    Confidence.LOW if normalizer.non_fresh else Confidence.MEDIUM,
                    "The current change touches one or more nodes in the bounded graph hotspot ranking.",
                    evidence,
                    suggestion="Review callers and validation breadth; degree centrality does not prove a defect.",
                )
            )

        observations = {
            "new_cross_community_relations": len(new_cross),
            "existing_or_undetermined_cross_community_relations": len(undetermined_cross),
            "ignored_containment_relations": ignored_containment,
            "directed_cycles_checked": bool(
                status.capabilities.dependencies and status.capabilities.dependents
            ),
            "changed_hotspots": [hotspot.to_dict() for hotspot in changed_hotspots],
        }
        result_status = (
            CheckStatus.WARNING
            if findings or normalizer.non_fresh or analysis.truncated
            else CheckStatus.PASS
        )
        return CheckResult(
            result_status,
            f"Architecture audit produced {len(findings)} conservative finding(s).",
            findings=tuple(findings),
            evidence=(graph_evidence,),
            metadata={
                "graph": graph_metadata,
                "warnings": analysis.warnings,
                "observations": observations,
                "structural_delta": _delta_policy(),
                "limits": {
                    "max_cycle_checks": MAX_CYCLE_CHECKS,
                    "max_cycle_hops": MAX_CYCLE_HOPS,
                    "max_cross_edges": MAX_ARCHITECTURE_CROSS_EDGES,
                    "truncated": analysis.truncated,
                },
            },
        )

    def _overview_metadata(
        self,
        overview: GraphOverview,
        normalizer: GraphEvidenceNormalizer,
    ) -> dict[str, Any]:
        community_relations: dict[tuple[str, str], int] = {}
        for edge in overview.cross_community_edges:
            source = self.graph_provider.get_node(edge.source)
            target = self.graph_provider.get_node(edge.target)
            if source is None or target is None:
                continue
            pair = tuple(sorted((str(source.community), str(target.community))))
            community_relations[pair] = community_relations.get(pair, 0) + 1
        return {
            "graph": normalizer.graph_metadata(truncated=overview.truncated),
            "warnings": normalizer.warnings(),
            "communities": [community.to_dict() for community in overview.communities],
            "hotspots": [hotspot.to_dict() for hotspot in overview.hotspots],
            "relations_between_communities": [
                {
                    "source_community": pair[0],
                    "target_community": pair[1],
                    "bounded_edge_count": count,
                }
                for pair, count in sorted(community_relations.items())
            ],
            "cross_community_edges": [
                edge.to_dict() for edge in overview.cross_community_edges
            ],
            "possible_entrypoints": [],
            "entrypoint_limitation": (
                "No entrypoint is inferred from an undirected graph."
                if not overview.directed
                else "Entrypoints require repository-specific execution evidence and are not inferred from degree alone."
            ),
            "limits": {
                "max_communities": MAX_ARCHITECTURE_COMMUNITIES,
                "max_hotspots": MAX_ARCHITECTURE_HOTSPOTS,
                "max_cross_edges": MAX_ARCHITECTURE_CROSS_EDGES,
                "truncated": overview.truncated,
            },
        }

    def _new_directed_cycles(
        self,
        new_paths: set[str],
        analysis,
        normalizer: GraphEvidenceNormalizer,
    ) -> list[Evidence]:
        status = normalizer.status
        if not (status.capabilities.dependencies and status.capabilities.dependents):
            return []
        evidence: list[Evidence] = []
        seen: set[tuple[str, ...]] = set()
        for seed in analysis.changed_nodes:
            if seed.source_file not in new_paths or len(evidence) >= MAX_CYCLE_CHECKS:
                continue
            try:
                dependencies = self.graph_provider.get_dependencies(seed.id)
            except GraphProviderError:
                continue
            for target in dependencies.nodes:
                if target.id == seed.id or len(evidence) >= MAX_CYCLE_CHECKS:
                    continue
                try:
                    path = self.graph_provider.find_path(target.id, seed.id, max_hops=MAX_CYCLE_HOPS)
                except GraphProviderError:
                    continue
                if len(path.nodes) < 2 or not path.edges:
                    continue
                signature = tuple(node.id for node in path.nodes)
                if signature in seen:
                    continue
                seen.add(signature)
                direct = next(
                    (
                        edge
                        for edge in dependencies.edges
                        if edge.source == seed.id and edge.target == target.id
                    ),
                    None,
                )
                relations = ([direct] if direct is not None else []) + list(path.edges)
                kinds = {edge.evidence_kind for edge in relations}
                if EvidenceKind.MANUAL_REVIEW_REQUIRED in kinds:
                    evidence_kind = EvidenceKind.MANUAL_REVIEW_REQUIRED
                elif EvidenceKind.INFERENCE in kinds:
                    evidence_kind = EvidenceKind.INFERENCE
                elif EvidenceKind.HEURISTIC in kinds:
                    evidence_kind = EvidenceKind.HEURISTIC
                else:
                    evidence_kind = EvidenceKind.FACT
                evidence.append(
                    Evidence(
                        evidence_kind,
                        status.provider,
                        {
                            "graph_item": "directed_cycle",
                            "new_node": seed.id,
                            "path": [seed.id, *signature],
                            "relations": [edge.to_dict() for edge in relations],
                            "freshness": status.freshness.value,
                        },
                    )
                )
        return evidence


def _delta_policy() -> dict[str, Any]:
    return {
        "new_file_relations": "attributable when the graph contains a relation from a Git added/untracked file",
        "modified_file_relations": "existing versus introduced cannot be distinguished without a historical graph baseline",
        "historical_baseline": (
            "the compact Stage 4 baseline compares finding signatures; it does not copy graph "
            "edges or simulate modified-file structural deltas"
        ),
    }


def _is_containment(relation: str | None) -> bool:
    return (relation or "").casefold() in {"contains", "contains_section", "defined_in"}
