# Aider

- **Vendor:** Paul Gauthier (open source)
- **Homepage:** <https://aider.chat/>
- **Rules file:** `.aider.conf.yml (config) + convention files added via read: (commonly CONVENTIONS.md)`
- **Skill file:** No native SKILL.md; conventions read into context via --read / read: setting
- **Install paths:**
  - Project: `.aider.conf.yml at repo root (with read: CONVENTIONS.md entries)`
  - User: `~/.aider.conf.yml (with read: entries for global conventions)`

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

CLI pair-programmer, not an agentic harness. Rules are convention files (e.g. CONVENTIONS.md) read into every session via the read: key in .aider.conf.yml or --read flag; plain Markdown, no YAML frontmatter, no per-skill directory. No PreToolUse/PostToolUse lifecycle hooks; runs lint/test commands after edits (auto-lint, --test/--lint) — different mechanism. No subagents, no context fork, no per-skill tool allowlist (auto-run via global --yes/--yes-always), no user-defined slash commands, no glob scoping, no per-skill model override (model/weak-model global via --model). Porting means flattening to CONVENTIONS.md; hook/agent/tool-allowlist features cannot be expressed.

## Sources

- <https://aider.chat/>
- See `data/agents.json` for the structured record.
