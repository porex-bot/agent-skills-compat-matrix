#!/usr/bin/env python3
"""One-off helper: backfill compatibility for agents not yet recorded per skill.

For each skill, infer the support level for agents missing from its `compatibility`
map, based on the skill's known levels and its `uses_claude_extensions`.

Inference rules (conservative; verified cells always win):
  - open-standard compatible/native  -> AGENTS.md agents (codex-cli, zed, amp,
    jules) compatible; aider compatible; copilot compatible; continue
    compatible; windsurf/cline partial (need rule rewrite).
  - open-standard partial/unsupported -> all backfilled agents inherit that
    ceiling (partial or unsupported).
  - skills using `hooks` extension -> agents without hooks (cursor, windsurf,
    cline, aider, copilot, zed, amp, jules, continue) are partial; gemini-cli
    keeps its recorded level.
  - skills using `agent` / `context:fork` -> non-Claude agents partial.

This script prints a JSON patch to stdout; review before merging into
data/skills.json. It does NOT modify files in place.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENTS_PATH = ROOT / "data" / "agents.json"
SKILLS_PATH = ROOT / "data" / "skills.json"

# Agents that consume AGENTS.md plain markdown.
AGENTS_MD_AGENTS = {"codex-cli", "zed", "amp", "jules"}
# Agents that need rules-file rewrite (no SKILL.md).
RULE_REWRITE_AGENTS = {"windsurf", "cline"}
# Agents with their own prompt/slash-command file format.
PROMPT_FILE_AGENTS = {"github-copilot", "continue"}
# Aider reads convention files.
CONVENTION_AGENTS = {"aider"}
# All backfill targets (everyone except claude-code, gemini-cli, open-standard).
BACKFILL_TARGETS = (
    AGENTS_MD_AGENTS | RULE_REWRITE_AGENTS | PROMPT_FILE_AGENTS | CONVENTION_AGENTS
)


def infer(skill: dict, agent_id: str) -> tuple[str, str]:
    """Return (level, caveat) for a missing agent cell."""
    compat = skill.get("compatibility", {})
    os_level = compat.get("open-standard", "unknown")
    claude_level = compat.get("claude-code", "unknown")
    extensions = set(skill.get("uses_claude_extensions", []) or [])
    uses_hooks = "hooks" in extensions
    uses_agent = "agent" in extensions
    uses_fork = "context:fork" in extensions or "context:fork" in extensions
    uses_advanced = uses_hooks or uses_agent or uses_fork

    # If the skill is unsupported on the open standard, it can't run anywhere
    # portable.
    if os_level == "unsupported":
        return "unsupported", "Hard dependency on a non-portable runtime; cannot run on this agent."

    # Ceiling for the open-standard level.
    ceiling = os_level if os_level in {"partial", "unsupported"} else "compatible"

    # AGENTS.md agents: skill body inlined into AGENTS.md.
    if agent_id in AGENTS_MD_AGENTS:
        if uses_advanced:
            return "partial", "SKILL.md body inlined into AGENTS.md; Claude-specific hooks/agent/context-fork are dropped."
        if agent_id == "codex-cli":
            return "compatible", "Drop frontmatter; inline the body into AGENTS.md (watch the 32 KiB budget)."
        return "compatible", "Inline the SKILL.md body into AGENTS.md; frontmatter is dropped."

    # Aider: flatten to a CONVENTIONS.md read into context.
    if agent_id in CONVENTION_AGENTS:
        if uses_advanced:
            return "partial", "Flatten to CONVENTIONS.md read via read:; hooks/agent/context-fork cannot be expressed."
        return "compatible", "Flatten the skill body into a CONVENTIONS.md file loaded via .aider.conf.yml read:."

    # Prompt-file agents (Copilot, Continue): convert to a prompt/slash file.
    if agent_id in PROMPT_FILE_AGENTS:
        if uses_advanced:
            return "partial", "Convert to a prompt file for slash invocation; hooks/agent/context-fork are dropped."
        return "compatible", "Convert the skill to a prompt/slash-command file for invocation."

    # Rule-rewrite agents (Windsurf, Cline): need manual rewrite to their rules format.
    if agent_id in RULE_REWRITE_AGENTS:
        if uses_advanced:
            return "partial", "Rewrite as a rules file; hooks/agent/context-fork are dropped."
        return "partial", "Rewrite the SKILL.md into this agent's rules format (description/glob or always-on)."

    return "unknown", ""


def main() -> int:
    agents_doc = json.loads(AGENTS_PATH.read_text(encoding="utf-8"))
    skills_doc = json.loads(SKILLS_PATH.read_text(encoding="utf-8"))
    agents = agents_doc["agents"]
    skills = skills_doc["skills"]
    agent_ids = [a["id"] for a in agents]

    patched = 0
    for skill in skills:
        compat = skill.setdefault("compatibility", {})
        caveats = skill.setdefault("caveats", {})
        changed = False
        for agent_id in agent_ids:
            if agent_id in compat:
                continue
            level, caveat = infer(skill, agent_id)
            compat[agent_id] = level
            if caveat and level != "native":
                caveats.setdefault(agent_id, caveat)
            changed = True
        if changed:
            patched += 1

    print(json.dumps(skills_doc, indent=2, ensure_ascii=False))
    print(f"\n# Backfilled {patched} skills.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
