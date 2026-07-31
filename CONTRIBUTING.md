# Contributing

Thanks for helping map the skill × agent compatibility surface. This document explains how to add or update entries.

## Quick path

1. Append a record to [`data/skills.json`](data/skills.json) (or update an existing one).
2. Run the validator locally:

   ```bash
   pip install jsonschema
   python scripts/validate.py
   ```

3. If you added a new skill, also update the compatibility table in [`README.md`](README.md).
4. Open a PR. CI runs the same validator.

## Support-level rubric

| Level | When to use it |
|---|---|
| `native` | First-class support; the agent implements every feature the skill uses. **No caveat allowed.** |
| `compatible` | The skill runs unmodified via the open-standard `SKILL.md` subset. Behavior matches the author's intent; only Claude-specific extensions are dropped (and noted). |
| `partial` | The skill loads and produces output, but a documented feature degrades or is missing. A caveat is **required**. |
| `unsupported` | The skill cannot run (missing primitive, hard MCP dependency, etc.). A caveat is recommended. |
| `unknown` | Not yet verified. Use for newly added skills until you run the checklist below. |

Full rubric and verification checklist: [`docs/methodology.md`](docs/methodology.md).

## Required fields for a skill entry

```json
{
  "id": "lowercase-kebab-case-slug",
  "name": "Display Name",
  "repo": "owner/name",
  "url": "https://github.com/owner/name",
  "category": "code-review",
  "description": "One sentence: what the skill does.",
  "compatibility": {
    "claude-code": "native",
    "cursor": "compatible",
    "codex-cli": "partial",
    "gemini-cli": "native",
    "open-standard": "compatible"
  },
  "caveats": {
    "codex-cli": "Explain what breaks and why."
  },
  "uses_claude_extensions": ["hooks", "context:fork"],
  "verified_at": "2026-07-29",
  "verified_by": "your-github-handle"
}
```

The `compatibility` map must include an entry for **every agent** in [`data/agents.json`](data/agents.json). If you have not yet verified a particular agent, set it to `unknown` rather than omitting it. To backfill missing cells mechanically, run `python scripts/backfill_compat.py` (review its inferences before committing).

Allowed `category` values: `code-review`, `tdd`, `refactor`, `debug`, `build`, `deploy`, `research`, `marketing`, `productivity`, `frontend`, `backend`, `devops`, `other`.

## Verification checklist

Before assigning any level other than `unknown`:

1. **Install** the skill in the target agent using the path in [`data/agents.json`](data/agents.json).
2. **Trigger** it via slash command, `description` auto-discovery, or glob match.
3. **Exercise** at least one representative task the skill claims to handle.
4. **Record** observed behavior, including silent fallbacks (hooks skipped, subagents collapsed to inline, etc.).
5. **Set** `verified_at` (ISO date) and `verified_by` (your handle or `matrix-maintainers`).

When official docs and observed behavior diverge, observed behavior wins — note the divergence in the caveat.

## Adding a new agent

If a new coding agent ships rules/skill support (e.g., Windsurf, Cline, Aider, Continue were all added this way), the change touches four places:

1. [`data/agents.json`](data/agents.json) — add an `AgentEntry` with install paths, frontmatter fields, and feature flags. The `id` must be lowercase kebab-case.
2. [`docs/agents/<id>.md`](docs/agents/) — run `python scripts/generate_agent_docs.py` to scaffold the doc page, then flesh out the "Why skills portability breaks here" section.
3. Update every existing skill entry in [`data/skills.json`](data/skills.json) with the new agent's support level. Run `python scripts/backfill_compat.py` to infer defaults mechanically, then review and override where you have verified data.
4. Regenerate the README with `python scripts/generate_readme.py` (CI also does this automatically).

The schema is agent-agnostic — `compatibility` is an open object whose keys must match agent ids in `agents.json`, so you do **not** need to edit `schema.json` when adding an agent. The validator will reject any compatibility/caveat key that does not match a known agent id.

Open an issue first if you're unsure whether the agent meets the bar (some form of native rules or skill-file support, not just generic prompt customization).

## Validation rules the CI enforces

Beyond JSON Schema conformance:

- No duplicate agent ids.
- No duplicate skill ids.
- Every skill's `compatibility` object must include all five agent keys.
- Every support level must be one of `native`, `compatible`, `partial`, `unsupported`, `unknown`.
- `native` cells must not have a caveat. If a caveat applies, the level is wrong — downgrade to `compatible` or `partial`.

## Style

- Keep `description` to one sentence. Detail goes in caveats.
- Caveats explain **what breaks and how**, not just that it breaks. "Cursor has no hooks" is less useful than "PreToolUse hooks are skipped; security checks must be invoked manually."
- ISO 8601 dates only (`YYYY-MM-DD`).

## License

By contributing you agree your contributions are licensed under the project's [MIT license](LICENSE).
