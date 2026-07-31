---
name: portable-code-review
description: A strictly portable code-review skill. Reviews staged changes against two axes (spec compliance + general code quality) and prints a consolidated report. Uses only open-standard frontmatter (name, description) so it runs unchanged on Claude Code, Gemini CLI, Cursor, Codex CLI, and every other agent in the compatibility matrix.
license: MIT
---

# Portable code review

Review the staged changes (or the changes in the current branch vs. `main`) along **two axes** and produce a single consolidated report.

## When to run

Invoke this skill when the user asks for a code review, a pre-PR check, or a "is this ready to merge?" sanity check.

## Procedure

1. **Gather the diff.** Run `git diff --staged` (or `git diff main...HEAD` if nothing is staged). If the diff is empty, tell the user and stop.

2. **Spec-axis review.** For each changed file, ask:
   - Does this change do what the user (or the linked issue/PR description) asked for?
   - Is there anything missing or half-implemented?
   - Are there obvious regressions vs. the previous behavior?

3. **Quality-axis review.** For each changed file, ask:
   - Are there bugs, off-by-one errors, or unhandled edge cases?
   - Are names clear and consistent with the surrounding code?
   - Is there dead code, unreachable branches, or copy-paste duplication?
   - Are there security concerns (input validation, secrets, injection)?

4. **Consolidate.** Group findings by file. For each finding, state: **severity** (blocker / should-fix / nit), **location** (file:line or function), and **suggested fix**.

5. **Report.** Print a markdown report:

   ```
   ## Code review

   ### Blockers
   - <file>:<line> — <issue> → <suggested fix>

   ### Should fix
   - ...

   ### Nits
   - ...

   ### Verdict
   <merge-ready | needs changes> — <one-line summary>
   ```

## Constraints

- Do **not** modify any files. This is a read-only review.
- Do **not** run any commands other than the read-only `git diff` / `git log` needed to gather context.
- If you cannot determine intent (no linked issue, no description), say so explicitly rather than guessing.

## Why this skill is portable

It uses only `name` + `description` (+ optional `license`) frontmatter — the open-standard subset. No `hooks`, no `agent`, no `context: fork`, no `allowed-tools`, no `model`. It works by instructing the model in plain Markdown, so it loads on:

- **Claude Code** — drop into `.claude/skills/portable-code-review/SKILL.md`
- **Gemini CLI** — drop into `.gemini/skills/portable-code-review/SKILL.md`
- **Cursor** — convert to `.cursor/rules/portable-code-review.mdc` (set `alwaysApply: false`, keep the `description`)
- **Codex CLI / Zed / Amp / Jules** — paste the body into `AGENTS.md`
- **Cline** — paste into `.clinerules/portable-code-review.md`
- **Aider** — add to `.aider.conf.yml` `read:` list
- **Copilot** — convert to `.github/prompts/portable-code-review.prompt.md`
- **Continue** — add as a `customCommands` entry in `config.yaml`

See `docs/porting-guide.md` for the full conversion recipes.
