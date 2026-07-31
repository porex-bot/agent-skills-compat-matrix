#!/usr/bin/env python3
"""One-off helper: write Chinese translations of handwritten caveats into
data/skills.json under the `caveats_zh` field. Only the 5 core agents
(claude-code/cursor/codex-cli/gemini-cli/open-standard) have handwritten
caveats; the 8 backfill agents share templated strings that are localized
at runtime via site/i18n.js instead.

Run once; safe to re-run (overwrites caveats_zh from the dict below).
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS_PATH = ROOT / "data" / "skills.json"

CORE_AGENTS = {"claude-code", "cursor", "codex-cli", "gemini-cli", "open-standard"}

# English caveat -> Chinese translation. Sourced from a translation pass
# over all 109 distinct handwritten caveats in the core agents.
TRANSLATIONS: dict[str, str] = {
    "Install as alwaysApply:false .mdc; the eval-viewer/generate_review.py harness runs via bash but must be invoked manually.": "以 alwaysApply:false 的 .mdc 安装;eval-viewer/generate_review.py 测试套件通过 bash 运行,但必须手动调用。",
    "Drop the prompt body into AGENTS.md; eval scripts under scripts/eval-viewer must be referenced explicitly and the 32 KiB budget may truncate the methodology.": "将提示主体放入 AGENTS.md;scripts/eval-viewer 下的 eval 脚本必须显式引用,且 32 KiB 预算可能会截断方法论。",
    "Procedural authoring guidance ports cleanly; the quantitative eval harness is bundled scripts that need manual wiring.": "流程化的编写指导可干净迁移;定量 eval 套件是打包脚本,需要手动连接。",
    "Scripts run via bash but Playwright must be installed separately and scripts/with_server.py invoked manually rather than auto-discovered.": "脚本通过 bash 运行,但 Playwright 必须单独安装,且 scripts/with_server.py 需手动调用而非自动发现。",
    "Bundled scripts/with_server.py is not auto-discovered; it must be referenced explicitly in AGENTS.md and the multi-server orchestration pattern degrades without it.": "打包的 scripts/with_server.py 不会被自动发现;必须在 AGENTS.md 中显式引用,缺少它则多服务器编排模式会退化。",
    "Procedural testing guidance ports; the bundled Python helpers need manual asset wiring.": "流程化的测试指导可迁移;打包的 Python 辅助工具需要手动连接资源。",
    "Install as .mdc; REFERENCE.md and FORMS.md load as context and pip deps must be installed manually.": "以 .mdc 安装;REFERENCE.md 和 FORMS.md 作为上下文加载,pip 依赖必须手动安装。",
    "Drop into AGENTS.md; the large REFERENCE.md may hit the 32 KiB budget and must be loaded selectively.": "放入 AGENTS.md;较大的 REFERENCE.md 可能触及 32 KiB 预算,需有选择地加载。",
    "Pure-prompt guide ports cleanly; only the bundled reference docs need path adjustment.": "纯提示指南可干净迁移;仅打包的参考文档需要调整路径。",
    "LibreOffice/soffice must be installed; scripts/recalc.py and scripts/office/soffice.py are invoked manually rather than auto-triggered.": "必须安装 LibreOffice/soffice;scripts/recalc.py 和 scripts/office/soffice.py 需手动调用而非自动触发。",
    "The mandatory recalc.py step is not auto-discovered and must be referenced explicitly in AGENTS.md, so shipped workbooks ship with None cached formula values.": "必需的 recalc.py 步骤不会被自动发现,必须在 AGENTS.md 中显式引用,因此发布的工作簿会以 None 缓存的公式值发布。",
    "Guidance ports; the recalc/soffice helper scripts need manual asset wiring.": "指导可迁移;recalc/soffice 辅助脚本需要手动连接资源。",
    "Install as alwaysApply:false .mdc using the description as the trigger; screenshot-based self-critique needs manual capture.": "以 alwaysApply:false 的 .mdc 安装,使用 description 作为触发器;基于截图的自我评审需要手动捕获。",
    "Drop the prompt body into AGENTS.md as a global instruction; works without any frontmatter.": "将提示主体作为全局指令放入 AGENTS.md;无需任何 frontmatter 即可工作。",
    "Pure-prompt design guidance ports with no asset dependencies.": "纯提示的设计指导可迁移,无资源依赖。",
    "Install as .mdc; the reference/*.md guides load as context and SDK docs are fetched via WebFetch manually.": "以 .mdc 安装;reference/*.md 指南作为上下文加载,SDK 文档需通过 WebFetch 手动获取。",
    "Drop into AGENTS.md; the reference/ doc set may exceed the 32 KiB budget and must be loaded selectively per phase.": "放入 AGENTS.md;reference/ 文档集可能超过 32 KiB 预算,需按阶段有选择地加载。",
    "Procedural build guidance ports; the bundled reference docs need path adjustment.": "流程化的构建指导可迁移;打包的参考文档需要调整路径。",
    "Install as .mdc; Poppins and Lora fonts must be pre-installed for correct rendering.": "以 .mdc 安装;必须预装 Poppins 和 Lora 字体才能正确渲染。",
    "Drop into AGENTS.md; the python-pptx dependency must be installed manually.": "放入 AGENTS.md;python-pptx 依赖必须手动安装。",
    "Pure-prompt brand spec ports cleanly; only font availability is environment-dependent.": "纯提示的品牌规范可干净迁移;仅字体可用性依赖于环境。",
    "Install as .mdc; generated tokens are applied manually to the codebase.": "以 .mdc 安装;生成的 token 需手动应用到代码库。",
    "Drop the prompt body into AGENTS.md as a global instruction.": "将提示主体作为全局指令放入 AGENTS.md。",
    "Pure-prompt token-generation guidance ports with no asset dependencies.": "纯提示的 token 生成指导可迁移,无资源依赖。",
    "Install as .mdc; sketches render in the preview pane but no auto-critique loop.": "以 .mdc 安装;草图在预览面板中渲染,但没有自动评审循环。",
    "Pure-prompt art guidance ports with no asset dependencies.": "纯提示的艺术指导可迁移,无资源依赖。",
    "Cursor has no parallel subagent spawning, so the per-domain tasks run sequentially inline, losing concurrency and context isolation.": "Cursor 没有并行 subagent 生成,因此各领域任务以内联方式顺序执行,丧失并发性和上下文隔离。",
    "Codex has no subagent isolation, so the independent investigations collapse into a single-thread inline pass with shared context.": "Codex 没有 subagent 隔离,因此独立调查会塌缩为共享上下文的单线程内联处理。",
    "Native multi-dispatch in one turn is unavailable; subagents must be orchestrated manually via settings.json hooks.": "一轮内的原生多路分派不可用;subagent 必须通过 settings.json 的 hooks 手动编排。",
    "Subagent dispatch is a Claude-specific capability; the skill falls back to sequential inline execution.": "subagent 分派是 Claude 专属能力;该 skill 回退为顺序内联执行。",
    "No subagent spawning means implementer and review steps collapse into one inline pass, losing isolated context per task.": "没有 subagent 生成意味着实现和评审步骤塌缩为一次内联处理,丧失每个任务的独立上下文。",
    "No subagent isolation means review steps run inline without a fresh context window, reducing review independence.": "没有 subagent 隔离意味着评审步骤在内联运行时没有新的上下文窗口,降低评审独立性。",
    "Per-task fresh-subagent dispatch is not native and must be orchestrated manually via settings.json.": "每任务全新 subagent 分派并非原生支持,必须通过 settings.json 手动编排。",
    "The fresh-subagent-per-task pattern is Claude-specific; it degrades to inline sequential execution.": "每任务全新 subagent 模式是 Claude 专属;它会退化为内联顺序执行。",
    "Install as .mdc; the methodology ports cleanly as on-demand guidance.": "以 .mdc 安装;方法论作为按需指导可干净迁移。",
    "Drop into AGENTS.md as a global instruction; no frontmatter needed.": "作为全局指令放入 AGENTS.md;无需 frontmatter。",
    "Pure-prompt debugging discipline ports with no asset dependencies.": "纯提示的调试规范可迁移,无资源依赖。",
    "Works as .mdc guidance; there is no enforcement hook, so compliance relies on the model.": "作为 .mdc 指导工作;没有强制执行 hook,因此合规性依赖模型自身。",
    "Drop into AGENTS.md; the gate is instruction-only with no hard block on unverified claims.": "放入 AGENTS.md;该 gate 仅为指令形式,对未经验证的声明没有硬性阻断。",
    "Pure-prompt discipline ports; no automated gating mechanism.": "纯提示的规范可迁移;没有自动化 gating 机制。",
    "The chrome-devtools MCP server must be configured separately in Cursor's MCP panel; skill prompts run but the underlying tools need manual setup.": "chrome-devtools MCP server 必须在 Cursor 的 MCP 面板中单独配置;skill 提示可以运行,但底层工具需要手动设置。",
    "MCP support is limited, so DevTools calls may require manual curl or script orchestration.": "MCP 支持有限,因此 DevTools 调用可能需要手动 curl 或脚本编排。",
    "Hard dependency on the chrome-devtools MCP server makes this non-portable as a standalone skill.": "对 chrome-devtools MCP server 的硬依赖使其作为独立 skill 不可移植。",
    "Install as .mdc; pipeline YAML is generated but not auto-committed to .github/workflows.": "以 .mdc 安装;pipeline YAML 会生成但不会自动提交到 .github/workflows。",
    "Drop into AGENTS.md; workflow files are written manually by the agent.": "放入 AGENTS.md;workflow 文件由 agent 手动写入。",
    "Pure-prompt pipeline guidance ports with no asset dependencies.": "纯提示的 pipeline 指导可迁移,无资源依赖。",
    "Install as .mdc; the review runs on demand rather than being enforced as a pre-commit gate.": "以 .mdc 安装;评审按需运行,而非作为 pre-commit gate 强制执行。",
    "Drop into AGENTS.md; instruction-only with no automated blocking of insecure writes.": "放入 AGENTS.md;仅为指令形式,不会自动阻断不安全的写入。",
    "Pure-prompt threat-modeling guidance ports with no asset dependencies.": "纯提示的威胁建模指导可迁移,无资源依赖。",
    "Install as .mdc; cross-skill references to planning-and-task-breakdown need manual linking.": "以 .mdc 安装;对 planning-and-task-breakdown 的跨 skill 引用需要手动链接。",
    "Drop into AGENTS.md; spec and tasks/*.md files are written manually by the agent.": "放入 AGENTS.md;spec 和 tasks/*.md 文件由 agent 手动写入。",
    "Pure-prompt gated workflow ports with no asset dependencies.": "纯提示的 gated workflow 可迁移,无资源依赖。",
    "Install as .mdc; the checklist runs as guidance rather than a hard deploy gate.": "以 .mdc 安装;checklist 作为指导运行,而非硬性 deploy gate。",
    "Drop into AGENTS.md; rollout and rollback commands are executed manually by the agent.": "放入 AGENTS.md;rollout 和 rollback 命令由 agent 手动执行。",
    "Pure-prompt launch guidance ports with no asset dependencies.": "纯提示的上线指导可迁移,无资源依赖。",
    "Install as .mdc; instrumentation code is generated on demand rather than enforced.": "以 .mdc 安装;instrumentation 代码按需生成,而非强制执行。",
    "Drop into AGENTS.md; telemetry snippets are written manually by the agent.": "放入 AGENTS.md;telemetry 代码片段由 agent 手动写入。",
    "Pure-prompt instrumentation guidance ports with no asset dependencies.": "纯提示的 instrumentation 指导可迁移,无资源依赖。",
    "argument-hint and disable-model-invocation frontmatter are ignored; install as .mdc and invoke manually.": "argument-hint 和 disable-model-invocation frontmatter 被忽略;以 .mdc 安装并手动调用。",
    "Frontmatter is stripped; drop the body into AGENTS.md and trigger the handoff write manually.": "frontmatter 被去除;将主体放入 AGENTS.md 并手动触发 handoff 写入。",
    "disable-model-invocation is a Claude-specific auto-trigger control that is ignored elsewhere; the prompt body itself is portable.": "disable-model-invocation 是 Claude 专属的自动触发控制,在其他环境中被忽略;提示主体本身是可移植的。",
    "disable-model-invocation is ignored; planning runs inline on demand as .mdc guidance.": "disable-model-invocation 被忽略;规划作为 .mdc 指导按需内联运行。",
    "Frontmatter is stripped; drop the body into AGENTS.md and trigger manually.": "frontmatter 被去除;将主体放入 AGENTS.md 并手动触发。",
    "disable-model-invocation auto-trigger control is ignored; the planning prompt is portable.": "disable-model-invocation 自动触发控制被忽略;规划提示是可移植的。",
    "No background-agent dispatch, so research runs inline and blocks the main session, losing the keep-working-while-it-reads parallelism.": "没有 background-agent 分派,因此研究以内联方式运行并阻塞主会话,丧失“边读边工作”的并行性。",
    "No background subagent, so the investigation runs in the foreground and consumes the shared context window.": "没有 background subagent,因此调查在前台运行并消耗共享的上下文窗口。",
    "Background-agent dispatch is not native and must be orchestrated manually via settings.json.": "background-agent 分派非原生支持,必须通过 settings.json 手动编排。",
    "Background-agent delegation is a Claude-specific capability; it degrades to inline foreground research.": "background-agent 委派是 Claude 专属能力;它退化为内联前台研究。",
    "Install as .mdc; companion tests.md and mocking.md load as context.": "以 .mdc 安装;配套的 tests.md 和 mocking.md 作为上下文加载。",
    "Drop into AGENTS.md; the companion .md files must be referenced manually.": "放入 AGENTS.md;配套的 .md 文件必须手动引用。",
    "Pure-prompt TDD discipline ports with no asset dependencies.": "纯提示的 TDD 规范可迁移,无资源依赖。",
    "Install as .mdc; the scripts/hitl-loop.template.sh helper is invoked manually for human-in-the-loop cases.": "以 .mdc 安装;scripts/hitl-loop.template.sh 辅助脚本在 human-in-the-loop 场景下需手动调用。",
    "Drop into AGENTS.md; the hitl-loop template must be referenced by path since Codex does not auto-discover skill assets.": "放入 AGENTS.md;hitl-loop 模板必须按路径引用,因为 Codex 不会自动发现 skill 资源。",
    "Procedural diagnosis guidance ports; the bundled script template is referenced by path.": "流程化的诊断指导可迁移;打包的脚本模板按路径引用。",
    "scripts/__main__.py runs via bash but must be invoked manually; the multi-skill plugin index must be split into separate .mdc files.": "scripts/__main__.py 通过 bash 运行但必须手动调用;多 skill 插件索引必须拆分为单独的 .mdc 文件。",
    "The adjacent scripts/ CLI is not auto-discovered and must be referenced explicitly in AGENTS.md, so compression will not run without manual wiring.": "相邻的 scripts/ CLI 不会被自动发现,必须在 AGENTS.md 中显式引用,因此没有手动连接时压缩不会运行。",
    "The bundled CLI is portable and the compression rules port as a prompt; only the script path needs adjustment.": "打包的 CLI 可移植,压缩规则可作为提示迁移;仅需调整脚本路径。",
    "The graphify CLI must be pip-installed and run via bash; the repo ships a Cursor-specific skill variant.": "graphify CLI 必须 pip 安装并通过 bash 运行;该仓库提供了一个 Cursor 专用的 skill 变体。",
    "The graphify CLI is installed separately and invoked as the /graphify command; its path must be declared in AGENTS.md.": "graphify CLI 单独安装并以 /graphify 命令调用;其路径必须在 AGENTS.md 中声明。",
    "CLI-backed with no MCP or vector-store dependency; ships explicit per-agent skill files for claude, codex, cursor, gemini, copilot, and trae.": "以 CLI 为后端,无 MCP 或 vector-store 依赖;为 claude、codex、cursor、gemini、copilot 和 trae 提供明确的 per-agent skill 文件。",
    "No subagent skill-dispatch and no hooks support, so the ten stages run sequentially inline and integrity gates become instruction-only.": "没有 subagent skill-dispatch 且不支持 hooks,因此十个阶段以内联方式顺序执行,integrity gates 变为仅指令形式。",
    "metadata.depends_on dispatch and hooks/ are unsupported, so the pipeline collapses to manual stage-by-stage execution with no automated integrity enforcement.": "metadata.depends_on 分派和 hooks/ 不受支持,因此 pipeline 塌缩为手动逐阶段执行,没有自动化 integrity 强制。",
    "Skill-dispatch orchestration is manual and the hooks/ integrity gates must be replicated in settings.json.": "skill-dispatch 编排是手动的,hooks/ integrity gates 必须在 settings.json 中复制。",
    "The orchestration and hooks are Claude-specific; only the procedural stage guidance ports.": "编排和 hooks 是 Claude 专属;仅流程化的阶段指导可迁移。",
    "The allowed-tools frontmatter is ignored and Cursor applies its own tool gating; Biopython must be pip-installed.": "allowed-tools frontmatter 被忽略,Cursor 应用自己的工具 gating;Biopython 必须 pip 安装。",
    "allowed-tools is unsupported in frontmatter and the metadata.openclaw envVars are ignored; the 32 KiB budget may truncate the comprehensive reference.": "allowed-tools 在 frontmatter 中不受支持,且 metadata.openclaw envVars 被忽略;32 KiB 预算可能会截断完整的参考文档。",
    "allowed-tools is Claude-specific tool-permissioning, so the skill ports as a prompt but tool-gating is not standardized.": "allowed-tools 是 Claude 专属的工具权限控制,因此 skill 作为提示可迁移,但 tool-gating 未标准化。",
    "The CLAUDE.md maps to .cursorrules and applies as always-on context.": "CLAUDE.md 映射到 .cursorrules 并作为常驻上下文应用。",
    "The CLAUDE.md maps to AGENTS.md global instructions.": "CLAUDE.md 映射到 AGENTS.md 全局指令。",
    "A plain Markdown memory file with no frontmatter or assets; portable as context but not a structured SKILL.md.": "一个无 frontmatter 或资源的纯 Markdown 记忆文件;可作为上下文移植,但不是结构化的 SKILL.md。",
    "Spec/Plan stages rely on Claude's subagent orchestration; in Cursor they run inline without parallel agents, slower and no isolation.": "Spec/Plan 阶段依赖 Claude 的 subagent 编排;在 Cursor 中它们以内联方式运行,没有并行 agent,更慢且无隔离。",
    "Requires manual conversion of SKILL.md into AGENTS.md fragments; 32 KiB budget may truncate the full methodology.": "需要手动将 SKILL.md 转换为 AGENTS.md 片段;32 KiB 预算可能会截断完整方法论。",
    "Procedural guidance ports cleanly; Claude-specific hooks and context:fork fall back to no-ops.": "流程化的指导可干净迁移;Claude 专属的 hooks 和 context:fork 回退为 no-ops。",
    "Pure-prompt skill, no frontmatter extensions needed; install as alwaysApply:false .mdc with description used as the trigger.": "纯提示 skill,无需 frontmatter 扩展;以 alwaysApply:false 的 .mdc 安装,使用 description 作为触发器。",
    "Drop the prompt body into AGENTS.md; works as global instruction.": "将提示主体放入 AGENTS.md;作为全局指令工作。",
    "No parallel subagent spawning; reviews run sequentially, doubling latency.": "没有并行 subagent 生成;评审顺序运行,延迟加倍。",
    "No subagent isolation; both review axes collapse into one pass.": "没有 subagent 隔离;两个评审维度塌缩为一次处理。",
    "Hooks for PostToolUse can replicate the aggregation step, but requires manual setup in settings.json.": "PostToolUse 的 hooks 可以复制聚合步骤,但需要在 settings.json 中手动设置。",
    "Subagent orchestration is Claude-specific; fall back to single-pass review.": "subagent 编排是 Claude 专属;回退为单次评审。",
    "Pre-tool hooks translate to manual confirmation prompts; security review must be invoked explicitly.": "pre-tool hooks 转换为手动确认提示;security review 必须显式调用。",
    "Hook-based checks become instructions only; Codex will not block writes without manual confirmation.": "基于 hook 的检查变为仅指令形式;没有手动确认时 Codex 不会阻断写入。",
    "Bundled scripts/ directory must be referenced explicitly in AGENTS.md; Codex does not auto-discover skill assets the way Claude/Gemini do.": "打包的 scripts/ 目录必须在 AGENTS.md 中显式引用;Codex 不会像 Claude/Gemini 那样自动发现 skill 资源。",
    "Install each skill as a separate .mdc file; the multi-skill index must be split manually.": "每个 skill 作为单独的 .mdc 文件安装;多 skill 索引必须手动拆分。",
    "Serena ships as an MCP server, not a skill; Cursor users must configure it via the MCP panel and invoke tools manually.": "Serena 以 MCP server 形式发布,而非 skill;Cursor 用户必须通过 MCP 面板配置并手动调用工具。",
    "MCP server must be registered in config.toml; skill-style invocation is not available.": "MCP server 必须在 config.toml 中注册;不支持 skill 风格的调用。",
    "Beyond the SKILL.md scope — Serena is tooling, not a portable skill.": "超出 SKILL.md 范围——Serena 是工具,而非可移植的 skill。",
    "Skill prompts run, but the executing MCP server must be configured separately in Cursor's MCP settings.": "skill 提示可以运行,但执行的 MCP server 必须在 Cursor 的 MCP 设置中单独配置。",
    "MCP support is limited; ad-account writes may require manual curl orchestration.": "MCP 支持有限;ad-account 写入可能需要手动 curl 编排。",
    "Hard dependency on the Hyper MCP server; not portable as a standalone skill.": "对 Hyper MCP server 的硬依赖;作为独立 skill 不可移植。",
}


def main() -> int:
    doc = json.loads(SKILLS_PATH.read_text(encoding="utf-8"))
    skills = doc["skills"]
    missing: list[tuple[str, str, str]] = []  # (skill_id, agent_id, english)
    written = 0
    for s in skills:
        caveats = s.get("caveats", {})
        caveats_zh: dict[str, str] = {}
        for aid, en in caveats.items():
            if aid not in CORE_AGENTS:
                continue  # templated caveats are localized at runtime
            zh = TRANSLATIONS.get(en)
            if zh is None:
                missing.append((s["id"], aid, en))
                continue
            caveats_zh[aid] = zh
        if caveats_zh:
            s["caveats_zh"] = caveats_zh
            written += 1

    if missing:
        print(f"WARNING: {len(missing)} handwritten caveats have no translation:")
        for sid, aid, en in missing:
            print(f"  [{sid} | {aid}] {en[:80]}")

    SKILLS_PATH.write_text(
        json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"Wrote caveats_zh for {written}/{len(skills)} skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
