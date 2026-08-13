from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from enum import StrEnum
from pathlib import Path
from typing import Any, Callable, Literal, Protocol

import networkx as nx
from networkx.readwrite import json_graph

from .evidence import EvidenceKind
from .paths import PathBoundaryError, resolve_within_repository


MAX_GRAPH_BYTES = 64 * 1024 * 1024


class GraphAvailability(StrEnum):
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    STALE = "stale"
    INVALID = "invalid"
    DISABLED = "disabled"


class GraphFreshness(StrEnum):
    AVAILABLE_AND_FRESH = "available_and_fresh"
    AVAILABLE_BUT_STALE = "available_but_stale"
    UNKNOWN_FRESHNESS = "unknown_freshness"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class GraphCapabilities:
    query: bool = False
    node: bool = False
    neighbors: bool = False
    dependencies: bool = False
    dependents: bool = False
    paths: bool = False
    communities: bool = False

    def to_dict(self) -> dict[str, bool]:
        return asdict(self)


@dataclass(frozen=True)
class GraphStatus:
    provider: str
    availability: GraphAvailability
    freshness: GraphFreshness
    graph_path: str | None
    capabilities: GraphCapabilities
    node_count: int | None = None
    edge_count: int | None = None
    detail: str | None = None

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["availability"] = self.availability.value
        result["freshness"] = self.freshness.value
        return result


@dataclass(frozen=True)
class GraphNode:
    id: str
    label: str
    source_file: str | None = None
    source_location: str | None = None
    file_type: str | None = None
    community: int | str | None = None
    community_name: str | None = None
    evidence_kind: EvidenceKind = EvidenceKind.MANUAL_REVIEW_REQUIRED
    provenance: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["evidence_kind"] = self.evidence_kind.value
        return result


@dataclass(frozen=True)
class GraphEdge:
    source: str
    target: str
    relation: str | None = None
    evidence_kind: EvidenceKind = EvidenceKind.MANUAL_REVIEW_REQUIRED
    confidence: str | None = None
    confidence_score: float | None = None
    source_file: str | None = None
    source_location: str | None = None
    provenance: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        result = asdict(self)
        result["evidence_kind"] = self.evidence_kind.value
        return result


@dataclass(frozen=True)
class GraphQueryResult:
    nodes: tuple[GraphNode, ...] = ()
    edges: tuple[GraphEdge, ...] = ()
    truncated: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "nodes": [node.to_dict() for node in self.nodes],
            "edges": [edge.to_dict() for edge in self.edges],
            "truncated": self.truncated,
        }


class GraphProviderError(RuntimeError):
    pass


class GraphUnavailableError(GraphProviderError):
    pass


class GraphAmbiguousNodeError(GraphProviderError):
    pass


class GraphProvider(Protocol):
    def get_status(self) -> GraphStatus: ...

    def query(self, text: str, *, limit: int = 20) -> GraphQueryResult: ...

    def get_node(self, identifier: str) -> GraphNode | None: ...

    def get_neighbors(
        self,
        identifier: str,
        *,
        direction: Literal["incoming", "outgoing", "both"] = "both",
    ) -> GraphQueryResult: ...

    def get_dependencies(self, identifier: str) -> GraphQueryResult: ...

    def get_dependents(self, identifier: str) -> GraphQueryResult: ...

    def find_path(self, source: str, target: str, *, max_hops: int = 8) -> GraphQueryResult: ...

    def get_community(self, community: int | str) -> GraphQueryResult: ...


class NullGraphProvider:
    def __init__(self, status: GraphStatus | None = None) -> None:
        self._status = status or GraphStatus(
            provider="none",
            availability=GraphAvailability.UNAVAILABLE,
            freshness=GraphFreshness.UNAVAILABLE,
            graph_path=None,
            capabilities=GraphCapabilities(),
            detail="no graph provider is configured",
        )

    def get_status(self) -> GraphStatus:
        return self._status

    def _unavailable(self) -> GraphUnavailableError:
        return GraphUnavailableError(self._status.detail or self._status.availability.value)

    def query(self, text: str, *, limit: int = 20) -> GraphQueryResult:
        raise self._unavailable()

    def get_node(self, identifier: str) -> GraphNode | None:
        raise self._unavailable()

    def get_neighbors(
        self,
        identifier: str,
        *,
        direction: Literal["incoming", "outgoing", "both"] = "both",
    ) -> GraphQueryResult:
        raise self._unavailable()

    def get_dependencies(self, identifier: str) -> GraphQueryResult:
        raise self._unavailable()

    def get_dependents(self, identifier: str) -> GraphQueryResult:
        raise self._unavailable()

    def find_path(self, source: str, target: str, *, max_hops: int = 8) -> GraphQueryResult:
        raise self._unavailable()

    def get_community(self, community: int | str) -> GraphQueryResult:
        raise self._unavailable()


FreshnessProbe = Callable[[Path, Path, str], tuple[GraphFreshness, str | None]]


def graphify_freshness_probe(
    repository_root: Path,
    graph_path: Path,
    freshness_kind: str,
) -> tuple[GraphFreshness, str | None]:
    manifest_path = graph_path.parent / "manifest.json"
    if not manifest_path.is_file():
        return GraphFreshness.UNKNOWN_FRESHNESS, "Graphify manifest is missing"
    try:
        from graphify.detect import detect_incremental
    except ImportError:
        return GraphFreshness.UNKNOWN_FRESHNESS, "Graphify is not installed"
    try:
        result = detect_incremental(
            repository_root,
            manifest_path=str(manifest_path),
            kind=freshness_kind,
        )
    except Exception as exc:
        return GraphFreshness.UNKNOWN_FRESHNESS, f"Graphify freshness check failed: {exc}"
    if freshness_kind == "ast":
        changed = len(result.get("new_files", {}).get("code", []))
        scope = "code "
    else:
        changed = int(result.get("new_total", 0))
        scope = ""
    deleted = len(result.get("deleted_files", []))
    if changed or deleted:
        return (
            GraphFreshness.AVAILABLE_BUT_STALE,
            f"Graphify detected {changed} changed/new {scope}and {deleted} deleted file(s)",
        )
    return GraphFreshness.AVAILABLE_AND_FRESH, "Graphify manifest matches the repository"


class GraphifyProvider:
    def __init__(
        self,
        repository_root: Path,
        graph_path: str | Path = "graphify-out/graph.json",
        *,
        freshness_kind: Literal["ast", "semantic"] = "semantic",
        freshness_probe: FreshnessProbe = graphify_freshness_probe,
    ) -> None:
        self.repository_root = repository_root.resolve(strict=True)
        self.graph_path = resolve_within_repository(self.repository_root, graph_path)
        self.freshness_kind = freshness_kind
        self._freshness_probe = freshness_probe
        self._graph: nx.Graph | None = None
        self._file_signature: tuple[int, int] | None = None
        self._invalid_detail: str | None = None

    def _load(self) -> nx.Graph:
        try:
            stat = self.graph_path.stat()
        except FileNotFoundError as exc:
            self._graph = None
            self._file_signature = None
            self._invalid_detail = None
            raise GraphUnavailableError(f"graph not found: {self.graph_path}") from exc
        signature = (stat.st_mtime_ns, stat.st_size)
        if signature == self._file_signature:
            if self._graph is not None:
                return self._graph
            if self._invalid_detail is not None:
                raise GraphProviderError(self._invalid_detail)
        if stat.st_size > MAX_GRAPH_BYTES:
            self._graph = None
            self._file_signature = signature
            self._invalid_detail = f"graph exceeds {MAX_GRAPH_BYTES} byte limit"
            raise GraphProviderError(self._invalid_detail)
        try:
            payload = json.loads(self.graph_path.read_text(encoding="utf-8"))
            normalized = self._validate_payload(payload)
            logical_directed = bool(normalized.get("directed", False))
            # Graphify stores relation arc order even for a logically undirected
            # graph. Preserve both facts exactly as its official loader does.
            normalized = {**normalized, "directed": True}
            try:
                graph = json_graph.node_link_graph(normalized, edges="links")
            except TypeError:
                graph = json_graph.node_link_graph(normalized)
            graph.graph["_logical_directed"] = logical_directed
        except (OSError, UnicodeError, json.JSONDecodeError, TypeError, ValueError, KeyError) as exc:
            self._graph = None
            self._file_signature = signature
            self._invalid_detail = f"invalid Graphify graph: {exc}"
            raise GraphProviderError(self._invalid_detail) from exc
        self._graph = graph
        self._file_signature = signature
        self._invalid_detail = None
        return graph

    @staticmethod
    def _validate_payload(payload: Any) -> dict[str, Any]:
        if not isinstance(payload, dict):
            raise ValueError("top level must be an object")
        nodes = payload.get("nodes")
        links = payload.get("links", payload.get("edges"))
        if not isinstance(nodes, list) or not isinstance(links, list):
            raise ValueError("nodes and links/edges must be arrays")
        node_ids: set[str] = set()
        for node in nodes:
            if not isinstance(node, dict) or not isinstance(node.get("id"), str):
                raise ValueError("every node must have a string id")
            if node["id"] in node_ids:
                raise ValueError(f"duplicate node id: {node['id']}")
            node_ids.add(node["id"])
        for link in links:
            if not isinstance(link, dict):
                raise ValueError("every edge must be an object")
            source, target = link.get("source"), link.get("target")
            if not isinstance(source, str) or not isinstance(target, str):
                raise ValueError("every edge must have string source and target")
            if source not in node_ids or target not in node_ids:
                raise ValueError(f"edge endpoint is missing: {source} -> {target}")
        normalized = dict(payload)
        normalized["links"] = links
        return normalized

    def get_status(self) -> GraphStatus:
        try:
            graph = self._load()
        except GraphUnavailableError as exc:
            return GraphStatus(
                provider="graphify",
                availability=GraphAvailability.UNAVAILABLE,
                freshness=GraphFreshness.UNAVAILABLE,
                graph_path=str(self.graph_path),
                capabilities=GraphCapabilities(),
                detail=str(exc),
            )
        except GraphProviderError as exc:
            return GraphStatus(
                provider="graphify",
                availability=GraphAvailability.INVALID,
                freshness=GraphFreshness.UNAVAILABLE,
                graph_path=str(self.graph_path),
                capabilities=GraphCapabilities(),
                detail=str(exc),
            )
        freshness, detail = self._freshness_probe(
            self.repository_root,
            self.graph_path,
            self.freshness_kind,
        )
        availability = (
            GraphAvailability.STALE
            if freshness == GraphFreshness.AVAILABLE_BUT_STALE
            else GraphAvailability.AVAILABLE
        )
        directed = bool(graph.graph.get("_logical_directed", graph.is_directed()))
        communities = any(data.get("community") is not None for _, data in graph.nodes(data=True))
        return GraphStatus(
            provider="graphify",
            availability=availability,
            freshness=freshness,
            graph_path=str(self.graph_path),
            capabilities=GraphCapabilities(
                query=True,
                node=True,
                neighbors=True,
                dependencies=directed,
                dependents=directed,
                paths=True,
                communities=communities,
            ),
            node_count=graph.number_of_nodes(),
            edge_count=graph.number_of_edges(),
            detail=detail,
        )

    def _require_graph(self) -> nx.Graph:
        try:
            return self._load()
        except GraphProviderError as exc:
            raise GraphUnavailableError(str(exc)) from exc

    @staticmethod
    def _provenance(data: dict[str, Any]) -> dict[str, Any]:
        keys = (
            "confidence",
            "confidence_score",
            "provenance",
            "source_url",
            "captured_at",
            "author",
            "contributor",
        )
        return {key: data[key] for key in keys if key in data}

    @staticmethod
    def _evidence_kind(data: dict[str, Any]) -> EvidenceKind:
        label = str(data.get("confidence") or data.get("provenance") or "").upper()
        return {
            "EXTRACTED": EvidenceKind.FACT,
            "FACT": EvidenceKind.FACT,
            "HEURISTIC": EvidenceKind.HEURISTIC,
            "INFERRED": EvidenceKind.INFERENCE,
            "INFERENCE": EvidenceKind.INFERENCE,
            "AMBIGUOUS": EvidenceKind.MANUAL_REVIEW_REQUIRED,
            "MANUAL_REVIEW_REQUIRED": EvidenceKind.MANUAL_REVIEW_REQUIRED,
        }.get(label, EvidenceKind.MANUAL_REVIEW_REQUIRED)

    def _node(self, node_id: str, data: dict[str, Any]) -> GraphNode:
        return GraphNode(
            id=node_id,
            label=str(data.get("label") or node_id),
            source_file=_optional_text(data.get("source_file")),
            source_location=_optional_text(data.get("source_location")),
            file_type=_optional_text(data.get("file_type")),
            community=data.get("community"),
            community_name=_optional_text(data.get("community_name")),
            evidence_kind=self._evidence_kind(data),
            provenance=self._provenance(data),
        )

    def _edge(self, source: str, target: str, data: dict[str, Any]) -> GraphEdge:
        confidence_score = data.get("confidence_score")
        return GraphEdge(
            source=source,
            target=target,
            relation=_optional_text(data.get("relation")),
            evidence_kind=self._evidence_kind(data),
            confidence=_optional_text(data.get("confidence")),
            confidence_score=float(confidence_score) if isinstance(confidence_score, (int, float)) else None,
            source_file=_optional_text(data.get("source_file")),
            source_location=_optional_text(data.get("source_location")),
            provenance=self._provenance(data),
        )

    def _resolve_node_id(self, graph: nx.Graph, identifier: str) -> str | None:
        if identifier in graph:
            return identifier
        folded = identifier.casefold()
        exact = [node_id for node_id, data in graph.nodes(data=True) if str(data.get("label", "")).casefold() == folded]
        if len(exact) > 1:
            raise GraphAmbiguousNodeError(f"multiple nodes have label: {identifier}")
        if exact:
            return exact[0]
        partial = [node_id for node_id, data in graph.nodes(data=True) if folded in str(data.get("label", "")).casefold()]
        if len(partial) > 1:
            raise GraphAmbiguousNodeError(f"identifier is ambiguous: {identifier}")
        return partial[0] if partial else None

    def query(self, text: str, *, limit: int = 20) -> GraphQueryResult:
        graph = self._require_graph()
        terms = [term.casefold() for term in text.split() if len(term) >= 2]
        if not terms or limit < 1:
            return GraphQueryResult()
        scored: list[tuple[int, str]] = []
        for node_id, data in graph.nodes(data=True):
            haystack = " ".join(
                str(data.get(key) or "") for key in ("label", "source_file", "file_type")
            ).casefold()
            score = sum(term in haystack for term in terms)
            if score:
                scored.append((score, node_id))
        scored.sort(key=lambda item: (-item[0], str(graph.nodes[item[1]].get("label") or item[1])))
        selected = [node_id for _, node_id in scored[:limit]]
        selected_set = set(selected)
        edges = tuple(
            self._edge(source, target, data)
            for source, target, data in _iter_edges(graph)
            if source in selected_set and target in selected_set
        )
        return GraphQueryResult(
            nodes=tuple(self._node(node_id, graph.nodes[node_id]) for node_id in selected),
            edges=edges,
            truncated=len(scored) > limit,
        )

    def get_node(self, identifier: str) -> GraphNode | None:
        graph = self._require_graph()
        node_id = self._resolve_node_id(graph, identifier)
        return self._node(node_id, graph.nodes[node_id]) if node_id is not None else None

    def get_neighbors(
        self,
        identifier: str,
        *,
        direction: Literal["incoming", "outgoing", "both"] = "both",
    ) -> GraphQueryResult:
        graph = self._require_graph()
        node_id = self._resolve_node_id(graph, identifier)
        if node_id is None:
            return GraphQueryResult()
        logical_directed = bool(graph.graph.get("_logical_directed", graph.is_directed()))
        if not logical_directed and direction != "both":
            raise GraphUnavailableError("neighbor direction is unavailable for an undirected graph")
        edges = []
        neighbor_ids: set[str] = {node_id}
        for source, target, data in _iter_edges(graph):
            include = (
                direction in {"outgoing", "both"} and source == node_id
            ) or (
                direction in {"incoming", "both"} and target == node_id
            )
            if include:
                edges.append(self._edge(source, target, data))
                neighbor_ids.update((source, target))
        nodes = tuple(self._node(current, graph.nodes[current]) for current in sorted(neighbor_ids))
        return GraphQueryResult(nodes=nodes, edges=tuple(edges))

    def get_dependencies(self, identifier: str) -> GraphQueryResult:
        graph = self._require_graph()
        if not bool(graph.graph.get("_logical_directed", graph.is_directed())):
            raise GraphUnavailableError("dependency direction is unavailable for an undirected graph")
        return self.get_neighbors(identifier, direction="outgoing")

    def get_dependents(self, identifier: str) -> GraphQueryResult:
        graph = self._require_graph()
        if not bool(graph.graph.get("_logical_directed", graph.is_directed())):
            raise GraphUnavailableError("dependent direction is unavailable for an undirected graph")
        return self.get_neighbors(identifier, direction="incoming")

    def find_path(self, source: str, target: str, *, max_hops: int = 8) -> GraphQueryResult:
        graph = self._require_graph()
        source_id = self._resolve_node_id(graph, source)
        target_id = self._resolve_node_id(graph, target)
        if source_id is None or target_id is None:
            return GraphQueryResult()
        try:
            path_graph = (
                graph
                if bool(graph.graph.get("_logical_directed", graph.is_directed()))
                else graph.to_undirected()
            )
            path = nx.shortest_path(path_graph, source_id, target_id)
        except nx.NetworkXNoPath:
            return GraphQueryResult()
        if len(path) - 1 > max_hops:
            return GraphQueryResult(truncated=True)
        edges: list[GraphEdge] = []
        logical_directed = bool(graph.graph.get("_logical_directed", graph.is_directed()))
        for current, following in zip(path, path[1:]):
            edge_source, edge_target = current, following
            if not graph.has_edge(current, following) and not logical_directed:
                edge_source, edge_target = following, current
            data = _first_edge_data(graph, edge_source, edge_target)
            edges.append(self._edge(edge_source, edge_target, data))
        return GraphQueryResult(
            nodes=tuple(self._node(node_id, graph.nodes[node_id]) for node_id in path),
            edges=tuple(edges),
        )

    def get_community(self, community: int | str) -> GraphQueryResult:
        graph = self._require_graph()
        target = str(community)
        nodes = tuple(
            self._node(node_id, data)
            for node_id, data in graph.nodes(data=True)
            if str(data.get("community")) == target
        )
        return GraphQueryResult(nodes=nodes)


def build_graph_provider(
    repository_root: Path,
    graph_path: str | Path = "graphify-out/graph.json",
    *,
    enabled: bool = True,
    freshness_kind: Literal["ast", "semantic"] = "semantic",
    freshness_probe: FreshnessProbe = graphify_freshness_probe,
) -> GraphProvider:
    if not enabled:
        return NullGraphProvider(
            GraphStatus(
                provider="none",
                availability=GraphAvailability.DISABLED,
                freshness=GraphFreshness.UNAVAILABLE,
                graph_path=None,
                capabilities=GraphCapabilities(),
                detail="graph integration is disabled",
            )
        )
    provider = GraphifyProvider(
        repository_root,
        graph_path,
        freshness_kind=freshness_kind,
        freshness_probe=freshness_probe,
    )
    # Keep the adapter active when the graph is missing or invalid so a later
    # Graphify rebuild is detected without restarting the MCP process.
    return provider


def _optional_text(value: Any) -> str | None:
    return str(value) if value is not None and str(value) else None


def _iter_edges(graph: nx.Graph):
    if graph.is_multigraph():
        for source, target, _, data in graph.edges(keys=True, data=True):
            yield str(source), str(target), data
    else:
        for source, target, data in graph.edges(data=True):
            yield str(source), str(target), data


def _first_edge_data(graph: nx.Graph, source: str, target: str) -> dict[str, Any]:
    data = graph.get_edge_data(source, target) or {}
    if graph.is_multigraph():
        first = next(iter(data.values()), {})
        return first if isinstance(first, dict) else {}
    return data if isinstance(data, dict) else {}
