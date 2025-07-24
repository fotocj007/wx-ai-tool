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
            
            # 3. 特殊处理bash代码块
            self._process_code_blocks(soup)
            
            # 4. 应用选定模板的样式
            self._apply_template_styles(soup, selected_template['styles'])
            
            # 5. 构建完整的HTML文档
            complete_html = self._build_complete_html_document(str(soup), selected_template, title, template_name)
            
            self.logger.info(f"Markdown转HTML完成，使用模板: {selected_template['name']}")
            return complete_html
            
        except Exception as e:
            self.logger.error(f"Markdown转HTML失败: {e}")
            return None
    
    def _process_code_blocks(self, soup: BeautifulSoup):
        """
        特殊处理所有代码块，为其添加统一的'code'样式和功能
        
        Args:
            soup: BeautifulSoup对象
        """
        try:
            # 查找所有的代码块
            code_blocks = soup.find_all('pre')
            
            for pre_tag in code_blocks:
                code_tag = pre_tag.find('code')
                if code_tag:
                    # 获取代码语言类型
                    code_classes = code_tag.get('class', [])
                    language = 'code'  # 默认语言类型
                    
                    # 尝试从class中提取语言类型
                    for cls in code_classes:
                        if cls.startswith('language-'):
                            language = cls.replace('language-', '')
                            break
                        elif cls in ['python', 'javascript', 'java', 'cpp', 'c', 'bash', 'shell', 'sh', 'html', 'css', 'sql', 'json', 'xml', 'yaml']:
                            language = cls
                            break
                    
                    # 为所有代码块添加统一标识
                    pre_tag['data-language'] = language
                    code_tag['data-language'] = language
                    
                    # 添加统一的CSS类
                    existing_classes = pre_tag.get('class', [])
                    if isinstance(existing_classes, str):
                        existing_classes = [existing_classes]
                    existing_classes.append('unified-code-block')
                    pre_tag['class'] = existing_classes
                    
                    self.logger.debug(f"检测到{language}代码块，已应用统一处理")
                        
        except Exception as e:
            self.logger.error(f"处理代码块时出错: {e}")
    
    def _is_bash_content(self, content: str) -> bool:
        """
        判断代码内容是否为bash脚本
        
        Args:
            content: 代码内容
            
        Returns:
            bool: 是否为bash内容
        """
        bash_indicators = [
            '#!/bin/bash', '#!/bin/sh', 
            'mkdir ', 'cd ', 'ls ', 'pwd', 'chmod ', 'chown ',
            'git clone', 'npm install', 'npm run', 'npm link',
            'echo ', 'cat ', 'grep ', 'find ', 'which ',
            'export ', 'source ', './'
        ]
        
        content_lower = content.lower().strip()
        return any(indicator in content_lower for indicator in bash_indicators)
    
    def _format_bash_code_content(self, code_tag):
        """
        格式化bash代码内容，添加特殊样式
        
        Args:
            code_tag: 代码标签
        """
        try:
            content = code_tag.get_text()
            lines = content.split('\n')
            
            # 保存原始内容作为备份
            original_content = content
            
            # 清空原内容
            code_tag.clear()
            
            # 如果没有内容，直接返回
            if not content.strip():
                code_tag.string = original_content
                return
            
            for i, line in enumerate(lines):
                # 创建行容器
                line_div = code_tag.parent.new_tag('div')
                line_div['class'] = 'bash-line'
                
                # 添加行号
                line_number = code_tag.parent.new_tag('span')
                line_number['class'] = 'line-number'
                line_number.string = f"{i+1:2d}"
                line_div.append(line_number)
                
                # 添加代码内容
                line_content = code_tag.parent.new_tag('span')
                line_content['class'] = 'line-content'
                
                # 处理注释
                if line.strip().startswith('#'):
                    line_content['class'] = 'line-content comment'
                
                # 保持原始行内容，包括空行
                line_content.string = line if line else ' '
                line_div.append(line_content)
                
                code_tag.append(line_div)
                    
        except Exception as e:
            self.logger.error(f"格式化bash代码内容时出错: {e}")
            # 如果格式化失败，恢复原内容
            code_tag.clear()
            code_tag.string = content
    
    def _is_code_related_tag(self, tag):
        """
        判断标签是否与代码块相关
        
        Args:
            tag: BeautifulSoup标签对象
        
        Returns:
            bool: 如果是代码相关标签返回True，否则返回False
        """
        try:
            # 检查标签本身是否是统一代码块
            if tag.name == 'pre' and 'unified-code-block' in tag.get('class', []):
                return True
            
            # 检查标签是否在统一代码块内部
            parent = tag.parent
            while parent:
                if parent.name == 'pre' and 'unified-code-block' in parent.get('class', []):
                    return True
                parent = parent.parent
            
            # 检查是否是代码标题栏
            if 'code-header' in tag.get('class', []):
                return True
                
            return False
            
        except Exception as e:
            self.logger.error(f"判断代码相关标签时出错: {e}")
            return False
    
    def _apply_template_styles(self, soup: BeautifulSoup, style_map: dict):
        """
        应用模板样式到HTML元素
        
        Args:
            soup: BeautifulSoup对象
            style_map: 样式映射表
        """
        for tag_name, style in style_map.items():
            for tag in soup.find_all(tag_name):
                # 跳过代码块相关的标签，避免模板样式覆盖自定义样式
                if self._is_code_related_tag(tag):
                    continue
                    
                # 保留原有的style属性，如果有的话
                existing_style = tag.get('style', '')
                if existing_style:
                    tag['style'] = f"{existing_style}; {style}"
                else:
                    tag['style'] = style
                    
        # 为所有代码块应用特殊样式
        self._apply_code_styles(soup)
    
    def _apply_code_styles(self, soup: BeautifulSoup):
        """
        为所有代码块应用特殊样式
        
        Args:
            soup: BeautifulSoup对象
        """
        try:
            # 查找所有统一代码块
            code_blocks = soup.find_all('pre', class_='unified-code-block')
            
            for pre_tag in code_blocks:
                # 为代码块容器添加特殊样式 - 黑色背景
                code_container_style = (
                    "background: #000000; "
                    "border: 2px solid #333333; "
                    "border-radius: 12px; "
                    "padding: 20px; "
                    "margin: 20px 0; "
                    "box-shadow: 0 8px 25px rgba(0, 0, 0, 0.5); "
                    "position: relative; "
                    "overflow: hidden;"
                )
                
                existing_style = pre_tag.get('style', '')
                if existing_style:
                    pre_tag['style'] = f"{existing_style}; {code_container_style}"
                else:
                    pre_tag['style'] = code_container_style
                
                # 添加代码标题栏
                self._add_code_header(pre_tag)
                
                # 为代码块中的code标签设置白色字体
                code_tag = pre_tag.find('code')
                if code_tag:
                    code_style = (
                        "color: #ffffff; "
                        "font-family: 'Consolas', 'Monaco', monospace; "
                        "font-size: 14px; "
                        "background: transparent; "
                        "padding: 0; "
                        "border: none;"
                    )
                    existing_code_style = code_tag.get('style', '')
                    if existing_code_style:
                        code_tag['style'] = f"{existing_code_style}; {code_style}"
                    else:
                        code_tag['style'] = code_style
                
                # 为代码行添加样式
                code_lines = pre_tag.find_all('div', class_='code-line')
                for line_div in code_lines:
                    line_style = (
                        "display: flex; "
                        "align-items: center; "
                        "margin: 2px 0; "
                        "padding: 3px 0; "
                        "border-radius: 4px; "
                        "transition: background-color 0.2s ease;"
                    )
                    line_div['style'] = line_style
                    
                    # 为行号添加样式 - 白色
                    line_number = line_div.find('span', class_='line-number')
                    if line_number:
                        number_style = (
                            "color: #ffffff; "
                            "font-family: 'Consolas', 'Monaco', monospace; "
                            "font-size: 12px; "
                            "margin-right: 15px; "
                            "min-width: 25px; "
                            "text-align: right; "
                            "user-select: none; "
                            "opacity: 0.7;"
                        )
                        line_number['style'] = number_style
                    
                    # 为代码内容添加样式 - 白色
                    line_content = line_div.find('span', class_='line-content')
                    if line_content:
                        if 'comment' in line_content.get('class', []):
                            # 注释样式 - 灰色
                            content_style = (
                                "color: #cccccc; "
                                "font-family: 'Consolas', 'Monaco', monospace; "
                                "font-size: 14px; "
                                "font-style: italic; "
                                "opacity: 0.8;"
                            )
                        else:
                            # 普通代码样式 - 白色
                            content_style = (
                                "color: #ffffff; "
                                "font-family: 'Consolas', 'Monaco', monospace; "
                                "font-size: 14px; "
                                "font-weight: 500;"
                            )
                        line_content['style'] = content_style
                        
        except Exception as e:
            self.logger.error(f"应用代码样式时出错: {e}")
    
    def _add_code_header(self, pre_tag):
        """
        为代码块添加标题栏
        
        Args:
            pre_tag: pre标签
        """
        try:
            # 创建标题栏
            header_div = pre_tag.parent.new_tag('div')
            header_div['class'] = 'code-header'
            header_style = (
                "background: #000000; "
                "color: #ffffff; "
                "padding: 10px 15px; "
                "border-radius: 8px 8px 0 0; "
                "font-family: 'SF Pro Display', 'Helvetica Neue', sans-serif; "
                "font-size: 13px; "
                "font-weight: 600; "
                "display: flex; "
                "align-items: center; "
                "justify-content: space-between; "
                "border-bottom: 1px solid #333333; "
                "margin: -20px -20px 15px -20px;"
            )
            header_div['style'] = header_style
            
            # 添加代码图标和标题
            title_span = pre_tag.parent.new_tag('span')
            title_span.string = "🖥️ code"
            header_div.append(title_span)
            
            # 添加复制按钮样式的装饰
            copy_span = pre_tag.parent.new_tag('span')
            copy_span.string = "📋"
            copy_span['style'] = "opacity: 0.7; cursor: pointer;"
            header_div.append(copy_span)
            
            # 将标题栏插入到代码块前面
            pre_tag.insert(0, header_div)
            
        except Exception as e:
            self.logger.error(f"添加代码标题栏时出错: {e}")
    
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
  <meta charset="UTF-8"> 
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
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