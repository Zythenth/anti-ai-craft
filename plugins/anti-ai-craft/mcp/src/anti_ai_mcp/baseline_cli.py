from __future__ import annotations

import argparse
import json
from pathlib import Path

from . import __version__
from .anti_ai_audit import AntiAiAuditService
from .architecture import ArchitectureService
from .baseline import BaselineService
from .checks import ProjectCheckService
from .git import GitInspector
from .graph import build_graph_provider
from .security_audit import SecurityAuditService


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        description="Create or validate a compact Anti-AI evidence baseline."
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    create = subparsers.add_parser("create")
    create.add_argument("--repository-root", required=True)
    create.add_argument("--output", default=".anti-ai/baseline.json")
    create.add_argument("--graph-path", default="graphify-out/graph.json")
    create.add_argument("--disable-graph", action="store_true")
    validate = subparsers.add_parser("validate")
    validate.add_argument("--repository-root", required=True)
    validate.add_argument("baseline_path")
    args = parser.parse_args(argv)
    repository_root = Path(args.repository_root).resolve(strict=True)
    baseline_service = BaselineService(repository_root)
    if args.command == "validate":
        document = baseline_service.load(args.baseline_path)
        print(
            json.dumps(
                {
                    "status": "PASS",
                    "schema_version": document["schema_version"],
                    "findings": len(document["findings"]),
                    "baseline_head": document["repository"].get("head"),
                },
                sort_keys=True,
            )
        )
        return

    inspector = GitInspector(repository_root)
    provider = build_graph_provider(
        repository_root,
        args.graph_path,
        enabled=not args.disable_graph,
        freshness_kind="ast",
    )
    architecture = ArchitectureService(inspector, provider)
    anti_ai = AntiAiAuditService(repository_root, inspector, provider, architecture).audit()
    security = SecurityAuditService(repository_root, inspector).audit()
    checks = ProjectCheckService(repository_root)
    selected_checks = [check.to_dict(repository_root) for check in checks.discover()]
    document = baseline_service.create_document(
        findings=[
            *(finding.to_dict() for finding in anti_ai.findings),
            *(finding.to_dict() for finding in security.findings),
        ],
        tool_version=__version__,
        graph=provider.get_status().to_dict(),
        validation={"selected_checks": selected_checks},
    )
    target = baseline_service.write(args.output, document)
    print(
        json.dumps(
            {
                "status": "PASS",
                "path": target.relative_to(repository_root).as_posix(),
                "schema_version": document["schema_version"],
                "findings": len(document["findings"]),
                "baseline_head": document["repository"].get("head"),
            },
            sort_keys=True,
        )
    )
