# -*- coding: utf-8 -*-
"""
HTML转换模块
负责将Markdown转换为带有内联CSS样式的HTML，适配微信公众号
"""

import markdown
from bs4 import BeautifulSoup
import os
import random
from typing import Optional
from core.logger import get_logger
from core.template_manager import TemplateManager


class HTMLConverter:
    """
    HTML转换器
    """
    
    def __init__(self):
        """
        初始化HTML转换器
        """
        self.logger = get_logger()
        self.template_manager = TemplateManager()
        self.style_templates = self.template_manager.get_style_templates()
    

    
    def markdown_to_styled_html(self, md_content: str, title: str = "", template_name: str = None) -> Optional[str]:
        """
        将Markdown转换为带有内联CSS样式的完整HTML文档
        
        Args:
            md_content: Markdown内容
            title: 文章标题（用于HTML title标签）
            template_name: 指定样式模板名称，如果为None则随机选择
        
        Returns:
            str: 转换后的完整HTML文档内容，失败返回None
        """
        try:
            # 选择样式模板
            if template_name and template_name in self.style_templates:
                selected_template = self.style_templates[template_name]
            else:
                # 随机选择一个模板
                template_name = random.choice(list(self.style_templates.keys()))
                selected_template = self.style_templates[template_name]
            
            self.logger.info(f"开始转换Markdown到HTML，使用样式模板: {selected_template['name']}")
            
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
            
            # 3. 应用选定模板的样式
            self._apply_template_styles(soup, selected_template['styles'])
            
            # 4. 构建完整的HTML文档
            complete_html = self._build_complete_html_document(str(soup), selected_template, title, template_name)
            
            self.logger.info(f"Markdown转HTML完成，使用模板: {selected_template['name']}")
            return complete_html
            
        except Exception as e:
            self.logger.error(f"Markdown转HTML失败: {e}")
            return None
    
    def _apply_template_styles(self, soup: BeautifulSoup, style_map: dict):
        """
        应用模板样式到HTML元素
        
        Args:
            soup: BeautifulSoup对象
            style_map: 样式映射表
        """
        for tag_name, style in style_map.items():
            for tag in soup.find_all(tag_name):
                # 保留原有的style属性，如果有的话
                existing_style = tag.get('style', '')
                if existing_style:
                    tag['style'] = f"{existing_style}; {style}"
                else:
                    tag['style'] = style
    
    def _build_complete_html_document(self, html_content: str, selected_template: dict, title: str = "", template_name: str = None) -> str:
        """
        构建完整的HTML文档，参考t1.html的结构
        
        Args:
            html_content: 转换后的HTML内容
            selected_template: 选定的样式模板
            title: 文档标题
            template_name: 模板名称，用于决定是否添加特殊样式
        
        Returns:
            str: 完整的HTML文档
        """
        # 获取容器样式
        container_style = selected_template['container']
        
        # 为数字序列主题添加特殊的数字标记样式
        if template_name == 'numbered_sequence':
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # 为h2标签添加数字序列的特殊样式
            for i, h2 in enumerate(soup.find_all('h2'), 1):
                existing_style = h2.get('style', '')
                number_style = "position: relative; padding-left: 70px;"
                if existing_style:
                    h2['style'] = f"{existing_style}; {number_style}"
                else:
                    h2['style'] = number_style
                    
                # 添加数字元素
                number_span = soup.new_tag('span')
                number_span.string = str(i)
                number_span['style'] = "position: absolute; left: 20px; top: 50%; transform: translateY(-50%); width: 35px; height: 35px; background: linear-gradient(45deg, #667eea, #764ba2); color: white; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 18px; box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);"
                h2.insert(0, number_span)
            
            html_content = str(soup)
        
        # 构建完整的HTML文档结构，参考t1.html的格式
        complete_html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<body>
  <section style="{container_style}">
    {html_content}
  </section>
</body>
</html>"""
        
        return complete_html
    
    def get_available_templates(self) -> list:
        """
        获取可用的样式模板列表
        
        Returns:
            list: 包含模板信息的列表，每个元素包含name和description字段
        """
        return self.template_manager.get_available_templates()
    
    def get_template_preview(self, template_name: str) -> Optional[str]:
        """
        获取指定模板的预览信息
        
        Args:
            template_name: 模板名称
        
        Returns:
            str: 模板描述，如果模板不存在返回None
        """
        return self.template_manager.get_template_preview(template_name)
    
    def extract_digest(self, html_content: str, max_length: int = 120) -> str:
        """
        从HTML内容中提取摘要
        
        Args:
            html_content: HTML内容（可以是完整文档或片段）
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