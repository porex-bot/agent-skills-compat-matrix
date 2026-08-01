"""skill 列表/详情/筛选路由。"""
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from ..database import get_cursor, loads
from ..models import SUPPORT_LEVELS, SkillListResponse, SkillOut

router = APIRouter(prefix="/skills", tags=["skills"])


def _row_to_skill(row) -> SkillOut:
    """把数据库行转换为 SkillOut 模型，解析 JSON 字段。"""
    cats = loads(row["categories"], []) if "categories" in row.keys() else None
    if not cats:
        # 旧数据无 categories 字段, 用 category 单值兜底
        cats = [row["category"]] if row["category"] else ["other"]
    return SkillOut(
        id=row["id"],
        name=row["name"],
        repo=row["repo"],
        url=row["url"],
        category=row["category"],
        categories=cats,
        description=row["description"],
        description_zh=row["description_zh"],
        usage_tutorial=row["usage_tutorial"],
        uses_claude_extensions=loads(row["uses_claude_extensions"], []) or [],
        verified_at=row["verified_at"],
        verified_by=row["verified_by"],
        stars=row["stars"] or 0,
        source=row["source"],
        crawled_at=row["crawled_at"],
        compatibility=loads(row["compatibility"], {}) or {},
        caveats=loads(row["caveats"], {}) or {},
        caveats_zh=loads(row["caveats_zh"], {}) or {},
    )


@router.get("", response_model=SkillListResponse)
def list_skills(
    q: Optional[str] = Query(None, description="关键词搜 name/description"),
    agent: Optional[str] = Query(None, description="按 agent_id 筛选该 agent 兼容"),
    level: Optional[str] = Query(None, description="兼容等级筛选"),
    category: Optional[str] = Query(None, description="分类筛选(匹配多标签中任一)"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
):
    """查询 skill 列表，支持关键词、agent、等级、分类筛选与分页。"""
    if level is not None and level not in SUPPORT_LEVELS:
        raise HTTPException(status_code=400, detail=f"level 必须为 {SUPPORT_LEVELS} 之一")

    # 基础 SQL：关键词用 SQL 过滤；分类/agent/level 在 Python 中过滤
    # (分类是多标签 categories 数组, SQL like 匹配不稳, 改 Python)
    sql = "SELECT * FROM skills WHERE 1=1"
    params = []
    if q:
        sql += " AND (name LIKE ? OR description LIKE ?)"
        params.extend([f"%{q}%", f"%{q}%"])
    sql += " ORDER BY stars DESC, id ASC"

    with get_cursor() as cur:
        cur.execute(sql, params)
        rows = cur.fetchall()

    skills = [_row_to_skill(r) for r in rows]

    # 分类过滤: 匹配 categories 多标签中任一包含该分类
    if category:
        skills = [s for s in skills if category in s.categories]

    # agent 过滤：保留 compatibility 中存在该 agent 键的 skill
    if agent:
        skills = [s for s in skills if agent in s.compatibility]

    # level 过滤
    if level:
        if agent:
            # agent+level 联合：该 agent 的兼容等级 == level
            skills = [s for s in skills if s.compatibility.get(agent) == level]
        else:
            # 仅 level：任意 agent 的兼容等级 == level
            skills = [s for s in skills if level in s.compatibility.values()]

    total = len(skills)
    start = (page - 1) * page_size
    items = skills[start:start + page_size]
    return SkillListResponse(items=items, total=total, page=page, page_size=page_size)


@router.get("/{skill_id}", response_model=SkillOut)
def get_skill(skill_id: str):
    """返回完整 skill 详情（含 usage_tutorial, compatibility, caveats）。"""
    with get_cursor() as cur:
        cur.execute("SELECT * FROM skills WHERE id=?", (skill_id,))
        row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail=f"skill {skill_id} 不存在")
    return _row_to_skill(row)
