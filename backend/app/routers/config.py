"""爬虫配置 GET/PUT 路由。"""
from datetime import datetime, timezone

from fastapi import APIRouter

from .. import scheduler
from ..database import get_cursor
from ..models import CrawlConfigOut, CrawlConfigUpdate

router = APIRouter(prefix="/config", tags=["config"])


def _row_to_config(row) -> CrawlConfigOut:
    """把数据库行转换为 CrawlConfigOut，auto_mode 转 bool，token 转为 has_token。"""
    return CrawlConfigOut(
        id=row["id"],
        min_stars=row["min_stars"],
        interval_hours=row["interval_hours"],
        auto_mode=bool(row["auto_mode"]),
        keywords=row["keywords"],
        has_token=bool(row["github_token"]),
        updated_at=row["updated_at"],
    )


@router.get("", response_model=CrawlConfigOut)
def get_config():
    """返回当前爬虫配置。"""
    with get_cursor() as cur:
        cur.execute("SELECT * FROM crawl_config WHERE id=1")
        row = cur.fetchone()
    return _row_to_config(row)


@router.put("", response_model=CrawlConfigOut)
def update_config(payload: CrawlConfigUpdate):
    """更新爬虫配置（min_stars/interval_hours/auto_mode/keywords/github_token）。

    更新 auto_mode 或 interval_hours 后自动重新调度定时任务。
    """
    fields = []
    params = []
    for key in ("min_stars", "interval_hours", "auto_mode", "keywords"):
        value = getattr(payload, key)
        if value is not None:
            if key == "auto_mode":
                value = 1 if value else 0
            fields.append(f"{key}=?")
            params.append(value)
    if payload.github_token is not None:
        # 空字符串视为清除 token
        fields.append("github_token=?")
        params.append(payload.github_token or None)
    fields.append("updated_at=?")
    params.append(datetime.now(timezone.utc).isoformat())
    params.append(1)  # WHERE id=1

    with get_cursor() as cur:
        if fields:
            cur.execute(
                f"UPDATE crawl_config SET {', '.join(fields)} WHERE id=?", params
            )
        cur.execute("SELECT * FROM crawl_config WHERE id=1")
        row = cur.fetchone()

    # 配置变更后重新调度
    scheduler.reschedule()
    return _row_to_config(row)
