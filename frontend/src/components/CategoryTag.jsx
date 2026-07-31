// 分类标签 — mono 小字 + 细边框
import { useI18n } from '../lib/lang.jsx';

export default function CategoryTag({ category, className = '' }) {
  const { t } = useI18n();
  const cat = category || 'other';
  return (
    <span
      className={`inline-block font-[var(--font-mono)] text-[10px] uppercase tracking-[0.14em] text-[var(--color-text-dim)] border border-[var(--color-border)] rounded px-1.5 py-0.5 ${className}`.trim()}
    >
      {t('cat_' + cat)}
    </span>
  );
}
