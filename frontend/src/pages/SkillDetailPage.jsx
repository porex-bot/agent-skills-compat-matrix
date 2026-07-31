// Skill 详情页 — 返回链接 + 分类 kicker + 标题 + 描述 + meta + Claude 扩展 chips + 各 agent 兼容表 + 教程
import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import ReactMarkdown from 'react-markdown';
import { useI18n } from '../lib/lang.jsx';
import { fetchSkill, fetchAgents } from '../lib/api.js';
import StatusDot from '../components/StatusDot.jsx';
import LevelBadge from '../components/LevelBadge.jsx';
import CategoryTag from '../components/CategoryTag.jsx';
import Loading from '../components/Loading.jsx';

export default function SkillDetailPage() {
  const { id } = useParams();
  const { t, lang, tc } = useI18n();
  const [skill, setSkill] = useState(null);
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    Promise.all([fetchSkill(id), fetchAgents()])
      .then(([s, a]) => {
        if (cancelled) return;
        setSkill(s);
        setAgents(Array.isArray(a) ? a : []);
        setError(null);
      })
      .catch((e) => !cancelled && setError(e.message))
      .finally(() => !cancelled && setLoading(false));
    return () => { cancelled = true; };
  }, [id]);

  if (loading) return <Loading />;
  if (error) {
    return (
      <div className="border border-[var(--color-unsupported)] text-[var(--color-unsupported)] px-4 py-3 text-sm font-[var(--font-mono)]">
        {error}
      </div>
    );
  }
  if (!skill) return null;

  const description = lang === 'zh' && skill.description_zh ? skill.description_zh : skill.description;
  const verifiedText = skill.verified_at ? t('verified', { date: skill.verified_at.slice(0, 10) }) : '';
  const sourceLabel = skill.source === 'seed' ? t('sourceSeed') : t('sourceCrawled');
  const claudeExt = Array.isArray(skill.uses_claude_extensions) ? skill.uses_claude_extensions : [];

  return (
    <div className="fade-in max-w-4xl">
      <Link to="/" className="inline-block font-[var(--font-mono)] text-xs uppercase tracking-wider text-[var(--color-text-dim)] hover:text-[var(--color-accent)] mb-6">
        {t('backToMatrix')}
      </Link>

      <div className="flex items-center gap-3 mb-3">
        <span className="block w-6 h-px bg-[var(--color-accent-2)]" />
        <CategoryTag category={skill.category} />
      </div>

      <h1 className="font-[var(--font-sans)] font-bold text-[32px] md:text-[40px] tracking-[-0.025em] text-[var(--color-text)] leading-[1.1]">
        {skill.name}
      </h1>

      {description && (
        <p className="mt-5 text-[17px] leading-[1.6] text-[var(--color-text-dim)] max-w-[62ch]">
          {description}
        </p>
      )}

      {/* meta 行 */}
      <div className="flex flex-wrap gap-x-5 gap-y-2 text-xs font-[var(--font-mono)] text-[var(--color-text-dim)] border-y border-[var(--color-border)] py-3 mt-7">
        {skill.url ? (
          <a href={skill.url} target="_blank" rel="noreferrer">{skill.repo || skill.url} ↗</a>
        ) : skill.repo ? (
          <span>{skill.repo}</span>
        ) : null}
        {verifiedText && <span>{verifiedText}</span>}
        {skill.stars != null && <span>★ {skill.stars} {t('stars')}</span>}
        <span className="text-[var(--color-text-faint)]">{sourceLabel}</span>
      </div>

      {/* Claude 扩展 chips */}
      {claudeExt.length > 0 && (
        <div className="mt-6">
          <div className="font-[var(--font-mono)] text-[10px] uppercase tracking-wider text-[var(--color-text-dim)] mb-2">
            {t('claudeExtUsed')}
          </div>
          <div className="flex flex-wrap gap-2">
            {claudeExt.map((ext, i) => (
              <span
                key={i}
                className="font-[var(--font-mono)] text-xs text-[var(--color-accent-2)] border border-[var(--color-border)] rounded px-2 py-1"
              >
                {ext}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* 各 Agent 兼容情况 */}
      <section className="mt-10">
        <h2 className="font-[var(--font-sans)] font-bold text-2xl mb-3 border-b border-[var(--color-rule)] pb-2">
          {t('compatPerAgent')}
        </h2>
        <div className="overflow-x-auto border border-[var(--color-border)] rounded">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="bg-[var(--color-bg-elev)] border-b border-[var(--color-rule)]">
                <th className="text-left font-[var(--font-mono)] text-[10px] uppercase tracking-wider text-[var(--color-text-dim)] px-4 py-3 min-w-[140px]">{t('colAgent')}</th>
                <th className="text-left font-[var(--font-mono)] text-[10px] uppercase tracking-wider text-[var(--color-text-dim)] px-4 py-3 min-w-[120px]">{t('colSupport')}</th>
                <th className="text-left font-[var(--font-mono)] text-[10px] uppercase tracking-wider text-[var(--color-text-dim)] px-4 py-3">{t('colCaveat')}</th>
              </tr>
            </thead>
            <tbody>
              {agents.map((a) => {
                const lvl = skill.compatibility?.[a.id] || 'unknown';
                const caveatEn = skill.caveats?.[a.id];
                const caveatZh = skill.caveats_zh?.[a.id];
                const text = tc(caveatEn, caveatZh);
                return (
                  <tr key={a.id} className="border-b border-[var(--color-border-soft)] last:border-b-0 align-top">
                    <td className="px-4 py-3">
                      <span className="text-[var(--color-text)]">{a.name}</span>
                    </td>
                    <td className="px-4 py-3">
                      <LevelBadge level={lvl} />
                    </td>
                    <td className="px-4 py-3 text-[var(--color-text-dim)] text-sm leading-[1.5]">
                      {text || <span className="text-[var(--color-text-faint)]">—</span>}
                    </td>
                  </tr>
                );
              })}
              {agents.length === 0 && (
                <tr>
                  <td colSpan={3} className="px-4 py-6 text-center text-[var(--color-text-faint)] font-[var(--font-mono)] text-xs">—</td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </section>

      {/* 使用教程 */}
      <section className="mt-10">
        <h2 className="font-[var(--font-sans)] font-bold text-2xl mb-4 border-b border-[var(--color-rule)] pb-2">
          {t('usageTutorial')}
        </h2>
        {skill.usage_tutorial ? (
          <div className="prose-tutorial">
            <ReactMarkdown>{skill.usage_tutorial}</ReactMarkdown>
          </div>
        ) : (
          <p className="text-[var(--color-text-dim)]">{t('usageTutorialEmpty')}</p>
        )}
      </section>
    </div>
  );
}
