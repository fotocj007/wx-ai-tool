# -*- coding: utf-8 -*-
"""
代码块处理模块
负责处理HTML中的代码块样式和功能
"""

from bs4 import BeautifulSoup
from core.logger import get_logger


class CodeProcessor:
    """
    代码块处理器
    负责处理代码块的样式、行号、标题栏等功能
    """
    
    def __init__(self):
        """
        初始化代码块处理器
        """
        self.logger = get_logger()
    
    def process_code_blocks(self, soup: BeautifulSoup):
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
    
    def is_code_related_tag(self, tag):
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
    
    def apply_code_styles(self, soup: BeautifulSoup):
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
                    "overflow-x: auto; "
                    "max-width: 100%; "
                    "-webkit-overflow-scrolling: touch; "
                    "scrollbar-width: thin; "
                    "scrollbar-color: #666 #333;"
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
                        "border: none; "
                        "white-space: pre; "
                        "word-wrap: break-word; "
                        "overflow-wrap: break-word;"
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
                        "align-items: flex-start; "
                        "margin: 2px 0; "
                        "padding: 3px 0; "
                        "border-radius: 4px; "
                        "transition: background-color 0.2s ease; "
                        "flex-wrap: wrap;"
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
                            "opacity: 0.7; "
                            "flex-shrink: 0;"
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
                                "opacity: 0.8; "
                                "word-wrap: break-word; "
                                "overflow-wrap: break-word; "
                                "white-space: pre-wrap; "
                                "flex: 1;"
                            )
                        else:
                            # 普通代码样式 - 白色
                            content_style = (
                                "color: #ffffff; "
                                "font-family: 'Consolas', 'Monaco', monospace; "
                                "font-size: 14px; "
                                "font-weight: 500; "
                                "word-wrap: break-word; "
                                "overflow-wrap: break-word; "
                                "white-space: pre-wrap; "
                                "flex: 1;"
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
            title_span.string = "🔴 code"
            header_div.append(title_span)
        
            # 将标题栏插入到代码块前面
            pre_tag.insert(0, header_div)
            
        except Exception as e:
            self.logger.error(f"添加代码标题栏时出错: {e}")


# 全局代码处理器实例
_global_code_processor = None


def get_code_processor() -> CodeProcessor:
    """
    获取全局代码处理器实例
    
    Returns:
        CodeProcessor: 代码处理器实例
    """
    global _global_code_processor
    if _global_code_processor is None:
        _global_code_processor = CodeProcessor()
    return _global_code_processor