from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

class MysqlManager:
    def __init__(self):
        # 数据库连接配置
        self.DB_HOST = "localhost"
        self.DB_PORT = "3306"
        self.DB_NAME = "fastapi_base"
        self.DB_USER = "root"
        self.DB_PASSWORD = "123456"
        
        self.DATABASE_URL = f"mysql+pymysql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        
        # 创建数据库引擎
        self.engine = create_engine(self.DATABASE_URL, echo=True)
        
        # 创建会话
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
    
    def getSession(self) -> Session:
        """获取数据库会话"""
        return self.SessionLocal()
    
    def closeSession(self, session: Session):
        """关闭数据库会话"""
        session.close()


# 创建全局MysqlManager实例
mysqlManager = MysqlManager()

# 依赖注入
def getMysqlSession():
    session = mysqlManager.getSession()
    try:
        yield session
    finally:
        mysqlManager.closeSession(session)