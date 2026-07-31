// Admin 爬虫控制台 — 配置表单 + 运行按钮 + 历史表格
import { useEffect, useState } from 'react';
import { useI18n } from '../lib/lang.jsx';
import { fetchCrawlConfig, updateCrawlConfig, runCrawl, fetchCrawlHistory, crawlAvailable } from '../lib/api.js';
import Loading from '../components/Loading.jsx';

const inputCls =
  'w-full bg-[var(--color-bg-elev)] border border-[var(--color-border)] rounded px-3 py-2 text-sm text-[var(--color-text)] placeholder:text-[var(--color-text-faint)] focus:outline-none focus:border-[var(--color-accent-2)] font-[var(--font-sans)]';

function Field({ label, children, hint }) {
  return (
    <div>
      <label className="block font-[var(--font-mono)] text-[10px] uppercase tracking-wider text-[var(--color-text-dim)] mb-1.5">
        {label}
      </label>
      {children}
      {hint && <div className="mt-1 text-xs text-[var(--color-text-faint)] font-[var(--font-mono)]">{hint}</div>}
    </div>
  );
}

function Th({ children, className = '' }) {
  return (
    <th className={`text-left font-[var(--font-mono)] text-[10px] uppercase tracking-wider text-[var(--color-text-dim)] px-3 py-2.5 whitespace-nowrap ${className}`.trim()}>
      {children}
    </th>
  );
}

function Td({ children, mono }) {
  return (
    <td className={`px-3 py-2.5 ${mono ? 'font-[var(--font-mono)] text-xs text-[var(--color-text-dim)]' : ''}`.trim()}>
      {children}
    </td>
  );
}

const STATUS_KEY = {
  success: 'statusSuccess',
  failed: 'statusFailed',
  running: 'statusRunning',
};

function statusColor(status) {
  if (status === 'success') return 'text-[var(--color-native)]';
  if (status === 'failed') return 'text-[var(--color-unsupported)]';
  if (status === 'running') return 'text-[var(--color-accent)]';
  return 'text-[var(--color-text-dim)]';
}

export default function AdminPage() {
  const { t, lang } = useI18n();
  const [config, setConfig] = useState(null);
  const [draft, setDraft] = useState(null);
  const [saving, setSaving] = useState(false);
  const [savedMsg, setSavedMsg] = useState(false);
  const [running, setRunning] = useState(false);
  const [history, setHistory] = useState({ items: [], total: 0, page: 1, page_size: 20 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // 拉取配置 + 历史
  const load = () => (
    Promise.all([fetchCrawlConfig(), fetchCrawlHistory({ page: 1, page_size: 20 })])
      .then(([c, h]) => {
        setConfig(c);
        setDraft({ ...c });
        setHistory(h || { items: [], total: 0, page: 1, page_size: 20 });
        setError(null);
      })
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  );

  useEffect(() => {
    let cancelled = false;
    setLoading(true);
    Promise.all([fetchCrawlConfig(), fetchCrawlHistory({ page: 1, page_size: 20 })])
      .then(([c, h]) => {
        if (cancelled) return;
        setConfig(c);
        setDraft({ ...c });
        setHistory(h || { items: [], total: 0, page: 1, page_size: 20 });
        setError(null);
      })
      .catch((e) => !cancelled && setError(e.message))
      .finally(() => !cancelled && setLoading(false));
    return () => { cancelled = true; };
  }, []);

  const onSave = async () => {
    setSaving(true);
    setError(null);
    try {
      // 编辑期允许空串(方便清空重输), 提交时归一为 0
      const payload = {
        ...draft,
        min_stars: draft.min_stars === '' ? 0 : draft.min_stars,
        interval_hours: draft.interval_hours === '' ? 0 : draft.interval_hours,
      };
      const updated = await updateCrawlConfig(payload);
      setConfig(updated);
      setDraft({ ...updated });
      setSavedMsg(true);
      setTimeout(() => setSavedMsg(false), 2500);
    } catch (e) {
      setError(e.message);
    } finally {
      setSaving(false);
    }
  };

  const onRun = async () => {
    setRunning(true);
    setError(null);
    try {
      await runCrawl();
      // 爬取完成后再刷新历史(后端可能异步, 给点缓冲)
      setTimeout(() => { load(); }, 1500);
    } catch (e) {
      setError(e.message);
    } finally {
      setRunning(false);
    }
  };

  return (
    <div className="space-y-8 fade-in">
      <section>
        <div className="flex items-center gap-3 mb-5">
          <span className="block w-8 h-px bg-[var(--color-accent-2)]" />
          <span className="font-[var(--font-mono)] text-[11px] uppercase tracking-[0.22em] text-[var(--color-text-dim)]">
            § 03 — Crawler Console
          </span>
        </div>
        <h1 className="font-[var(--font-sans)] font-bold text-[32px] md:text-[40px] tracking-[-0.025em] text-[var(--color-text)] mb-3">
          {t('adminTitle')}
        </h1>
        <p className="text-[17px] leading-[1.6] text-[var(--color-text-dim)] max-w-[62ch]">
          {t('adminLede')}
        </p>
      </section>

      {loading ? (
        <Loading />
      ) : (
        <>
          {!crawlAvailable && (
            <div className="border border-[var(--color-accent-2)] bg-[var(--color-bg-elev)] text-[var(--color-text-dim)] px-4 py-3 text-sm leading-relaxed">
              <span className="font-[var(--font-mono)] text-[var(--color-accent)] uppercase tracking-wider text-[10px] mr-2">static</span>
              {lang === 'zh'
                ? '当前为静态部署（GitHub Pages），爬虫控制台仅只读。数据由 GitHub Actions 每 6 小时自动爬取并回写。要交互式配置/触发爬虫，请在本地或自部署后端运行。'
                : 'This is a static deployment (GitHub Pages); the crawler console is read-only. Data is refreshed every 6 hours by GitHub Actions. To configure or trigger crawls interactively, run the backend locally or self-host.'}
            </div>
          )}
          {error && (
            <div className="border border-[var(--color-unsupported)] text-[var(--color-unsupported)] px-4 py-2 text-sm font-[var(--font-mono)]">
              {error}
            </div>
          )}

          {/* 配置表单 */}
          {draft && (
            <section className="border border-[var(--color-border)] rounded p-5 md:p-6 space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <Field label={t('configMinStars')}>
                  <input
                    type="number"
                    min="0"
                    value={draft.min_stars ?? ''}
                    onChange={(e) => setDraft({ ...draft, min_stars: e.target.value === '' ? '' : parseInt(e.target.value, 10) })}
                    className={inputCls}
                  />
                </Field>
                <Field label={t('configInterval')}>
                  <input
                    type="number"
                    min="0"
                    value={draft.interval_hours ?? ''}
                    onChange={(e) => setDraft({ ...draft, interval_hours: e.target.value === '' ? '' : parseInt(e.target.value, 10) })}
                    className={inputCls}
                  />
                </Field>
              </div>

              <Field label={t('configKeywords')}>
                <input
                  type="text"
                  value={Array.isArray(draft.keywords) ? draft.keywords.join(', ') : ''}
                  onChange={(e) => setDraft({
                    ...draft,
                    keywords: e.target.value.split(',').map((s) => s.trim()).filter(Boolean),
                  })}
                  placeholder="SKILL.md, agent-skills, …"
                  className={inputCls}
                />
              </Field>

              <Field label={t('configGithubToken')}>
                <input
                  type="password"
                  value={draft.github_token || ''}
                  onChange={(e) => setDraft({ ...draft, github_token: e.target.value })}
                  placeholder="ghp_…"
                  autoComplete="off"
                  className={inputCls}
                />
              </Field>

              <div className="flex items-center gap-3">
                <label className="font-[var(--font-mono)] text-[10px] uppercase tracking-wider text-[var(--color-text-dim)]">
                  {t('configAuto')}
                </label>
                <button
                  type="button"
                  onClick={() => setDraft({ ...draft, auto_mode: !draft.auto_mode })}
                  className={`px-3 py-1.5 rounded text-xs font-[var(--font-mono)] uppercase tracking-wider border transition-colors ${
                    draft.auto_mode
                      ? 'border-[var(--color-accent-2)] text-[var(--color-accent)] bg-[var(--color-bg-elev)]'
                      : 'border-[var(--color-border)] text-[var(--color-text-dim)]'
                  }`}
                  aria-pressed={!!draft.auto_mode}
                >
                  {draft.auto_mode ? t('configAutoOn') : t('configAutoOff')}
                </button>
              </div>

              <div className="flex items-center gap-3 pt-2">
                <button
                  type="button"
                  onClick={onSave}
                  disabled={saving}
                  className="px-4 py-2 rounded bg-[var(--color-accent)] text-[var(--color-bg)] font-[var(--font-mono)] text-xs uppercase tracking-wider hover:opacity-90 disabled:opacity-50"
                >
                  {t('configSave')}
                </button>
                {savedMsg && (
                  <span className="font-[var(--font-mono)] text-xs text-[var(--color-native)]">
                    {t('configSaved')}
                  </span>
                )}
              </div>
            </section>
          )}

          {/* 立即运行 */}
          <section>
            <button
              type="button"
              onClick={onRun}
              disabled={running}
              className="px-4 py-2 rounded border border-[var(--color-accent-2)] text-[var(--color-accent)] font-[var(--font-mono)] text-xs uppercase tracking-wider hover:bg-[var(--color-bg-elev)] disabled:opacity-50"
            >
              {running ? t('crawlRunning') : t('crawlRun')}
            </button>
          </section>

          {/* 历史表格 */}
          <section>
            <h2 className="font-[var(--font-sans)] font-bold text-2xl mb-4 border-b border-[var(--color-rule)] pb-2">
              {t('crawlHistory')}
            </h2>
            <div className="overflow-x-auto border border-[var(--color-border)] rounded">
              <table className="w-full text-sm border-collapse">
                <thead>
                  <tr className="bg-[var(--color-bg-elev)] border-b border-[var(--color-rule)]">
                    <Th>{t('colStarted')}</Th>
                    <Th>{t('colFinished')}</Th>
                    <Th>{t('colStatus')}</Th>
                    <Th className="text-right">{t('colFound')}</Th>
                    <Th className="text-right">{t('colNew')}</Th>
                    <Th>{t('colError')}</Th>
                  </tr>
                </thead>
                <tbody>
                  {history.items.length === 0 ? (
                    <tr>
                      <td colSpan={6} className="px-4 py-6 text-center text-[var(--color-text-faint)] font-[var(--font-mono)] text-xs">—</td>
                    </tr>
                  ) : (
                    history.items.map((h, i) => {
                      const statusLabel = STATUS_KEY[h.status] ? t(STATUS_KEY[h.status]) : (h.status || '—');
                      const started = h.started_at || h.started || '—';
                      const finished = h.finished_at || h.finished || '—';
                      return (
                        <tr key={h.id ?? i} className="border-b border-[var(--color-border-soft)] last:border-b-0 align-top">
                          <Td mono>{started}</Td>
                          <Td mono>{finished}</Td>
                          <td className="px-3 py-2.5">
                            <span className={`font-[var(--font-mono)] text-xs ${statusColor(h.status)}`}>{statusLabel}</span>
                          </td>
                          <td className="px-3 py-2.5 text-right font-[var(--font-mono)] text-xs text-[var(--color-text-dim)] tnum">{h.found ?? '—'}</td>
                          <td className="px-3 py-2.5 text-right font-[var(--font-mono)] text-xs text-[var(--color-text-dim)] tnum">{h.new ?? '—'}</td>
                          <td className="px-3 py-2.5 font-[var(--font-mono)] text-xs text-[var(--color-text-faint)] break-all max-w-[280px]">{h.error || '—'}</td>
                        </tr>
                      );
                    })
                  )}
                </tbody>
              </table>
            </div>
          </section>
        </>
      )}
    </div>
  );
}
