# -*- coding: utf-8 -*-
"""
日志系统模块
提供统一的日志记录功能，支持按日期命名的日志文件
"""

import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler


class Logger:
    """
    日志管理器
    """
    
    def __init__(self, name="vx_tool", log_dir="logs", log_level=logging.INFO):
        """
        初始化日志器
        
        Args:
            name: 日志器名称
            log_dir: 日志文件目录
            log_level: 日志级别
        """
        self.name = name
        self.log_dir = log_dir
        self.log_level = log_level
        
        # 确保日志目录存在
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        # 创建日志器
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)
        
        # 避免重复添加处理器
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """
        设置日志处理器
        """
        # 创建格式器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        
        # 文件处理器 - 按日期命名
        today = datetime.now().strftime('%Y-%m-%d')
        log_file = os.path.join(self.log_dir, f"{today}.txt")
        
        file_handler = RotatingFileHandler(
            log_file, 
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(self.log_level)
        file_handler.setFormatter(formatter)
        
        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        console_handler.setFormatter(formatter)
        
        # 添加处理器
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def get_logger(self):
        """
        获取日志器实例
        
        Returns:
            logging.Logger: 日志器实例
        """
        return self.logger
    
    def info(self, message):
        """记录信息日志"""
        self.logger.info(message)
    
    def error(self, message):
        """记录错误日志"""
        self.logger.error(message)
    
    def warning(self, message):
        """记录警告日志"""
        self.logger.warning(message)
    
    def debug(self, message):
        """记录调试日志"""
        self.logger.debug(message)
    
    def exception(self, message):
        """记录异常日志"""
        self.logger.exception(message)


# 全局日志器实例
_global_logger = None


def get_logger(name="vx_tool", log_dir="logs", log_level=logging.INFO):
    """
    获取全局日志器实例
    
    Args:
        name: 日志器名称
        log_dir: 日志文件目录
        log_level: 日志级别
    
    Returns:
        Logger: 日志器实例
    """
    global _global_logger
    if _global_logger is None:
        _global_logger = Logger(name, log_dir, log_level)
    return _global_logger


def cleanup_old_logs(log_dir="logs", keep_days=30):
    """
    清理旧的日志文件
    
    Args:
        log_dir: 日志目录
        keep_days: 保留天数
    """
    if not os.path.exists(log_dir):
        return
    
    import time
    current_time = time.time()
    
    for filename in os.listdir(log_dir):
        if filename.endswith('.txt'):
            file_path = os.path.join(log_dir, filename)
            file_time = os.path.getctime(file_path)
            
            # 如果文件超过保留天数，则删除
            if (current_time - file_time) > (keep_days * 24 * 3600):
                try:
                    os.remove(file_path)
                    print(f"已删除旧日志文件: {filename}")
                except Exception as e:
                    print(f"删除日志文件失败 {filename}: {e}")