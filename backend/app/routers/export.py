"""静态 JSON 导出路由：GET /api/export?target=路径（本地工具用）。

部署到 GitHub Pages 前把数据库导出成静态 JSON；CI 里通常直接用 CLI
``python -m backend.app.exporter``，本路由主要供本地调试使用。
"""
from typing import Optional

from fastapi import APIRouter, HTTPException, Query

from ..exporter import export_static

router = APIRouter(prefix="/export", tags=["export"])


@router.get("")
def export_data(target: Optional[str] = Query(None, description="导出目标目录")):
    """把数据库导出成静态 JSON 到 target 目录，返回各生成文件路径。"""
    if not target:
        raise HTTPException(status_code=400, detail="target 参数必填")
    written = export_static(target)
    return {"status": "ok", "files": written}
