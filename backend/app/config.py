"""配置管理：从环境变量读取 GitHub token 等敏感配置。"""
import os
from pathlib import Path

# backend/ 目录绝对路径，用于定位 ../data 种子文件
BASE_DIR = Path(__file__).resolve().parent.parent
# 数据文件目录（backend/../data）
DATA_DIR = BASE_DIR.parent / "data"
# SQLite 数据库文件路径
DB_PATH = BASE_DIR / "db.sqlite"
# 种子数据文件
SKILLS_JSON = DATA_DIR / "skills.json"
AGENTS_JSON = DATA_DIR / "agents.json"


def env_github_token() -> str:
    """从环境变量读取 GitHub token，未设置则返回空字符串。"""
    return os.environ.get("GITHUB_TOKEN", "")


def env_db_path() -> str:
    """返回 SQLite 数据库文件路径，允许通过环境变量覆盖。"""
    return os.environ.get("DB_PATH", str(DB_PATH))
