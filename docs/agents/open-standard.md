# Agent Skills open standard

- **Steward:** Anthropic-originated, community-maintained
- **Homepage:** <https://agentskills.io/>
- **Specification:** <https://agentskills.io/specification>
- **Adopted by:** Claude Code, Gemini CLI, Codex CLI (as `AGENTS.md` fragments), Cursor (as `.mdc` rules with manual conversion), VS Code, GitHub Copilot, and 20+ other tools.

## Directory structure

```
skill-name/
├── SKILL.md            # required: frontmatter + instructions
├── scripts/            # optional: executable code (runs without loading source)
│   └── validate.py
├── references/         # optional: docs loaded on demand
│   └── REFERENCE.md
└── assets/             # optional: templates, data files, schemas
    └── template.json
```

The directory name must match the `name` field exactly.

## Frontmatter

| Field | Required | Constraint |
|---|---|---|
| `name` | yes | 1–64 chars, lowercase letters / digits / hyphens, no leading/trailing hyphen |
| `description` | yes | 1–1024 chars; the primary trigger mechanism — agents use it to decide whether to load the skill |
| `license` | no | SPDX identifier or reference |
| `compatibility` | no | ≤500 chars; environment requirements (e.g., "Requires git, docker") |
| `metadata` | no | Arbitrary key-value pairs |
| `allowed-tools` | no | Space-separated pre-authorized tool list (experimental) |

## Progressive disclosure

Three-tier loading to optimize context usage:

1. **Metadata** (~100 tokens): only `name` + `description` loaded at startup.
2. **Instructions** (recommend <5,000 tokens): full `SKILL.md` body loaded on activation.
3. **Resources** (on demand): `scripts/`, `references/`, `assets/` loaded only when referenced.

## Features supported

- Hooks: unsupported (vendor-specific extension)
- Subagent spawning: unsupported
- Context fork: unsupported
- Progressive disclosure: native
- Pre-approved tools: partial (`allowed-tools` is experimental; enforcement varies by agent)
- Slash command: native (`/skill-name`)
- Glob scoping: unsupported
- Model override: unsupported

## Portability rules of thumb

A skill that uses **only** `name` + `description` (+ optional `license`, `compatibility`, `metadata`) will run on every agent in this matrix, with these caveats:

| Agent | What works | What's dropped |
|---|---|---|
| Claude Code | Everything | Nothing — Claude is a superset |
| Gemini CLI | Body + metadata | Hooks must be re-declared in `settings.json` |
| Codex CLI | Body only | Frontmatter stripped; subject to 32 KiB budget |
| Cursor | Body + `description` | Must convert to `.mdc` with `alwaysApply` + `globs` |

Skills that lean on Claude-specific extensions (`hooks`, `context: fork`, `agent`, `model`) are **not portable** to the open-standard subset. They will load elsewhere but lose that behavior silently.

## Sources

- <https://agentskills.io/specification>
- <https://code.claude.com/docs/en/skills>
