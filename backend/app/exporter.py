"""静态 JSON 导出器：把数据库里的 skills/agents/stats 导出为静态 JSON 文件。

部署到 GitHub Pages 时没有后端服务，前端通过这些静态 JSON 读取数据。
本模块既可在路由 ``GET /api/export`` 中调用，也可作为 CLI 直接运行：

    python -m backend.app.exporter /path/to/output

生成的文件：
    - skills.json: 完整 skill 列表（数组，字段同 /api/skills 但不分页）
    - agents.json: 完整 agent 列表
    - stats.json:  {skills, agents, portable, risky}
"""
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

from .database import get_cursor, init_db
from .models import StatsOut
from .routers.agents import _row_to_agent
from .routers.skills import _row_to_skill
from .routers.stats import get_stats


def _collect_skills() -> List[Dict[str, Any]]:
    """读取全部 skill（按 stars DESC, id ASC 排序，与 /api/skills 默认排序一致）。"""
    with get_cursor() as cur:
        cur.execute("SELECT * FROM skills ORDER BY stars DESC, id ASC")
        rows = cur.fetchall()
    # 复用 skills 路由的行转换逻辑，确保导出字段与 API 完全一致
    return [_row_to_skill(r).model_dump() for r in rows]


def _collect_agents() -> List[Dict[str, Any]]:
    """读取全部 agent（按 id ASC 排序）。"""
    with get_cursor() as cur:
        cur.execute("SELECT * FROM agents ORDER BY id ASC")
        rows = cur.fetchall()
    # 复用 agents 路由的行转换逻辑
    return [_row_to_agent(r).model_dump() for r in rows]


def _collect_stats() -> Dict[str, Any]:
    """读取统计数字 {skills, agents, portable, risky}。复用 stats 路由逻辑。"""
    stats: StatsOut = get_stats()
    return stats.model_dump()


def export_static(target_dir: str) -> Dict[str, str]:
    """把数据库里的 skills/agents/stats 导出成静态 JSON 文件到 target_dir。

    幂等调用 ``init_db()`` 确保表存在，避免空库/全新环境导出时崩溃；
    不会触发 seed，导出结果反映数据库当前真实状态。

    返回各生成文件的绝对路径，形如 {"skills.json": "...", ...}。
    """
    # 确保表存在（CREATE IF NOT EXISTS，幂等），空库时导出空数组
    init_db()

    out_dir = Path(target_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    skills = _collect_skills()
    agents = _collect_agents()
    stats = _collect_stats()

    written: Dict[str, str] = {}
    for name, payload in (
        ("skills.json", skills),
        ("agents.json", agents),
        ("stats.json", stats),
    ):
        path = out_dir / name
        with open(path, "w", encoding="utf-8") as f:
            # ensure_ascii=False 保留中文，indent=2 便于 diff 与审阅
            json.dump(payload, f, ensure_ascii=False, indent=2)
        written[name] = str(path)
    return written


if __name__ == "__main__":
    # CLI 入口：python -m backend.app.exporter <output_dir>
    if len(sys.argv) < 2:
        print("用法: python -m backend.app.exporter <output_dir>", file=sys.stderr)
        sys.exit(1)

    target = sys.argv[1]
    # CLI 运行在全新检出时，先建表并导入种子，保证导出有内容可用
    init_db()
    from .seed import seed

    seed()
    result = export_static(target)
    for fname, fpath in result.items():
        print(f"{fname} -> {fpath}")
