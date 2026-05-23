#!/usr/bin/env python3
"""Offline structural validator for DESIGN.md drafts."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path


CANONICAL_SECTIONS = [
    "Overview",
    "Colors",
    "Typography",
    "Layout",
    "Elevation & Depth",
    "Shapes",
    "Components",
    "Do's and Don'ts",
]

ALIASES = {
    "Brand & Style": "Overview",
    "Layout & Spacing": "Layout",
    "Elevation": "Elevation & Depth",
}

VALID_COMPONENT_PROPS = {
    "backgroundColor",
    "textColor",
    "typography",
    "rounded",
    "padding",
    "size",
    "height",
    "width",
}


def finding(severity: str, path: str, message: str) -> dict[str, str]:
    return {"severity": severity, "path": path, "message": message}


def split_front_matter(text: str) -> tuple[str | None, str, list[dict[str, str]]]:
    findings: list[dict[str, str]] = []
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        findings.append(finding("error", "frontmatter", "File must start with a YAML front matter fence: ---"))
        return None, text, findings

    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "\n".join(lines[1:index]), "\n".join(lines[index + 1 :]), findings

    findings.append(finding("error", "frontmatter", "Missing closing YAML front matter fence: ---"))
    return None, "", findings


def parse_yaml(front_matter: str | None) -> tuple[dict | None, list[dict[str, str]]]:
    findings: list[dict[str, str]] = []
    if front_matter is None:
        return None, findings

    try:
        import yaml  # type: ignore
    except Exception:
        findings.append(
            finding(
                "warning",
                "frontmatter",
                "PyYAML is not installed; skipped deep YAML token validation.",
            )
        )
        return None, findings

    try:
        data = yaml.safe_load(front_matter) or {}
    except Exception as exc:
        findings.append(finding("error", "frontmatter", f"YAML could not be parsed: {exc}"))
        return None, findings

    if not isinstance(data, dict):
        findings.append(finding("error", "frontmatter", "YAML front matter must be a mapping."))
        return None, findings

    return data, findings


def validate_tokens(data: dict | None) -> list[dict[str, str]]:
    if data is None:
        return []

    findings: list[dict[str, str]] = []
    for key in ["name", "colors", "typography", "rounded", "spacing", "components"]:
        if key not in data:
            severity = "error" if key in {"name", "colors", "typography"} else "warning"
            findings.append(finding(severity, key, f"Missing `{key}` in YAML front matter."))

    colors = data.get("colors")
    if isinstance(colors, dict):
        if "primary" not in colors:
            findings.append(finding("warning", "colors.primary", "Missing recommended `primary` color token."))
        for name, value in colors.items():
            if not isinstance(value, str) or not re.fullmatch(r"#[0-9A-Fa-f]{6}([0-9A-Fa-f]{2})?", value):
                findings.append(finding("error", f"colors.{name}", "Color must be an sRGB hex string like `#1A1C1E`."))
    elif colors is not None:
        findings.append(finding("error", "colors", "`colors` must be a mapping."))

    typography = data.get("typography")
    if isinstance(typography, dict):
        for name, value in typography.items():
            if not isinstance(value, dict):
                findings.append(finding("error", f"typography.{name}", "Typography token must be a mapping."))
                continue
            for required in ["fontFamily", "fontSize"]:
                if required not in value:
                    findings.append(finding("warning", f"typography.{name}.{required}", f"Missing `{required}`."))
    elif typography is not None:
        findings.append(finding("error", "typography", "`typography` must be a mapping."))

    token_paths = collect_token_paths(data)
    components = data.get("components")
    if isinstance(components, dict):
        for component_name, component in components.items():
            if not isinstance(component, dict):
                findings.append(finding("error", f"components.{component_name}", "Component must be a mapping."))
                continue
            for prop, value in component.items():
                if prop not in VALID_COMPONENT_PROPS:
                    findings.append(
                        finding("warning", f"components.{component_name}.{prop}", "Unknown component property.")
                    )
                if isinstance(value, str):
                    for ref in re.findall(r"\{([^{}]+)\}", value):
                        if ref not in token_paths:
                            findings.append(
                                finding(
                                    "error",
                                    f"components.{component_name}.{prop}",
                                    f"Broken token reference `{{{ref}}}`.",
                                )
                            )
    elif components is not None:
        findings.append(finding("error", "components", "`components` must be a mapping."))

    return findings


def collect_token_paths(data: object, prefix: str = "") -> set[str]:
    paths: set[str] = set()
    if isinstance(data, dict):
        for key, value in data.items():
            key_path = f"{prefix}.{key}" if prefix else str(key)
            if isinstance(value, dict):
                paths.add(key_path)
                paths.update(collect_token_paths(value, key_path))
            else:
                paths.add(key_path)
    return paths


def validate_sections(body: str) -> list[dict[str, str]]:
    findings: list[dict[str, str]] = []
    headings = re.findall(r"^##\s+(.+?)\s*$", body, flags=re.MULTILINE)
    normalized = [ALIASES.get(heading, heading) for heading in headings]

    seen: set[str] = set()
    for heading, canonical in zip(headings, normalized):
        if canonical in seen:
            findings.append(finding("error", f"sections.{heading}", "Duplicate section heading."))
        seen.add(canonical)

    order = {name: index for index, name in enumerate(CANONICAL_SECTIONS)}
    last_index = -1
    for heading, canonical in zip(headings, normalized):
        if canonical not in order:
            findings.append(finding("warning", f"sections.{heading}", "Unknown section heading; preserve only if intentional."))
            continue
        current = order[canonical]
        if current < last_index:
            findings.append(finding("warning", f"sections.{heading}", "Section is out of canonical order."))
        last_index = max(last_index, current)

    missing = [section for section in CANONICAL_SECTIONS if section not in normalized]
    for section in missing:
        findings.append(finding("info", f"sections.{section}", "Canonical section is omitted."))

    return findings


def validate(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    front_matter, body, findings = split_front_matter(text)
    data, yaml_findings = parse_yaml(front_matter)
    findings.extend(yaml_findings)
    findings.extend(validate_tokens(data))
    findings.extend(validate_sections(body))

    summary = {
        "errors": sum(1 for item in findings if item["severity"] == "error"),
        "warnings": sum(1 for item in findings if item["severity"] == "warning"),
        "info": sum(1 for item in findings if item["severity"] == "info"),
    }
    return {"findings": findings, "summary": summary}


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: validate_design_md.py DESIGN.md", file=sys.stderr)
        return 2

    report = validate(Path(argv[1]))
    print(json.dumps(report, indent=2))
    return 1 if report["summary"]["errors"] else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
