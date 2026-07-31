# Gemini CLI

- **Vendor:** Google
- **Homepage:** <https://geminicli.com/>
- **Rules file:** `GEMINI.md` (global at `~/.gemini/GEMINI.md`, project at repo root, nested at `<subdir>/GEMINI.md` — loaded from cwd up to root and concatenated)
- **Skill file:** `SKILL.md` (follows the open standard)
- **Install paths:**
  - Project (workspace): `.gemini/skills/<skill-name>/SKILL.md` (or the `.agents/skills/` alias)
  - User: `~/.gemini/skills/<skill-name>/SKILL.md` (or `~/.agents/skills/`)
  - Extension: bundled inside installed extensions

## Frontmatter

Required: `name`, `description`.

Optional (open-standard subset): `license`, `compatibility`, `metadata`, `allowed-tools`.

Gemini does **not** recognize Claude-specific fields (`hooks`, `context: fork`, `agent`, `model`). They are silently ignored.

## Discovery tiers

Precedence (highest to lowest): **Workspace > User > Extension**.

Within the same tier, the `.agents/skills/` alias takes precedence over `.gemini/skills/`. The generic alias exists so the same skill directory works across multiple agent tools.

## Management commands

Interactive session:

- `/skills list` — list discovered skills and their status
- `/skills link <path>` — symlink a local directory into the skills folder
- `/skills enable <name>` / `/skills disable <name>` — toggle (defaults to `user` scope; use `--scope workspace`)
- `/skills reload` — refresh the discovered list

Terminal:

```bash
gemini skills list
gemini skills install https://github.com/user/repo.git
gemini skills install /path/to/local/skill --scope workspace
gemini skills install https://github.com/org/repo.git --path skills/frontend-design
gemini skills uninstall my-expertise --scope workspace
gemini skills enable my-expertise
```

## Hooks

Defined in `.gemini/settings.json` (project or user), not in `SKILL.md` frontmatter:

```json
{
  "hooks": {
    "my-pre-commit-hook": {
      "type": "command",
      "command": "python3 scripts/check-secrets.py",
      "description": "Checks for secrets before writing files",
      "matcher": "write_file|replace",
      "on": "BeforeTool"
    }
  }
}
```

Events: `SessionStart`, `SessionEnd`, `BeforeModel`, `AfterModel`, `BeforeTool`, `AfterTool`, `BeforeAgent`, `AfterAgent`, `BeforeToolSelection`.

This is **the closest peer to Claude Code** for hooks — but the configuration surface is different (settings.json vs. frontmatter), so a Claude skill that ships its own hooks cannot be auto-installed in Gemini without manual porting.

## Features supported

- Hooks: native (configured in settings.json, not frontmatter)
- Subagent spawning: partial (sub-agents exist via `/agents config`, but per-skill `agent:` delegation is not wired)
- Context fork: unsupported
- Progressive disclosure: native (metadata → SKILL.md body → bundled assets)
- Pre-approved tools: partial (`allowed-tools` is read but enforcement is weaker than Claude's)
- Slash command: native
- Glob scoping: unsupported
- Model override: unsupported

## Why skills portability breaks here

Open-standard skills (just `name` + `description` + Markdown body) port cleanly. The two failure modes are:

1. **Hooks** — a Claude skill that bundles `hooks:` in its frontmatter will load in Gemini but the hooks are silently dropped. The user must re-implement them in `settings.json` manually.
2. **Subagent delegation** — `agent: general-purpose` is ignored; Gemini's sub-agent system is configured separately via `/agents config` and is not invoked per-skill.

Skills must enable the experimental flag in settings:

```json
{ "experimental": { "skills": true } }
```

## Sources

- <https://geminicli.com/docs/cli/tutorials/skills-getting-started/>
- <https://gemini.openml.io/cli/skills/>
- <https://agentskills.io/specification>
