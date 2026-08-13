from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from pathlib import PurePosixPath
from typing import Any, Iterable

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
from .graph import GraphEdge, GraphNode, GraphProvider, GraphProviderError, GraphStatus
from .graph_evidence import GraphEvidenceNormalizer, relation_direction
from .paths import PathBoundaryError, normalize_repository_path


MAX_CHANGED_FILES = 100
MAX_DEPTH = 3
MAX_NODES_PER_FILE = 100
MAX_IMPACT_NODES = 200
MAX_IMPACT_EDGES = 400
MAX_CROSS_COMMUNITY_PATHS = 50


@dataclass(frozen=True)
class ImpactCandidate:
    node: GraphNode
    distance: int
    level: str
    evidence_kind: EvidenceKind
    confidence: Confidence
    path: tuple[str, ...]
    path_edges: tuple[GraphEdge, ...]
    reasons: tuple[str, ...]

    def to_dict(self, normalizer: GraphEvidenceNormalizer) -> dict[str, Any]:
        edge_evidence = []
        for index, edge in enumerate(self.path_edges):
            origin = self.path[index]
            following = self.path[index + 1]
            edge_evidence.append(
                normalizer.edge(
                    edge,
                    direction=relation_direction(normalizer.status, edge, origin),
                    distance=index + 1,
                    traversal_source=origin,
                    traversal_target=following,
                ).to_dict()
            )
        return {
            "node": self.node.to_dict(),
            "distance": self.distance,
            "impact": self.level,
            "evidence_kind": self.evidence_kind.value,
            "confidence": self.confidence.value,
            "path": list(self.path),
            "relations": edge_evidence,
            "ranking_reasons": list(self.reasons),
        }


@dataclass(frozen=True)
class ImpactAnalysis:
    changed_files: tuple[str, ...]
    changed_nodes: tuple[GraphNode, ...]
    candidates: tuple[ImpactCandidate, ...]
    affected_communities: tuple[dict[str, Any], ...]
    cross_community_paths: tuple[dict[str, Any], ...]
    candidate_tests: tuple[dict[str, Any], ...]
    coverage: dict[str, Any]
    warnings: tuple[str, ...]
    risk: str
    risk_reasons: tuple[str, ...]
    truncated: bool
    limits: dict[str, int]

    def to_metadata(self, normalizer: GraphEvidenceNormalizer) -> dict[str, Any]:
        direct = [
            candidate.to_dict(normalizer)
            for candidate in self.candidates
            if candidate.distance == 1
        ]
        indirect = [
            candidate.to_dict(normalizer)
            for candidate in self.candidates
            if candidate.distance > 1
        ]
        return {
            "changed_files": list(self.changed_files),
            "changed_nodes": [node.to_dict() for node in self.changed_nodes],
            "direct_structural_neighbors": direct,
            "indirectly_reachable_nodes": indirect,
            "affected_graph_communities": list(self.affected_communities),
            "cross_community_paths": list(self.cross_community_paths),
            "candidate_affected_tests": list(self.candidate_tests),
            "risk": self.risk,
            "risk_reasons": list(self.risk_reasons),
            "warnings": list(self.warnings),
            "graph": normalizer.graph_metadata(
                truncated=self.truncated,
                coverage=self.coverage,
            ),
            "limits": {**self.limits, "truncated": self.truncated},
        }


class GraphImpactAnalyzer:
    def __init__(self, graph_provider: GraphProvider) -> None:
        self.graph_provider = graph_provider

    def analyze(
        self,
        changed_files: Iterable[str],
        *,
        max_depth: int = 2,
        include_tests: bool = True,
        graph_status: GraphStatus | None = None,
    ) -> ImpactAnalysis:
        requested_files = tuple(
            dict.fromkeys(normalize_repository_path(path) for path in changed_files)
        )
        files = requested_files[:MAX_CHANGED_FILES]
        input_truncated = len(requested_files) > MAX_CHANGED_FILES
        status = graph_status or self.graph_provider.get_status()
        normalizer = GraphEvidenceNormalizer(status)
        warnings = normalizer.warnings()
        if input_truncated:
            warnings.append(
                f"Only the first {MAX_CHANGED_FILES} changed files were analyzed."
            )
        limits = {
            "max_depth": max_depth,
            "max_changed_files": MAX_CHANGED_FILES,
            "max_nodes_per_file": MAX_NODES_PER_FILE,
            "max_impact_nodes": MAX_IMPACT_NODES,
            "max_impact_edges": MAX_IMPACT_EDGES,
            "max_cross_community_paths": MAX_CROSS_COMMUNITY_PATHS,
        }
        if not normalizer.usable:
            return ImpactAnalysis(
                files,
                (),
                (),
                (),
                (),
                (),
                _coverage(files, set(), (), requested_count=len(requested_files)),
                tuple(warnings),
                "UNKNOWN",
                ("Graph evidence is unavailable.",),
                False,
                limits,
            )

        seeds: dict[str, GraphNode] = {}
        file_matches: set[str] = set()
        truncated = input_truncated
        for path in files:
            try:
                result = self.graph_provider.get_nodes_for_file(path, limit=MAX_NODES_PER_FILE)
            except GraphProviderError as exc:
                warnings.append(f"Graph lookup failed for {path}: {exc}")
                continue
            if result.nodes:
                file_matches.add(path)
            truncated = truncated or result.truncated
            if result.nodes:
                # The file node is the stable change anchor. Seeding every symbol
                # consumes the traversal budget before external impact is visited.
                seeds.setdefault(result.nodes[0].id, result.nodes[0])

        nodes: dict[str, GraphNode] = dict(seeds)
        paths: dict[str, tuple[str, ...]] = {node_id: (node_id,) for node_id in seeds}
        path_edges: dict[str, tuple[GraphEdge, ...]] = {node_id: () for node_id in seeds}
        distances: dict[str, int] = {node_id: 0 for node_id in seeds}
        queue = deque(sorted(seeds))
        processed_edges = 0
        while queue:
            current = queue.popleft()
            distance = distances[current]
            if distance >= max_depth:
                continue
            try:
                neighborhood = self.graph_provider.get_neighbors(
                    current,
                    direction="both",
                    limit=max(1, MAX_IMPACT_EDGES - processed_edges),
                )
            except GraphProviderError as exc:
                warnings.append(f"Graph traversal stopped at {current}: {exc}")
                truncated = True
                break
            truncated = truncated or neighborhood.truncated
            neighbor_nodes = {node.id: node for node in neighborhood.nodes}
            ordered_edges = sorted(
                neighborhood.edges,
                key=lambda edge: (edge.source, edge.target, edge.relation or ""),
            )
            for edge in ordered_edges:
                if processed_edges >= MAX_IMPACT_EDGES:
                    truncated = True
                    queue.clear()
                    break
                processed_edges += 1
                following = _other_endpoint(edge, current)
                if following is None or following in seeds:
                    continue
                next_distance = distance + 1
                if following in distances and distances[following] <= next_distance:
                    continue
                if following not in nodes and len(nodes) >= MAX_IMPACT_NODES:
                    truncated = True
                    queue.clear()
                    break
                node = neighbor_nodes.get(following)
                if node is None:
                    try:
                        node = self.graph_provider.get_node(following)
                    except GraphProviderError:
                        node = None
                if node is None:
                    continue
                nodes[following] = node
                distances[following] = next_distance
                paths[following] = (*paths[current], following)
                path_edges[following] = (*path_edges[current], edge)
                queue.append(following)

        candidates = []
        for node_id, node in nodes.items():
            distance = distances[node_id]
            if distance == 0:
                continue
            edges = path_edges[node_id]
            kind = _path_evidence_kind(edges, distance)
            level = _impact_level(distance, kind, normalizer.non_fresh)
            seed = seeds[paths[node_id][0]]
            reasons = _ranking_reasons(node, seed, distance, kind)
            candidates.append(
                ImpactCandidate(
                    node=node,
                    distance=distance,
                    level=level,
                    evidence_kind=kind,
                    confidence=normalizer.confidence(kind, distance=distance),
                    path=paths[node_id],
                    path_edges=edges,
                    reasons=tuple(reasons),
                )
            )
        candidates.sort(key=_candidate_rank)

        communities = _communities(tuple(seeds.values()), tuple(candidates))
        cross_paths = _cross_community_paths(tuple(seeds.values()), tuple(candidates))
        if len(cross_paths) > MAX_CROSS_COMMUNITY_PATHS:
            cross_paths = cross_paths[:MAX_CROSS_COMMUNITY_PATHS]
            truncated = True
        candidate_tests = _candidate_tests(tuple(candidates)) if include_tests else ()
        risk, risk_reasons = _impact_risk(tuple(candidates), communities, cross_paths, truncated)
        if truncated:
            warnings.append("Impact output reached an explicit traversal or output limit.")
        coverage = _coverage(
            files,
            file_matches,
            tuple(seeds.values()),
            requested_count=len(requested_files),
        )
        if coverage["missing_files"]:
            warnings.append(
                f"{len(coverage['missing_files'])} changed file(s) have no matching graph node."
            )
        return ImpactAnalysis(
            files,
            tuple(sorted(seeds.values(), key=lambda node: (node.source_file or "", node.label, node.id))),
            tuple(candidates),
            communities,
            tuple(cross_paths),
            candidate_tests,
            coverage,
            tuple(dict.fromkeys(warnings)),
            risk,
            risk_reasons,
            truncated,
            limits,
        )


class ChangeImpactService:
    def __init__(self, git_inspector: GitInspector, graph_provider: GraphProvider) -> None:
        self.git_inspector = git_inspector
        self.graph_provider = graph_provider
        self.analyzer = GraphImpactAnalyzer(graph_provider)

    def analyze(
        self,
        *,
        changed_files: Iterable[str] | None = None,
        max_depth: int = 2,
        include_tests: bool = True,
        mode: DiffMode = "combined",
    ) -> CheckResult:
        if max_depth < 1 or max_depth > MAX_DEPTH:
            return CheckResult(
                CheckStatus.ERROR,
                "Change-impact depth is outside the allowed range.",
                errors=(CheckError("AA-IMPACT-INPUT", f"max_depth must be between 1 and {MAX_DEPTH}"),),
            )
        try:
            if changed_files is None:
                snapshot = self.git_inspector.snapshot(mode)
                files = tuple(
                    dict.fromkeys(
                        endpoint
                        for change in snapshot.files
                        for endpoint in change.endpoints()
                    )
                )
            else:
                files = tuple(
                    dict.fromkeys(normalize_repository_path(str(path)) for path in changed_files)
                )
            if len(files) > MAX_CHANGED_FILES:
                raise ValueError(f"at most {MAX_CHANGED_FILES} changed files may be analyzed")
            graph_status = self.graph_provider.get_status()
            analysis = self.analyzer.analyze(
                files,
                max_depth=max_depth,
                include_tests=include_tests,
                graph_status=graph_status,
            )
        except (PathBoundaryError, RuntimeError, ValueError) as exc:
            return CheckResult(
                CheckStatus.ERROR,
                "Change impact could not be analyzed.",
                errors=(CheckError("AA-IMPACT-INPUT", str(exc)),),
            )
        normalizer = GraphEvidenceNormalizer(graph_status)
        metadata = analysis.to_metadata(normalizer)
        graph_evidence = Evidence(
            EvidenceKind.FACT,
            "graph provider status",
            metadata["graph"],
        )
        if not files:
            return CheckResult(
                CheckStatus.NOT_APPLICABLE,
                "No changed files require structural impact analysis.",
                evidence=(graph_evidence,),
                metadata=metadata,
            )
        if not normalizer.usable:
            manual = Evidence(
                EvidenceKind.MANUAL_REVIEW_REQUIRED,
                "graph provider",
                metadata["graph"],
            )
            return CheckResult(
                CheckStatus.MANUAL_REVIEW_REQUIRED,
                "Structural impact cannot be concluded because graph evidence is unavailable.",
                findings=(
                    Finding(
                        "AA-IMPACT-001",
                        "change-impact",
                        Severity.MEDIUM,
                        Confidence.HIGH,
                        "No usable graph is available for structural impact analysis.",
                        (manual,),
                        suggestion="Rebuild or enable Graphify, then rerun the bounded impact analysis.",
                    ),
                ),
                evidence=(graph_evidence, manual),
                metadata=metadata,
            )
        if not analysis.changed_nodes:
            missing = Evidence(
                EvidenceKind.MANUAL_REVIEW_REQUIRED,
                "graph coverage",
                analysis.coverage,
            )
            return CheckResult(
                CheckStatus.MANUAL_REVIEW_REQUIRED,
                "No changed file could be mapped to a graph node.",
                findings=(
                    Finding(
                        "AA-IMPACT-002",
                        "change-impact",
                        Severity.MEDIUM,
                        Confidence.HIGH,
                        "The graph does not cover any requested changed file.",
                        (missing,),
                        suggestion="Update Graphify or inspect the changed files manually.",
                    ),
                ),
                evidence=(graph_evidence, missing),
                metadata=metadata,
            )

        findings: list[Finding] = []
        if analysis.truncated:
            limit_evidence = Evidence(EvidenceKind.FACT, "impact limits", analysis.limits)
            findings.append(
                Finding(
                    "AA-IMPACT-004",
                    "change-impact",
                    Severity.LOW,
                    Confidence.HIGH,
                    "Structural impact output reached an explicit limit.",
                    (limit_evidence,),
                    suggestion="Narrow the changed files or reduce max_depth for a complete bounded result.",
                )
            )
        result_status = (
            CheckStatus.WARNING
            if normalizer.non_fresh or analysis.truncated or analysis.coverage["missing_files"]
            else CheckStatus.PASS
        )
        return CheckResult(
            result_status,
            (
                f"Mapped {analysis.coverage['matched_files']} of {len(files)} changed file(s) "
                f"to {len(analysis.candidates)} bounded structural impact candidate(s)."
            ),
            findings=tuple(findings),
            evidence=(graph_evidence,),
            metadata=metadata,
        )


def _other_endpoint(edge: GraphEdge, current: str) -> str | None:
    if edge.source == current:
        return edge.target
    if edge.target == current:
        return edge.source
    return None


def _path_evidence_kind(edges: tuple[GraphEdge, ...], distance: int) -> EvidenceKind:
    kinds = {edge.evidence_kind for edge in edges}
    if EvidenceKind.MANUAL_REVIEW_REQUIRED in kinds:
        return EvidenceKind.MANUAL_REVIEW_REQUIRED
    if EvidenceKind.INFERENCE in kinds or distance > 1:
        return EvidenceKind.INFERENCE
    if EvidenceKind.HEURISTIC in kinds:
        return EvidenceKind.HEURISTIC
    return EvidenceKind.FACT


def _impact_level(distance: int, kind: EvidenceKind, non_fresh: bool) -> str:
    if distance == 1:
        return "DIRECT"
    if distance == 2 and kind is EvidenceKind.INFERENCE and not non_fresh:
        return "LIKELY_INDIRECT"
    return "POSSIBLE"


def _ranking_reasons(
    node: GraphNode,
    seed: GraphNode,
    distance: int,
    kind: EvidenceKind,
) -> list[str]:
    reasons = ["direct relation" if distance == 1 else f"graph distance {distance}"]
    if kind is EvidenceKind.FACT:
        reasons.append("all traversed relations are extracted")
    elif kind is EvidenceKind.INFERENCE:
        reasons.append("impact propagation or an inferred relation requires caution")
    if seed.community is not None and seed.community == node.community:
        reasons.append("same graph community as the changed node")
    elif seed.community is not None and node.community is not None:
        reasons.append("crosses a graph community boundary")
    if node.source_file and _is_test_path(node.source_file):
        reasons.append("candidate is a test")
    return reasons


def _candidate_rank(candidate: ImpactCandidate) -> tuple[Any, ...]:
    kind_rank = {
        EvidenceKind.FACT: 0,
        EvidenceKind.HEURISTIC: 1,
        EvidenceKind.INFERENCE: 2,
        EvidenceKind.MANUAL_REVIEW_REQUIRED: 3,
    }
    return (
        candidate.distance,
        kind_rank[candidate.evidence_kind],
        0 if candidate.node.source_file and _is_test_path(candidate.node.source_file) else 1,
        candidate.node.source_file or "",
        candidate.node.label,
        candidate.node.id,
    )


def _communities(
    changed_nodes: tuple[GraphNode, ...],
    candidates: tuple[ImpactCandidate, ...],
) -> tuple[dict[str, Any], ...]:
    grouped: dict[str, dict[str, Any]] = {}
    for role, nodes in (
        ("changed_nodes", changed_nodes),
        ("impact_candidates", tuple(candidate.node for candidate in candidates)),
    ):
        for node in nodes:
            if node.community is None:
                continue
            key = str(node.community)
            item = grouped.setdefault(
                key,
                {
                    "community": node.community,
                    "community_name": node.community_name,
                    "changed_nodes": 0,
                    "impact_candidates": 0,
                },
            )
            item[role] += 1
    return tuple(sorted(grouped.values(), key=lambda item: str(item["community"])))


def _cross_community_paths(
    changed_nodes: tuple[GraphNode, ...],
    candidates: tuple[ImpactCandidate, ...],
) -> list[dict[str, Any]]:
    by_id = {node.id: node for node in changed_nodes}
    paths = []
    for candidate in candidates:
        seed = by_id.get(candidate.path[0])
        if (
            seed is None
            or seed.community is None
            or candidate.node.community is None
            or seed.community == candidate.node.community
        ):
            continue
        paths.append(
            {
                "path": list(candidate.path),
                "distance": candidate.distance,
                "source_community": seed.community,
                "target_community": candidate.node.community,
                "evidence_kind": candidate.evidence_kind.value,
                "confidence": candidate.confidence.value,
            }
        )
    paths.sort(key=lambda item: (item["distance"], str(item["source_community"]), str(item["target_community"]), item["path"]))
    return paths


def _candidate_tests(candidates: tuple[ImpactCandidate, ...]) -> tuple[dict[str, Any], ...]:
    selected: dict[str, ImpactCandidate] = {}
    for candidate in candidates:
        source_file = candidate.node.source_file
        if source_file and _is_test_path(source_file):
            selected.setdefault(source_file, candidate)
    return tuple(
        {
            "test_path": path,
            "graph_distance": candidate.distance,
            "impact": candidate.level,
            "evidence_kind": candidate.evidence_kind.value,
            "confidence": candidate.confidence.value,
            "selection_reason": "; ".join(candidate.reasons),
            "path": list(candidate.path),
        }
        for path, candidate in sorted(selected.items())
    )


def _impact_risk(
    candidates: tuple[ImpactCandidate, ...],
    communities: tuple[dict[str, Any], ...],
    cross_paths: list[dict[str, Any]],
    truncated: bool,
) -> tuple[str, tuple[str, ...]]:
    direct = sum(candidate.distance == 1 for candidate in candidates)
    if any(path["distance"] == 1 for path in cross_paths) or len(communities) >= 3:
        return "HIGH", (
            "Direct impact crosses a graph community or at least three communities are involved.",
        )
    if candidates or truncated:
        reasons = []
        if direct:
            reasons.append(f"{direct} direct structural neighbor(s) were found.")
        if truncated:
            reasons.append("Traversal was truncated, so additional impact may exist.")
        if not reasons:
            reasons.append("Only bounded indirect structural impact was found.")
        return "MEDIUM", tuple(reasons)
    return "LOW", ("No structural neighbor was found within the bounded traversal.",)


def _coverage(
    files: tuple[str, ...],
    matched_files: set[str],
    changed_nodes: tuple[GraphNode, ...],
    *,
    requested_count: int | None = None,
) -> dict[str, Any]:
    return {
        "changed_files": requested_count if requested_count is not None else len(files),
        "analyzed_files": len(files),
        "matched_files": len(matched_files),
        "missing_files": sorted(set(files) - matched_files),
        "changed_nodes": len(changed_nodes),
    }


def _is_test_path(path: str) -> bool:
    pure = PurePosixPath(path)
    parts = {part.lower() for part in pure.parts}
    name = pure.name.lower()
    return (
        "tests" in parts
        or "test" in parts
        or "__tests__" in parts
        or name.startswith("test_")
        or ".test." in name
        or ".spec." in name
    )
