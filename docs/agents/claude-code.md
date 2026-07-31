# Claude Code

- **Vendor:** Anthropic
- **Homepage:** <https://code.claude.com/>
- **Rules file:** `CLAUDE.md` (user-level at `~/.claude/CLAUDE.md`, project-level at repo root or `.claude/CLAUDE.md`, local override at `CLAUDE.local.md`, nested at `<subdir>/CLAUDE.md`)
- **Skill file:** `SKILL.md`
- **Install paths:**
  - Project: `.claude/skills/<skill-name>/SKILL.md`
  - User: `~/.claude/skills/<skill-name>/SKILL.md`
  - Plugin: `<plugin>/skills/<skill-name>/SKILL.md`
  - Enterprise: managed settings

## Frontmatter

Required: `name`, `description`.

Optional (Claude-specific extensions beyond the open standard):

| Field | Purpose |
|---|---|
| `argument-hint` | Hint shown next to the slash command. |
| `allowed-tools` | Comma-separated tools Claude may use without prompting. |
| `model` | Per-skill model override (`opus`, `sonnet`, `haiku`, or full id). |
| `context` | `fork` runs the skill in an isolated context. |
| `agent` | Delegate to a subagent (e.g., `general-purpose`, `Explore`). |
| `user-invocable` | If `true`, appears as a `/skill-name` command. |
| `disable-model-invocation` | If `true`, only the user can trigger it. |
| `hooks` | PreToolUse / PostToolUse / Stop lifecycle hooks. |

## Features supported

- Hooks: native
- Subagent spawning: native
- Context fork: native
- Progressive disclosure: native
- Pre-approved tools: native
- Slash command: native
- Glob scoping: unsupported (use `description` for auto-triggering)
- Model override: native

## Why skills portability breaks here

Claude Code is a **superset** of the open standard. Skills written with only `name` + `description` (+ optional `license`, `compatibility`, `metadata`) port cleanly to Cursor / Codex / Gemini. Skills that lean on `hooks`, `context: fork`, `agent`, or `model` will run elsewhere but lose that behavior silently.

Custom commands under `.claude/commands/` were merged into skills — a file at `.claude/commands/deploy.md` and `.claude/skills/deploy/SKILL.md` both produce `/deploy`.

## Sources

- <https://code.claude.com/docs/en/skills>
- <https://docs.anthropic.com/en/docs/claude-code/skills>
- <https://agentskills.io/specification>
