from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from db.MysqlManager import getMysqlSession, mysqlManager
from model.User import User as User
from util.LogUtil import LogUtil

router = APIRouter()

@router.get("/")
def index():
    return {"message": "user module"}    

@router.get("/{user_id:int}")
def getUserById(user_id: int, session = Depends(getMysqlSession)):
    # 获取数据库会话（依赖注入的方式）
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    LogUtil.info(jsonable_encoder(user))
    return user

@router.get("/users")
def getUsers():
    # 获取数据库会话（主动创建的方式）
    session = mysqlManager.getSession()
    try:
        users = session.query(User).all()
        LogUtil.info(jsonable_encoder(users))
        return users
    finally:
        mysqlManager.closeSession(session)