"""agent 列表/详情路由。"""
from fastapi import APIRouter, HTTPException

from ..database import get_cursor, loads
from ..models import AgentOut

router = APIRouter(prefix="/agents", tags=["agents"])


def _row_to_agent(row) -> AgentOut:
    """把数据库行转换为 AgentOut 模型，解析 JSON 字段。"""
    return AgentOut(
        id=row["id"],
        name=row["name"],
        vendor=row["vendor"],
        homepage=row["homepage"],
        rules_file=row["rules_file"],
        skills_file=row["skills_file"],
        install_path=loads(row["install_path"], {}) or {},
        frontmatter_required=loads(row["frontmatter_required"], []) or [],
        frontmatter_optional=loads(row["frontmatter_optional"], []) or [],
        features=loads(row["features"], {}) or {},
        notes=row["notes"],
        notes_zh=row["notes_zh"],
    )


@router.get("", response_model=list[AgentOut])
def list_agents():
    """返回全部 agent 列表。"""
    with get_cursor() as cur:
        cur.execute("SELECT * FROM agents ORDER BY id ASC")
        rows = cur.fetchall()
    return [_row_to_agent(r) for r in rows]


@router.get("/{agent_id}", response_model=AgentOut)
def get_agent(agent_id: str):
    """返回单个 agent 详情。"""
    with get_cursor() as cur:
        cur.execute("SELECT * FROM agents WHERE id=?", (agent_id,))
        row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail=f"agent {agent_id} 不存在")
    return _row_to_agent(row)
