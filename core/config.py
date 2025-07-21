# -*- coding: utf-8 -*-
"""
配置管理模块
负责读取和管理系统配置信息
"""

import configparser
import os
from typing import Optional


class ConfigManager:
    """
    配置管理器
    """
    
    def __init__(self, config_file: str = "config.ini"):
        """
        初始化配置管理器
        
        Args:
            config_file: 配置文件路径
        """
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self._load_config()
    
    def _load_config(self):
        """
        加载配置文件
        """
        if not os.path.exists(self.config_file):
            raise FileNotFoundError(f"配置文件不存在: {self.config_file}")
        
        try:
            self.config.read(self.config_file, encoding='utf-8')
        except Exception as e:
            raise Exception(f"读取配置文件失败: {e}")
    
    def get(self, section: str, key: str, fallback: Optional[str] = None) -> str:
        """
        获取配置值
        
        Args:
            section: 配置节
            key: 配置键
            fallback: 默认值
        
        Returns:
            str: 配置值
        """
        try:
            return self.config.get(section, key, fallback=fallback)
        except (configparser.NoSectionError, configparser.NoOptionError):
            if fallback is not None:
                return fallback
            raise
    
    def get_int(self, section: str, key: str, fallback: Optional[int] = None) -> int:
        """
        获取整数配置值
        
        Args:
            section: 配置节
            key: 配置键
            fallback: 默认值
        
        Returns:
            int: 配置值
        """
        try:
            return self.config.getint(section, key, fallback=fallback)
        except (configparser.NoSectionError, configparser.NoOptionError):
            if fallback is not None:
                return fallback
            raise
    
    def get_bool(self, section: str, key: str, fallback: Optional[bool] = None) -> bool:
        """
        获取布尔配置值
        
        Args:
            section: 配置节
            key: 配置键
            fallback: 默认值
        
        Returns:
            bool: 配置值
        """
        try:
            return self.config.getboolean(section, key, fallback=fallback)
        except (configparser.NoSectionError, configparser.NoOptionError):
            if fallback is not None:
                return fallback
            raise
    
    def get_gemini_api_key(self) -> str:
        """
        获取Gemini API Key
        
        Returns:
            str: API Key
        """
        return self.get('API', 'gemini_api_key', '')
    
    def get_ai_model(self) -> str:
        """
        获取AI模型选择
        
        Returns:
            str: AI模型 (gemini 或 qwen)
        """
        return self.get('API', 'ai_model', 'gemini')
    
    def get_qwen_config(self) -> dict:
        """
        获取Qwen配置
        
        Returns:
            dict: Qwen配置信息
        """
        return {
            'model': self.get('API', 'qwen_model', 'qwen-plus'),
            'api_key': self.get('API', 'qwen_api_key', ''),
            'base_url': self.get('API', 'qwen_base_url', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
        }
    
    def get_wechat_config(self) -> dict:
        """
        获取微信配置
        
        Returns:
            dict: 微信配置信息
        """
        return {
            'appid': self.get('WECHAT', 'appid'),
            'appsecret': self.get('WECHAT', 'appsecret'),
            'author': self.get('WECHAT', 'author')
        }
    
    def get_log_level(self) -> str:
        """
        获取日志级别
        
        Returns:
            str: 日志级别
        """
        return self.get('SYSTEM', 'log_level', 'INFO')
    
    def get_max_log_files(self) -> int:
        """
        获取最大日志文件数
        
        Returns:
            int: 最大日志文件数
        """
        return self.get_int('SYSTEM', 'max_log_files', 30)


# 全局配置管理器实例
_global_config = None


def get_config(config_file: str = "config.ini") -> ConfigManager:
    """
    获取全局配置管理器实例
    
    Args:
        config_file: 配置文件路径
    
    Returns:
        ConfigManager: 配置管理器实例
    """
    global _global_config
    if _global_config is None:
        _global_config = ConfigManager(config_file)
    return _global_config