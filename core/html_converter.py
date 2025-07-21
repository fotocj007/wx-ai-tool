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
        将Markdown转换为带有内联CSS样式的HTML
        
        Args:
            md_content: Markdown内容
            title: 文章标题（仅用于日志记录）
            template_name: 指定样式模板名称，如果为None则随机选择
        
        Returns:
            str: 转换后的HTML内容，失败返回None
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
            
            # 4. 添加整体容器样式
            styled_html = self._wrap_with_template_container(str(soup), selected_template['container'], template_name)
            
            self.logger.info(f"Markdown转HTML完成，使用模板: {selected_template['name']}")
            return styled_html
            
        except Exception as e:
            self.logger.error(f"Markdown转HTML失败: {e}")
            return None
    
    def _apply_template_styles(self, soup: BeautifulSoup, style_map: dict):
        """
        应用模板样式
        
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
    
    def _wrap_with_template_container(self, html_content: str, container_style: str, template_name: str = None) -> str:
        """
        用模板容器包装HTML内容
        
        Args:
            html_content: HTML内容
            container_style: 容器样式
            template_name: 模板名称，用于决定是否添加特殊样式
        
        Returns:
            str: 包装后的HTML
        """
        css_styles = ""
        
        # 根据模板类型添加相应的CSS样式
        if template_name == 'svg_animation':
            # 只为SVG动画主题添加动画样式
            css_styles = """
            <style>
            @keyframes pulse {
                0% { transform: scale(1); }
                50% { transform: scale(1.05); }
                100% { transform: scale(1); }
            }
            @keyframes slideInLeft {
                0% { transform: translateX(-100%); opacity: 0; }
                100% { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideInRight {
                0% { transform: translateX(100%); opacity: 0; }
                100% { transform: translateX(0); opacity: 1; }
            }
            @keyframes fadeInUp {
                0% { transform: translateY(30px); opacity: 0; }
                100% { transform: translateY(0); opacity: 1; }
            }
            @keyframes fadeInLeft {
                0% { transform: translateX(-30px); opacity: 0; }
                100% { transform: translateX(0); opacity: 1; }
            }
            @keyframes fadeIn {
                0% { opacity: 0; }
                100% { opacity: 1; }
            }
            @keyframes bounceIn {
                0% { transform: scale(0.3); opacity: 0; }
                50% { transform: scale(1.05); }
                70% { transform: scale(0.9); }
                100% { transform: scale(1); opacity: 1; }
            }
            @keyframes flash {
                0%, 50%, 100% { opacity: 1; }
                25%, 75% { opacity: 0.5; }
            }
            @keyframes zoomIn {
                0% { transform: scale(0.5); opacity: 0; }
                100% { transform: scale(1); opacity: 1; }
            }
            @keyframes rotateIn {
                0% { transform: rotate(-200deg); opacity: 0; }
                100% { transform: rotate(0); opacity: 1; }
            }
            @keyframes rainbow {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }
            @keyframes glow {
                0% { text-shadow: 0 0 5px rgba(254, 202, 87, 0.5); }
                100% { text-shadow: 0 0 20px rgba(254, 202, 87, 0.8), 0 0 30px rgba(254, 202, 87, 0.6); }
            }
            </style>
            """
        elif template_name == 'numbered_sequence':
            # 只为数字序列主题添加数字样式
            css_styles = """
            <style>
            /* 数字序列样式 */
            h2::before {
                content: counter(section);
                position: absolute;
                left: 20px;
                top: 50%;
                transform: translateY(-50%);
                width: 35px;
                height: 35px;
                background: linear-gradient(45deg, #667eea, #764ba2);
                color: white;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 18px;
                box-shadow: 0 3px 10px rgba(0, 0, 0, 0.2);
            }
            
            h3::before {
                content: counter(section) "." counter(subsection);
                position: absolute;
                left: 15px;
                top: 50%;
                transform: translateY(-50%);
                width: 30px;
                height: 30px;
                background: linear-gradient(45deg, #f5576c, #f093fb);
                color: white;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 14px;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
            }
            
            h4::before {
                content: counter(section) "." counter(subsection) "." counter(subsubsection);
                position: absolute;
                left: 10px;
                top: 50%;
                transform: translateY(-50%);
                width: 25px;
                height: 25px;
                background: linear-gradient(45deg, #f093fb, #667eea);
                color: white;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                font-size: 12px;
                box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
            }
            
            /* 重置子计数器 */
            h2 {
                counter-reset: subsection;
            }
            h3 {
                counter-reset: subsubsection;
            }
            </style>
            """
        
        wrapped_html = f'{css_styles}<div style="{container_style}">{html_content}</div>'
        return wrapped_html
    
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