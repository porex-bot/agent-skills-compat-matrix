// 圆点 + 等级文本
import { useI18n } from '../lib/lang.jsx';
import StatusDot from './StatusDot.jsx';

export default function LevelBadge({ level }) {
  const { t } = useI18n();
  const safe = level || 'unknown';
  return (
    <span className="inline-flex items-center gap-2 whitespace-nowrap">
      <StatusDot level={safe} />
      <span className="font-[var(--font-mono)] text-xs text-[var(--color-text)]">
        {t('level_' + safe)}
      </span>
    </span>
  );
}
