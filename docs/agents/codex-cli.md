# Codex CLI

- **Vendor:** OpenAI
- **Homepage:** <https://developers.openai.com/codex/cli>
- **Rules file:** `AGENTS.md` (stewarded by the Agentic AI Foundation under the Linux Foundation; adopted by 60,000+ repos)
- **Skill file:** No separate skill file. `SKILL.md` content must be inlined or referenced from `AGENTS.md`.
- **Install paths:**
  - Project: `AGENTS.md` at repo root, or any subdirectory (walked from cwd up to root)
  - User: `~/.codex/AGENTS.md`
  - Override: `AGENTS.override.md` at any level **replaces** (not merges) the same-level `AGENTS.md`

## Format

Plain Markdown. No YAML frontmatter (v1.1 proposes optional `description` + `tags`). No required headings. No build step.

## Discovery and merging

1. **Global scope:** `~/.codex/AGENTS.override.md` (if present, skips `AGENTS.md`), then `~/.codex/AGENTS.md`.
2. **Project scope:** Codex walks from the Git root down to the current working directory. At each level it reads `AGENTS.override.md` (if present) or `AGENTS.md`.
3. **Merge:** All discovered files are concatenated root → cwd. Deeper files appear later and weigh more heavily.

## The 32 KiB budget

Codex stops reading once it has accumulated `project_doc_max_bytes` (default 32 KiB) of `AGENTS.md` content. Large skill libraries may be **silently truncated** — the most common cause of "Codex is ignoring my instructions" complaints.

Tune via `~/.codex/config.toml`:

```toml
project_doc_max_bytes = 65536  # 64 KiB
project_doc_fallback_filenames = ["CLAUDE.md", "README.md"]
```

## Features supported

- Hooks: unsupported
- Subagent spawning: unsupported
- Context fork: unsupported
- Progressive disclosure: partial (no `scripts/` / `references/` auto-loading; everything inlined)
- Pre-approved tools: unsupported
- Slash command: unsupported
- Glob scoping: unsupported
- Model override: unsupported

## Why skills portability breaks here

Codex is the **most constrained** of the four. The open standard's `SKILL.md` does not map directly: there is no per-skill directory, no frontmatter, no auto-triggering from `description`. To port a skill:

1. Strip the YAML frontmatter.
2. Append the body to the relevant `AGENTS.md` (project or user).
3. Reference any `scripts/` assets explicitly with paths in the Markdown.
4. Watch the 32 KiB budget — split into multiple `AGENTS.md` files in subdirectories if needed.

Skills that depend on hooks, subagents, or per-skill tool allowlists cannot be expressed at all.

## Sources

- <https://developers.openai.com/codex/guides/agents-md>
- <https://thepromptshelf.dev/blog/agents-md-codex-setup-guide-2026/>
- <https://codersera.com/blog/agents-md-complete-guide-2026/>
