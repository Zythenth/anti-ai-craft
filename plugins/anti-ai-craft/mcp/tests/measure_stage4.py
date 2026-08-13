from __future__ import annotations

import argparse
import gc
import json
import tempfile
import time
import tracemalloc
from pathlib import Path

from anti_ai_mcp.git import GitInspector
from anti_ai_mcp.graph import GraphFreshness, GraphifyProvider
from anti_ai_mcp.impact import ChangeImpactService


NEAR_LIMIT_PAYLOAD_BYTES = 60 * 1024 * 1024


def fresh(*_args):
    return GraphFreshness.AVAILABLE_AND_FRESH, "measurement fixture"


def measure(repository_root: Path) -> dict:
    results: dict[str, dict] = {}
    provider = GraphifyProvider(
        repository_root,
        repository_root / "graphify-out" / "graph.json",
        freshness_kind="ast",
    )
    results["current_graph"] = _memory_call(provider.get_overview)

    inspector = GitInspector(repository_root)
    impact = ChangeImpactService(inspector, provider)

    def repeated_impact() -> None:
        for _index in range(20):
            impact.analyze(max_depth=2, include_tests=True)

    results["repeated_impact_20"] = _memory_call(repeated_impact)
    del impact, provider
    gc.collect()

    with tempfile.TemporaryDirectory(prefix="anti-ai-memory-") as directory:
        temporary_repository = Path(directory)
        graph_path = temporary_repository / "graphify-out" / "graph.json"
        graph_path.parent.mkdir()
        _write_near_limit_graph(graph_path)
        near_limit = GraphifyProvider(
            temporary_repository,
            graph_path,
            freshness_probe=fresh,
        )
        results["near_64_mib_graph"] = {
            **_memory_call(near_limit.get_status),
            "file_bytes": graph_path.stat().st_size,
        }
    return results


def _memory_call(operation) -> dict:
    gc.collect()
    tracemalloc.start()
    started = time.monotonic()
    operation()
    elapsed = time.monotonic() - started
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "duration_seconds": round(elapsed, 6),
        "current_bytes": current,
        "peak_bytes": peak,
    }


def _write_near_limit_graph(path: Path) -> None:
    prefix = (
        '{"directed":false,"multigraph":false,"graph":{},"nodes":['
        '{"id":"large","label":"'
    )
    suffix = '"}],"links":[]}'
    remaining = NEAR_LIMIT_PAYLOAD_BYTES - len(prefix.encode()) - len(suffix.encode())
    chunk = "x" * (1024 * 1024)
    with path.open("w", encoding="utf-8", newline="") as handle:
        handle.write(prefix)
        while remaining:
            value = chunk[: min(remaining, len(chunk))]
            handle.write(value)
            remaining -= len(value)
        handle.write(suffix)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("repository_root", type=Path)
    args = parser.parse_args()
    print(json.dumps(measure(args.repository_root.resolve()), indent=2))


if __name__ == "__main__":
    main()
