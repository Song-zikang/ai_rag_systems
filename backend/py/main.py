from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import JSONResponse
from py.api.routes import router  # 导入拆分后的路由

# 创建 FastAPI 应用实例
app = FastAPI(title="RAG Intelligent Q&A System", version="1.0")

# 配置跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 全局异常处理器
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    from py.config import logger  # 确保能导入 logger
    logger.error(f"Server error {request.url}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )


# 注册路由（核心：把所有接口挂载到 app 上）
app.include_router(router)

# 启动入口（可选，方便直接运行）
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)