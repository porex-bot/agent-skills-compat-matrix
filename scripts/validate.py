#!/usr/bin/env python3
"""Validate data/agents.json and data/skills.json against data/schema.json
plus business rules the JSON Schema cannot express.

Exit code is non-zero if any check fails. Designed to run locally and in CI.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

try:
    import jsonschema  # type: ignore
except ImportError:
    print(
        "ERROR: jsonschema is required. Install with: pip install jsonschema",
        file=sys.stderr,
    )
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SCHEMA_PATH = DATA / "schema.json"
AGENTS_PATH = DATA / "agents.json"
SKILLS_PATH = DATA / "skills.json"

SUPPORT_LEVELS = {"native", "compatible", "partial", "unsupported", "unknown"}
# native support should never need a caveat; everything else may carry one.
CAVEAT_FORBIDDEN_LEVELS = {"native"}
ID_PATTERN = re.compile(r"^[a-z][a-z0-9-]*$")
FEATURE_NAMES = {
    "hooks",
    "subagent",
    "context_fork",
    "progressive_disclosure",
    "pre_approved_tools",
    "slash_command",
    "glob_scoping",
    "model_override",
}


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def validate_schema(instance: dict, schema: dict, label: str, errors: list[str]) -> None:
    validator = jsonschema.Draft7Validator(schema)
    collected = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
    for err in collected:
        loc = ".".join(str(p) for p in err.path) or "<root>"
        errors.append(f"[{label}] schema violation at {loc}: {err.message}")


def validate_business_rules(bundle: dict, errors: list[str]) -> None:
    agents = bundle.get("agents", [])
    skills = bundle.get("skills", [])

    agent_ids: set[str] = set()
    agent_id_errors: list[str] = []

    # Duplicate / malformed agent ids
    seen_agents: set[str] = set()
    for a in agents:
        aid = a.get("id", "")
        if aid in seen_agents:
            errors.append(f"[agents] duplicate agent id: {aid}")
        seen_agents.add(aid)
        if not ID_PATTERN.match(aid):
            agent_id_errors.append(f"[agents] malformed id (must be kebab-case): {aid}")
        agent_ids.add(aid)

        # Features must be exactly the canonical set.
        feats = a.get("features", {})
        missing_feats = FEATURE_NAMES - set(feats.keys())
        if missing_feats:
            errors.append(
                f"[agents:{aid}] features missing keys: {sorted(missing_feats)}"
            )
        for fname, level in feats.items():
            if level not in SUPPORT_LEVELS:
                errors.append(
                    f"[agents:{aid}] invalid feature level for {fname}: {level}"
                )

    errors[:0] = agent_id_errors

    # Duplicate / malformed skill ids; compatibility must reference known agents.
    seen_skills: set[str] = set()
    for s in skills:
        sid = s.get("id", "")
        if sid in seen_skills:
            errors.append(f"[skills] duplicate skill id: {sid}")
        seen_skills.add(sid)
        if not ID_PATTERN.match(sid):
            errors.append(f"[skills:{sid}] malformed id (must be kebab-case)")

        compat = s.get("compatibility", {})
        caveats = s.get("caveats", {}) or {}

        for agent_id, level in compat.items():
            if agent_id not in agent_ids:
                errors.append(
                    f"[skills:{sid}] references unknown agent id: {agent_id}"
                )
            if level not in SUPPORT_LEVELS:
                errors.append(
                    f"[skills:{sid}] invalid support level for {agent_id}: {level}"
                )
            if level in CAVEAT_FORBIDDEN_LEVELS and agent_id in caveats:
                errors.append(
                    f"[skills:{sid}] caveat for {agent_id} is redundant "
                    f"(support is '{level}')"
                )

        # Caveats must only reference known agents.
        for agent_id in caveats:
            if agent_id not in agent_ids:
                errors.append(
                    f"[skills:{sid}] caveat references unknown agent id: {agent_id}"
                )

        # category must be one of the allowed set (schema also enforces this, but
        # this gives a clearer error message). categories 数组同理校验。
        category = s.get("category")
        categories = s.get("categories", [])
        allowed_categories = {
            "code_quality", "testing", "debugging", "devops", "frontend_ui",
            "data_docs", "text_content", "research_analysis", "agent_workflow",
            "integration", "other",
        }
        if category and category not in allowed_categories:
            errors.append(
                f"[skills:{sid}] invalid category: {category}"
            )
        if isinstance(categories, list):
            for c in categories:
                if c not in allowed_categories:
                    errors.append(
                        f"[skills:{sid}] invalid categories item: {c}"
                    )


def main() -> int:
    errors: list[str] = []

    schema = load_json(SCHEMA_PATH)
    agents_doc = load_json(AGENTS_PATH)
    skills_doc = load_json(SKILLS_PATH)

    bundle = {"agents": agents_doc.get("agents", []), "skills": skills_doc.get("skills", [])}
    validate_schema(bundle, schema, "bundle", errors)

    if not errors:
        validate_business_rules(bundle, errors)

    if errors:
        print(f"\nValidation FAILED with {len(errors)} issue(s):\n")
        for e in errors:
            print(f"  - {e}")
        return 1

    agent_count = len(bundle["agents"])
    skill_count = len(bundle["skills"])
    print(
        f"Validation OK: {agent_count} agents, {skill_count} skills. "
        f"All entries conform to schema and business rules."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
