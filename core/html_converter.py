# -*- coding: utf-8 -*-
"""
HTML转换模块
负责将Markdown转换为带有内联CSS样式的HTML，适配微信公众号
"""

import markdown
from bs4 import BeautifulSoup
import os
from typing import Optional
from core.logger import get_logger


class HTMLConverter:
    """
    HTML转换器
    """
    
    def __init__(self):
        """
        初始化HTML转换器
        """
        self.logger = get_logger()
        self.style_map = self._get_style_map()
    
    def _get_style_map(self) -> dict:
        """
        获取样式映射表
        
        Returns:
            dict: 样式映射表
        """
        return {
            'h1': 'font-size: 24px; font-weight: bold; color: #333; margin: 30px 0 20px; padding-bottom: 8px; border-bottom: 3px solid #007bff; text-align: center;',
            'h2': 'font-size: 20px; font-weight: bold; color: #333; margin: 25px 0 15px; padding-bottom: 5px; border-bottom: 2px solid #007bff;',
            'h3': 'font-size: 18px; font-weight: bold; color: #444; margin: 20px 0 10px; padding-left: 10px; border-left: 4px solid #007bff;',
            'h4': 'font-size: 16px; font-weight: bold; color: #555; margin: 15px 0 8px;',
            'p': 'font-size: 16px; color: #555; line-height: 1.8; margin-bottom: 15px; text-align: justify; text-indent: 2em;',
            'strong': 'color: #d9534f; font-weight: bold;',
            'em': 'color: #5bc0de; font-style: italic;',
            'ul': 'padding-left: 20px; margin: 15px 0;',
            'ol': 'padding-left: 20px; margin: 15px 0;',
            'li': 'margin-bottom: 8px; line-height: 1.6;',
            'blockquote': 'border-left: 4px solid #ccc; padding-left: 15px; color: #777; font-style: italic; margin: 15px 0; background-color: #f9f9f9; padding: 10px 15px;',
            'code': 'background-color: #f4f4f4; padding: 2px 4px; border-radius: 3px; font-family: Consolas, Monaco, monospace; color: #c7254e;',
            'pre': 'background-color: #f8f8f8; padding: 15px; border-radius: 5px; border: 1px solid #e1e1e8; overflow-x: auto; margin: 15px 0;',
            'a': 'color: #007bff; text-decoration: none;',
            'img': 'max-width: 100%; height: auto; display: block; margin: 15px auto;',
            'table': 'border-collapse: collapse; width: 100%; margin: 15px 0;',
            'th': 'border: 1px solid #ddd; padding: 8px; background-color: #f2f2f2; font-weight: bold; text-align: center;',
            'td': 'border: 1px solid #ddd; padding: 8px; text-align: left;',
            'hr': 'border: none; height: 1px; background-color: #ddd; margin: 20px 0;'
        }
    
    def markdown_to_styled_html(self, md_content: str, title: str = "") -> Optional[str]:
        """
        将Markdown转换为带有内联CSS样式的HTML
        
        Args:
            md_content: Markdown内容
            title: 文章标题（仅用于日志记录）
        
        Returns:
            str: 转换后的HTML内容，失败返回None
        """
        try:
            self.logger.info("开始转换Markdown到HTML")
            
            # 1. Markdown转为基础HTML
            html = markdown.markdown(
                md_content,
                extensions=['extra', 'codehilite', 'toc'],
                extension_configs={
                    'codehilite': {
                        'css_class': 'highlight',
                        'use_pygments': False
                    }
                }
            )
            
            # 2. 使用BeautifulSoup解析HTML并注入样式
            soup = BeautifulSoup(html, 'html.parser')
            
            # 3. 应用样式
            self._apply_styles(soup)
            
            # 4. 添加整体容器样式
            styled_html = self._wrap_with_container(str(soup))
            
            self.logger.info("Markdown转HTML完成")
            return styled_html
            
        except Exception as e:
            self.logger.error(f"Markdown转HTML失败: {e}")
            return None
    
    def _apply_styles(self, soup: BeautifulSoup):
        """
        应用内联样式
        
        Args:
            soup: BeautifulSoup对象
        """
        for tag_name, style in self.style_map.items():
            for tag in soup.find_all(tag_name):
                # 保留原有的style属性，如果有的话
                existing_style = tag.get('style', '')
                if existing_style:
                    tag['style'] = f"{existing_style}; {style}"
                else:
                    tag['style'] = style
    
    def _wrap_with_container(self, html_content: str) -> str:
        """
        用容器包装HTML内容
        
        Args:
            html_content: HTML内容
        
        Returns:
            str: 包装后的HTML
        """
        container_style = (
            "max-width: 100%; "
            "margin: 0 auto; "
            "padding: 20px; "
            "font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif; "
            "background-color: #ffffff; "
            "color: #333333; "
            "line-height: 1.6;"
        )
        
        wrapped_html = f'<div style="{container_style}">{html_content}</div>'
        return wrapped_html
    

    
    def _create_full_html_document(self, body_content: str, title: str) -> str:
        """
        创建完整的HTML文档
        
        Args:
            body_content: 正文内容
            title: 文档标题
        
        Returns:
            str: 完整的HTML文档
        """
        html_template = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
        }}
    </style>
</head>
<body>
    {body_content}
</body>
</html>
"""
        return html_template
    

    
    def extract_digest(self, html_content: str, max_length: int = 120) -> str:
        """
        从HTML内容中提取摘要
        
        Args:
            html_content: HTML内容
            max_length: 最大长度
        
        Returns:
            str: 摘要文本
        """
        try:
            # 解析HTML
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 提取纯文本
            text = soup.get_text()
            
            # 清理文本
            text = ' '.join(text.split())
            
            # 截取指定长度
            if len(text) > max_length:
                text = text[:max_length] + "..."
            
            return text
            
        except Exception as e:
            self.logger.error(f"提取摘要失败: {e}")
            return "精彩内容，敬请阅读..."


# 全局HTML转换器实例
_global_html_converter = None


def get_html_converter() -> HTMLConverter:
    """
    获取全局HTML转换器实例
    
    Returns:
        HTMLConverter: HTML转换器实例
    """
    global _global_html_converter
    if _global_html_converter is None:
        _global_html_converter = HTMLConverter()
    return _global_html_converter