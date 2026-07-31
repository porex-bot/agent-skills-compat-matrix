"""Pydantic 数据模型：API 请求/响应与数据库行映射。"""
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


# 兼容性等级枚举
SUPPORT_LEVELS = ["native", "compatible", "partial", "unsupported", "unknown"]


class SkillOut(BaseModel):
    """skill 列表/详情响应模型。"""

    model_config = ConfigDict(from_attributes=True)

    id: str
    name: Optional[str] = None
    repo: Optional[str] = None
    url: Optional[str] = None
    category: Optional[str] = None
    description: Optional[str] = None
    description_zh: Optional[str] = None
    usage_tutorial: Optional[str] = None
    uses_claude_extensions: List[str] = Field(default_factory=list)
    verified_at: Optional[str] = None
    verified_by: Optional[str] = None
    stars: Optional[int] = 0
    source: Optional[str] = None
    crawled_at: Optional[str] = None
    compatibility: Dict[str, str] = Field(default_factory=dict)
    caveats: Dict[str, str] = Field(default_factory=dict)
    caveats_zh: Dict[str, str] = Field(default_factory=dict)


class SkillListResponse(BaseModel):
    """GET /api/skills 分页响应。"""

    items: List[SkillOut]
    total: int
    page: int
    page_size: int


class AgentOut(BaseModel):
    """agent 列表/详情响应模型。"""

    model_config = ConfigDict(from_attributes=True)

    id: str
    name: Optional[str] = None
    vendor: Optional[str] = None
    homepage: Optional[str] = None
    rules_file: Optional[str] = None
    skills_file: Optional[str] = None
    install_path: Dict[str, Any] = Field(default_factory=dict)
    frontmatter_required: List[str] = Field(default_factory=list)
    frontmatter_optional: List[str] = Field(default_factory=list)
    features: Dict[str, Any] = Field(default_factory=dict)
    notes: Optional[str] = None


class CrawlConfigOut(BaseModel):
    """爬虫配置响应模型。"""

    model_config = ConfigDict(from_attributes=True)

    id: int = 1
    min_stars: int = 10
    interval_hours: float = 24.0
    auto_mode: bool = False
    keywords: str = "SKILL.md"
    has_token: bool = False
    updated_at: Optional[str] = None


class CrawlConfigUpdate(BaseModel):
    """PUT /api/config 请求体，所有字段可选。"""

    min_stars: Optional[int] = None
    interval_hours: Optional[float] = None
    auto_mode: Optional[bool] = None
    keywords: Optional[str] = None
    github_token: Optional[str] = None


class CrawlHistoryOut(BaseModel):
    """爬取历史记录响应模型。"""

    model_config = ConfigDict(from_attributes=True)

    id: int
    started_at: Optional[str] = None
    finished_at: Optional[str] = None
    status: Optional[str] = None
    found_count: Optional[int] = 0
    new_count: Optional[int] = 0
    error: Optional[str] = None


class CrawlHistoryListResponse(BaseModel):
    """GET /api/crawl/history 分页响应。"""

    items: List[CrawlHistoryOut]
    total: int
    page: int
    page_size: int


class CrawlTriggerResponse(BaseModel):
    """POST /api/crawl 触发响应。"""

    history_id: int
    status: str
    message: Optional[str] = None


class StatsOut(BaseModel):
    """GET /api/stats 统计响应。"""

    skills: int
    agents: int
    portable: int
    risky: int
