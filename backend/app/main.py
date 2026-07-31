"""FastAPI 应用入口：CORS、路由注册、启动时建表+导入种子+启动调度器。"""
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import scheduler
from .database import init_db
from .seed import seed
from .routers import agents, config, crawl, skills, stats, export

logger = logging.getLogger("agent-skills-matrix")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期：启动时建表+导入种子+启动调度器，退出时关闭调度器。"""
    init_db()
    seed()
    scheduler.start_scheduler()
    logger.info("应用启动完成")
    yield
    scheduler.shutdown_scheduler()
    logger.info("应用已关闭")


app = FastAPI(title="Agent Skills Matrix API", lifespan=lifespan)

# CORS 允许所有源（开发用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册所有 router，前缀 /api
app.include_router(skills.router, prefix="/api")
app.include_router(agents.router, prefix="/api")
app.include_router(config.router, prefix="/api")
app.include_router(crawl.router, prefix="/api")
app.include_router(stats.router, prefix="/api")
app.include_router(export.router, prefix="/api")


@app.get("/")
def root():
    """根路径健康检查。"""
    return {"status": "ok"}
