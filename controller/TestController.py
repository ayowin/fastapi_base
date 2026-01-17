from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from redis import connection
from db.RedisManager import getRedisConnection, redisManager
from util.LogUtil import LogUtil

router = APIRouter()

@router.get("/")
def index():
    return {"message": "test module"}   

@router.get("/set")
def set(connection = Depends(getRedisConnection)):
    # 获取redis连接（依赖注入的方式）
    result = connection.set("test", "test")
    LogUtil.info(jsonable_encoder(result))
    return result

@router.get("/get")
def get():
    # 获取redis连接（主动创建的方式）
    connection = None
    try:
        connection = redisManager.getConnection()
        result = connection.get("test")
        LogUtil.info(jsonable_encoder(result))
        return result
    finally:
        if connection:
            redisManager.closeConnection(connection)

@router.get("/delete")
def delete(connection = Depends(getRedisConnection)):
    # 获取redis连接（依赖注入的方式）
    result = connection.delete("test")
    LogUtil.info(jsonable_encoder(result))
    return result