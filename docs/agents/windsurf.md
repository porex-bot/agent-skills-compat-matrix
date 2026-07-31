# Windsurf

- **Vendor:** Codeium (Windsurf, Inc.)
- **Homepage:** <https://windsurf.com/>
- **Rules file:** `.windsurfrules (legacy, repo root) → .windsurf/rules/*.md (modern); also reads AGENTS.md`
- **Skill file:** No native SKILL.md; rules served via .windsurf/rules/*.md (SKILL.md not recognized)
- **Install paths:**
  - Project: `.windsurf/rules/<name>.md (legacy .windsurfrules at repo root)`
  - User: `~/.codeium/windsurf/rules/ (global rules also managed via editor Global Rules / Memories)`

## Frontmatter

Required: trigger.

Optional: globs, description.

## Features supported

- Hooks (PreToolUse / PostToolUse / etc.): unsupported
- Subagent spawning: unsupported
- Context fork (`context: fork`): unsupported
- Progressive disclosure (metadata → body → assets): partial
- Pre-approved tools (`allowed-tools`): unsupported
- Slash command invocation (`/skill-name`): unsupported
- Glob-scoped activation: native
- Per-skill model override: unsupported

## Why skills portability breaks here

Activation model is trigger/glob-driven (like Cursor), not description-driven. The frontmatter trigger field accepts always/manual/glob/model_decision; globs is required when trigger=glob, description is used by model_decision and manual. No PreToolUse/PostToolUse hooks, no per-rule subagent spawning, no per-rule tool allowlist, no per-rule model override (Cascade model is chosen globally). SKILL.md is not natively recognized; open-standard skills must be rewritten as .windsurf/rules/*.md files.

## Sources

- <https://windsurf.com/>
- See `data/agents.json` for the structured record.
