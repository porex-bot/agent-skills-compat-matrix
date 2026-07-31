# FAQ

## Why not just use the open standard everywhere?

The [Agent Skills open standard](https://agentskills.io/) defines a portable `SKILL.md` with `name` + `description` (+ optional `license`, `compatibility`, `metadata`, `allowed-tools`). Skills written to that subset do run on every agent in this matrix. The problem is that the most useful skills lean on **vendor-specific extensions** — hooks, subagents, context forks, per-skill model overrides — that the open standard does not cover. Those extensions silently vanish when you move the skill to a different agent.

This matrix exists to make that silent loss **visible and explicit**, cell by cell.

## Why is Claude Code `native` for almost every skill?

Claude Code is a **superset** of the open standard. It implements every feature the standard defines, plus hooks, `context: fork`, subagent delegation, per-skill `allowed-tools`, and `model` override. So a skill written for the open standard — or for any other agent — runs on Claude Code with no loss. The interesting portability questions go the other direction: *away from* Claude Code.

## Why is `compatible` shown with the same emoji as `native`?

Both are green (🟢) because from a user's perspective the skill works as intended. The difference is provenance: `native` means the agent implements the skill's required features first-class; `compatible` means the skill runs unmodified via the open-standard subset, with only Claude-specific extensions dropped. The exact level and any caveat are visible in the data files and the detail modal on the site.

## How do you verify a cell?

See [`docs/methodology.md`](methodology.md). In short: install the skill in the target agent via its documented path, trigger it, exercise a representative task, and record what degrades. `verified_at` and `verified_by` are required fields. When official docs and observed behavior diverge, observed behavior wins.

## A cell says `partial` — can I still use the skill?

Usually yes. `partial` means the skill loads and produces output, but a documented feature degrades or is missing. Read the `caveats` field for that cell to see exactly what breaks. For example, a skill that spawns parallel review subagents in Claude Code will run sequential inline reviews in Cursor — slower, but still useful.

## A cell says `unsupported` — what does that mean?

The skill cannot run on that agent at all. Common causes: a hard dependency on an MCP server the agent doesn't support, or a feature with no workaround (e.g. `context: fork` outside Claude Code). The `caveats` field explains why.

## Why is `unknown` a level?

For newly added skills or agents before a maintainer runs the verification checklist. It is an explicit "we don't know yet" rather than a silent gap. The validator accepts it; the stats script reports coverage as the share of non-`unknown` cells.

## How do I add a new agent?

See [CONTRIBUTING.md](../CONTRIBUTING.md#adding-a-new-agent). In short: add an `AgentEntry` to `data/agents.json`, run `scripts/generate_agent_docs.py` to scaffold its doc page, add its id to every skill's `compatibility` (default `unknown`), and update the README via `scripts/generate_readme.py`. Open an issue first if you're unsure whether the agent meets the bar (native rules/skill support, not just generic prompt customization).

## The README tables look auto-generated — can I edit them?

No. The tables are regenerated from `data/*.json` by `scripts/generate_readme.py` on every change to `data/`. Editing them by hand will be overwritten by CI. Edit the JSON, then run the generator locally (or let CI do it).

## Is the site built from the same data?

Yes. `site/index.html` fetches `data/agents.json` and `data/skills.json` at runtime. The GitHub Pages deployment (`deploy-site.yml`) copies the data files next to the HTML so relative `./data` paths resolve. There is no separate build step or duplicated data.

## How is this different from awesome-mcp-servers or awesome-claude-skills?

Those are **static curated lists** — link dumps with at most a one-line description. This is a **structured, validated dataset** with per-cell compatibility records, machine-checkable business rules, an auto-generated README, a queryable site, and a porting guide. The value is the matrix cells and their caveats, not the list of links.

## The data looks wrong for cell X. What do I do?

Open a PR with the corrected level and an updated `caveats` entry, or open an issue with your observed behavior and the agent + skill versions you tested. See [CONTRIBUTING.md](../CONTRIBUTING.md).
