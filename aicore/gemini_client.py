# -*- coding: utf-8 -*-
"""
Gemini AI客户端模块
负责与Google Gemini API交互，生成文章内容
"""

import google.generativeai as genai
from typing import Optional

from core.config import get_config
from core.logger import get_logger
from tools.utils import clean_markdown_content, validate_markdown_content


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

    def generate_article_from_title(self, title: str, use_catchy_title: bool = True) -> tuple[
        Optional[str], Optional[str]]:
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

            self.logger.info(f"开始使用Gemini生成文章: {title}")

            # 2. 生成文章内容
            prompt = self._create_article_prompt(title)

            # 调用Gemini API生成内容
            response = self.model.generate_content(prompt)

            if not response or not response.text:
                self.logger.error("Gemini API返回空内容")
                return None, None

            # 清理AI生成的markdown内容中的多余字符
            raw_content = response.text
            markdown_content = clean_markdown_content(raw_content)
            
            # 验证清理后的内容是否有效
            if not validate_markdown_content(markdown_content):
                self.logger.warning(f"清理后的markdown内容可能有问题，原始内容: {raw_content[:100]}...")
                # 如果清理后的内容有问题，使用原始内容但记录警告
                markdown_content = raw_content
            else:
                self.logger.info("成功清理markdown内容中的多余字符")

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
6. 文章字数控制在1500-2500字之间。

特别注意：文章内容的文字一定要使用正常的一般性口语，不要用特别的专业性疏于。而且一定要去除AI味的痕迹。

文章内容必须围绕主题："{title}"

现在，请开始你的创作：
"""
        return prompt

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
