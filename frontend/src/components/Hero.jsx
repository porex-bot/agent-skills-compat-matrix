// Hero 区 — 左对齐, kicker 带横线, H1 Fraunces 700 + accent em, lede max-w 62ch
// titleParts: { pre, accent, post }
export default function Hero({ kicker, titleParts, lede, sectionNumber = '01' }) {
  return (
    <section className="fade-in">
      <div className="flex items-center gap-3 mb-6">
        <span className="block w-8 h-px bg-[var(--color-accent-2)]" />
        <span className="font-[var(--font-mono)] text-[11px] uppercase tracking-[0.22em] text-[var(--color-text-dim)]">
          {kicker ?? `§ ${sectionNumber}`}
        </span>
      </div>
      <h1 className="font-[var(--font-serif)] font-bold text-[44px] md:text-[56px] leading-[1.04] tracking-[-0.025em] text-[var(--color-text)] max-w-[20ch] md:max-w-[24ch]">
        {titleParts.pre}
        <em className="font-black text-[var(--color-accent)]">{titleParts.accent}</em>
        {titleParts.post}
      </h1>
      {lede && (
        <p className="mt-6 text-[17px] leading-[1.6] text-[var(--color-text-dim)] max-w-[62ch]">
          {lede}
        </p>
      )}
    </section>
  );
}
