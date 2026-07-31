"""手动触发爬取 / 历史记录路由。"""
from fastapi import APIRouter, Query

from .. import crawler
from ..database import get_cursor
from ..models import CrawlHistoryListResponse, CrawlHistoryOut, CrawlTriggerResponse

router = APIRouter(prefix="/crawl", tags=["crawl"])


@router.post("", response_model=CrawlTriggerResponse)
def trigger_crawl():
    """手动触发一次爬取，立即在后台执行并返回本次历史 id。"""
    history_id = crawler.run_crawl_background()
    return CrawlTriggerResponse(
        history_id=history_id, status="running", message="爬取已在后台启动"
    )


@router.get("/history", response_model=CrawlHistoryListResponse)
def crawl_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """返回爬取历史（分页，按时间倒序）。"""
    with get_cursor() as cur:
        cur.execute("SELECT COUNT(*) AS c FROM crawl_history")
        total = cur.fetchone()["c"]
        cur.execute(
            "SELECT * FROM crawl_history ORDER BY id DESC LIMIT ? OFFSET ?",
            (page_size, (page - 1) * page_size),
        )
        rows = cur.fetchall()
    items = [
        CrawlHistoryOut(
            id=r["id"],
            started_at=r["started_at"],
            finished_at=r["finished_at"],
            status=r["status"],
            found_count=r["found_count"] or 0,
            new_count=r["new_count"] or 0,
            error=r["error"],
        )
        for r in rows
    ]
    return CrawlHistoryListResponse(items=items, total=total, page=page, page_size=page_size)
