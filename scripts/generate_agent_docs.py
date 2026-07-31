#!/usr/bin/env python3
"""Generate docs/agents/<id>.md stubs from data/agents.json for any agent
that does not yet have a doc file. Existing files are never overwritten.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENTS_PATH = ROOT / "data" / "agents.json"
DOCS_DIR = ROOT / "docs" / "agents"

FEATURE_LABELS = {
    "hooks": "Hooks (PreToolUse / PostToolUse / etc.)",
    "subagent": "Subagent spawning",
    "context_fork": "Context fork (`context: fork`)",
    "progressive_disclosure": "Progressive disclosure (metadata → body → assets)",
    "pre_approved_tools": "Pre-approved tools (`allowed-tools`)",
    "slash_command": "Slash command invocation (`/skill-name`)",
    "glob_scoping": "Glob-scoped activation",
    "model_override": "Per-skill model override",
}


def main() -> None:
    agents = json.loads(AGENTS_PATH.read_text(encoding="utf-8"))["agents"]
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    created = 0
    for a in agents:
        path = DOCS_DIR / f"{a['id']}.md"
        if path.exists():
            continue
        feats = a["features"]
        feat_lines = "\n".join(
            f"- {FEATURE_LABELS.get(k, k)}: {v}" for k, v in feats.items()
        )
        fm_req = ", ".join(a.get("frontmatter_required", [])) or "none"
        fm_opt = ", ".join(a.get("frontmatter_optional", [])) or "none"

        body = f"""# {a['name']}

- **Vendor:** {a['vendor']}
- **Homepage:** <{a['homepage']}>
- **Rules file:** `{a['rules_file']}`
- **Skill file:** {a['skills_file']}
- **Install paths:**
  - Project: `{a['install_path']['project']}`
  - User: `{a['install_path']['user']}`

## Frontmatter

Required: {fm_req}.

Optional: {fm_opt}.

## Features supported

{feat_lines}

## Why skills portability breaks here

{a['notes']}

## Sources

- <{a['homepage']}>
- See `data/agents.json` for the structured record.
"""
        path.write_text(body, encoding="utf-8")
        created += 1
    print(f"Created {created} agent doc stub(s) in {DOCS_DIR}.")


if __name__ == "__main__":
    main()
