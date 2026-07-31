// 统计行 — 4 列横排, 顶底 rule 分隔线, 每块顶部 § 0X 序号 + 大数字 + 底部带细线的标签
export default function StatRow({ stats }) {
  return (
    <section className="fade-in border-y border-[var(--color-rule)]">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-px bg-[var(--color-border-soft)]">
        {stats.map((s, i) => (
          <div key={i} className="bg-[var(--color-bg)] px-5 md:px-7 py-6 md:py-8">
            <span className="block text-[var(--color-accent)] font-[var(--font-mono)] text-[10px] tracking-[0.18em]">
              § {String(i + 1).padStart(2, '0')}
            </span>
            <span className="block mt-3 font-[var(--font-serif)] font-normal text-[34px] md:text-5xl tnum tracking-[-0.03em] leading-none text-[var(--color-text)]">
              {s.value}
            </span>
            <div className="mt-4 pt-3 border-t border-[var(--color-border-soft)]">
              <span className="font-[var(--font-mono)] text-[10.5px] uppercase tracking-[0.14em] text-[var(--color-text-dim)]">
                {s.label}
              </span>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
