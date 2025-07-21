# -*- coding: utf-8 -*-
"""
工具函数模块
提供各种通用的工具函数
"""

import re
from typing import Optional


def clean_markdown_content(content: str) -> str:
    """
    清理markdown内容中的多余字符
    
    主要功能：
    1. 去除开头的 ```markdown 标记
    2. 去除结尾的 ``` 标记
    3. 去除首尾多余的空白字符
    
    Args:
        content (str): 原始markdown内容
        
    Returns:
        str: 清理后的markdown内容
    """
    if not content:
        return content
    
    # 去除首尾空白字符
    cleaned_content = content.strip()
    
    # 去除开头的 ```markdown 标记（不区分大小写）
    if cleaned_content.lower().startswith('```markdown'):
        cleaned_content = cleaned_content[11:].strip()
    elif cleaned_content.startswith('```'):
        # 处理其他类型的代码块标记
        first_newline = cleaned_content.find('\n')
        if first_newline != -1:
            cleaned_content = cleaned_content[first_newline + 1:].strip()
    
    # 去除结尾的 ``` 标记
    if cleaned_content.endswith('```'):
        cleaned_content = cleaned_content[:-3].strip()
    
    return cleaned_content


def validate_markdown_content(content: str) -> bool:
    """
    验证markdown内容是否有效
    
    Args:
        content (str): markdown内容
        
    Returns:
        bool: 内容是否有效
    """
    if not content or not content.strip():
        return False
    
    # 检查是否还有未清理的代码块标记
    cleaned = content.strip()
    if cleaned.startswith('```') or cleaned.endswith('```'):
        return False
    
    return True


def extract_title_from_markdown(content: str) -> Optional[str]:
    """
    从markdown内容中提取第一个标题
    
    Args:
        content (str): markdown内容
        
    Returns:
        Optional[str]: 提取的标题，如果没有找到则返回None
    """
    if not content:
        return None
    
    # 查找第一个标题（# 开头的行）
    lines = content.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            # 去除 # 符号和空格，返回标题文本
            title = re.sub(r'^#+\s*', '', line).strip()
            if title:
                return title
    
    return None