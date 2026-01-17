import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from util.LogUtil import LogUtil

class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        
        # 记录详细的请求信息
        client_host = request.client.host if request.client else "unknown"
        client_port = request.client.port if request.client else "unknown"
        LogUtil.info(f"[{client_host}:{client_port}] 收到请求: {request.method} {request.url}")
        LogUtil.debug(f"请求头: {dict(request.headers)}")
        
        try:
            response = await call_next(request)
        except Exception as e:
            # 记录异常
            process_time = time.time() - start_time
            LogUtil.error(f"请求处理异常: {str(e)}, 处理时间: {process_time:.4f}s")
            raise e
        else:
            # 计算处理时间
            process_time = time.time() - start_time
            
            # 记录响应信息
            LogUtil.info(f"响应状态: {response.status_code}, 处理时间: {process_time:.4f}s")
        
        return response