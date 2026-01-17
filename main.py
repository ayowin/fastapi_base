import uvicorn
import sys
import logging
from util.LogUtil import LogUtil
from fastapi_offline import FastAPIOffline
from middleware.LogMiddleware import LogMiddleware
from controller.UserController import router as userControllerRouter
from controller.TestController import router as testControllerRouter

app = FastAPIOffline()

# 添加日志中间件（过滤器）
app.add_middleware(LogMiddleware)

app.include_router(userControllerRouter, prefix="/user")
app.include_router(testControllerRouter, prefix="/test")

@app.get("/")
def index():
    content = {"content": "Welcome to access our fastapi service!"}
    return content

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
