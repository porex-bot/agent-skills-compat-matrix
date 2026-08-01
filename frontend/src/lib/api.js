// 数据获取封装 — 双模式:
// - 开发: 调 FastAPI 后端 /api/* (经 vite 代理)
// - 生产(gh-pages): 读静态 JSON site-data/*.json, 筛选/分页在前端做
// 爬虫配置/触发仅在有后端时可用 (dev 模式), 静态模式下 admin 页只读

const isStatic = import.meta.env.PROD;

const API_BASE = '/api';
const STATIC_BASE = import.meta.env.BASE_URL + 'site-data'; // gh-pages 子路径也兼容

// ---------- 静态模式: 一次性加载并缓存 ----------
let staticSkills = null;
let staticAgents = null;
let staticStats = null;

async function loadStaticData() {
  if (staticSkills) return { skills: staticSkills, agents: staticAgents, stats: staticStats };
  const [sRes, aRes, stRes] = await Promise.all([
    fetch(`${STATIC_BASE}/skills.json`),
    fetch(`${STATIC_BASE}/agents.json`),
    fetch(`${STATIC_BASE}/stats.json`),
  ]);
  if (!sRes.ok || !aRes.ok || !stRes.ok) throw new Error('静态数据加载失败');
  staticSkills = await sRes.json();
  staticAgents = await aRes.json();
  staticStats = await stRes.json();
  return { skills: staticSkills, agents: staticAgents, stats: staticStats };
}

// ---------- HTTP (dev 模式) ----------
async function http(path, options = {}) {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
    ...options,
  });
  if (!res.ok) {
    const text = await res.text().catch(() => '');
    throw new Error(`API ${path} → ${res.status}: ${text}`);
  }
  if (res.status === 204) return null;
  return res.json();
}

// ---------- skills ----------
export async function fetchSkills(params = {}) {
  if (isStatic) {
    const { skills } = await loadStaticData();
    let items = [...skills];
    const { q, agent, level, category, page = 1, page_size = 20 } = params;
    if (q) {
      const needle = q.toLowerCase();
      items = items.filter((s) =>
        [s.name, s.repo, s.description, s.description_zh].some((v) => (v || '').toLowerCase().includes(needle))
      );
    }
    if (agent) {
      items = items.filter((s) => s.compatibility && s.compatibility[agent]);
      if (level) items = items.filter((s) => s.compatibility[agent] === level);
    } else if (level) {
      items = items.filter((s) => Object.values(s.compatibility || {}).includes(level));
    }
    if (category) items = items.filter((s) => {
      // 多标签匹配: categories 数组任一包含, 或单值 category 等于
      const cats = Array.isArray(s.categories) && s.categories.length > 0
        ? s.categories
        : (s.category ? [s.category] : []);
      return cats.includes(category);
    });
    const total = items.length;
    const start = (page - 1) * page_size;
    return { items: items.slice(start, start + page_size), total, page, page_size };
  }
  const q = new URLSearchParams();
  Object.entries(params).forEach(([k, v]) => {
    if (v != null && v !== '') q.set(k, v);
  });
  return http(`/skills?${q.toString()}`);
}

export async function fetchSkill(id) {
  if (isStatic) {
    const { skills } = await loadStaticData();
    const s = skills.find((x) => x.id === id);
    if (!s) throw new Error(`skill ${id} not found`);
    return s;
  }
  return http(`/skills/${encodeURIComponent(id)}`);
}

// ---------- agents ----------
export async function fetchAgents() {
  if (isStatic) {
    const { agents } = await loadStaticData();
    return agents;
  }
  return http('/agents');
}

export async function fetchAgent(id) {
  if (isStatic) {
    const { agents } = await loadStaticData();
    const a = agents.find((x) => x.id === id);
    if (!a) throw new Error(`agent ${id} not found`);
    return a;
  }
  return http(`/agents/${encodeURIComponent(id)}`);
}

// ---------- stats ----------
export async function fetchStats() {
  if (isStatic) {
    const { stats } = await loadStaticData();
    return stats;
  }
  return http('/stats');
}

// ---------- 爬虫配置/触发: 仅 dev 模式可用 ----------
// 静态模式下返回占位/空, AdminPage 据此提示"需本地或自部署后端"
export const crawlAvailable = !isStatic;

export async function fetchCrawlConfig() {
  if (isStatic) return { min_stars: 10, interval_hours: 24, auto_mode: false, keywords: 'SKILL.md', has_token: false, static: true };
  return http('/config');
}

export async function updateCrawlConfig(payload) {
  if (isStatic) throw new Error('静态部署不支持修改配置');
  return http('/config', { method: 'PUT', body: JSON.stringify(payload) });
}

export async function runCrawl() {
  if (isStatic) throw new Error('静态部署不支持触发爬取');
  return http('/crawl', { method: 'POST' });
}

export async function fetchCrawlHistory(params = {}) {
  if (isStatic) return { items: [], total: 0, page: 1, page_size: 20, static: true };
  const q = new URLSearchParams();
  Object.entries(params).forEach(([k, v]) => {
    if (v != null && v !== '') q.set(k, v);
  });
  return http(`/crawl/history?${q.toString()}`);
}
