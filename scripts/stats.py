#!/usr/bin/env python3
"""Print a coverage and distribution report for the matrix.

Useful as a CI health check and for contributors to see which agents/categories
are under-verified. Exit code is non-zero only on data errors (not on low
coverage — that is informational).
"""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
AGENTS_PATH = ROOT / "data" / "agents.json"
SKILLS_PATH = ROOT / "data" / "skills.json"

LEVELS = ["native", "compatible", "partial", "unsupported", "unknown"]


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def main() -> int:
    agents = load(AGENTS_PATH)["agents"]
    skills = load(SKILLS_PATH)["skills"]

    print(f"Matrix: {len(skills)} skills × {len(agents)} agents\n")

    # Per-agent support-level distribution.
    print("Per-agent support distribution:")
    print(f"  {'Agent':<22} " + " ".join(f"{l:>10}" for l in LEVELS))
    for a in agents:
        counts = Counter(
            s.get("compatibility", {}).get(a["id"], "unknown") for s in skills
        )
        row = " ".join(f"{counts.get(l, 0):>10}" for l in LEVELS)
        print(f"  {a['name']:<22} {row}")

    # Coverage: share of cells that are not 'unknown'.
    total_cells = len(skills) * len(agents)
    unknown_cells = sum(
        1
        for s in skills
        for a in agents
        if s.get("compatibility", {}).get(a["id"], "unknown") == "unknown"
    )
    coverage = (total_cells - unknown_cells) / total_cells * 100 if total_cells else 0
    print(f"\nVerified cell coverage: {coverage:.1f}% ({total_cells - unknown_cells}/{total_cells})")

    # Per-category skill counts.
    cat_counts = Counter(s.get("category", "other") for s in skills)
    print("\nSkills per category:")
    for cat, n in cat_counts.most_common():
        print(f"  {cat:<16} {n}")

    # Most portable skills (all-native or all-compatible across primary agents).
    primary = ["claude-code", "cursor", "codex-cli", "gemini-cli", "open-standard"]
    fully_portable = []
    for s in skills:
        compat = s.get("compatibility", {})
        levels = {compat.get(a, "unknown") for a in primary}
        if levels <= {"native", "compatible"}:
            fully_portable.append(s["name"])
    print(f"\nFully portable across 5 primary agents: {len(fully_portable)}/{len(skills)}")
    for name in sorted(fully_portable):
        print(f"  - {name}")

    # Skills that depend on Claude-specific extensions (portability risk).
    risky = [s for s in skills if s.get("uses_claude_extensions")]
    print(f"\nSkills using Claude-specific extensions ({len(risky)}):")
    for s in sorted(risky, key=lambda x: x["name"].lower()):
        exts = ", ".join(s.get("uses_claude_extensions", []))
        print(f"  - {s['name']} [{exts}]")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
