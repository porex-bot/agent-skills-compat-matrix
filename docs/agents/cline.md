# Cline

- **Vendor:** Cline (formerly Claude Dev)
- **Homepage:** <https://cline.bot/>
- **Rules file:** `.clinerules (single file) or .clinerules/ (directory of .md files)`
- **Skill file:** No native SKILL.md; project rules via .clinerules (SKILL.md not recognized)
- **Install paths:**
  - Project: `.clinerules (file) or .clinerules/<name>.md (directory)`
  - User: `n/a (global custom instructions and auto-approve live in VS Code settings, not a filesystem path)`

## Frontmatter

Required: none.

Optional: none.

## Features supported

- Hooks (PreToolUse / PostToolUse / etc.): unsupported
- Subagent spawning: unsupported
- Context fork (`context: fork`): unsupported
- Progressive disclosure (metadata → body → assets): partial
- Pre-approved tools (`allowed-tools`): partial
- Slash command invocation (`/skill-name`): unsupported
- Glob-scoped activation: unsupported
- Per-skill model override: unsupported

## Why skills portability breaks here

VS Code extension (formerly Claude Dev). Rules are plain Markdown/.clinerules with no YAML frontmatter; the whole file is loaded as always-on context (no glob/auto-trigger, no description-driven activation). No skills system, no native SKILL.md. Strong Auto-Approve settings panel (toggle per tool family: file edits, commands, MCP, browser) — closest analog to pre-approved tools, but global/workspace setting, not per-skill allowed-tools frontmatter. Model chosen per session in UI. Skills must be flattened into .clinerules; hook/agent extensions cannot be expressed.

## Sources

- <https://cline.bot/>
- See `data/agents.json` for the structured record.
