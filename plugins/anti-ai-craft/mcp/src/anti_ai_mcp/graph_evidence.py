from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .evidence import Confidence, Evidence, EvidenceKind
from .graph import GraphEdge, GraphFreshness, GraphNode, GraphStatus


@dataclass(frozen=True)
class GraphEvidenceNormalizer:
    status: GraphStatus

    @property
    def usable(self) -> bool:
        return self.status.availability.value in {"available", "stale"}

    @property
    def non_fresh(self) -> bool:
        return self.status.freshness in {
            GraphFreshness.AVAILABLE_BUT_STALE,
            GraphFreshness.UNKNOWN_FRESHNESS,
        }

    def graph_metadata(
        self,
        *,
        truncated: bool = False,
        coverage: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        return {
            "provider": self.status.provider,
            "availability": self.status.availability.value,
            "freshness": self.status.freshness.value,
            "node_count": self.status.node_count,
            "edge_count": self.status.edge_count,
            "directed": bool(
                self.status.capabilities.dependencies
                and self.status.capabilities.dependents
            ),
            "truncated": truncated,
            "coverage": coverage or {},
            "detail": self.status.detail,
        }

    def warnings(self) -> list[str]:
        warnings: list[str] = []
        if not self.usable:
            warnings.append(
                f"Graph evidence is unavailable ({self.status.availability.value})."
            )
        elif self.status.freshness is GraphFreshness.AVAILABLE_BUT_STALE:
            warnings.append("Graph evidence is available but stale; freshness-sensitive conclusions are reduced.")
        elif self.status.freshness is GraphFreshness.UNKNOWN_FRESHNESS:
            warnings.append("Graph freshness is unknown; structural conclusions require caution.")
        if self.usable and not (
            self.status.capabilities.dependencies
            and self.status.capabilities.dependents
        ):
            warnings.append(
                "Graph direction is unknown; relationships are reported as structural adjacency, not dependencies or dependents."
            )
        return warnings

    def confidence(
        self,
        kind: EvidenceKind,
        *,
        distance: int = 1,
    ) -> Confidence:
        if kind is EvidenceKind.MANUAL_REVIEW_REQUIRED:
            return Confidence.LOW
        if kind is EvidenceKind.INFERENCE or distance > 1:
            return Confidence.LOW if self.non_fresh else Confidence.MEDIUM
        if kind is EvidenceKind.HEURISTIC:
            return Confidence.LOW if self.non_fresh else Confidence.MEDIUM
        return Confidence.MEDIUM if self.non_fresh else Confidence.HIGH

    def node(self, node: GraphNode, *, role: str) -> Evidence:
        return Evidence(
            node.evidence_kind,
            self.status.provider,
            {
                "graph_item": "node",
                "role": role,
                "id": node.id,
                "label": node.label,
                "source_file": node.source_file,
                "source_location": node.source_location,
                "community": node.community,
                "community_name": node.community_name,
                "graph_provenance": _graph_provenance(node.provenance),
                "freshness": self.status.freshness.value,
            },
            node.provenance,
        )

    def edge(
        self,
        edge: GraphEdge,
        *,
        direction: str,
        distance: int,
        traversal_source: str,
        traversal_target: str,
    ) -> Evidence:
        provenance = dict(edge.provenance)
        if edge.confidence is not None:
            provenance.setdefault("confidence", edge.confidence)
        if edge.confidence_score is not None:
            provenance.setdefault("confidence_score", edge.confidence_score)
        return Evidence(
            edge.evidence_kind,
            self.status.provider,
            {
                "graph_item": "relation",
                "source": edge.source,
                "target": edge.target,
                "relation": edge.relation,
                "direction": direction,
                "traversal_source": traversal_source,
                "traversal_target": traversal_target,
                "distance": distance,
                "graph_provenance": edge.confidence or _graph_provenance(edge.provenance),
                "freshness": self.status.freshness.value,
                "confidence": self.confidence(edge.evidence_kind, distance=distance).value,
                "source_file": edge.source_file,
                "source_location": edge.source_location,
            },
            provenance,
        )


def relation_direction(status: GraphStatus, edge: GraphEdge, origin: str) -> str:
    if not (status.capabilities.dependencies and status.capabilities.dependents):
        return "UNKNOWN"
    if edge.source == origin:
        return "OUTGOING"
    if edge.target == origin:
        return "INCOMING"
    return "UNKNOWN"


def _graph_provenance(provenance: dict[str, Any]) -> str | None:
    value = provenance.get("confidence") or provenance.get("provenance")
    return str(value) if value is not None else None
