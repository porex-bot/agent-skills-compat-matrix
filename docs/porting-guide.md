# Porting guide: moving a skill across agents

A practical guide to taking a skill written for one agent and making it run on another. The matrix tells you **whether** it works; this guide tells you **how**.

## The five-minute portability test

Before porting, check two things in the skill's `SKILL.md`:

1. **Does it use Claude-specific frontmatter?** Look for `hooks`, `context: fork`, `agent`, `allowed-tools`, `model`, `user-invocable`, `disable-model-invocation`. If yes, that behavior will be lost on non-Claude agents.
2. **Does it depend on an MCP server or bundled scripts?** If the skill is really a wrapper around a tool (e.g. `chrome-devtools` MCP, `serena` LSP), the skill text ports but the tool must be installed and configured separately on each agent.

If neither applies, the skill is **pure-prompt** and ports to every agent in this matrix with at most a file-format conversion.

## Target-by-target recipes

### → Claude Code (the superset)

Everything ports here. Drop the skill into `.claude/skills/<name>/SKILL.md` and it works. If you wrote it for another agent, add `name` + `description` frontmatter to get slash-command invocation and description-driven auto-triggering.

### → Gemini CLI

Open-standard skills (just `name` + `description`) work natively. The only failure mode is **hooks**: a Claude skill that bundles `hooks:` in frontmatter will load in Gemini but the hooks are silently dropped. Re-declare them in `.gemini/settings.json`:

```json
{
  "hooks": {
    "my-hook": {
      "type": "command",
      "command": "python3 scripts/check.py",
      "matcher": "write_file|replace",
      "on": "BeforeTool"
    }
  }
}
```

Enable the experimental flag: `{ "experimental": { "skills": true } }`.

### → Cursor

Cursor does not use `SKILL.md` description-driven triggering. Convert each skill to a `.cursor/rules/<name>.mdc` file with frontmatter:

```yaml
---
description: One-liner used by Cursor to decide relevance.
globs: "**/*.{ts,tsx}"
alwaysApply: false
---
```

Pick the activation mode:

| You want… | `alwaysApply` | `globs` |
|---|---|---|
| Always-on context | `true` | (empty) |
| Fire when editing certain files | `false` | `**/*.py` |
| Cursor decides from the description | `false` | (empty) |
| Manual `@rule-name` only | `false` | (empty, no description) |

Hooks, subagents, `context: fork`, `allowed-tools`, `model` — all dropped. A skill that gates writes via `PreToolUse` hooks becomes guidance only.

### → Windsurf

Same idea as Cursor, but with `.windsurf/rules/<name>.md` and a `trigger` field (`always` / `manual` / `glob` / `model_decision`). `globs` is required when `trigger: glob`; `description` is used when `trigger: model_decision`. SKILL.md is not recognized.

### → Codex CLI / Zed / Amp / Jules (AGENTS.md family)

These read plain `AGENTS.md` Markdown. Strip the YAML frontmatter and inline the skill body into the relevant `AGENTS.md`:

```bash
# Extract just the body (everything after the second ---)
awk 'BEGIN{f=0} /^---$/{f++; next} f>=2{print}' SKILL.md >> AGENTS.md
```

Caveats:
- **Codex CLI**: 32 KiB combined budget. If the skill is large, split it across subdirectory `AGENTS.md` files.
- **Zed / Amp**: model is global (Assistant Profiles / app settings), no per-skill override.
- **Jules**: async, repo-centric. No user-level path. Skills become PR-time instructions.
- Reference any `scripts/` assets by explicit path in the Markdown — these agents do not auto-discover skill directories.

### → Cline

Flatten the skill into `.clinerules` (single file) or `.clinerules/<name>.md` (directory). No frontmatter, no auto-trigger — the whole file is always-on context. For selective activation, split into multiple `.md` files and instruct the model in chat to follow a specific one.

### → Aider

Flatten into a `CONVENTIONS.md` (or any Markdown file) and add it to `.aider.conf.yml`:

```yaml
read:
  - CONVENTIONS.md
  - skills/my-skill.md
```

Aider reads these into every session as always-on context. No frontmatter, no per-skill tool allowlist (use global `--yes` / `--yes-always`).

### → GitHub Copilot

Two conversion targets:

- **Slash-invoked** (like a `/skill-name` command): write `.github/prompts/<name>.prompt.md` with frontmatter `description`, `mode: agent`, optional `tools` and `model`.
- **Auto-applied on certain files**: write `.github/instructions/<name>.instructions.md` with frontmatter `applyTo: "**/*.py"`.

`.github/copilot-instructions.md` is always-on (the analog of `CLAUDE.md`). The cloud Copilot coding agent also reads `AGENTS.md`.

### → Continue

Define a slash command in `~/.continue/config.yaml`:

```yaml
customCommands:
  - name: my-skill
    description: What this skill does
    prompt: |
      <paste the skill body here>
```

Or drop a prompt file in `~/.continue/prompts/my-skill.prompt`. Invoke with `/my-skill`. Per-prompt `model` binding is supported in some versions.

## What never ports

These capabilities have **no equivalent** outside Claude Code and (partly) Gemini CLI:

| Capability | Available on | Workaround elsewhere |
|---|---|---|
| `context: fork` (isolated context per skill run) | Claude Code only | None — runs inline in shared context |
| Per-skill `agent` subagent delegation | Claude Code (native), Gemini CLI (manual) | Collapse to inline sequential execution |
| Per-skill `model` override | Claude Code (native), Copilot/Continue (limited) | Use the global model |
| `PreToolUse` / `PostToolUse` hooks | Claude Code, Gemini CLI | Instruction-only guidance ("before writing, run X") |
| Per-skill `allowed-tools` allowlist | Claude Code (native), open standard (experimental) | Global auto-approve settings |

If your skill critically depends on one of these, mark the non-supporting agents as `partial` or `unsupported` in `data/skills.json` and explain the degradation in the `caveats` field.

## Checklist before marking a cell `compatible`

1. The skill loads without errors in the target agent.
2. Its primary task produces equivalent output.
3. Any dropped feature is documented in the `caveats` field.
4. You set `verified_at` and `verified_by`.

If any step fails, downgrade to `partial` (works but degraded) or `unsupported` (cannot run).
