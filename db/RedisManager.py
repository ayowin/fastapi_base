import redis
from typing import Optional, Any

class RedisManager:
    def __init__(self):
        # Redis连接配置
        self.REDIS_HOST = "localhost"
        self.REDIS_PORT = 6379
        self.REDIS_DB = 0
        self.REDIS_PASSWORD = None
        self.REDIS_DECODE_RESPONSES = True
        
    def getConnection(self):
        """获取Redis连接"""
        return redis.Redis(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            db=self.REDIS_DB,
            password=self.REDIS_PASSWORD,
            decode_responses=self.REDIS_DECODE_RESPONSES
        )
    
    def closeConnection(self, connection):
        """关闭Redis连接"""
        try:
            connection.quit()
        except:
            # quit命令可能在某些操作后不可用，所以捕获异常并忽略
            pass

# 创建全局RedisManager实例
redisManager = RedisManager()

# 依赖注入
def getRedisConnection():
    connection = redisManager.getConnection()
    try:
        yield connection
    finally:
        redisManager.closeConnection(connection)