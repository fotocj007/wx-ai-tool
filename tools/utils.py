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


def decompress_html(html_content, use_compress=True):
    """
    压缩 HTML 内容，移除多余的空白字符和换行符，解决微信公众号发布时的格式问题。

    参数：
        html_content (str): 输入的 HTML 字符串
        use_compress (bool): 是否压缩 HTML（True）或直接返回（False）

    返回：
        str: 压缩后的 HTML 字符串
    """
    if not html_content or not use_compress:
        return html_content
    
    try:
        # 移除HTML注释
        html_content = re.sub(r'<!--.*?-->', '', html_content, flags=re.DOTALL)
        
        # 压缩HTML：移除标签间的换行和多余空格
        # 但保留标签内的文本内容的空格
        compressed = re.sub(r'>\s+<', '><', html_content)
        
        # 移除行首行尾的空白字符
        compressed = re.sub(r'^\s+|\s+$', '', compressed, flags=re.MULTILINE)
        
        # 将多个连续的空白字符（包括换行符）压缩为单个空格
        # 但要小心处理，不要影响pre标签内的内容
        compressed = re.sub(r'\s+', ' ', compressed)
        
        # 移除标签前后的空格（但保留标签内文本的空格）
        compressed = re.sub(r'\s*<\s*', '<', compressed)
        compressed = re.sub(r'\s*>\s*', '>', compressed)
        
        return compressed.strip()
        
    except Exception as e:
        # 错误处理：压缩失败时返回原始内容
        print(f"HTML压缩失败: {e}")
        return html_content.strip()