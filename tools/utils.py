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


def decompress_html(compressed_content, use_compress=True):
    """
    格式化 HTML 内容，处理压缩和未压缩 HTML，确保输出的内容适合网页渲染。

    参数：
        compressed_content (str): 输入的 HTML 字符串
        use_compress (bool): 是否作为压缩 HTML 处理（True）或直接返回（False）

    返回：
        str: 格式化后的 HTML 字符串
    """
    # 如果 use_compress 为 False 或内容已格式化（有换行和缩进），直接返回
    if not use_compress or re.search(r"\n\s{2,}", compressed_content):
        return compressed_content.strip()

    try:
        # 使用 lxml 解析器处理 HTML，支持不规范的 HTML
        soup = BeautifulSoup(compressed_content, "lxml")

        # 移除多余空白和注释，清理输出
        for element in soup.find_all(text=True):
            if element.strip() == "":
                element.extract()  # 移除空文本节点
            elif element.strip().startswith("<!--") and element.strip().endswith("-->"):
                element.extract()  # 移除注释

        # 判断是否为 HTML 片段（无 DOCTYPE 或 <html> 标签）
        is_fragment = not (
            compressed_content.strip().startswith("<!DOCTYPE")
            or compressed_content.strip().startswith("<html")
        )

        if is_fragment:
            # 对于片段，避免包裹 <html> 或 <body> 标签
            formatted_lines = []
            for child in soup.contents:
                if hasattr(child, "prettify"):
                    formatted_lines.append(child.prettify().strip())
                else:
                    formatted_lines.append(str(child).strip())
            return "\n".join(line for line in formatted_lines if line)

        # 对于完整 HTML 文档，返回格式化输出
        return soup.prettify(formatter="minimal").strip()

    except Exception as e:  # noqa 841
        # 错误处理：解析失败时返回原始内容
        return compressed_content.strip()