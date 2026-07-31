// 简单加载状态 — spinner + loading 文案
import { useI18n } from '../lib/lang.jsx';

export default function Loading({ className = '' }) {
  const { t } = useI18n();
  return (
    <div className={`flex items-center gap-3 text-[var(--color-text-dim)] font-[var(--font-mono)] text-sm py-12 ${className}`.trim()}>
      <span className="inline-block w-3.5 h-3.5 border-2 border-[var(--color-accent)] border-t-transparent rounded-full animate-spin" />
      {t('loading')}
    </div>
  );
}
