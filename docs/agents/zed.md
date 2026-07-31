# Zed

- **Vendor:** Zed Industries
- **Homepage:** <https://zed.dev/>
- **Rules file:** `AGENTS.md (read by the Assistant); .zed/settings.json for project settings`
- **Skill file:** No native SKILL.md; AGENTS.md is the only rules mechanism
- **Install paths:**
  - Project: `AGENTS.md at repo root`
  - User: `n/a (no documented user-level AGENTS.md path; global Assistant settings in ~/.config/zed/settings.json)`

## Frontmatter

Required: none.

Optional: none.

## Features supported

- Hooks (PreToolUse / PostToolUse / etc.): unsupported
- Subagent spawning: unsupported
- Context fork (`context: fork`): unsupported
- Progressive disclosure (metadata → body → assets): partial
- Pre-approved tools (`allowed-tools`): unsupported
- Slash command invocation (`/skill-name`): unsupported
- Glob-scoped activation: unsupported
- Per-skill model override: unsupported

## Why skills portability breaks here

Zed's AI is an inline-edit / Assistant panel feature. Project context via AGENTS.md (read by the Assistant) plus .zed/settings.json; no dedicated rules filesystem, no SKILL.md support, no YAML frontmatter. Model selection is global via Assistant Profiles (each binds a provider+model), not per-rule. Built-in assistant slash commands (/file, /tab, /project) insert context but cannot invoke user-defined skills. No hooks, no subagent spawning, no context fork, no per-skill tool allowlist, no glob-triggered rules. MCP-style Context Servers exist for retrieval but are not a skills system. Porting means flattening a skill body into AGENTS.md; all advanced extensions are dropped.

## Sources

- <https://zed.dev/>
- See `data/agents.json` for the structured record.
