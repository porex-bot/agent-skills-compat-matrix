// 首页 — hero + 统计行 + 筛选器 + 技能矩阵(桌面)/卡片(移动)
import { useEffect, useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { useI18n } from '../lib/lang.jsx';
import { fetchSkills, fetchAgents, fetchStats } from '../lib/api.js';
import Hero from '../components/Hero.jsx';
import StatRow from '../components/StatRow.jsx';
import StatusDot from '../components/StatusDot.jsx';
import CategoryTag from '../components/CategoryTag.jsx';
import PortabilityBadge from '../components/PortabilityBadge.jsx';
import Loading from '../components/Loading.jsx';

const LEVELS = ['native', 'compatible', 'partial', 'unsupported', 'unknown'];
const CATEGORIES = [
  'code_quality', 'testing', 'debugging', 'devops', 'frontend_ui',
  'data_docs', 'text_content', 'research_analysis', 'agent_workflow',
  'integration', 'other',
];
const PAGE_SIZE = 25;

const selectCls =
  'bg-[var(--color-bg-elev)] border border-[var(--color-border)] rounded px-3 py-2 text-sm text-[var(--color-text)] focus:outline-none focus:border-[var(--color-accent-2)] font-[var(--font-sans)]';
const inputCls =
  'flex-1 w-full bg-[var(--color-bg-elev)] border border-[var(--color-border)] rounded px-4 py-2 text-sm text-[var(--color-text)] placeholder:text-[var(--color-text-faint)] focus:outline-none focus:border-[var(--color-accent-2)] font-[var(--font-sans)]';

export default function HomePage() {
  const { t, lang } = useI18n();
  const navigate = useNavigate();
  const [searchParams, setSearchParams] = useSearchParams();

  const [agents, setAgents] = useState([]);
  const [stats, setStats] = useState({ skills: 0, agents: 0, portable: 0, risky: 0 });
  const [data, setData] = useState({ items: [], total: 0, page: 1, page_size: PAGE_SIZE });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // 从 URL 派生筛选状态
  const q = searchParams.get('q') || '';
  const agent = searchParams.get('agent') || '';
  const level = searchParams.get('level') || '';
  const category = searchParams.get('category') || '';
  const page = Math.max(1, parseInt(searchParams.get('page') || '1', 10) || 1);

  // 一次性加载 agents + stats
  useEffect(() => {
    let cancelled = false;
    Promise.all([fetchAgents(), fetchStats()])
      .then(([a, s]) => {
        if (cancelled) return;
        setAgents(Array.isArray(a) ? a : []);
        setStats(s || { skills: 0, agents: 0, portable: 0, risky: 0 });
      })
      .catch((e) => !cancelled && setError(e.message));
    return () => { cancelled = true; };
  }, []);

  // 筛选条件变化时重新加载技能
  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    fetchSkills({ q, agent, level, category, page, page_size: PAGE_SIZE })
      .then((d) => {
        if (cancelled) return;
        setData(d || { items: [], total: 0, page, page_size: PAGE_SIZE });
        setError(null);
      })
      .catch((e) => !cancelled && setError(e.message))
      .finally(() => !cancelled && setLoading(false));
    return () => { cancelled = true; };
  }, [q, agent, level, category, page]);

  // 修改单个查询参数(改 q/agent/level/category 时重置 page)
  const updateParam = (key, value) => {
    const next = new URLSearchParams(searchParams);
    if (value) next.set(key, value); else next.delete(key);
    if (key !== 'page') next.delete('page');
    setSearchParams(next);
  };

  const totalPages = Math.max(1, Math.ceil(data.total / (data.page_size || PAGE_SIZE)));

  const heroParts = {
    pre: t('heroTitlePre'),
    accent: t('heroTitleAccent'),
    post: t('heroTitlePost'),
  };
  const statBlocks = [
    { value: stats.skills, label: t('statSkills') },
    { value: stats.agents, label: t('statAgents') },
    { value: stats.portable, label: t('statPortable') },
    { value: stats.risky, label: t('statRisky') },
  ];

  return (
    <div className="space-y-10">
      <Hero kicker="§ 01 — Skill × Agent" titleParts={heroParts} lede={t('heroLede')} />
      <StatRow stats={statBlocks} />

      <section className="space-y-5">
        {/* 筛选器 */}
        <div className="flex flex-col md:flex-row md:items-stretch gap-3">
          <input
            type="text"
            value={q}
            onChange={(e) => updateParam('q', e.target.value)}
            placeholder={t('searchPlaceholder')}
            className={inputCls}
          />
          <select value={agent} onChange={(e) => updateParam('agent', e.target.value)} className={selectCls} aria-label={t('filterAgent')}>
            <option value="">{t('allAgents')}</option>
            {agents.map((a) => (
              <option key={a.id} value={a.id}>{a.name}</option>
            ))}
          </select>
          <select value={level} onChange={(e) => updateParam('level', e.target.value)} className={selectCls} aria-label={t('filterLevel')}>
            <option value="">{t('anyLevel')}</option>
            {LEVELS.map((l) => (
              <option key={l} value={l}>{t('level_' + l)}</option>
            ))}
          </select>
          <select value={category} onChange={(e) => updateParam('category', e.target.value)} className={selectCls} aria-label={t('filterCategory')}>
            <option value="">{t('allCategories')}</option>
            {CATEGORIES.map((c) => (
              <option key={c} value={c}>{t('cat_' + c)}</option>
            ))}
          </select>
        </div>

        {/* 计数 + 图例 */}
        <div className="flex flex-wrap items-center justify-between gap-3">
          <span className="font-[var(--font-mono)] text-[11px] uppercase tracking-wider text-[var(--color-text-dim)]">
            {t('resultCount', { n: data.total })}
          </span>
          <div className="flex flex-wrap items-center gap-x-4 gap-y-1.5">
            {LEVELS.map((l) => (
              <span key={l} className="inline-flex items-center gap-1.5 font-[var(--font-mono)] text-[10px] uppercase tracking-wider text-[var(--color-text-dim)]">
                <StatusDot level={l} />
                {t('level_' + l)}
              </span>
            ))}
          </div>
        </div>

        {/* 主体 */}
        {loading ? (
          <Loading />
        ) : error ? (
          <div className="border border-[var(--color-unsupported)] text-[var(--color-unsupported)] px-4 py-3 text-sm font-[var(--font-mono)]">
            {error}
          </div>
        ) : data.items.length === 0 ? (
          <div className="border border-dashed border-[var(--color-border)] rounded px-4 py-10 text-center text-[var(--color-text-dim)] font-[var(--font-mono)] text-sm">
            {t('noResults')}
          </div>
        ) : (
          <>
            {/* 桌面矩阵 */}
            <div className="hidden md:block overflow-x-auto border border-[var(--color-border)] rounded">
              <table className="w-full text-sm border-collapse">
                <thead>
                  <tr className="bg-[var(--color-bg-elev)] border-b border-[var(--color-rule)]">
                    <th className="sticky left-0 z-20 bg-[var(--color-bg-elev)] text-left font-[var(--font-mono)] text-[10px] uppercase tracking-wider text-[var(--color-text-dim)] px-4 py-3 min-w-[220px]">
                      {t('colSkill')}
                    </th>
                    {agents.map((a) => (
                      <th key={a.id} className="px-3 py-3 font-[var(--font-mono)] text-[10px] uppercase tracking-wider text-[var(--color-text-dim)] text-center min-w-[64px] whitespace-nowrap">
                        {a.name}
                      </th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {data.items.map((sk) => {
                    const description = lang === 'zh' && sk.description_zh ? sk.description_zh : sk.description;
                    return (
                      <tr
                        key={sk.id}
                        onClick={() => navigate(`/skill/${encodeURIComponent(sk.id)}`)}
                        className="group cursor-pointer border-b border-[var(--color-border-soft)] hover:bg-[var(--color-bg-elev)] last:border-b-0"
                      >
                        <td className="sticky left-0 z-10 bg-[var(--color-bg)] group-hover:bg-[var(--color-bg-elev)] px-4 py-4 align-top">
                          <div className="flex flex-col gap-2 min-w-[280px] max-w-[360px]">
                            <div className="flex items-center gap-2">
                              <span className="text-[var(--color-text)] text-sm font-semibold leading-tight">{sk.name}</span>
                              <CategoryTag categories={sk.categories} category={sk.category} />
                            </div>
                            {description && (
                              <p className="text-xs text-[var(--color-text-dim)] leading-[1.5] line-clamp-2">{description}</p>
                            )}
                            <div className="flex items-center gap-3 text-[10px] font-[var(--font-mono)] text-[var(--color-text-faint)]">
                              <span className="truncate max-w-[180px]">{sk.repo}</span>
                              {sk.stars != null && sk.stars > 0 && <span>★ {sk.stars}</span>}
                              <span className="text-[var(--color-accent)] group-hover:underline">{t('tapForDetails')}</span>
                            </div>
                          </div>
                        </td>
                        {agents.map((a) => {
                          const lvl = sk.compatibility?.[a.id] || 'unknown';
                          return (
                            <td key={a.id} className="text-center px-3 py-4 align-middle">
                              <span className="inline-flex justify-center" title={`${sk.name} × ${a.name}: ${t('level_' + lvl)}`}>
                                <StatusDot level={lvl} />
                              </span>
                            </td>
                          );
                        })}
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>

            {/* 移动卡片 */}
            <div className="md:hidden space-y-3">
              {data.items.map((sk) => {
                const description = lang === 'zh' && sk.description_zh ? sk.description_zh : sk.description;
                return (
                  <Link
                    key={sk.id}
                    to={`/skill/${encodeURIComponent(sk.id)}`}
                    className="block border border-[var(--color-border)] rounded p-4 hover:border-[var(--color-accent-2)] transition-colors"
                  >
                    <div className="flex items-start justify-between gap-3 mb-2">
                      <span className="font-[var(--font-sans)] font-semibold text-lg text-[var(--color-text)] leading-tight">{sk.name}</span>
                      <CategoryTag categories={sk.categories} category={sk.category} />
                    </div>
                    {description && (
                      <p className="text-sm text-[var(--color-text-dim)] leading-[1.5] line-clamp-2 mb-3">{description}</p>
                    )}
                    <div className="flex items-center justify-between gap-2">
                      <PortabilityBadge skill={sk} agents={agents} />
                      <span className="font-[var(--font-mono)] text-xs text-[var(--color-accent)]">{t('tapForDetails')}</span>
                    </div>
                  </Link>
                );
              })}
            </div>
          </>
        )}

        {/* 分页 */}
        {totalPages > 1 && !loading && (
          <div className="flex items-center justify-between pt-2 border-t border-[var(--color-border-soft)]">
            <button
              type="button"
              disabled={page <= 1}
              onClick={() => updateParam('page', String(page - 1))}
              className="font-[var(--font-mono)] text-xs uppercase tracking-wider text-[var(--color-text-dim)] hover:text-[var(--color-accent)] disabled:opacity-30 disabled:hover:text-[var(--color-text-dim)]"
            >
              {t('prev')}
            </button>
            <span className="font-[var(--font-mono)] text-xs text-[var(--color-text-dim)] tnum">
              {page} / {totalPages}
            </span>
            <button
              type="button"
              disabled={page >= totalPages}
              onClick={() => updateParam('page', String(page + 1))}
              className="font-[var(--font-mono)] text-xs uppercase tracking-wider text-[var(--color-text-dim)] hover:text-[var(--color-accent)] disabled:opacity-30 disabled:hover:text-[var(--color-text-dim)]"
            >
              {t('next')}
            </button>
          </div>
        )}
      </section>
    </div>
  );
}
