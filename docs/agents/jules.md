# Jules

- **Vendor:** Google
- **Homepage:** <https://jules.google/>
- **Rules file:** `AGENTS.md (repo root)`
- **Skill file:** No native SKILL.md; AGENTS.md is the only rules mechanism
- **Install paths:**
  - Project: `AGENTS.md at repo root`
  - User: `n/a (Jules operates on GitHub repos; no user-level rules filesystem path)`

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

Google's async, GitHub-connected coding agent: picks up a task (issue/PR), runs in an isolated cloud VM, opens a pull request. Project instructions from AGENTS.md at repo root (plain Markdown, no YAML frontmatter, no native SKILL.md). No user-level rules path (repo-centric). No hooks, no per-skill subagents (one agent per task, multi-step), no context fork, no per-skill tool allowlist (tool permissions fixed by sandbox VM), no slash-command skill invocation (tasks created from GitHub issue / web UI), no glob scoping, no per-skill model override (runs on Gemini models). Portability similar to Codex CLI (flatten SKILL.md into AGENTS.md) but Jules is async/PR-oriented rather than interactive.

## Sources

- <https://jules.google/>
- See `data/agents.json` for the structured record.
