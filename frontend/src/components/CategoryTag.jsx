// 分类标签 — mono 小字 + 细边框, 支持多标签
import { useI18n } from '../lib/lang.jsx';

export default function CategoryTag({ category, categories, className = '' }) {
  const { t } = useI18n();
  // 优先用 categories 数组; 否则回退到 category 单值
  let cats = Array.isArray(categories) && categories.length > 0
    ? categories
    : (category ? [category] : ['other']);

  return (
    <div className={`inline-flex flex-wrap gap-1.5 ${className}`.trim()}>
      {cats.map((cat) => (
        <span
          key={cat}
          className="inline-block font-[var(--font-mono)] text-[10px] uppercase tracking-[0.14em] text-[var(--color-text-dim)] border border-[var(--color-border)] bg-[var(--color-bg-elev)] rounded px-1.5 py-0.5"
        >
          {t('cat_' + cat)}
        </span>
      ))}
    </div>
  );
}
