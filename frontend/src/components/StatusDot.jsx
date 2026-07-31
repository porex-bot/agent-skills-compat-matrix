// 状态色圆点 — 单元格内仅显示颜色, 不带文字
export default function StatusDot({ level, title, className = '' }) {
  const safe = level || 'unknown';
  return (
    <span
      className={`dot-${safe} inline-block w-2 h-2 rounded-full align-middle ${className}`.trim()}
      title={title}
      aria-label={safe}
    />
  );
}
