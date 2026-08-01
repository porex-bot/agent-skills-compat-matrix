"""SQLite 连接与建表。使用标准库 sqlite3，单文件 db.sqlite。"""
import json
import sqlite3
from contextlib import contextmanager

from . import config


def get_conn() -> sqlite3.Connection:
    """打开一个 SQLite 连接，启用外键约束并让 row 可按列名访问。"""
    conn = sqlite3.connect(config.env_db_path())
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


@contextmanager
def get_cursor():
    """便捷上下文管理器：自动提交/回滚并关闭连接。"""
    conn = get_conn()
    try:
        cur = conn.cursor()
        yield cur
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """建表（IF NOT EXISTS），在应用启动时调用。"""
    with get_cursor() as cur:
        # skills 表：skill 数据库主表
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS skills (
                id TEXT PRIMARY KEY,
                name TEXT,
                repo TEXT,
                url TEXT,
                category TEXT,
                categories TEXT,
                description TEXT,
                description_zh TEXT,
                usage_tutorial TEXT,
                uses_claude_extensions TEXT,
                verified_at TEXT,
                verified_by TEXT,
                stars INTEGER,
                source TEXT,
                crawled_at TEXT,
                compatibility TEXT,
                caveats TEXT,
                caveats_zh TEXT
            )
            """
        )
        # 旧库迁移：若 skills 表已存在但缺少 categories 列，则补上
        try:
            cur.execute("ALTER TABLE skills ADD COLUMN categories TEXT")
        except sqlite3.OperationalError:
            # 列已存在时 sqlite 会抛 OperationalError，忽略即可
            pass
        # agents 表：agent 能力矩阵
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS agents (
                id TEXT PRIMARY KEY,
                name TEXT,
                vendor TEXT,
                homepage TEXT,
                rules_file TEXT,
                skills_file TEXT,
                install_path TEXT,
                frontmatter_required TEXT,
                frontmatter_optional TEXT,
                features TEXT,
                notes TEXT,
                notes_zh TEXT
            )
            """
        )
        # 旧库迁移：若 agents 表已存在但缺少 notes_zh 列，则补上
        try:
            cur.execute("ALTER TABLE agents ADD COLUMN notes_zh TEXT")
        except sqlite3.OperationalError:
            # 列已存在时 sqlite 会抛 OperationalError，忽略即可
            pass
        # crawl_config 表：单行爬虫配置（id 固定为 1）
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS crawl_config (
                id INTEGER PRIMARY KEY DEFAULT 1,
                min_stars INTEGER DEFAULT 500,
                interval_hours REAL DEFAULT 24,
                auto_mode INTEGER DEFAULT 0,
                keywords TEXT DEFAULT 'SKILL.md',
                github_token TEXT,
                updated_at TEXT
            )
            """
        )
        # crawl_history 表：爬取历史
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS crawl_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                started_at TEXT,
                finished_at TEXT,
                status TEXT,
                found_count INTEGER,
                new_count INTEGER,
                error TEXT
            )
            """
        )
        # 确保 crawl_config 至少有一行默认配置
        cur.execute(
            """
            INSERT OR IGNORE INTO crawl_config (id, min_stars, interval_hours, auto_mode, keywords, github_token, updated_at)
            VALUES (1, 500, 24, 0, 'SKILL.md', NULL, NULL)
            """
        )


# ---- 以下为通用的 JSON 字段序列化/反序列化辅助函数 ----

def dumps(value) -> str:
    """把 Python 对象序列化为 JSON 字符串，None 也安全处理。"""
    if value is None:
        return "null"
    return json.dumps(value, ensure_ascii=False)


def loads(text: str, default=None):
    """把 JSON 字符串反序列化为 Python 对象，失败时返回默认值。"""
    if not text:
        return default
    try:
        return json.loads(text)
    except (ValueError, TypeError):
        return default
