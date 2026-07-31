#!/usr/bin/env python3
"""One-off helper: enrich each skill with a detailed bilingual description.

For every skill in data/skills.json, replace `description` with a clearer
"what it does + what effect it has" English line, and add `description_zh`
with the Chinese equivalent. The website picks the right one based on the
current UI language.

Run once; safe to re-run (idempotent — overwrites from the dict below).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_PATH = ROOT / "data" / "skills.json"

# id -> (english, chinese). English is rewritten to clearly state
# purpose + effect. Chinese mirrors it.
DESCRIPTIONS: dict[str, tuple[str, str]] = {
    "anthropics-skill-creator": (
        "Drafts, evaluates, and iteratively improves agent skills using a bundled eval harness with quantitative benchmarks. Effect: produces higher-quality skills whose behavior is measured, not guessed.",
        "用内置的评测工具和量化基准来起草、评估并迭代改进 agent skill。效果：产出的 skill 质量更高，行为有数据支撑而非凭感觉。",
    ),
    "anthropics-webapp-testing": (
        "Drives, inspects, and verifies local web apps with Playwright via a bundled with_server.py lifecycle helper. Effect: catches runtime/DOM/console regressions before a human would, without manual clicking.",
        "用 Playwright 驱动、检查并验证本地 web 应用，附带 with_server.py 生命周期助手。效果：在人工点击之前就能发现运行时、DOM、控制台的回归问题。",
    ),
    "anthropics-pdf": (
        "Extracts, merges, splits, OCRs, and encrypts PDFs using pypdf, pdfplumber, reportlab, and qpdf with bundled reference docs. Effect: turns ad-hoc PDF chores into reliable, repeatable pipelines.",
        "用 pypdf、pdfplumber、reportlab、qpdf 完成 PDF 的抽取、合并、拆分、OCR、加密，附带参考文档。效果：把零散的 PDF 处理变成可靠、可重复的流水线。",
    ),
    "anthropics-xlsx": (
        "Creates and edits spreadsheets with openpyxl and pandas plus a mandatory LibreOffice recalc step and financial-modeling conventions. Effect: ships workbooks whose cached formula values are correct on first open in Excel.",
        "用 openpyxl 和 pandas 创建、编辑电子表格，强制走 LibreOffice 重算步骤，遵循金融建模规范。效果：交付的工作簿在 Excel 中首次打开时缓存的公式值就是正确的。",
    ),
    "anthropics-frontend-design": (
        "Gives opinionated visual-design direction for UI builds — palette, typography, layout — plus a self-critique pass to avoid templated AI aesthetics. Effect: UIs that look intentionally designed instead of generic.",
        "为 UI 构建提供有主见的视觉设计方向（配色、字体、布局），并做一轮自我批判以避免模板化的 AI 审美。效果：产出的界面像是有意设计的，而非千篇一律。",
    ),
    "anthropics-mcp-builder": (
        "Guides building high-quality MCP servers in TypeScript or Python across design, implementation, review, and evaluation. Effect: ships MCP servers that follow consistent structure and pass review on the first try.",
        "指导用 TypeScript 或 Python 构建高质量 MCP server，覆盖设计、实现、评审、评测。效果：交付的 MCP server 结构一致，首次评审即可通过。",
    ),
    "anthropics-brand-guidelines": (
        "Applies Anthropic brand colors and Poppins/Lora typography to artifacts via python-pptx with font fallbacks. Effect: generated slides/docs match the brand spec without manual reformatting.",
        "用 python-pptx 将 Anthropic 品牌色和 Poppins/Lora 字体应用到产物上，带字体回退。效果：生成的幻灯片/文档符合品牌规范，无需手工重排。",
    ),
    "anthropics-theme-factory": (
        "Generates coherent design-token themes — color, typography, spacing — for UI projects from a brief. Effect: gives a project a consistent, reusable token system in one pass instead of ad-hoc values.",
        "根据需求为 UI 项目生成一致的设计令牌主题（颜色、字体、间距）。效果：一次性给项目一套一致、可复用的令牌体系，而非零散取值。",
    ),
    "anthropics-algorithmic-art": (
        "Produces generative-art sketches on canvas, SVG, and Processing with deliberate compositional and palette choices. Effect: outputs sketches with intentional composition instead of random noise.",
        "在 canvas、SVG、Processing 上生成生成艺术草图，带有意的构图和配色选择。效果：产出的草图有刻意构图，而非随机噪声。",
    ),
    "superpowers-dispatching-parallel-agents": (
        "Delegates two or more independent tasks to isolated parallel subagents, crafting focused prompts and integrating their results. Effect: finishes independent work concurrently and keeps each task's context clean.",
        "把两个或多个独立任务委派给隔离的并行子 agent，精心编写聚焦的提示并整合结果。效果：独立工作并发完成，且每个任务的上下文保持干净。",
    ),
    "superpowers-subagent-driven-development": (
        "Executes implementation plans by dispatching a fresh implementer subagent per task, plus per-task and final whole-branch reviews. Effect: each task gets a clean context and an independent review, raising code quality at the branch level.",
        "按实现计划为每个任务派发全新的实现子 agent，并做逐任务和整分支的评审。效果：每个任务都有干净上下文和独立评审，提升整分支的代码质量。",
    ),
    "superpowers-systematic-debugging": (
        "Four-phase root-cause debugging discipline that forbids symptom fixes by requiring investigation before any fix is proposed. Effect: eliminates patch-on-patch fixes and finds the actual cause.",
        "四阶段根因调试纪律，要求先调查再提修复方案，禁止只治症状。效果：消除补丁套补丁的修复，找到真正的根因。",
    ),
    "superpowers-verification-before-completion": (
        "Enforces evidence-before-claims by requiring fresh verification command output before any success or completion assertion. Effect: stops the agent from claiming 'done' without proof.",
        "强制先有证据再下结论——任何成功或完成断言前必须先跑验证命令并看输出。效果：阻止 agent 没有证据就声称'完成'。",
    ),
    "addyosmani-browser-testing-with-devtools": (
        "Live browser testing via the chrome-devtools MCP server for DOM inspection, console errors, network analysis, and performance profiling. Effect: reproduces and diagnoses front-end bugs in a real browser session.",
        "通过 chrome-devtools MCP server 做实时浏览器测试，检查 DOM、控制台错误、网络请求、性能。效果：在真实浏览器会话里复现并诊断前端 bug。",
    ),
    "addyosmani-ci-cd-and-automation": (
        "Sets up CI/CD quality-gate pipelines from lint through e2e with shift-left checks and small-batch deployment strategy. Effect: gives a repo a working pipeline that gates merges on quality signals.",
        "搭建从 lint 到 e2e 的 CI/CD 质量门禁流水线，带左移检查和小批量部署策略。效果：给仓库一套能用的流水线，按质量信号门禁合并。",
    ),
    "addyosmani-security-and-hardening": (
        "Security-first hardening via STRIDE threat modeling over trust boundaries covering input validation, auth, secrets, and transport. Effect: surfaces concrete threats and where to mitigate them, not generic advice.",
        "用 STRIDE 威胁建模在信任边界上做安全优先的加固，覆盖输入校验、鉴权、密钥、传输。效果：给出具体的威胁和缓解点，而非泛泛建议。",
    ),
    "addyosmani-spec-driven-development": (
        "Gated specify-plan-tasks-implement workflow that writes a reviewed spec before any code, surfacing assumptions and boundaries. Effect: catches wrong assumptions before code is written, reducing rework.",
        "门禁式的 specify-plan-tasks-implement 工作流，写代码前先产出经评审的规格，暴露假设和边界。效果：在写代码前就抓住错误假设，减少返工。",
    ),
    "addyosmani-shipping-and-launch": (
        "Pre-launch checklist and staged-rollout or rollback strategy covering code quality, security, performance, and monitoring. Effect: makes launches auditable and reversible instead of all-or-nothing.",
        "发布前清单 + 分阶段上线/回滚策略，覆盖代码质量、安全、性能、监控。效果：让发布可审计、可回滚，而非一锤子买卖。",
    ),
    "addyosmani-observability-and-instrumentation": (
        "Adds logging, metrics, tracing, and alerting telemetry alongside features by defining on-call questions before instrumenting. Effect: ships features that are already observable, not black boxes in prod.",
        "在开发功能的同时加日志、指标、链路追踪、告警，先定义值班问题再加埋点。效果：交付的功能天生可观测，而非生产环境的黑盒。",
    ),
    "mattpocock-handoff": (
        "Compacts the current conversation into a redacted handoff document with suggested skills for a fresh agent session. Effect: lets you continue work in a new context window without losing thread or leaking secrets.",
        "把当前对话压缩成一份脱敏的交接文档，并推荐下个会话用的 skill。效果：在新上下文窗口继续工作时不丢线索、不泄密。",
    ),
    "mattpocock-wayfinder": (
        "Charts huge efforts as a shared map of decision tickets on the issue tracker, resolving them one at a time until the route is clear. Effect: turns an overwhelming project into a queue of single, decidable questions.",
        "把大型项目画成 issue tracker 上的决策工单地图，逐个解决直到路径清晰。效果：把令人无从下手的项目变成一串可单独决策的问题。",
    ),
    "mattpocock-research": (
        "Spins up a background agent to investigate a question against primary sources and write cited findings to a Markdown file. Effect: you keep working while research runs in parallel and lands as a cited doc.",
        "起一个后台 agent 针对原始资料调研某个问题，把带引用的结论写成 Markdown。效果：你继续干活，调研在后台并行跑，最终落地成带引用的文档。",
    ),
    "mattpocock-tdd": (
        "Red-green TDD reference defining seams, anti-patterns, and vertical-slice loop rules that produce tests worth keeping. Effect: yields tests that guide design and survive refactors, not tests that rot.",
        "红绿 TDD 参考，定义接缝、反模式、垂直切片循环规则，产出值得保留的测试。效果：得到能引导设计、能扛重构的测试，而非会腐烂的测试。",
    ),
    "mattpocock-diagnosing-bugs": (
        "Six-phase hard-bug diagnosis loop that demands a tight red-capable feedback loop before any hypothesis, with bisection and instrumentation. Effect: turns flaky, hard-to-repro bugs into reproducible, locatable failures.",
        "六阶段疑难 bug 诊断循环，要求先有能复现的红色反馈循环再提假设，配合二分和埋点。效果：把难复现的 bug 变成可复现、可定位的故障。",
    ),
    "caveman-compress": (
        "Compresses natural-language memory files into caveman-speak via a bundled Python CLI, cutting roughly 65 percent of input tokens while preserving code and URLs. Effect: fits more project context into a model's budget without losing the parts that matter.",
        "用内置 Python CLI 把自然语言记忆文件压缩成'穴居人语'，约省 65% 输入 token，同时保留代码和 URL。效果：在模型预算里塞进更多项目上下文，又不丢关键部分。",
    ),
    "graphify": (
        "Turns any codebase, docs, and configs into a queryable knowledge graph via local tree-sitter AST parsing, with HTML viz, GraphRAG JSON, and an audit report. Effect: lets the agent answer structural questions about a repo it couldn't from raw files.",
        "用本地 tree-sitter AST 解析把任意代码库、文档、配置变成可查询的知识图谱，输出 HTML 可视化、GraphRAG JSON 和审计报告。效果：让 agent 能回答从原始文件答不了的结构性问题。",
    ),
    "academic-pipeline": (
        "Ten-stage orchestrator coordinating deep-research, academic-paper, and reviewer skills with mandatory integrity gates and two-stage peer review. Effect: produces a reviewed, citation-backed academic draft instead of a one-shot essay.",
        "十阶段编排器，协调深度研究、学术论文、评审 skill，带强制诚信门禁和两阶段同行评审。效果：产出经评审、有引用支撑的学术草稿，而非一次性文章。",
    ),
    "scientific-biopython": (
        "Biopython toolkit for sequence manipulation, FASTA/GenBank/PDB parsing, phylogenetics, and programmatic NCBI/PubMed access. Effect: lets the agent run real bioinformatics workflows instead of describing them.",
        "Biopython 工具集，做序列操作、FASTA/GenBank/PDB 解析、系统发育、程序化访问 NCBI/PubMed。效果：让 agent 真正跑生信流程，而非只是描述。",
    ),
    "karpathy-claude-md": (
        "A single CLAUDE.md encoding Andrej Karpathy's LLM-coding-pitfall observations to steer the agent toward better coding behavior. Effect: bakes hard-won coding lessons into always-on context so the agent avoids common traps.",
        "一份 CLAUDE.md，编码了 Andrej Karpathy 对 LLM 编程陷阱的观察，引导 agent 更好地编码。效果：把来之不易的编程经验变成常驻上下文，让 agent 避开常见坑。",
    ),
    "superpowers-tdd": (
        "Vertical-slice red-green-refactor TDD methodology packaged as Spec→Plan→Implement→Review→Ship skills. Effect: enforces a full TDD loop per slice so features ship with covering tests by construction.",
        "垂直切片的红绿重构 TDD 方法论，打包成 Spec→Plan→Implement→Review→Ship 一组 skill。效果：每个切片强制走完整 TDD 循环，功能天生带覆盖测试。",
    ),
    "mattpocock-grill-me": (
        "The agent relentlessly interrogates the user until every decision branch is resolved. Effect: cures 'start before requirements are clear' by forcing ambiguity to surface upfront.",
        "agent 持续追问用户，直到每个决策分支都明确。效果：治好'需求没理清就开始'的毛病，把含糊处逼到台前。",
    ),
    "mattpocock-code-review": (
        "Standard-axis plus spec-axis parallel code review — spawns two review agents and aggregates findings. Effect: catches both spec drift and quality issues in one pass, with independent reviewers.",
        "标准轴 + 规格轴的并行代码评审——派发两个评审 agent 并汇总发现。效果：一轮同时抓住规格偏离和质量问题，且评审相互独立。",
    ),
    "addyosmani-agent-skills": (
        "Senior-engineer quality discipline: pre-commit checks, security review, dependency audits, output validation. Effect: gates work behind a checklist a staff engineer would run, consistently.",
        "资深工程师级质量纪律：提交前检查、安全评审、依赖审计、输出校验。效果：用主任工程师会跑的清单一致地把好关。",
    ),
    "mvanhorn-last30days": (
        "Competitor monitoring and voice-of-customer research across Reddit, X, YouTube, Hacker News, and the open web. Effect: turns scattered chatter into a structured 30-day market snapshot.",
        "跨 Reddit、X、YouTube、Hacker News 和开放网络的竞品监控与客户声音调研。效果：把零散讨论变成结构化的 30 天市场快照。",
    ),
    "coreyhaines-marketing": (
        "Marketing skill collection covering ad copy, landing-page optimization, email sequences, and analytics tagging. Effect: produces coordinated marketing assets instead of disconnected one-offs.",
        "营销 skill 集合，覆盖广告文案、落地页优化、邮件序列、分析埋点。效果：产出协同的营销素材，而非互不相关的零碎件。",
    ),
    "serena-semantic-edit": (
        "Symbol-level code understanding via the Language Server Protocol across 40+ languages. Effect: the agent edits functions and types, not string matches, so refactors stay correct across a codebase.",
        "通过 LSP 在 40+ 语言上做符号级代码理解。效果：agent 编辑的是函数和类型而非字符串匹配，重构在代码库里保持正确。",
    ),
    "hyper-marketing-mcp": (
        "Marketing skills paired with a production MCP server that executes against real ad accounts (Meta, Google, LinkedIn). Effect: the agent can both plan and actually run live campaigns, not just draft them.",
        "营销 skill 配合生产级 MCP server，能对真实广告账户（Meta、Google、LinkedIn）执行操作。效果：agent 既能规划也能真正投放线上活动，而非只是起草。",
    ),
}


def main() -> int:
    doc = json.loads(SKILLS_PATH.read_text(encoding="utf-8"))
    skills = doc["skills"]
    missing = []
    updated = 0
    for s in skills:
        sid = s["id"]
        if sid not in DESCRIPTIONS:
            missing.append(sid)
            continue
        en, zh = DESCRIPTIONS[sid]
        s["description"] = en
        s["description_zh"] = zh
        updated += 1

    if missing:
        print(f"WARNING: {len(missing)} skills have no enriched description: {missing}")

    SKILLS_PATH.write_text(
        json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Enriched {updated}/{len(skills)} skills with bilingual descriptions.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
