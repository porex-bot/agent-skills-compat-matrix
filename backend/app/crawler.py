"""GitHub 爬虫核心逻辑：搜索 SKILL.md，拉取内容，解析并入库。"""
import re
import threading
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

import httpx

from . import config
from .database import dumps, get_cursor, loads

# GitHub API 基址
GITHUB_API = "https://api.github.com"
RAW_BASE = "https://raw.githubusercontent.com"
# 单次搜索最大页数
MAX_PAGES = 5
PER_PAGE = 100
# 默认超时（秒）
TIMEOUT = 20.0
# usage_tutorial 最大字符数
TUTORIAL_MAX_CHARS = 2000
# MyMemory 翻译 API 单次请求最大字符数
TRANSLATE_MAX_CHARS = 480

# 并发爬取锁，避免多次爬取同时写库
_crawl_lock = threading.Lock()
# 当前是否有爬取正在进行
_running_lock = threading.Lock()
_is_running = {"value": False}


def _now() -> str:
    """返回当前 UTC 时间 ISO 字符串。"""
    return datetime.now(timezone.utc).isoformat()


def _kebab(s: str) -> str:
    """把字符串转换为 kebab-case（小写，非字母数字转为连字符）。"""
    s = (s or "").strip().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-")


def _agent_ids() -> List[str]:
    """从数据库读取全部 agent id 列表。"""
    with get_cursor() as cur:
        cur.execute("SELECT id FROM agents")
        return [row["id"] for row in cur.fetchall()]


def _default_compatibility() -> Dict[str, str]:
    """构造默认兼容性：open-standard=compatible，其余 agent=unknown。"""
    compat = {aid: "unknown" for aid in _agent_ids()}
    compat["open-standard"] = "compatible"
    return compat


def _headers(token: str) -> Dict[str, str]:
    """构造 GitHub API 请求头。"""
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "agent-skills-matrix"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    return headers


def _parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """解析 markdown 顶部的 YAML frontmatter，返回 (字段字典, 正文)。

    依赖最小化：优先用 PyYAML（若已安装），否则用简易键值解析器。
    """
    if not content.startswith("---"):
        return {}, content
    # 找到第二个 --- 作为 frontmatter 结束
    end = content.find("\n---", 3)
    if end == -1:
        return {}, content
    fm_text = content[3:end].strip()
    body = content[end + 4:].lstrip("\n")

    try:
        import yaml  # type: ignore

        data = yaml.safe_load(fm_text) or {}
        if isinstance(data, dict):
            return data, body
    except Exception:
        pass

    # 简易解析器：处理 key: value 与块列表
    data: Dict[str, Any] = {}
    current_key = None
    for line in fm_text.splitlines():
        if not line.strip():
            continue
        if line.startswith("  - ") or line.startswith("- "):
            # 块列表项
            item = line.split("-", 1)[1].strip().strip('"').strip("'")
            if current_key is not None:
                if not isinstance(data.get(current_key), list):
                    data[current_key] = []
                data[current_key].append(item)
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            key = key.strip()
            value = value.strip()
            current_key = key
            if not value:
                data[key] = []
            elif value.startswith("[") and value.endswith("]"):
                inner = value[1:-1]
                data[key] = [x.strip().strip('"').strip("'") for x in inner.split(",") if x.strip()]
            else:
                data[key] = value.strip('"').strip("'")
    return data, body


def _extract_usage_tutorial(skill_body: str, readme: str) -> str:
    """从 SKILL.md 正文或 README.md 提取使用教程草稿。

    优先提取 ## Usage / ## How to use 段落；否则取正文前 2000 字符。
    """
    # 优先：SKILL.md 里的 ## Usage / ## How to use 段落
    for source in (skill_body, readme):
        if not source:
            continue
        m = re.search(
            r"(?m)^#{1,3}\s*(Usage|How to use|How to Use|用法|使用方法|使用教程).*$",
            source,
        )
        if m:
            start = m.start()
            # 截取到下一个同级或更高级标题
            rest = source[start:]
            next_heading = re.search(r"(?m)^#{1,3}\s+\S", rest[len(m.group(0)):])
            if next_heading:
                section = rest[: len(m.group(0)) + next_heading.start()]
            else:
                section = rest
            return section.strip()[:TUTORIAL_MAX_CHARS]
    # 回退：SKILL.md 正文前 2000 字符，再回退 README 前 2000 字符
    for source in (skill_body, readme):
        if source and source.strip():
            return source.strip()[:TUTORIAL_MAX_CHARS]
    return ""


def _search_code(keywords: str, token: str) -> List[Dict[str, Any]]:
    """调用 GitHub Code Search API，返回去重后的搜索结果项列表。"""
    headers = _headers(token)
    items: List[Dict[str, Any]] = []
    seen = set()
    # 关键词组合：filename:SKILL 与 filename:skill 各搜一遍
    queries = [
        f"{keywords} extension:md filename:SKILL",
        f"{keywords} extension:md filename:skill",
    ]
    for q in queries:
        for page in range(1, MAX_PAGES + 1):
            try:
                resp = httpx.get(
                    f"{GITHUB_API}/search/code",
                    params={"q": q, "per_page": PER_PAGE, "page": page},
                    headers=headers,
                    timeout=TIMEOUT,
                )
            except httpx.HTTPError:
                break
            if resp.status_code != 200:
                break
            payload = resp.json()
            page_items = payload.get("items", [])
            if not page_items:
                break
            for it in page_items:
                repo = it.get("repository", {})
                full = repo.get("full_name") or ""
                path = it.get("path") or ""
                key = f"{full}:{path}"
                if key in seen:
                    continue
                seen.add(key)
                items.append(it)
            # 不足一页说明没有更多
            if len(page_items) < PER_PAGE:
                break
    return items


def _get_repo(owner: str, repo: str, token: str) -> Optional[Dict[str, Any]]:
    """获取仓库信息（stars、默认分支）。"""
    try:
        resp = httpx.get(
            f"{GITHUB_API}/repos/{owner}/{repo}",
            headers=_headers(token),
            timeout=TIMEOUT,
        )
        if resp.status_code == 200:
            return resp.json()
    except httpx.HTTPError:
        pass
    return None


def _fetch_raw(owner: str, repo: str, branch: str, path: str, token: str) -> str:
    """拉取 raw 文件内容，失败返回空字符串。"""
    url = f"{RAW_BASE}/{owner}/{repo}/{branch}/{path}"
    try:
        resp = httpx.get(url, headers=_headers(token), timeout=TIMEOUT)
        if resp.status_code == 200:
            return resp.text
    except httpx.HTTPError:
        pass
    return ""


def _translate_to_zh(text: str) -> str:
    """把英文 description 翻译成中文，失败/无变化返回空串。

    优先用 Google Translate 非官方 endpoint（无需 key、相对稳定），
    失败回退 MyMemory 免费翻译 API。两者都免费但按 IP 限流，
    对爬虫低频场景够用。失败时返回空串，前端会兜底显示英文 description。
    """
    if not text or not text.strip():
        return ""
    src = text.strip()
    # 单次请求截断，避免超长文本被拒
    src = src[:TRANSLATE_MAX_CHARS]

    # 1) Google Translate 非官方 endpoint
    try:
        resp = httpx.get(
            "https://translate.googleapis.com/translate_a/single",
            params={"client": "gtx", "sl": "en", "tl": "zh-CN", "dt": "t", "q": src},
            timeout=15.0,
        )
        if resp.status_code == 200:
            data = resp.json()
            # 返回结构 [[["译文","原文",...],...], ...]，拼接每段译文
            parts = data[0] if data and isinstance(data[0], list) else []
            translated = "".join(p[0] for p in parts if isinstance(p, list) and p and p[0])
            if translated and translated.strip().upper() != src.upper():
                return translated.strip()
    except (httpx.HTTPError, ValueError, IndexError):
        pass

    # 2) MyMemory 兜底
    try:
        resp = httpx.get(
            "https://api.mymemory.translated.net/get",
            params={"q": src, "langpair": "en|zh-CN"},
            timeout=15.0,
        )
        if resp.status_code == 200:
            data = resp.json()
            translated = (data.get("responseData") or {}).get("translatedText", "")
            if translated and translated.strip().upper() != src.upper():
                up = translated.upper()
                if "MYMEMORY WARNING" not in up and "PLEASE SELECT" not in up:
                    return translated.strip()
    except (httpx.HTTPError, ValueError):
        pass

    return ""


def _start_history() -> int:
    """创建一条 status='running' 的爬取历史，返回其 id。"""
    with get_cursor() as cur:
        cur.execute(
            "INSERT INTO crawl_history (started_at, status, found_count, new_count) VALUES (?, 'running', 0, 0)",
            (_now(),),
        )
        return cur.lastrowid


def _finish_history(history_id: int, status: str, found: int, new: int, error: str = "") -> None:
    """更新爬取历史为完成状态。"""
    with get_cursor() as cur:
        cur.execute(
            "UPDATE crawl_history SET finished_at=?, status=?, found_count=?, new_count=?, error=? WHERE id=?",
            (_now(), status, found, new, error, history_id),
        )


def _load_config() -> Dict[str, Any]:
    """读取 crawl_config 单行配置。"""
    with get_cursor() as cur:
        cur.execute("SELECT * FROM crawl_config WHERE id=1")
        row = cur.fetchone()
        return dict(row) if row else {}


def execute_crawl(history_id: Optional[int] = None) -> int:
    """执行一次完整爬取流程，返回历史 id。

    若 history_id 为 None，则内部创建一条历史记录。
    """
    cfg = _load_config()
    token = cfg.get("github_token") or config.env_github_token()
    min_stars = cfg.get("min_stars", 500) or 500

    if history_id is None:
        history_id = _start_history()

    # 爬取前清理：删除 source='crawled' 且 stars 低于当前门槛的旧记录。
    # seed 种子数据不受影响；CI 每次重建库无旧数据，此步主要服务于自部署后端。
    with get_cursor() as cur:
        cur.execute(
            "DELETE FROM skills WHERE source='crawled' AND (stars IS NULL OR stars < ?)",
            (min_stars,),
        )
        purged = cur.rowcount
    if purged:
        print(f"[crawl] 清理 {purged} 条低于 {min_stars} star 的旧 crawled 记录")

    found = 0
    new_count = 0
    try:
        results = _search_code(cfg.get("keywords", "SKILL.md"), token)
        for item in results:
            repo_info = item.get("repository", {})
            full_name = repo_info.get("full_name", "")
            if not full_name or "/" not in full_name:
                continue
            owner, repo = full_name.split("/", 1)
            found += 1

            repo_data = _get_repo(owner, repo, token)
            stars = repo_data.get("stargazers_count", 0) if repo_data else 0
            # 按 min_stars 过滤
            if stars < min_stars:
                continue

            branch = (repo_data or {}).get("default_branch", "main")
            path = item.get("path", "SKILL.md")
            content = _fetch_raw(owner, repo, branch, path, token)
            fm, body = _parse_frontmatter(content) if content else ({}, "")

            # usage_tutorial：优先 SKILL.md 正文段落，回退 README
            readme = _fetch_raw(owner, repo, branch, "README.md", token)
            tutorial = _extract_usage_tutorial(body, readme)

            skill_id = _kebab(repo)
            name = fm.get("name") or repo
            description = fm.get("description") or (repo_data or {}).get("description", "") or ""

            # 翻译 description 为中文（失败返回空串，前端兜底显示英文）
            description_zh = _translate_to_zh(description)

            # 兼容性默认：open-standard=compatible，其余 unknown
            compatibility = _default_compatibility()
            uses_ext = fm.get("uses_claude_extensions") or []
            if not isinstance(uses_ext, list):
                uses_ext = [str(uses_ext)]

            inserted = _upsert_skill(
                {
                    "id": skill_id,
                    "name": name,
                    "repo": full_name,
                    "url": f"https://github.com/{full_name}",
                    "category": fm.get("category") or "other",
                    "description": description,
                    "description_zh": description_zh,
                    "usage_tutorial": tutorial,
                    "uses_claude_extensions": uses_ext,
                    "verified_at": "",
                    "verified_by": "crawler",
                    "stars": stars,
                    "source": "crawled",
                    "crawled_at": _now(),
                    "compatibility": compatibility,
                    "caveats": {},
                    "caveats_zh": {},
                }
            )
            if inserted:
                new_count += 1

        _finish_history(history_id, "success", found, new_count, "")
    except Exception as e:  # noqa: BLE001
        _finish_history(history_id, "failed", found, new_count, str(e))
    finally:
        with _running_lock:
            _is_running["value"] = False
    return history_id


def _upsert_skill(skill: Dict[str, Any]) -> bool:
    """插入 skill 记录：已存在则跳过（不覆盖手动 compatibility），但可更新 stars。

    返回 True 表示新增了一条记录。
    """
    with get_cursor() as cur:
        cur.execute("SELECT id FROM skills WHERE id=?", (skill["id"],))
        existing = cur.fetchone()
        if existing:
            # 已存在：只更新 stars，不覆盖 compatibility 等手动编辑字段
            cur.execute(
                "UPDATE skills SET stars=?, crawled_at=? WHERE id=?",
                (skill.get("stars", 0), skill.get("crawled_at"), skill["id"]),
            )
            return False
        cur.execute(
            """
            INSERT INTO skills (id, name, repo, url, category, description, description_zh,
                                usage_tutorial, uses_claude_extensions, verified_at,
                                verified_by, stars, source, crawled_at, compatibility,
                                caveats, caveats_zh)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                skill["id"],
                skill.get("name"),
                skill.get("repo"),
                skill.get("url"),
                skill.get("category"),
                skill.get("description"),
                skill.get("description_zh", ""),
                skill.get("usage_tutorial", ""),
                dumps(skill.get("uses_claude_extensions", [])),
                skill.get("verified_at", ""),
                skill.get("verified_by"),
                skill.get("stars", 0),
                skill.get("source", "crawled"),
                skill.get("crawled_at"),
                dumps(skill.get("compatibility", {})),
                dumps(skill.get("caveats", {})),
                dumps(skill.get("caveats_zh", {})),
            ),
        )
        return True


def run_crawl() -> int:
    """调度器/手动触发入口：同步执行一次爬取，返回历史 id。"""
    with _running_lock:
        if _is_running["value"]:
            # 已有爬取进行中，直接返回最近一条 running 历史
            with get_cursor() as cur:
                cur.execute(
                    "SELECT id FROM crawl_history WHERE status='running' ORDER BY id DESC LIMIT 1"
                )
                row = cur.fetchone()
                return row["id"] if row else 0
        _is_running["value"] = True
    # 注意：锁释放后再执行，execute_crawl 内部会在 finally 复位 _is_running
    return execute_crawl()


def run_crawl_background() -> int:
    """手动触发入口：创建历史记录后用后台线程执行，立即返回历史 id。"""
    with _running_lock:
        if _is_running["value"]:
            with get_cursor() as cur:
                cur.execute(
                    "SELECT id FROM crawl_history WHERE status='running' ORDER BY id DESC LIMIT 1"
                )
                row = cur.fetchone()
                return row["id"] if row else 0
        _is_running["value"] = True
    history_id = _start_history()
    thread = threading.Thread(target=execute_crawl, args=(history_id,), daemon=True)
    thread.start()
    return history_id
