#!/usr/bin/env python3
"""Generate README.md from data/*.json.

Rebuilds the two matrix tables (skill × agent and feature × agent) plus the
status line and repository-layout block directly from the structured data, so
the README never drifts from the JSON. CI commits any diff.

The non-table prose sections are kept as static templates here so a single run
produces a complete, human-readable README.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
AGENTS_PATH = DATA / "agents.json"
SKILLS_PATH = DATA / "skills.json"
README_PATH = ROOT / "README.md"

LEVEL_EMOJI = {
    "native": "🟢",
    "compatible": "🟢",
    "partial": "🟡",
    "unsupported": "🔴",
    "unknown": "⚪",
}

# Agents shown as columns in the README tables. Order matters.
PRIMARY_AGENT_IDS = [
    "claude-code",
    "cursor",
    "codex-cli",
    "gemini-cli",
    "open-standard",
]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def agent_label(agent: dict) -> str:
    return agent["name"]


def cell(level: str) -> str:
    return LEVEL_EMOJI.get(level, "⚪")


def render_skill_table(agents: list[dict], skills: list[dict]) -> str:
    # Columns: the 5 primary agents, in fixed order, then the rest.
    primary = [a for a in agents if a["id"] in PRIMARY_AGENT_IDS]
    primary.sort(key=lambda a: PRIMARY_AGENT_IDS.index(a["id"]))
    secondary = [a for a in agents if a["id"] not in PRIMARY_AGENT_IDS]
    cols = primary + secondary

    header = "| Skill | Category | " + " | ".join(agent_label(a) for a in cols) + " |"
    sep = "|---|---|" + "|".join([":---:"] * len(cols)) + "|"
    lines = [header, sep]

    for s in sorted(skills, key=lambda x: x["name"].lower()):
        compat = s.get("compatibility", {})
        row_cells = []
        for a in cols:
            row_cells.append(cell(compat.get(a["id"], "unknown")))
        url = s.get("url") or f"https://github.com/{s['repo']}"
        name = f"[{s['name']}]({url})"
        lines.append(f"| {name} | {s.get('category', '')} | " + " | ".join(row_cells) + " |")
    return "\n".join(lines)


def render_feature_table(agents: list[dict]) -> str:
    primary = [a for a in agents if a["id"] in PRIMARY_AGENT_IDS]
    primary.sort(key=lambda a: PRIMARY_AGENT_IDS.index(a["id"]))
    secondary = [a for a in agents if a["id"] not in PRIMARY_AGENT_IDS]
    cols = primary + secondary

    feature_rows = [
        ("Hooks (PreToolUse / PostToolUse / etc.)", "hooks"),
        ("Subagent spawning", "subagent"),
        ("Context fork (`context: fork`)", "context_fork"),
        ("Progressive disclosure (metadata → body → assets)", "progressive_disclosure"),
        ("Pre-approved tools (`allowed-tools`)", "pre_approved_tools"),
        ("Slash command invocation (`/skill-name`)", "slash_command"),
        ("Glob-scoped activation", "glob_scoping"),
        ("Per-skill model override", "model_override"),
    ]

    header = "| Feature | " + " | ".join(agent_label(a) for a in cols) + " |"
    sep = "|---|" + "|".join([":---:"] * len(cols)) + "|"
    lines = [header, sep]
    for label, key in feature_rows:
        cells = [cell(a["features"].get(key, "unknown")) for a in cols]
        lines.append(f"| {label} | " + " | ".join(cells) + " |")
    return "\n".join(lines)


def render_legend() -> str:
    return (
        "Legend: 🟢 native / compatible · 🟡 partial · 🔴 unsupported · ⚪ unknown"
    )


def render_layout() -> str:
    return """```
.
├── data/
│   ├── schema.json     # JSON Schema for the two datasets below
│   ├── agents.json     # Per-agent capability + install-path records
│   └── skills.json     # Per-skill compatibility records with caveats
├── docs/
│   ├── methodology.md  # How support levels are assigned
│   ├── porting-guide.md# How to port a skill across agents
│   ├── faq.md
│   └── agents/         # One deep-dive markdown file per agent
├── site/               # Static single-page web app (GitHub Pages)
├── scripts/
│   ├── validate.py     # Schema + business-rule validator (runs in CI)
│   ├── generate_readme.py  # Rebuilds this README from the JSON data
│   ├── stats.py        # Coverage and distribution report
│   ├── backfill_compat.py  # Infer missing agent cells (helper)
│   └── merge_skills.py # Merge new skill entries (helper)
└── .github/workflows/
    ├── validate.yml
    ├── generate.yml    # Auto-regenerate README on data changes
    └── deploy-site.yml # Deploy site/ to GitHub Pages
```"""


def main() -> None:
    agents = load(AGENTS_PATH)["agents"]
    skills = load(SKILLS_PATH)["skills"]

    # Sort agents: primary first, then secondary alphabetical.
    primary = [a for a in agents if a["id"] in PRIMARY_AGENT_IDS]
    primary.sort(key=lambda a: PRIMARY_AGENT_IDS.index(a["id"]))
    secondary = sorted(
        [a for a in agents if a["id"] not in PRIMARY_AGENT_IDS],
        key=lambda a: a["name"].lower(),
    )
    ordered = primary + secondary

    readme = f"""# Agent Skills Compatibility Matrix

> One question every AI-coding user asks within a week: *"Will this skill work in my agent?"* This repo answers it, per skill, per agent, with sources.

中文简介：每个 AI 编程 Agent（Claude Code / Cursor / Codex CLI / Gemini CLI / Windsurf / Cline / Aider / Copilot / Zed / Amp / Jules / Continue）都声称支持 Agent Skills，但实际兼容性参差不齐——hooks、子 agent、上下文 fork 这些扩展能力各家都没有。本仓库用一张可校验的矩阵表说明每个开源 Skill 在每个 harness 里的真实支持情况，附带各 Agent 的能力差异详解和跨 Agent 移植指南。

## Why this exists

The Agent Skills open standard ([agentskills.io](https://agentskills.io/)) promises portability. In practice:

- **Claude Code** is a superset — hooks, `context: fork`, subagents, model override all work, but only here.
- **Cursor** and **Windsurf** use glob/trigger-driven activation and have no hooks, no subagents.
- **Codex CLI**, **Zed**, **Amp**, **Jules** read plain `AGENTS.md` with no YAML frontmatter; Codex caps context at 32 KiB.
- **Gemini CLI** implements the open standard plus hooks (configured in `settings.json`, not frontmatter).
- **Cline**, **Aider**, **Continue**, **Copilot** each have their own rules/prompt-file formats with no `SKILL.md`.

A skill that "runs everywhere" often silently loses half its behavior. This matrix records, per skill, **what actually works where** and **what degrades how**.

## Status

{len(skills)} skills × {len(agents)} agents currently tracked. See [`data/skills.json`](data/skills.json) for the structured records and [CONTRIBUTING.md](CONTRIBUTING.md) to add more. Live site: see `site/` or the GitHub Pages deployment.

## Skill × Agent compatibility

{render_legend()}

{render_skill_table(ordered, skills)}

Per-cell caveats (why a cell is partial or unsupported) live in [`data/skills.json`](data/skills.json) under the `caveats` field.

## Agent capability matrix

{render_legend()}

{render_feature_table(ordered)}

Source: [`data/agents.json`](data/agents.json). Per-agent deep dives in [`docs/agents/`](docs/agents/).

## Repository layout

{render_layout()}

## Validate locally

```bash
pip install jsonschema
python scripts/validate.py
```

CI runs the same validator on every PR touching `data/` or `scripts/`.

## Regenerate this README

The tables above are generated from the JSON data — never edit them by hand.

```bash
python scripts/generate_readme.py
```

CI auto-commits any diff on `data/` changes via the `generate.yml` workflow.

## Contribute

Add a skill: append a record to [`data/skills.json`](data/skills.json), run the validator, open a PR. See [CONTRIBUTING.md](CONTRIBUTING.md) for the support-level rubric and verification checklist. New agents welcome — see the "Adding a new agent" section.

## Forking & deployment

After forking, replace the `OWNER` placeholder with your GitHub username or org:

```bash
# from the repo root
git grep -l 'OWNER' | xargs sed -i 's/OWNER/<your-github-name>/g'
```

Then enable GitHub Pages for the site: **Settings → Pages → Source: GitHub Actions**. The `deploy-site.yml` workflow will publish `site/` (with `data/` copied alongside) on every push to `main` that touches `site/` or `data/`.

## License

MIT — see [LICENSE](LICENSE).
"""
    README_PATH.write_text(readme, encoding="utf-8")
    print(f"Generated {README_PATH.relative_to(ROOT)} ({len(skills)} skills × {len(agents)} agents).")


if __name__ == "__main__":
    main()
