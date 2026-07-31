"""统计数字路由。"""
from fastapi import APIRouter

from ..database import get_cursor, loads
from ..models import StatsOut

router = APIRouter(prefix="/stats", tags=["stats"])

# 视为"可移植"的兼容等级
PORTABLE_LEVELS = {"native", "compatible"}


@router.get("", response_model=StatsOut)
def get_stats():
    """返回统计数字：skills/agents/portable/risky。

    - portable = 兼容性里 native+compatible 数量 >= agents 总数一半 的 skill 数
    - risky = 兼容性里 unsupported 数量 > 0 的 skill 数
    """
    with get_cursor() as cur:
        cur.execute("SELECT COUNT(*) AS c FROM skills")
        skills_count = cur.fetchone()["c"]
        cur.execute("SELECT COUNT(*) AS c FROM agents")
        agents_count = cur.fetchone()["c"]
        cur.execute("SELECT compatibility FROM skills")
        rows = cur.fetchall()

    half = agents_count / 2 if agents_count else 0
    portable = 0
    risky = 0
    for r in rows:
        compat = loads(r["compatibility"], {}) or {}
        portable_count = sum(1 for v in compat.values() if v in PORTABLE_LEVELS)
        if portable_count >= half and agents_count > 0:
            portable += 1
        if any(v == "unsupported" for v in compat.values()):
            risky += 1

    return StatsOut(skills=skills_count, agents=agents_count, portable=portable, risky=risky)
