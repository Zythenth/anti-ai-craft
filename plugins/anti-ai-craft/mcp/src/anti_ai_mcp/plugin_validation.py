from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml


SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*)(?:\."
    r"(?:0|[1-9]\d*|\d*[A-Za-z-][0-9A-Za-z-]*))*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
MANIFEST_KEYS = {
    "id",
    "name",
    "version",
    "description",
    "skills",
    "apps",
    "mcpServers",
    "interface",
    "author",
    "homepage",
    "repository",
    "license",
    "keywords",
}
INTERFACE_KEYS = {
    "displayName",
    "shortDescription",
    "longDescription",
    "developerName",
    "category",
    "capabilities",
    "websiteURL",
    "privacyPolicyURL",
    "termsOfServiceURL",
    "brandColor",
    "composerIcon",
    "logo",
    "logoDark",
    "screenshots",
    "defaultPrompt",
    "default_prompt",
}


def validate_plugin(plugin_root: Path, marketplace_path: Path | None = None) -> list[str]:
    root = plugin_root.resolve()
    errors: list[str] = []
    manifest = _json_object(root / ".codex-plugin" / "plugin.json", "plugin manifest", errors)
    if manifest is None:
        return errors
    _reject_todos(manifest, "$", errors)
    _unknown(manifest, MANIFEST_KEYS, "plugin.json", errors)
    for field in ("name", "version", "description"):
        _required_text(manifest, field, "plugin.json", errors)
    version = manifest.get("version")
    if isinstance(version, str) and SEMVER.fullmatch(version) is None:
        errors.append("plugin.json version must be strict semver")
    author = manifest.get("author")
    if not isinstance(author, dict):
        errors.append("plugin.json author must be an object")
    else:
        _unknown(author, {"name", "email", "url"}, "plugin.json author", errors)
        _required_text(author, "name", "plugin.json author", errors)
        _optional_https(author, "url", "plugin.json author", errors)
    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        errors.append("plugin.json interface must be an object")
    else:
        _unknown(interface, INTERFACE_KEYS, "plugin.json interface", errors)
        for field in (
            "displayName",
            "shortDescription",
            "longDescription",
            "developerName",
            "category",
        ):
            _required_text(interface, field, "plugin.json interface", errors)
        if "defaultPrompt" not in interface and "default_prompt" not in interface:
            errors.append("plugin.json interface requires defaultPrompt or default_prompt")
        capabilities = interface.get("capabilities")
        if not isinstance(capabilities, list) or not all(
            isinstance(item, str) and item.strip() for item in capabilities
        ):
            errors.append("plugin.json interface capabilities must be an array of strings")
        _optional_https(interface, "websiteURL", "plugin.json interface", errors)
    if _normalize_contract_path(manifest.get("skills")) != "skills":
        errors.append("plugin.json skills must resolve to skills")
    _validate_skills(root, errors)
    if marketplace_path is not None:
        _validate_marketplace(root, manifest, marketplace_path.resolve(), errors)
    return errors


def _validate_skills(root: Path, errors: list[str]) -> None:
    skills = root / "skills"
    if not skills.is_dir():
        errors.append("plugin skills directory is missing")
        return
    for skill in sorted(path for path in skills.iterdir() if path.is_dir() and not path.name.startswith(".")):
        skill_md = skill / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"skill {skill.name} is missing SKILL.md")
            continue
        try:
            text = skill_md.read_text(encoding="utf-8")
        except (OSError, UnicodeError):
            errors.append(f"skill {skill.name} could not be read as UTF-8")
            continue
        if not text.startswith("---\n") or "\n---" not in text[4:]:
            errors.append(f"skill {skill.name} must have closed YAML frontmatter")
            continue
        end = text.find("\n---", 4)
        try:
            frontmatter = yaml.safe_load(text[4:end])
        except yaml.YAMLError:
            errors.append(f"skill {skill.name} frontmatter must be valid YAML")
            continue
        if not isinstance(frontmatter, dict):
            errors.append(f"skill {skill.name} frontmatter must be an object")
            continue
        for field in ("name", "description"):
            _required_text(frontmatter, field, f"skill {skill.name} frontmatter", errors)
        disabled = frontmatter.get(
            "disable-model-invocation", frontmatter.get("disable_model_invocation")
        )
        if disabled not in (None, False):
            errors.append(f"skill {skill.name} disable-model-invocation must be false")


def _validate_marketplace(
    plugin_root: Path,
    manifest: dict[str, Any],
    path: Path,
    errors: list[str],
) -> None:
    marketplace = _json_object(path, "marketplace", errors)
    if marketplace is None:
        return
    entries = marketplace.get("plugins")
    if not isinstance(entries, list):
        errors.append("marketplace plugins must be an array")
        return
    matching = [item for item in entries if isinstance(item, dict) and item.get("name") == manifest.get("name")]
    if len(matching) != 1:
        errors.append("marketplace must contain exactly one matching plugin entry")
        return
    entry = matching[0]
    source = entry.get("source")
    expected = f"./plugins/{plugin_root.name}"
    if not isinstance(source, dict) or source.get("source") != "local" or source.get("path") not in {
        expected,
    }:
        errors.append("marketplace source must point to the local plugin root")
    policy = entry.get("policy")
    if not isinstance(policy, dict) or policy.get("installation") not in {
        "NOT_AVAILABLE",
        "AVAILABLE",
        "INSTALLED_BY_DEFAULT",
    } or policy.get("authentication") not in {"ON_INSTALL", "ON_USE"}:
        errors.append("marketplace policy is missing or invalid")
    if not isinstance(entry.get("category"), str) or not entry["category"].strip():
        errors.append("marketplace category must be a non-empty string")


def _json_object(path: Path, label: str, errors: list[str]) -> dict[str, Any] | None:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError):
        errors.append(f"{label} must be readable valid JSON: {path}")
        return None
    if not isinstance(payload, dict):
        errors.append(f"{label} must contain an object")
        return None
    return payload


def _required_text(payload: dict[str, Any], field: str, label: str, errors: list[str]) -> None:
    if not isinstance(payload.get(field), str) or not payload[field].strip():
        errors.append(f"{label} {field} must be a non-empty string")


def _optional_https(payload: dict[str, Any], field: str, label: str, errors: list[str]) -> None:
    value = payload.get(field)
    if value is None:
        return
    parsed = urlparse(value) if isinstance(value, str) else None
    if parsed is None or parsed.scheme != "https" or not parsed.netloc:
        errors.append(f"{label} {field} must be an absolute HTTPS URL")


def _unknown(payload: dict[str, Any], allowed: set[str], label: str, errors: list[str]) -> None:
    for field in sorted(set(payload) - allowed):
        errors.append(f"{label} field {field} is not accepted")


def _reject_todos(value: Any, path: str, errors: list[str]) -> None:
    if isinstance(value, str) and "[TODO:" in value:
        errors.append(f"{path} contains a TODO placeholder")
    elif isinstance(value, list):
        for index, item in enumerate(value):
            _reject_todos(item, f"{path}[{index}]", errors)
    elif isinstance(value, dict):
        for key, item in value.items():
            _reject_todos(item, f"{path}.{key}", errors)


def _normalize_contract_path(value: Any) -> str | None:
    if not isinstance(value, str) or Path(value).is_absolute():
        return None
    return Path(value).as_posix().rstrip("/") or None


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate Anti-AI Craft plugin artifacts.")
    parser.add_argument("plugin_root")
    parser.add_argument("--marketplace")
    args = parser.parse_args(argv)
    errors = validate_plugin(
        Path(args.plugin_root),
        Path(args.marketplace) if args.marketplace else None,
    )
    if errors:
        print("Plugin validation failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(f"Plugin validation passed: {Path(args.plugin_root).resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
