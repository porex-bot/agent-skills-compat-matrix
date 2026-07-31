#!/usr/bin/env python3
"""Merge data/_new_skills.json into data/skills.json (dedup by id), then backfill
missing agent compatibility cells using the inference rules in backfill_compat,
and write the result back to data/skills.json. Removes the temp file afterwards.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_PATH = ROOT / "data" / "skills.json"
NEW_SKILLS_PATH = ROOT / "data" / "_new_skills.json"
AGENTS_PATH = ROOT / "data" / "agents.json"

# Reuse the inference logic from backfill_compat.
sys.path.insert(0, str(ROOT / "scripts"))
from backfill_compat import infer, BACKFILL_TARGETS  # type: ignore  # noqa: E402


def main() -> int:
    existing = json.loads(SKILLS_PATH.read_text(encoding="utf-8"))
    new = json.loads(NEW_SKILLS_PATH.read_text(encoding="utf-8"))
    agents = json.loads(AGENTS_PATH.read_text(encoding="utf-8"))["agents"]
    agent_ids = [a["id"] for a in agents]

    merged: dict[str, dict] = {}
    # New entries first so they win on id collision (they have fresher data).
    for skill in new:
        merged[skill["id"]] = skill
    for skill in existing.get("skills", []):
        if skill["id"] not in merged:
            merged[skill["id"]] = skill

    skills = list(merged.values())

    # Backfill missing agent cells.
    for skill in skills:
        compat = skill.setdefault("compatibility", {})
        caveats = skill.setdefault("caveats", {})
        for agent_id in agent_ids:
            if agent_id in compat:
                continue
            level, caveat = infer(skill, agent_id)
            compat[agent_id] = level
            if caveat and level != "native":
                caveats.setdefault(agent_id, caveat)

    out = {"skills": skills}
    SKILLS_PATH.write_text(
        json.dumps(out, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    NEW_SKILLS_PATH.unlink()
    print(f"Merged and backfilled: {len(skills)} skills total.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
