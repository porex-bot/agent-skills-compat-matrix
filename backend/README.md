# Agent Skills Matrix Backend

基于 FastAPI 的爬虫后端服务，从 GitHub 爬取 SKILL.md 文件汇总成 skill 数据库，并提供 API 给前端。

## 依赖

标准 PyPI 包：fastapi、uvicorn[standard]、httpx、apscheduler、pydantic。数据库使用标准库 sqlite3（单文件 `db.sqlite`）。

```bash
pip install -r requirements.txt
```

## 启动

```bash
uvicorn app.main:app --reload --port 8000
```

可选环境变量：

- `GITHUB_TOKEN`：GitHub 个人访问令牌，提升爬虫 API 速率限制（也可通过 `PUT /api/config` 写入数据库）。
- `DB_PATH`：自定义 SQLite 数据库文件路径，默认 `backend/db.sqlite`。

启动时会自动建表；若 skills 表为空，从 `../data/skills.json` 与 `../data/agents.json` 导入种子数据。

## API 端点

### skills
- `GET /api/skills` 查询参数：`q`、`agent`、`level`、`category`、`page`、`page_size`，返回 `{items, total, page, page_size}`
- `GET /api/skills/{id}` 返回 skill 完整详情

### agents
- `GET /api/agents` agent 列表
- `GET /api/agents/{id}` agent 详情

### config（爬虫配置）
- `GET /api/config` 返回当前配置
- `PUT /api/config` 更新 min_stars/interval_hours/auto_mode/keywords/github_token

### crawl
- `POST /api/crawl` 手动触发一次爬取，返回本次历史 id
- `GET /api/crawl/history?page=1&page_size=20` 返回爬取历史

### stats
- `GET /api/stats` 返回 `{skills, agents, portable, risky}`

### 其他
- `GET /` 健康检查，返回 `{"status":"ok"}`

## 爬虫逻辑

调用 GitHub Code Search API 搜索 `SKILL.md` 文件（`filename:SKILL` 与 `filename:skill` 各搜一遍，每页 100 条，最多 5 页），按 `min_stars` 过滤仓库，拉取 raw 内容解析 YAML frontmatter，提取 usage_tutorial，写入数据库。已存在的 skill 只更新 stars，不覆盖手动编辑的 compatibility。每次爬取记录到 `crawl_history`。

`auto_mode=1` 时由 APScheduler 按 `interval_hours` 自动调度爬取；`PUT /api/config` 变更后自动重新调度。
