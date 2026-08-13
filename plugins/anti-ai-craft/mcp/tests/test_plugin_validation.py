from __future__ import annotations

import json
from pathlib import Path

from anti_ai_mcp.plugin_validation import validate_plugin


def test_repository_plugin_and_marketplace_validate() -> None:
    root = Path(__file__).resolve().parents[2]
    marketplace = root.parents[1] / ".agents" / "plugins" / "marketplace.json"
    assert validate_plugin(root, marketplace) == []


def test_plugin_validation_rejects_invalid_manifest_and_skill(tmp_path: Path) -> None:
    plugin = tmp_path / "invalid"
    (plugin / ".codex-plugin").mkdir(parents=True)
    (plugin / "skills" / "broken").mkdir(parents=True)
    (plugin / ".codex-plugin" / "plugin.json").write_text(
        json.dumps(
            {
                "name": "invalid",
                "version": "not-semver",
                "description": "[TODO: fill]",
                "skills": "../outside",
                "author": {"name": "Tests"},
                "interface": {},
            }
        ),
        encoding="utf-8",
    )
    (plugin / "skills" / "broken" / "SKILL.md").write_text(
        "---\nname: broken\n---\n", encoding="utf-8"
    )
    errors = validate_plugin(plugin)
    assert any("strict semver" in error for error in errors)
    assert any("TODO placeholder" in error for error in errors)
    assert any("skills must resolve" in error for error in errors)
    assert any("description" in error for error in errors)
