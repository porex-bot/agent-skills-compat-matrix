# Amp

- **Vendor:** Sourcegraph
- **Homepage:** <https://ampcode.com/>
- **Rules file:** `AGENTS.md (repo root + subdirectories, walked and concatenated like Codex)`
- **Skill file:** No native SKILL.md; AGENTS.md is the only rules mechanism
- **Install paths:**
  - Project: `AGENTS.md at repo root or any subdirectory`
  - User: `~/.config/amp/AGENTS.md (global; Amp also exposes global instructions via app settings)`

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

Strong AGENTS.md adopter: rules are plain-Markdown AGENTS.md files (project root + subdirs, merged root→cwd) with no YAML frontmatter and no native SKILL.md. Runtime is richer than Codex CLI — built-in Sourcegraph code-search tools, MCP support, async/background cloud agents, and an approval system — but none of this is wired to per-skill frontmatter. pre_approved_tools partial: Amp has command/tool approval settings (auto-approve vs. ask) but no per-AGENTS.md allowed-tools allowlist. No hooks, no per-skill subagent delegation (background agents are async execution, not skill-scoped), no context fork, no slash-command skill invocation, no glob scoping (directory-scoped only), no per-skill model override.

## Sources

- <https://ampcode.com/>
- See `data/agents.json` for the structured record.
