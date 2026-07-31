// 统计行 — 4 列横排, 顶底浅灰分隔线, 留白分隔单元格, § 0X 淡灰序号 + Inter 700 大数字 + 大写小字标签
export default function StatRow({ stats }) {
  return (
    <section className="fade-in border-y border-[var(--color-border)]">
      <div className="grid grid-cols-2 md:grid-cols-4 gap-x-6 gap-y-6">
        {stats.map((s, i) => (
          <div key={i} className="px-1 md:px-2 py-6 md:py-8">
            <span className="block text-[var(--color-text-faint)] font-[var(--font-mono)] text-[10px] tracking-[0.18em]">
              § {String(i + 1).padStart(2, '0')}
            </span>
            <span className="block mt-3 font-[var(--font-sans)] font-bold text-[34px] md:text-[40px] tnum tracking-[-0.02em] leading-none text-[var(--color-text)]">
              {s.value}
            </span>
            <div className="mt-4">
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
