// 可移植性 badge — 统计 native+compatible 的 agent 数 / 总数
import { useI18n } from '../lib/lang.jsx';

export default function PortabilityBadge({ skill, agents }) {
  const { t } = useI18n();
  const total = agents?.length ?? 0;
  let n = 0;
  const compat = skill?.compatibility || {};
  for (const a of agents || []) {
    const lvl = compat[a.id];
    if (lvl === 'native' || lvl === 'compatible') n++;
  }
  return (
    <span className="inline-block font-[var(--font-mono)] text-[11px] tracking-wider text-[var(--color-text-dim)] border border-[var(--color-border)] rounded px-2 py-1">
      {t('portableSummary', { n, total })}
    </span>
  );
}
