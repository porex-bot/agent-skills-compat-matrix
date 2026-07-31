# Agent Skills Compatibility Matrix

> One question every AI-coding user asks within a week: *"Will this skill work in my agent?"* This repo answers it, per skill, per agent, with sources.

中文简介：每个 AI 编程 Agent（Claude Code / Cursor / Codex CLI / Gemini CLI / Windsurf / Cline / Aider / Copilot / Zed / Amp / Jules / Continue）都声称支持 Agent Skills，但实际兼容性参差不齐——hooks、子 agent、上下文 fork 这些扩展能力各家都没有。本仓库用一张可校验的矩阵表说明每个开源 Skill 在每个 harness 里的真实支持情况，附带各 Agent 的能力差异详解和跨 Agent 移植指南。

## Why this exists

The Agent Skills open standard ([agentskills.io](https://agentskills.io/)) promises portability. In practice:

- **Claude Code** is a superset — hooks, `context: fork`, subagents, model override all work, but only here.
- **Cursor** and **Windsurf** use glob/trigger-driven activation and have no hooks, no subagents.
- **Codex CLI**, **Zed**, **Amp**, **Jules** read plain `AGENTS.md` with no YAML frontmatter; Codex caps context at 32 KiB.
- **Gemini CLI** implements the open standard plus hooks (configured in `settings.json`, not frontmatter).
- **Cline**, **Aider**, **Continue**, **Copilot** each have their own rules/prompt-file formats with no `SKILL.md`.

A skill that "runs everywhere" often silently loses half its behavior. This matrix records, per skill, **what actually works where** and **what degrades how**.

## Status

37 skills × 13 agents currently tracked. See [`data/skills.json`](data/skills.json) for the structured records and [CONTRIBUTING.md](CONTRIBUTING.md) to add more. Live site: see `site/` or the GitHub Pages deployment.

## Skill × Agent compatibility

Legend: 🟢 native / compatible · 🟡 partial · 🔴 unsupported · ⚪ unknown

| Skill | Category | Claude Code | Cursor | Codex CLI | Gemini CLI | Agent Skills (open standard) | Aider | Amp | Cline | Continue | GitHub Copilot | Jules | Windsurf | Zed |
|---|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| [academic-pipeline](https://github.com/Imbad0202/academic-research-skills) | research | 🟢 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| [agent-skills (production patterns)](https://github.com/addyosmani/agent-skills) | productivity | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| [algorithmic-art](https://github.com/anthropics/skills) | frontend | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | productivity | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [biopython](https://github.com/K-Dense-AI/scientific-agent-skills) | research | 🟢 | 🟢 | 🟡 | 🟢 | 🟡 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [brand-guidelines](https://github.com/anthropics/skills) | marketing | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [browser-testing-with-devtools](https://github.com/addyosmani/agent-skills) | debug | 🟢 | 🟡 | 🟡 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 |
| [caveman-compress](https://github.com/JuliusBrussee/caveman) | productivity | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [ci-cd-and-automation](https://github.com/addyosmani/agent-skills) | devops | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [code-review (dual-axis)](https://github.com/mattpocock/skills) | code-review | 🟢 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| [diagnosing-bugs](https://github.com/mattpocock/skills) | debug | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [dispatching-parallel-agents](https://github.com/obra/superpowers) | refactor | 🟢 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| [frontend-design](https://github.com/anthropics/skills) | frontend | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [graphify](https://github.com/Graphify-Labs/graphify) | research | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [grill-me](https://github.com/mattpocock/skills) | productivity | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [handoff](https://github.com/mattpocock/skills) | productivity | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [last30days-skill](https://github.com/mvanhorn/last30days-skill) | research | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [marketing-skills (Hyper MCP)](https://github.com/hyperfx-ai/marketing-skills) | marketing | 🟢 | 🟡 | 🟡 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 |
| [marketingskills](https://github.com/coreyhaines31/marketingskills) | marketing | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [mcp-builder](https://github.com/anthropics/skills) | backend | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [observability-and-instrumentation](https://github.com/addyosmani/agent-skills) | devops | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [pdf](https://github.com/anthropics/skills) | productivity | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [research](https://github.com/mattpocock/skills) | research | 🟢 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| [security-and-hardening](https://github.com/addyosmani/agent-skills) | code-review | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [serena (LSP semantic edit)](https://github.com/oraios/serena) | refactor | 🟢 | 🟡 | 🟡 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 |
| [shipping-and-launch](https://github.com/addyosmani/agent-skills) | deploy | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [skill-creator](https://github.com/anthropics/skills) | productivity | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [spec-driven-development](https://github.com/addyosmani/agent-skills) | build | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [subagent-driven-development](https://github.com/obra/superpowers) | refactor | 🟢 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| [superpowers (TDD flow)](https://github.com/obra/superpowers) | tdd | 🟢 | 🟡 | 🟡 | 🟢 | 🟢 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| [systematic-debugging](https://github.com/obra/superpowers) | debug | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [tdd](https://github.com/mattpocock/skills) | tdd | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [theme-factory](https://github.com/anthropics/skills) | frontend | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [verification-before-completion](https://github.com/obra/superpowers) | code-review | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [wayfinder](https://github.com/mattpocock/skills) | productivity | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [webapp-testing](https://github.com/anthropics/skills) | debug | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |
| [xlsx](https://github.com/anthropics/skills) | productivity | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 | 🟢 | 🟢 | 🟡 | 🟢 |

Per-cell caveats (why a cell is partial or unsupported) live in [`data/skills.json`](data/skills.json) under the `caveats` field.

## Agent capability matrix

Legend: 🟢 native / compatible · 🟡 partial · 🔴 unsupported · ⚪ unknown

| Feature | Claude Code | Cursor | Codex CLI | Gemini CLI | Agent Skills (open standard) | Aider | Amp | Cline | Continue | GitHub Copilot | Jules | Windsurf | Zed |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Hooks (PreToolUse / PostToolUse / etc.) | 🟢 | 🔴 | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 |
| Subagent spawning | 🟢 | 🟡 | 🔴 | 🟡 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 |
| Context fork (`context: fork`) | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 |
| Progressive disclosure (metadata → body → assets) | 🟢 | 🟡 | 🟡 | 🟢 | 🟢 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 | 🟡 |
| Pre-approved tools (`allowed-tools`) | 🟢 | 🔴 | 🔴 | 🟡 | 🟡 | 🔴 | 🟡 | 🟡 | 🔴 | 🟡 | 🔴 | 🔴 | 🔴 |
| Slash command invocation (`/skill-name`) | 🟢 | 🔴 | 🔴 | 🟢 | 🟢 | 🔴 | 🔴 | 🔴 | 🟢 | 🟢 | 🔴 | 🔴 | 🔴 |
| Glob-scoped activation | 🔴 | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟢 | 🔴 | 🟢 | 🔴 |
| Per-skill model override | 🟢 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🔴 | 🟡 | 🟡 | 🔴 | 🔴 | 🔴 |

Source: [`data/agents.json`](data/agents.json). Per-agent deep dives in [`docs/agents/`](docs/agents/).

## Repository layout

```
.
├── data/
│   ├── schema.json     # JSON Schema for the two datasets below
│   ├── agents.json     # Per-agent capability + install-path records
│   └── skills.json     # Per-skill compatibility records with caveats
├── docs/
│   ├── methodology.md  # How support levels are assigned
│   ├── porting-guide.md# How to port a skill across agents
│   ├── faq.md
│   └── agents/         # One deep-dive markdown file per agent
├── site/               # Static single-page web app (GitHub Pages)
├── scripts/
│   ├── validate.py     # Schema + business-rule validator (runs in CI)
│   ├── generate_readme.py  # Rebuilds this README from the JSON data
│   ├── stats.py        # Coverage and distribution report
│   ├── backfill_compat.py  # Infer missing agent cells (helper)
│   └── merge_skills.py # Merge new skill entries (helper)
└── .github/workflows/
    ├── validate.yml
    ├── generate.yml    # Auto-regenerate README on data changes
    └── deploy-site.yml # Deploy site/ to GitHub Pages
```

## Validate locally

```bash
pip install jsonschema
python scripts/validate.py
```

CI runs the same validator on every PR touching `data/` or `scripts/`.

## Regenerate this README

The tables above are generated from the JSON data — never edit them by hand.

```bash
python scripts/generate_readme.py
```

CI auto-commits any diff on `data/` changes via the `generate.yml` workflow.

## Contribute

Add a skill: append a record to [`data/skills.json`](data/skills.json), run the validator, open a PR. See [CONTRIBUTING.md](CONTRIBUTING.md) for the support-level rubric and verification checklist. New agents welcome — see the "Adding a new agent" section.

## Forking & deployment

After forking, replace the `OWNER` placeholder with your GitHub username or org:

```bash
# from the repo root
git grep -l 'OWNER' | xargs sed -i 's/OWNER/<your-github-name>/g'
```

Then enable GitHub Pages for the site: **Settings → Pages → Source: GitHub Actions**. The `deploy-site.yml` workflow will publish `site/` (with `data/` copied alongside) on every push to `main` that touches `site/` or `data/`.

## License

MIT — see [LICENSE](LICENSE).
