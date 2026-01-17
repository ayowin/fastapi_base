# FastAPI Base 后端框架

这是一个基于 FastAPI 构建的基础后端框架，集成了 MySQL 和 Redis 数据库支持，提供了完整的数据库操作和缓存功能。

## 项目结构

```
fastapi_base/
├── controller/           # 控制器层，处理HTTP请求
│   ├── TestController.py   # 测试模块控制器
│   └── UserController.py   # 用户模块控制器
├── db/                   # 数据库管理模块
│   ├── MysqlManager.py     # MySQL数据库管理器
│   └── RedisManager.py     # Redis数据库管理器
├── model/                # 数据模型层
│   └── User.py             # 用户数据模型
├── middleware/           # 中间件模块
│   └── LogMiddleware.py    # 日志中间件
├── util/                 # 工具类模块
│   └── LogUtil.py          # 日志工具类
├── clean.py             # 项目清理脚本
├── fastapi_base.sql      # MySQL数据库初始化脚本
├── main.py              # 应用入口文件
└── README.md            # 项目说明文档
```

## 功能特性

- **基于 FastAPI**：现代化、高性能的 Python Web 框架
- **离线 Swagger UI**：使用 `fastapi-offline` 提供离线 API 文档
- **MySQL 支持**：集成 SQLAlchemy ORM，提供用户数据模型
- **Redis 支持**：集成 Redis 缓存，提供键值对存储功能
- **日志管理**：提供统一的日志工具类和日志中间件，支持多种日志级别
- **依赖注入**：使用 FastAPI 的依赖注入系统管理数据库连接
- **中间件支持**：内置日志记录中间件，自动记录请求和响应信息
- **清理工具**：提供清理脚本，可删除缓存文件和日志目录
- **RESTful API**：遵循 RESTful 设计原则

## 技术栈

- **Python**: 3.x
- **FastAPI**: Web 框架
- **SQLAlchemy**: ORM 框架
- **MySQL**: 关系型数据库
- **PyMySQL**: MySQL 连接驱动
- **Redis**: 缓存数据库
- **FastAPI-Offline**: 离线 API 文档

## 安装与运行

### 1. 环境准备

确保已安装 Python 3.x 和以下依赖包：

```bash
pip install fastapi
pip install fastapi-offline
pip install uvicorn
pip install sqlalchemy
pip install pymysql
pip install redis
```

### 2. 数据库配置

#### MySQL 配置
编辑 `db/MysqlManager.py` 文件中的数据库连接参数：
```python
self.DB_HOST = "localhost"        # 数据库主机
self.DB_PORT = "3306"             # 数据库端口
self.DB_NAME = "fastapi_base"     # 数据库名
self.DB_USER = "root"             # 用户名
self.DB_PASSWORD = "123456"       # 密码
```

#### Redis 配置
编辑 `db/RedisManager.py` 文件中的 Redis 连接参数：
```python
self.REDIS_HOST = "localhost"     # Redis 主机
self.REDIS_PORT = 6379            # Redis 端口
self.REDIS_DB = 0                 # Redis 数据库编号
self.REDIS_PASSWORD = None        # Redis 密码
```

### 3. 初始化数据库

执行 `fastapi_base.sql` 脚本创建数据库和表结构，或者手动创建 fastapi_base 数据库及 user 表。

### 4. 启动应用

方式一：直接运行Python文件
```bash
python main.py
```

方式二：使用uvicorn命令（推荐用于开发）
```bash
uvicorn main:app --reload
```

方式三：指定主机和端口
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

服务器将在 `http://0.0.0.0:8000` 上启动。

> **注意**：`--reload` 参数启用热重载功能，在代码更改时自动重启服务器，适合开发阶段使用。生产环境应省略此参数。


## API 接口

### 文档访问
`http://0.0.0.0:8000/docs` - 访问 Swagger UI 交互式 API 文档  
`http://0.0.0.0:8000/redoc` - 访问 ReDoc API 文档  

### 根路径
- `GET /` - 返回欢迎信息

### 用户模块 (User Module)
- `GET /user/` - 返回用户模块信息
- `GET /user/{user_id}` - 根据ID获取用户信息
- `GET /user/users` - 获取所有用户列表

### 测试模块 (Test Module)
- `GET /test/` - 返回测试模块信息
- `GET /test/set` - 在Redis中设置测试键值对
- `GET /test/get` - 从Redis中获取测试键值对
- `GET /test/delete` - 从Redis中删除测试键值对

## 代码示例

### MySQL 数据库操作
```python
# 通过依赖注入获取数据库会话
@router.get("/{user_id}")
def getUserById(user_id: int, session = Depends(getMysqlSession)):
    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# 主动创建数据库会话
@router.get("/users")
def getUsers():
    session = mysqlManager.getSession()
    try:
        users = session.query(User).all()
        return users
    finally:
        mysqlManager.closeSession(session)
```

### Redis 数据库操作

```python
# 通过依赖注入获取Redis连接
@router.get("/set")
def set(connection = Depends(getRedisConnection)):
    result = connection.set("test", "test")
    return result

# 主动创建Redis连接
@router.get("/get")
def get():
    try:
        connection = redisManager.getConnection()
        result = connection.get("test")
        return result
    finally:
        redisManager.closeConnection(connection)
```

### 日志工具类使用

日志工具类 `LogUtil`，位于 `util/LogUtil.py`，支持多种日志级别和自定义日志文件路径。
#### 1.默认日志路径
```python
from util.LogUtil import LogUtil

# 使用默认日志目录 "logs"
LogUtil.info("这是一条信息日志")
LogUtil.debug("这是一条调试日志")
LogUtil.error("这是一条错误日志")
LogUtil.fatal("这是一条致命错误日志")
```

#### 2.自定义日志路径

```python
from util.LogUtil import LogUtil

# 设置自定义日志目录
LogUtil.setDir("./my_logs")
LogUtil.info("这会保存到自定义的日志目录")
```

日志文件将以日期命名（例如 `log_yyyymmdd.log`）保存在指定目录中，并同时输出到控制台。

### 日志中间件

日志中间件 `LogMiddleware`，位于 `middleware/LogMiddleware.py`，自动记录每个请求的详细信息，包括客户端IP、请求方法、URL、请求头、响应状态码和处理时间。

中间件会在以下时机记录日志：
- 收到请求时记录请求信息
- 请求处理完成后记录响应状态和处理时间
- 请求处理异常时记录错误信息

使用中间件无需额外配置，已在主应用中注册。

## 项目优势

1. **模块化设计**：采用分层架构，控制器、数据库管理器、模型分离
2. **灵活的数据库访问**：同时支持依赖注入和主动创建两种数据库连接方式
3. **完善的资源管理**：自动管理数据库连接的开启和关闭
4. **统一的日志管理**：提供便捷的日志记录工具，便于问题追踪和调试
5. **易于扩展**：可以轻松添加新的控制器和模型

## 清理脚本

项目提供了一个 `clean.py` 脚本，用于清理项目中的缓存文件和日志目录：

```bash
python clean.py
```

该脚本会自动删除项目中所有的 `__pycache__` 目录以及根目录下的 `logs` 目录，帮助保持项目目录的整洁。

## 注意事项

- 修改数据库连接参数时，请确保数据库服务正在运行
- 生产环境部署前请修改默认的数据库用户名和密码
- 使用完数据库会话和连接后，务必调用相应的关闭方法释放资源
- 日志文件会根据日期自动轮转，定期清理旧日志文件以节省磁盘空间
- 定期运行清理脚本以维护项目整洁