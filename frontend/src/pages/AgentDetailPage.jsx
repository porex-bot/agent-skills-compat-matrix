// Agent 详情页 — 返回链接 + vendor kicker + 标题 + homepage + notes + 特性 grid + Facts
import { useEffect, useState } from 'react';
import { Link, useParams } from 'react-router-dom';
import { useI18n } from '../lib/lang.jsx';
import { fetchAgent } from '../lib/api.js';
import Loading from '../components/Loading.jsx';

const FEATURES = [
  'hooks',
  'subagent',
  'context_fork',
  'progressive_disclosure',
  'pre_approved_tools',
  'slash_command',
  'glob_scoping',
  'model_override',
];

function Fact({ label, value, mono }) {
  if (value == null || value === '') return null;
  return (
    <div className="border-b border-[var(--color-border-soft)] pb-2">
      <dt className="font-[var(--font-mono)] text-[10px] uppercase tracking-wider text-[var(--color-text-dim)] mb-1">{label}</dt>
      <dd className={`text-sm break-all ${mono ? 'font-[var(--font-mono)] text-[var(--color-accent)]' : 'text-[var(--color-text)]'}`}>{value}</dd>
    </div>
  );
}

export default function AgentDetailPage() {
  const { id } = useParams();
  const { t, lang } = useI18n();
  const [agent, setAgent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    fetchAgent(id)
      .then((a) => {
        if (cancelled) return;
        setAgent(a);
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
  if (!agent) return null;

  const fmReq = Array.isArray(agent.frontmatter_required) ? agent.frontmatter_required : [];
  const fmOpt = Array.isArray(agent.frontmatter_optional) ? agent.frontmatter_optional : [];

  return (
    <div className="fade-in max-w-4xl">
      <Link to="/agents" className="inline-block font-[var(--font-mono)] text-xs uppercase tracking-wider text-[var(--color-text-dim)] hover:text-[var(--color-accent)] mb-6">
        {t('backToAgents')}
      </Link>

      <div className="flex items-center gap-3 mb-3">
        <span className="block w-6 h-px bg-[var(--color-accent-2)]" />
        <span className="font-[var(--font-mono)] text-[10px] uppercase tracking-wider text-[var(--color-text-dim)]">{agent.vendor || '—'}</span>
      </div>

      <h1 className="font-[var(--font-sans)] font-bold text-[32px] md:text-[40px] tracking-[-0.025em] text-[var(--color-text)] leading-[1.1]">
        {agent.name}
      </h1>

      {agent.homepage && (
        <a
          href={agent.homepage}
          target="_blank"
          rel="noreferrer"
          className="inline-block mt-3 text-sm text-[var(--color-accent)] font-[var(--font-mono)]"
        >
          {agent.homepage} ↗
        </a>
      )}

      {agent.notes && (
        <p className="mt-6 text-[17px] leading-[1.6] text-[var(--color-text-dim)] max-w-[62ch]">
          {lang === 'zh' && agent.notes_zh ? agent.notes_zh : agent.notes}
        </p>
      )}

      {/* 特性 grid */}
      <section className="mt-10">
        <h2 className="font-[var(--font-sans)] font-bold text-2xl mb-4 border-b border-[var(--color-rule)] pb-2">
          {t('features')}
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
          {FEATURES.map((f) => {
            const on = !!agent.features?.[f];
            return (
              <div
                key={f}
                className={`flex items-start gap-3 border rounded px-3 py-2.5 ${on ? 'border-[var(--color-border)] bg-[var(--color-bg-elev)]' : 'border-[var(--color-border-soft)]'}`}
              >
                <span className={on ? 'text-[var(--color-native)]' : 'text-[var(--color-text-faint)]'} aria-hidden>
                  {on ? '●' : '○'}
                </span>
                <span className={`text-sm ${on ? 'text-[var(--color-text)]' : 'text-[var(--color-text-dim)]'}`}>
                  {t('feat_' + f)}
                </span>
              </div>
            );
          })}
        </div>
      </section>

      {/* Facts */}
      <section className="mt-10">
        <h2 className="font-[var(--font-sans)] font-bold text-2xl mb-4 border-b border-[var(--color-rule)] pb-2">
          {t('facts')}
        </h2>
        <dl className="grid grid-cols-1 md:grid-cols-2 gap-x-6 gap-y-3">
          <Fact label={t('rulesFile')} value={agent.rules_file} mono />
          <Fact label={t('skillFile')} value={agent.skills_file} mono />
          <Fact label={t('installProject')} value={agent.install_path?.project} mono />
          <Fact label={t('installUser')} value={agent.install_path?.user} mono />
          <Fact
            label={t('frontmatterReq')}
            value={fmReq.length ? fmReq.join(', ') : null}
            mono
          />
          <Fact
            label={t('frontmatterOpt')}
            value={fmOpt.length ? fmOpt.join(', ') : null}
            mono
          />
        </dl>
      </section>
    </div>
  );
}
