# Methodology

How support levels are assigned to each skill × agent cell.

## Support levels

| Level | Meaning |
|---|---|
| `native` | First-class support. The agent implements the skill's required features directly. No caveats. |
| `compatible` | The skill runs unmodified on this agent using the open standard `SKILL.md` subset. Behavior matches the skill author's intent; only Claude-specific extensions (if any) are dropped. |
| `partial` | The skill loads and produces output, but a documented feature degrades or is missing. The `caveats` field must explain what breaks and how. |
| `unsupported` | The skill cannot run on this agent at all (missing primitive, hard dependency on a non-portable MCP server, etc.). |
| `unknown` | Not yet verified. Default for newly added skills until a maintainer runs the checklist below. |

## Verification checklist

Before assigning any level other than `unknown`, a contributor must:

1. **Install** the skill in the target agent using its documented install path (see `data/agents.json` → `install_path`).
2. **Trigger** the skill via its intended invocation: slash command, auto-discovery via `description`, or glob match.
3. **Exercise** at least one representative task the skill claims to handle.
4. **Record** the observed behavior, including any silent fallbacks (e.g., hooks skipped, subagents collapsed to inline passes).
5. **Set** `verified_at` to the verification date (ISO 8601) and `verified_by` to the contributor's GitHub handle or `matrix-maintainers`.

## Caveats policy

- `native` cells must not have a caveat. The validator rejects this.
- `compatible`, `partial`, `unsupported`, and `unknown` cells may carry a caveat. `partial` and `unsupported` cells **should** carry one — the value of this matrix is the explanation, not the emoji.

## Sources

Per-agent behavior is verified against:

- Official agent documentation (linked in each `docs/agents/*.md` file).
- The [Agent Skills open specification](https://agentskills.io/specification).
- Hands-on testing in a clean environment.

When official docs and observed behavior diverge, observed behavior wins and the divergence is noted in the caveat.
