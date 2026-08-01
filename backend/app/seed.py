"""种子数据导入：从 ../data/skills.json 和 ../data/agents.json 导入。

- 启动时若 skills 表为空，导入种子 skill（source='seed', stars=0, usage_tutorial 留空）。
- agents 全量 upsert。
"""
import json

from . import config
from .database import dumps, get_cursor


def _read_json(path):
    """读取 JSON 文件，文件不存在时返回空字典。"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def seed() -> None:
    """导入种子数据：skills 表为空时填入种子 skill，agents 全量 upsert。"""
    skills_data = _read_json(config.SKILLS_JSON)
    agents_data = _read_json(config.AGENTS_JSON)

    with get_cursor() as cur:
        # ---- agents：全量 upsert ----
        for agent in agents_data.get("agents", []):
            cur.execute(
                """
                INSERT INTO agents (id, name, vendor, homepage, rules_file, skills_file,
                                    install_path, frontmatter_required, frontmatter_optional,
                                    features, notes, notes_zh)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    name=excluded.name, vendor=excluded.vendor, homepage=excluded.homepage,
                    rules_file=excluded.rules_file, skills_file=excluded.skills_file,
                    install_path=excluded.install_path,
                    frontmatter_required=excluded.frontmatter_required,
                    frontmatter_optional=excluded.frontmatter_optional,
                    features=excluded.features, notes=excluded.notes, notes_zh=excluded.notes_zh
                """,
                (
                    agent.get("id"),
                    agent.get("name"),
                    agent.get("vendor"),
                    agent.get("homepage"),
                    agent.get("rules_file"),
                    agent.get("skills_file"),
                    dumps(agent.get("install_path", {})),
                    dumps(agent.get("frontmatter_required", [])),
                    dumps(agent.get("frontmatter_optional", [])),
                    dumps(agent.get("features", {})),
                    agent.get("notes"),
                    agent.get("notes_zh"),
                ),
            )

        # ---- skills：仅当表为空时导入种子 ----
        cur.execute("SELECT COUNT(*) AS c FROM skills")
        count = cur.fetchone()["c"]
        if count > 0:
            return

        for skill in skills_data.get("skills", []):
            cat = skill.get("category") or "other"
            cur.execute(
                """
                INSERT INTO skills (id, name, repo, url, category, categories, description, description_zh,
                                    usage_tutorial, uses_claude_extensions, verified_at,
                                    verified_by, stars, source, crawled_at, compatibility,
                                    caveats, caveats_zh)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    skill.get("id"),
                    skill.get("name"),
                    skill.get("repo"),
                    skill.get("url"),
                    cat,
                    dumps(skill.get("categories", [cat])),
                    skill.get("description"),
                    skill.get("description_zh"),
                    "",  # 种子 skill 的 usage_tutorial 暂留空字符串
                    dumps(skill.get("uses_claude_extensions", [])),
                    skill.get("verified_at"),
                    skill.get("verified_by"),
                    0,  # 种子 skill stars=0
                    "seed",  # source='seed'
                    None,  # crawled_at
                    dumps(skill.get("compatibility", {})),
                    dumps(skill.get("caveats", {})),
                    dumps(skill.get("caveats_zh", {})),
                ),
            )
