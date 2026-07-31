"""APScheduler 自动调度：根据 crawl_config 的 auto_mode/interval_hours 定时爬取。"""
import logging

from apscheduler.schedulers.background import BackgroundScheduler

from . import crawler
from .database import get_cursor

logger = logging.getLogger("agent-skills-matrix.scheduler")

# 调度器单例
_scheduler: BackgroundScheduler | None = None
# 调度任务固定 id
JOB_ID = "auto_crawl"


def _load_auto_config() -> tuple[bool, float]:
    """读取 auto_mode 与 interval_hours。返回 (auto_mode, interval_hours)。"""
    with get_cursor() as cur:
        cur.execute("SELECT auto_mode, interval_hours FROM crawl_config WHERE id=1")
        row = cur.fetchone()
        if not row:
            return False, 24.0
        return bool(row["auto_mode"]), float(row["interval_hours"] or 24.0)


def _reschedule() -> None:
    """根据当前配置重排定时任务：移除旧 job，若 auto_mode=1 则按 interval 添加新 job。"""
    global _scheduler
    if _scheduler is None:
        return
    try:
        _scheduler.remove_job(JOB_ID)
    except Exception:
        # job 不存在时忽略
        pass

    auto_mode, interval_hours = _load_auto_config()
    if not auto_mode:
        return
    if interval_hours <= 0:
        interval_hours = 24.0
    _scheduler.add_job(
        crawler.run_crawl,
        "interval",
        hours=interval_hours,
        id=JOB_ID,
        replace_existing=True,
    )
    logger.info("已调度自动爬取，间隔 %.1f 小时", interval_hours)


def start_scheduler() -> None:
    """启动后台调度器并按配置添加首次任务。"""
    global _scheduler
    if _scheduler is not None:
        return
    _scheduler = BackgroundScheduler()
    _scheduler.start()
    _reschedule()
    logger.info("调度器已启动")


def shutdown_scheduler() -> None:
    """关闭调度器（应用退出时调用）。"""
    global _scheduler
    if _scheduler is not None:
        _scheduler.shutdown(wait=False)
        _scheduler = None


def reschedule() -> None:
    """供 PUT /api/config 调用：配置变更后重新调度。"""
    _reschedule()
