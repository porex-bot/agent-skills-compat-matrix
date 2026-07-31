# GitHub Copilot

- **Vendor:** GitHub (Microsoft)
- **Homepage:** <https://github.com/features/copilot>
- **Rules file:** `.github/copilot-instructions.md (always-on); Copilot coding agent also reads AGENTS.md`
- **Skill file:** No native SKILL.md; analogs are .github/prompts/<name>.prompt.md (slash-invoked) and .github/instructions/<name>.instructions.md (glob-scoped)
- **Install paths:**
  - Project: `.github/copilot-instructions.md, .github/prompts/<name>.prompt.md, .github/instructions/<name>.instructions.md`
  - User: `n/a (user custom instructions in VS Code / GitHub settings; prompt and instruction files are workspace-scoped)`

## Frontmatter

Required: none.

Optional: description, mode, tools, model, applyTo.

## Features supported

- Hooks (PreToolUse / PostToolUse / etc.): unsupported
- Subagent spawning: unsupported
- Context fork (`context: fork`): unsupported
- Progressive disclosure (metadata → body → assets): partial
- Pre-approved tools (`allowed-tools`): partial
- Slash command invocation (`/skill-name`): native
- Glob-scoped activation: native
- Per-skill model override: partial

## Why skills portability breaks here

Closest analog to skills splits into two file types. Prompt files (.github/prompts/*.prompt.md) are slash-invoked via /prompt-name in Chat and accept frontmatter: description, mode (chat/agent/edit), tools (per-prompt tool allowlist), model (per-prompt override, constrained to Copilot catalog). Instruction files (.github/instructions/*.instructions.md) auto-apply based on applyTo glob. .github/copilot-instructions.md is always-on. Cloud Copilot coding agent additionally reads AGENTS.md. No native SKILL.md, no hooks, no subagents, no context fork. pre_approved_tools partial because the prompt-file tools field is a real per-prompt allowlist but uses Copilot-specific tool identifiers. model_override partial because the model field exists but is limited to Copilot-offered models.

## Sources

- <https://github.com/features/copilot>
- See `data/agents.json` for the structured record.
