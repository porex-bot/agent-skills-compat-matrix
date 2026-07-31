// 404 — 简单居中
import { Link } from 'react-router-dom';
import { useI18n } from '../lib/lang.jsx';

export default function NotFoundPage() {
  const { t } = useI18n();
  return (
    <div className="fade-in min-h-[55vh] flex flex-col items-center justify-center text-center">
      <div className="font-[var(--font-serif)] font-bold text-7xl md:text-8xl text-[var(--color-text)] tracking-[-0.04em] leading-none">
        404
      </div>
      <div className="mt-3 font-[var(--font-mono)] text-xs uppercase tracking-[0.22em] text-[var(--color-text-dim)]">
        — Not found —
      </div>
      <Link
        to="/"
        className="mt-7 font-[var(--font-mono)] text-xs uppercase tracking-wider text-[var(--color-accent)] border border-[var(--color-accent-2)] rounded px-4 py-2 hover:bg-[var(--color-bg-elev)]"
      >
        {t('backToMatrix')}
      </Link>
    </div>
  );
}
