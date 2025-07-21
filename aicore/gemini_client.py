# -*- coding: utf-8 -*-
"""
Gemini AI客户端模块
负责与Google Gemini API交互，生成文章内容
"""

import google.generativeai as genai
import os
import re
from typing import Optional
from datetime import datetime
from core.config import get_config
from core.logger import get_logger


class GeminiClient:
    """
    Gemini AI客户端
    """
    
    def __init__(self):
        """
        初始化Gemini客户端
        """
        self.config = get_config()
        self.logger = get_logger()
        self.model = None
        self._initialize_client()
    
    def _initialize_client(self):
        """
        初始化Gemini客户端
        """
        try:
            # 获取API Key
            api_key = self.config.get_gemini_api_key()
            if not api_key:
                raise ValueError("未找到Gemini API Key")
            
            # 配置API
            genai.configure(api_key=api_key)
            
            # 创建模型实例
            self.model = genai.GenerativeModel('gemini-2.0-flash')
            
            self.logger.info("Gemini客户端初始化成功")
            
        except Exception as e:
            self.logger.error(f"Gemini客户端初始化失败: {e}")
            raise
    
    def generate_catchy_title(self, original_title: str) -> Optional[str]:
        """
        根据原始标题生成更吸引人的爆款标题
        
        Args:
            original_title (str): 原始标题
            
        Returns:
            Optional[str]: 生成的爆款标题
        """
        try:
            self.logger.info(f"开始生成爆款标题，原标题: {original_title}")
            
            prompt = f"""
请根据以下原始标题，生成一个更加吸引人的爆款标题：

原始标题：{original_title}

要求：
1. 标题要有吸引力，能够激发读者的好奇心
2. 使用适当的情感词汇和数字
3. 长度控制在10-30个字之间
4. 符合微信公众号文章标题的特点
5. 避免过于夸张或标题党
6. 保持与原标题的相关性
7. 可以使用疑问句、感叹句等形式

请只输出一个最佳的标题，不要包含任何解释或说明。
"""
            
            # 调用Gemini API生成爆款标题
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                # 清理标题，移除可能的引号和多余空格
                catchy_title = response.text.strip().strip('"').strip("'")
                self.logger.info(f"爆款标题生成成功: {catchy_title}")
                return catchy_title
            else:
                self.logger.error(f"爆款标题生成失败，使用原标题: {original_title}")
                return original_title
                
        except Exception as e:
            self.logger.error(f"生成爆款标题时发生错误: {e}，使用原标题")
            return original_title
    
    def generate_article_from_title(self, title: str, use_catchy_title: bool = True) -> tuple[Optional[str], Optional[str]]:
        """
        根据标题生成文章
        
        Args:
            title (str): 原始文章标题
            use_catchy_title (bool): 是否生成爆款标题
            
        Returns:
            tuple[Optional[str], Optional[str]]: (文章内容, 最终标题)
        """
        if not self.model:
            self.logger.error("Gemini模型未初始化")
            return None, None
        
        try:
            # 1. 生成爆款标题（如果需要）
            final_title = title
            if use_catchy_title:
                catchy_title = self.generate_catchy_title(title)
                if catchy_title and catchy_title != title:
                    final_title = catchy_title
                    self.logger.info(f"使用爆款标题: {final_title}")
            
            self.logger.info(f"开始使用Gemini生成文章: {final_title}")
            
            # 2. 生成文章内容
            prompt = self._create_article_prompt(final_title)
            
            # 调用Gemini API生成内容
            response = self.model.generate_content(prompt)
            
            if not response or not response.text:
                self.logger.error("Gemini API返回空内容")
                return None, None
            
            markdown_content = response.text
            
            # 保存生成的文章到本地
            self.save_article_locally(final_title, markdown_content)
            
            self.logger.info(f"文章生成成功，标题: {final_title}")
            return markdown_content, final_title
            
        except Exception as e:
            self.logger.error(f"调用Gemini API失败: {e}")
            return None, None
    
    def _create_article_prompt(self, title: str) -> str:
        """
        创建文章生成提示词
        
        Args:
            title: 文章标题
        
        Returns:
            str: 提示词
        """
        prompt = f"""
请你扮演一位资深的微信公众号文章作者。
你的任务是根据下面的热点标题，创作一篇结构清晰、内容丰富、引人入胜的微信公众号文章。

要求如下：
1. 输出格式为标准的 Markdown。
2. 文章开头要有一个吸引人的引言，结尾要有总结或引导性的观点。
3. 文章结构需要分点论述，使用 Markdown 的标题（如 ##, ###）来组织段落。
4. 段落之间空一行，排版美观。
5. 内容要客观、深入，能够引发读者思考。
6. 文章字数控制在1000-2000字之间。
7. 语言要尽量使用普通的口语，一定要去除AI生成的痕迹。

文章内容必须围绕主题："{title}"

现在，请开始你的创作：
"""
        return prompt
    
    def save_article_locally(self, title: str, content: str) -> bool:
        """
        保存文章到本地
        
        Args:
            title (str): 文章标题
            content (str): 文章内容
            
        Returns:
            bool: 是否保存成功
        """
        try:
            # 确保articles目录存在
            articles_dir = "articles"
            if not os.path.exists(articles_dir):
                os.makedirs(articles_dir)
            
            # 生成安全的文件名
            safe_title = self._sanitize_filename(title)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{safe_title}.md"
            filepath = os.path.join(articles_dir, filename)
            
            # 保存文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"# {title}\n\n")
                f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"AI模型: Gemini (gemini-2.0-flash)\n\n")
                f.write("---\n\n")
                f.write(content)
            
            self.logger.info(f"文章已保存到: {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"保存文章失败: {e}")
            return False
    
    def _sanitize_filename(self, filename: str) -> str:
        """
        清理文件名，移除不安全字符
        
        Args:
            filename (str): 原始文件名
            
        Returns:
            str: 清理后的文件名
        """
        # 移除或替换不安全字符
        filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
        filename = re.sub(r'[\s]+', '_', filename)
        # 限制长度
        if len(filename) > 50:
            filename = filename[:50]
        return filename
    
    def test_connection(self) -> bool:
        """
        测试Gemini API连接
        
        Returns:
            bool: 连接是否成功
        """
        try:
            if not self.model:
                return False
            
            # 发送一个简单的测试请求
            response = self.model.generate_content("请回复'连接成功'")
            
            if response and response.text:
                self.logger.info("Gemini API连接测试成功")
                return True
            else:
                self.logger.error("Gemini API连接测试失败：无响应")
                return False
                
        except Exception as e:
            self.logger.error(f"Gemini API连接测试失败: {e}")
            return False


# 全局Gemini客户端实例
_global_gemini_client = None


def get_gemini_client() -> GeminiClient:
    """
    获取全局Gemini客户端实例
    
    Returns:
        GeminiClient: Gemini客户端实例
    """
    global _global_gemini_client
    if _global_gemini_client is None:
        _global_gemini_client = GeminiClient()
    return _global_gemini_client