# Cursor

- **Vendor:** Anysphere
- **Homepage:** <https://www.cursor.com/>
- **Rules file:** `.cursor/rules/*.mdc` (modern); legacy `.cursorrules` at repo root (deprecated)
- **Skill file:** `.mdc` rule files. `SKILL.md` files also load but lose Claude-specific fields.
- **Install paths:**
  - Project: `.cursor/rules/<name>.mdc`
  - User: `~/.cursor/rules/<name>.mdc`

## Frontmatter

Required: `description`.

Optional:

| Field | Purpose |
|---|---|
| `globs` | Gitignore-style patterns; rule auto-activates when matching files are in context. |
| `alwaysApply` | `true` injects the rule into every prompt. |

## Four activation modes

The combination of `alwaysApply` and `globs` determines activation:

| `alwaysApply` | `globs` | Behavior |
|---|---|---|
| `true` | empty | Always injected. |
| `false` | set | Auto-attached when matching files are referenced. |
| `false` | empty (with `description`) | Agent decides relevance from `description`. |
| `false` | empty (no `description`) | Manual only — invoke with `@rule-name`. |

## Features supported

- Hooks: unsupported
- Subagent spawning: partial (no isolated parallel agents; runs inline)
- Context fork: unsupported
- Progressive disclosure: partial (no `scripts/` / `references/` tier; whole body loads)
- Pre-approved tools: unsupported
- Slash command: unsupported (use `@rule-name` mentions instead)
- Glob scoping: native
- Model override: unsupported

## Why skills portability breaks here

Cursor's activation model is **file-glob driven**, not description-driven like Claude/Gemini. A Claude skill that auto-triggers on "user asks for code review" must be rewritten as either:

- an `alwaysApply: false` + `description` rule (Cursor reads the description and decides), or
- a `globs` rule scoped to `**/*.{ts,tsx,py,go}` so it fires on code files.

Cursor has no hooks, no per-skill tool allowlist, no subagent isolation. Skills that rely on `PreToolUse` hooks to block writes, or on `agent: general-purpose` to spawn a parallel reviewer, will run but skip that behavior.

The legacy `.cursorrules` (single plain-text file at repo root) is still supported but deprecated; new projects should use `.cursor/rules/*.mdc`.

## Sources

- <https://cursor.zone/docs/context/ai-rules.html>
- <https://www.morphllm.com/cursor-rules-best-practices>
- <https://skills-hub.ai/cursor-rules>
