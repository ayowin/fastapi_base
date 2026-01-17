import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

class LogUtil:
    _logger = None
    _log_dir = "logs"  # 默认日志目录
    _max_bytes = 10 * 1024 * 1024  # 最大文件大小：10MB
    _backup_count = 10  # 保留备份文件数量
    
    @staticmethod
    def setDir(log_dir, max_bytes=None, backup_count=None):
        """
        设置日志文件的路径和大小限制
        :param log_dir: 日志文件目录
        :param max_bytes: 单个日志文件最大字节数，默认10MB
        :param backup_count: 保留的备份文件数量，默认5个
        """
        LogUtil._log_dir = log_dir
        
        if max_bytes is not None:
            LogUtil._max_bytes = max_bytes
        if backup_count is not None:
            LogUtil._backup_count = backup_count
            
        os.makedirs(log_dir, exist_ok=True)
        
        # 配置日志记录器
        logger = logging.getLogger("FastAPILogger")
        logger.setLevel(logging.DEBUG)
        
        # 清除之前的处理器，避免重复日志
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)
        
        # 创建轮转文件处理器
        log_file = os.path.join(log_dir, f"log_{datetime.now().strftime('%Y%m%d')}.log")
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=LogUtil._max_bytes, 
            backupCount=LogUtil._backup_count,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        
        # 创建控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        
        # 定义日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)
        
        # 添加处理器到日志记录器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        LogUtil._logger = logger
    
    @staticmethod
    def debug(message):
        """
        记录调试信息
        :param message: 调试信息内容
        """
        if LogUtil._logger is None:
            LogUtil._initialize_logger()
        LogUtil._logger.debug(message)
    
    @staticmethod
    def info(message):
        """
        记录普通信息
        :param message: 普通信息内容
        """
        if LogUtil._logger is None:
            LogUtil._initialize_logger()
        LogUtil._logger.info(message)
    
    @staticmethod
    def error(message):
        """
        记录错误信息
        :param message: 错误信息内容
        """
        if LogUtil._logger is None:
            LogUtil._initialize_logger()
        LogUtil._logger.error(message)
    
    @staticmethod
    def fatal(message):
        """
        记录致命错误信息
        :param message: 致命错误信息内容
        """
        if LogUtil._logger is None:
            LogUtil._initialize_logger()
        # 在Python logging中，fatal是error级别的别名
        LogUtil._logger.fatal(message)
    
    @staticmethod
    def _initialize_logger():
        """
        初始化日志记录器
        """
        # 确保日志目录存在
        os.makedirs(LogUtil._log_dir, exist_ok=True)
        LogUtil.setDir(LogUtil._log_dir)
