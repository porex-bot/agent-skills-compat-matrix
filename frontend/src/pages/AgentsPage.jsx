// Agents 页 — agent 能力矩阵(特性 × agent) + agent 卡片网格
import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { useI18n } from '../lib/lang.jsx';
import { fetchAgents } from '../lib/api.js';
import Loading from '../components/Loading.jsx';

// 与 i18n.js feat_* key 对应的特性列表
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

export default function AgentsPage() {
  const { t } = useI18n();
  const [agents, setAgents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    fetchAgents()
      .then((a) => {
        if (cancelled) return;
        setAgents(Array.isArray(a) ? a : []);
        setError(null);
      })
      .catch((e) => !cancelled && setError(e.message))
      .finally(() => !cancelled && setLoading(false));
    return () => { cancelled = true; };
  }, []);

  return (
    <div className="space-y-8 fade-in">
      <section>
        <div className="flex items-center gap-3 mb-5">
          <span className="block w-8 h-px bg-[var(--color-accent-2)]" />
          <span className="font-[var(--font-mono)] text-[11px] uppercase tracking-[0.22em] text-[var(--color-text-dim)]">
            § 02 — Agents
          </span>
        </div>
        <h1 className="font-[var(--font-serif)] font-bold text-4xl md:text-5xl tracking-[-0.025em] text-[var(--color-text)] mb-3">
          {t('agentCapMatrix')}
        </h1>
        <p className="text-[17px] leading-[1.6] text-[var(--color-text-dim)] max-w-[62ch]">
          {t('agentCapLede')}
        </p>
      </section>

      {loading ? (
        <Loading />
      ) : error ? (
        <div className="border border-[var(--color-unsupported)] text-[var(--color-unsupported)] px-4 py-3 text-sm font-[var(--font-mono)]">
          {error}
        </div>
      ) : agents.length === 0 ? (
        <div className="border border-dashed border-[var(--color-border)] rounded px-4 py-10 text-center text-[var(--color-text-dim)] font-[var(--font-mono)] text-sm">
          {t('none')}
        </div>
      ) : (
        <>
          {/* 能力矩阵 */}
          <section className="overflow-x-auto border border-[var(--color-border)] rounded">
            <table className="w-full text-sm border-collapse">
              <thead>
                <tr className="bg-[var(--color-bg-elev)] border-b border-[var(--color-rule)]">
                  <th className="sticky left-0 z-20 bg-[var(--color-bg-elev)] text-left font-[var(--font-mono)] text-[10px] uppercase tracking-wider text-[var(--color-text-dim)] px-4 py-3 min-w-[240px]">
                    {t('colFeature')}
                  </th>
                  {agents.map((a) => (
                    <th key={a.id} className="px-4 py-3 font-[var(--font-mono)] text-[10px] uppercase tracking-wider text-[var(--color-text-dim)] text-center min-w-[80px] whitespace-nowrap">
                      {a.name}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {FEATURES.map((feat) => (
                  <tr key={feat} className="border-b border-[var(--color-border-soft)] last:border-b-0">
                    <td className="sticky left-0 z-10 bg-[var(--color-bg)] px-4 py-3 text-[var(--color-text)] text-[13px]">
                      {t('feat_' + feat)}
                    </td>
                    {agents.map((a) => {
                      const on = !!a.features?.[feat];
                      return (
                        <td key={a.id} className="text-center px-4 py-3">
                          <span
                            className={on ? 'text-[var(--color-native)]' : 'text-[var(--color-text-faint)]'}
                            title={on ? t('feat_' + feat) : '—'}
                          >
                            {on ? '●' : '○'}
                          </span>
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </section>

          {/* agent 卡片网格 */}
          <section className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
            {agents.map((a) => (
              <Link
                key={a.id}
                to={`/agent/${encodeURIComponent(a.id)}`}
                className="block border border-[var(--color-border)] rounded p-4 hover:border-[var(--color-accent-2)] transition-colors"
              >
                <div className="flex items-baseline justify-between gap-3 mb-1">
                  <span className="font-[var(--font-serif)] text-lg text-[var(--color-text)] leading-tight">{a.name}</span>
                  <span className="font-[var(--font-mono)] text-[10px] uppercase tracking-wider text-[var(--color-text-faint)]">{a.vendor}</span>
                </div>
                {a.notes && (
                  <p className="text-xs text-[var(--color-text-dim)] line-clamp-2 leading-[1.5]">{a.notes}</p>
                )}
                <div className="mt-3 pt-3 border-t border-[var(--color-border-soft)] font-[var(--font-mono)] text-[10px] uppercase tracking-wider text-[var(--color-accent)]">
                  {t('tapForDetails')}
                </div>
              </Link>
            ))}
          </section>
        </>
      )}
    </div>
  );
}
