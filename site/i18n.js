// Bilingual (English / 简体中文) string dictionary for the compatibility matrix site.
// All keys are snake_case. Support-level keys are `level_native` etc. so that
// `t('level_' + cellLevel(...))` concatenation resolves correctly.

const I18N = (() => {
  const en = {
    brandText: 'Compat <strong>Matrix</strong>',
    navSkills: 'Skills',
    navAgents: 'Agents',
    langToggleTitle: 'Switch language / 切换语言',

    heroTitle: 'Will this skill run in <em>your</em> agent?',
    heroLede: 'Every AI coding agent claims to support the open Agent Skills standard. In practice hooks, subagents, context forks and tool allowlists silently vanish. This matrix records, per skill and per agent, <strong>what actually works where</strong> — and <strong>what degrades how</strong>.',
    statSkills: 'skills',
    statAgents: 'agents',
    statPortable: 'fully portable',
    statRisky: 'claude-only',

    loading: 'Loading the matrix…',

    portableSummary: '{n}/{total} agents',
    tapForDetails: 'Tap for details ›',

    searchPlaceholder: 'Search skills by name, repo, description…',
    filterAgent: 'Agent',
    filterLevel: 'Support',
    filterCategory: 'Category',
    allAgents: 'All agents',
    anyLevel: 'Any level',
    allCategories: 'All categories',
    noResults: 'No skills match these filters.',
    prev: '‹ Prev',
    next: 'Next ›',
    legend: 'native / compatible · partial · unsupported · unknown — open any row for per-cell caveats.',

    colSkill: 'Skill',
    colFeature: 'Feature',
    colAgent: 'Agent',
    colSupport: 'Support',
    colCaveat: 'Caveat',

    level_native: 'native',
    level_compatible: 'compatible',
    level_partial: 'partial',
    level_unsupported: 'unsupported',
    level_unknown: 'unknown',

    agentCapMatrix: 'Agent capability matrix',
    agentCapLede: 'Which primitives each agent actually implements. This drives every cell in the skill matrix.',

    rulesFile: 'Rules file',
    skillFile: 'Skill file',
    installProject: 'Install (project)',
    installUser: 'Install (user)',
    frontmatterReq: 'Frontmatter required',
    frontmatterOpt: 'Frontmatter optional',
    features: 'Features',
    notes: 'Notes',
    none: 'none',

    verified: 'verified {date}',
    claudeExtUsed: 'Claude extensions used:',
    compatPerAgent: 'Compatibility per agent',

    footerMain: 'Agent Skills Compatibility Matrix — machine-validated, auto-generated from <code>data/*.json</code>. Contribute on <a href="https://github.com/porex-bot/agent-skills-compat-matrix">GitHub</a>.',
    footerFineprint: 'MIT licensed. Replace <code>OWNER</code> with your GitHub username/org after forking.',

    feat_hooks: 'Hooks (PreToolUse / PostToolUse)',
    feat_subagent: 'Subagent spawning',
    feat_context_fork: 'Context fork',
    feat_progressive_disclosure: 'Progressive disclosure',
    feat_pre_approved_tools: 'Pre-approved tools (allowed-tools)',
    feat_slash_command: 'Slash command (/skill-name)',
    feat_glob_scoping: 'Glob-scoped activation',
    feat_model_override: 'Per-skill model override',

    cat_code_review: 'code-review',
    cat_tdd: 'tdd',
    cat_refactor: 'refactor',
    cat_debug: 'debug',
    cat_build: 'build',
    cat_deploy: 'deploy',
    cat_research: 'research',
    cat_marketing: 'marketing',
    cat_productivity: 'productivity',
    cat_frontend: 'frontend',
    cat_backend: 'backend',
    cat_devops: 'devops',
    cat_other: 'other',
  };

  const zh = {
    brandText: '兼容 <strong>矩阵</strong>',
    navSkills: 'Skills',
    navAgents: 'Agents',
    langToggleTitle: 'Switch language / 切换语言',

    heroTitle: '这个 skill 在<em>你的</em> agent 里能跑吗？',
    heroLede: '每个 AI 编程 agent 都声称支持开放的 Agent Skills 标准。但实际使用中，hooks、子 agent、上下文 fork、工具白名单常常悄悄失效。本矩阵逐 skill、逐 agent 记录<strong>哪里真正能用</strong>，以及<strong>哪里会怎样降级</strong>。',
    statSkills: '个 skill',
    statAgents: '个 agent',
    statPortable: '个完全可移植',
    statRisky: '个仅 Claude',

    loading: '正在加载矩阵…',

    portableSummary: '{n}/{total} 个 agent',
    tapForDetails: '点击查看详情 ›',

    searchPlaceholder: '按名称、仓库、描述搜索 skill…',
    filterAgent: 'Agent',
    filterLevel: '支持',
    filterCategory: '分类',
    allAgents: '全部 agent',
    anyLevel: '任意等级',
    allCategories: '全部分类',
    noResults: '没有 skill 匹配这些筛选条件。',
    prev: '‹ 上一页',
    next: '下一页 ›',
    legend: '原生 / 兼容 · 部分支持 · 不支持 · 未知 — 点开任意行查看每个单元格的说明。',

    colSkill: 'Skill',
    colFeature: '特性',
    colAgent: 'Agent',
    colSupport: '支持情况',
    colCaveat: '说明',

    level_native: '原生',
    level_compatible: '兼容',
    level_partial: '部分支持',
    level_unsupported: '不支持',
    level_unknown: '未知',

    agentCapMatrix: 'Agent 能力矩阵',
    agentCapLede: '每个 agent 实际实现了哪些原语。这决定了 skill 矩阵里的每一个单元格。',

    rulesFile: '规则文件',
    skillFile: 'Skill 文件',
    installProject: '安装路径（项目级）',
    installUser: '安装路径（用户级）',
    frontmatterReq: '必需 frontmatter',
    frontmatterOpt: '可选 frontmatter',
    features: '特性',
    notes: '说明',
    none: '无',

    verified: '验证于 {date}',
    claudeExtUsed: '使用的 Claude 扩展：',
    compatPerAgent: '各 Agent 兼容情况',

    footerMain: 'Agent Skills 兼容矩阵 — 数据由机器校验，从 <code>data/*.json</code> 自动生成。在 <a href="https://github.com/porex-bot/agent-skills-compat-matrix">GitHub</a> 贡献。',
    footerFineprint: 'MIT 协议。Fork 后请将 <code>OWNER</code> 替换为你的 GitHub 用户名/组织。',

    feat_hooks: 'Hooks（PreToolUse / PostToolUse 等生命周期钩子）',
    feat_subagent: '子 agent 生成',
    feat_context_fork: '上下文 fork（context: fork）',
    feat_progressive_disclosure: '渐进式披露（metadata → body → assets）',
    feat_pre_approved_tools: '预授权工具（allowed-tools）',
    feat_slash_command: '斜杠命令调用（/skill-name）',
    feat_glob_scoping: 'Glob 模式匹配触发',
    feat_model_override: '按 skill 覆盖模型',

    cat_code_review: '代码评审',
    cat_tdd: 'TDD',
    cat_refactor: '重构',
    cat_debug: '调试',
    cat_build: '构建',
    cat_deploy: '部署',
    cat_research: '研究',
    cat_marketing: '营销',
    cat_productivity: '效率',
    cat_frontend: '前端',
    cat_backend: '后端',
    cat_devops: 'DevOps',
    cat_other: '其他',
  };

  function interpolate(str, params) {
    if (!params) return str;
    return str.replace(/\{(\w+)\}/g, (_, k) => (params[k] != null ? String(params[k]) : `{${k}}`));
  }

  function translate(lang, key, params) {
    const dict = lang === 'zh' ? zh : en;
    const val = dict[key];
    if (val == null) {
      const fallback = (lang === 'zh' ? en : zh)[key];
      return fallback != null ? interpolate(fallback, params) : key;
    }
    return interpolate(val, params);
  }

  // Templated caveats from scripts/backfill_compat.py are identical across
  // skills for a given agent+situation. Map them to Chinese at runtime.
  const CAVEAT_ZH = {
    'Rewrite the SKILL.md into this agent\'s rules format (description/glob or always-on).':
      '需将 SKILL.md 改写为该 agent 的规则文件格式（description/glob 或常驻）。',
    'Rewrite as a rules file; hooks/agent/context-fork are dropped.':
      '改写为规则文件；hooks/agent/context-fork 等扩展会被丢弃。',
    'Hard dependency on a non-portable runtime; cannot run on this agent.':
      '强依赖不可移植的运行时；在该 agent 上无法运行。',
    'Flatten the skill body into a CONVENTIONS.md file loaded via .aider.conf.yml read:.':
      '将 skill 正文压平成 CONVENTIONS.md，通过 .aider.conf.yml 的 read: 加载。',
    'Flatten to CONVENTIONS.md read via read:; hooks/agent/context-fork cannot be expressed.':
      '压平为 CONVENTIONS.md 经 read: 加载；hooks/agent/context-fork 无法表达。',
    'Convert the skill to a prompt/slash-command file for invocation.':
      '将 skill 转换为 prompt/斜杠命令文件来调用。',
    'Convert to a prompt file for slash invocation; hooks/agent/context-fork are dropped.':
      '转换为 prompt 文件用斜杠调用；hooks/agent/context-fork 会被丢弃。',
    'Inline the SKILL.md body into AGENTS.md; frontmatter is dropped.':
      '将 SKILL.md 正文内联进 AGENTS.md；frontmatter 会被丢弃。',
    'SKILL.md body inlined into AGENTS.md; Claude-specific hooks/agent/context-fork are dropped.':
      'SKILL.md 正文内联进 AGENTS.md；Claude 特有的 hooks/agent/context-fork 会被丢弃。',
  };

  function caveat(lang, agentId, enText, zhOverride) {
    if (lang !== 'zh') return enText || '';
    if (zhOverride) return zhOverride;
    if (!enText) return '';
    return CAVEAT_ZH[enText] || enText;
  }

  return { translate, caveat, en, zh };
})();

if (typeof window !== 'undefined') {
  window.I18N = I18N;
}
if (typeof module !== 'undefined' && module.exports) {
  module.exports = I18N;
}
