# Continue

- **Vendor:** Continue Dev, Inc. (open source)
- **Homepage:** <https://www.continue.dev/>
- **Rules file:** `.continue/config.yaml (project; legacy .continuerc.json) and ~/.continue/config.yaml (user)`
- **Skill file:** No native SKILL.md; analog is custom slash-command / prompt files under ~/.continue/prompts/ (or .continue/prompts/)
- **Install paths:**
  - Project: `.continue/config.yaml (or .continuerc.json); .continue/prompts/<name>.prompt`
  - User: `~/.continue/config.yaml; ~/.continue/prompts/<name>.prompt`

## Frontmatter

Required: none.

Optional: description, model, temperature, context.

## Features supported

- Hooks (PreToolUse / PostToolUse / etc.): unsupported
- Subagent spawning: unsupported
- Context fork (`context: fork`): unsupported
- Progressive disclosure (metadata → body → assets): partial
- Pre-approved tools (`allowed-tools`): unsupported
- Slash command invocation (`/skill-name`): native
- Glob-scoped activation: unsupported
- Per-skill model override: partial

## Why skills portability breaks here

Open-source AI coding extension. Rules/configuration live in config.yaml (~/.continue/config.yaml global, .continue/config.yaml or .continuerc.json project) as YAML, not Markdown frontmatter. Skills analog is custom slash commands defined under customCommands/slashCommands (name, description, prompt, optional context providers) in config.yaml, or as separate prompt files in ~/.continue/prompts/ — invoked via /name in chat. No native SKILL.md, no YAML frontmatter on rules. model_override partial: Continue supports many local/cloud models and allows per-slash-command model binding in some prompt-file formats, but it is not the open-standard model field. No hooks, no subagent spawning, no context fork, no per-skill tool allowlist (tool usage governed by global config + approvals), no glob-triggered rules (context pulled via @-mention context providers).

## Sources

- <https://www.continue.dev/>
- See `data/agents.json` for the structured record.
