import os
from fastapi import FastAPI
from langserve import add_routes

from api.routers import router
from config.core import settings

# 创建应用
app = FastAPI(
    title="智能知识库助手",
    version="1.0",
    description="基于LangChain构建的RAG知识库系统，支持文档上传与智能问答"
)

# 确保必要目录存在
os.makedirs(settings.upload_folder, exist_ok=True)
os.makedirs(settings.vector_store_path, exist_ok=True)

# --- 方式1：使用 LangServe 挂载 RAG 链（适合 playground 调试）---
# 注意：你需要先创建 chains/rag_chain.py
# try:
#     from chains.rag_chain import get_rag_chain
#     # 挂载 LangServe playground（自动生成 UI）
#     add_routes(
#         app,
#         get_rag_chain(),
#         path="/rag"
#     )
# except Exception as e:
#     print(f"⚠️  RAG 链加载失败: {e}")

# --- 方式2：注册自定义 API 路由（推荐用于正式功能）---
# 更灵活，支持上传、查询等复杂逻辑
try:
    app.include_router(router)
except Exception as e:
    print(f"⚠️  API 路由注册失败: {e}")


# --- 健康检查 ---
@app.get("/health")
def health_check():
    return {"status": "ok", "environment": settings.environment}