#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qwen AI客户端
用于与阿里云通义千问API交互，生成文章内容
"""

import requests
import json
from typing import Optional

from core.config import get_config
from core.logger import get_logger
from tools.utils import clean_markdown_content, validate_markdown_content


class QwenClient:
    """
    Qwen AI客户端类
    """

    def __init__(self, model_type: str = 'qwen'):
        """
        初始化Qwen客户端
        
        Args:
            model_type: 模型类型 ('qwen' 或 'kimi')
        """
        self.config = get_config()
        self.logger = get_logger()
        self.model_type = model_type
        self.qwen_config = self.config.get_qwen_config(model_type)

        # 验证配置
        if not self.qwen_config['api_key']:
            self.logger.error("Qwen API Key未配置")
            raise ValueError("Qwen API Key未配置")

        self.api_key = self.qwen_config['api_key']
        self.base_url = self.qwen_config['base_url']
        self.model = self.qwen_config['model']

        self.logger.info(f"Qwen客户端初始化成功，模型: {self.model}")

    def _make_request(self, messages: list, max_tokens: int = 2000) -> Optional[str]:
        """
        发送请求到Qwen API
        
        Args:
            messages (list): 消息列表
            max_tokens (int): 最大token数
            
        Returns:
            Optional[str]: 生成的内容
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'application/json'
            }

            data = {
                'model': self.model,
                'messages': messages,
                'max_tokens': max_tokens,
                'temperature': 0.7,
                'top_p': 0.9
            }

            self.logger.info(f"发送请求到Qwen API: {self.base_url}/chat/completions")

            response = requests.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=data,
                    timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                if 'choices' in result and len(result['choices']) > 0:
                    content = result['choices'][0]['message']['content']
                    self.logger.info("Qwen API请求成功")
                    return content
                else:
                    self.logger.error(f"Qwen API响应格式错误: {result}")
                    return None
            else:
                self.logger.error(f"Qwen API请求失败: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            self.logger.error(f"Qwen API请求异常: {e}")
            return None

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

            messages = [
                {
                    "role": "system",
                    "content": "你是一位专业的新媒体编辑，擅长创作吸引人的文章标题。你的标题总是能够吸引读者点击，同时保持内容的准确性。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]

            # 发送请求
            catchy_title = self._make_request(messages, max_tokens=100)

            if catchy_title:
                # 清理标题，移除可能的引号和多余空格
                catchy_title = catchy_title.strip().strip('"').strip("'")
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
        try:
            # 1. 生成爆款标题（如果需要）
            final_title = title
            if use_catchy_title:
                catchy_title = self.generate_catchy_title(title)
                if catchy_title and catchy_title != title:
                    final_title = catchy_title
                    self.logger.info(f"使用爆款标题: {final_title}")

            self.logger.info(f"开始使用Qwen生成文章: {final_title}")

            # 2. 构建提示词
            prompt = f"""
请根据以下标题创作一篇高质量的微信公众号文章：

标题：{final_title}。
文章内容必须围绕话题 "{title}" 展开。

要求：
1. 文章结构清晰，包含引言、正文和结尾
2. 内容有深度，有见解，有价值
3. 语言生动有趣，适合微信公众号阅读
4. 字数控制在1500-2500字之间
5. 使用Markdown格式输出
6. 包含适当的小标题和段落分隔
7. 结尾要有启发性或总结性
8. 避免过于商业化的内容

特别注意：文章内容的文字一定要使用正常的一般性口语，不要用特别的专业性疏于。而且一定要去除AI味的痕迹。

请直接输出文章内容，不要包含任何解释或说明文字。
"""

            messages = [
                {
                    "role": "system",
                    "content": "你是一位专业的内容创作者，擅长写作高质量的微信公众号文章。你的文章总是能够吸引读者，内容有深度且易于理解。"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]

            # 3. 发送请求
            content = self._make_request(messages, max_tokens=3000)

            if content:
                # 清理AI生成的Markdown内容中的多余字符
                cleaned_content = clean_markdown_content(content)
                
                # 验证清理后的内容
                if validate_markdown_content(cleaned_content):
                    self.logger.info(f"文章生成成功，内容已清理: {final_title}")
                    return cleaned_content, final_title
                else:
                    self.logger.warning(f"内容清理后验证失败，使用原始内容: {final_title}")
                    return content, final_title
            else:
                self.logger.error(f"文章生成失败: {final_title}")
                return None, None

        except Exception as e:
            self.logger.error(f"生成文章时发生错误: {e}")
            return None, None

    def test_connection(self) -> bool:
        """
        测试与Qwen API的连接
        
        Returns:
            bool: 连接是否成功
        """
        try:
            self.logger.info("测试Qwen API连接...")

            messages = [
                {
                    "role": "user",
                    "content": "请回复'连接测试成功'"
                }
            ]

            result = self._make_request(messages, max_tokens=50)

            if result:
                self.logger.info("Qwen API连接测试成功")
                return True
            else:
                self.logger.error("Qwen API连接测试失败")
                return False

        except Exception as e:
            self.logger.error(f"Qwen API连接测试异常: {e}")
            return False


# 全局实例
_qwen_client = None
_kimi_client = None


def get_qwen_client(model_type: str = 'qwen') -> QwenClient:
    """
    获取全局Qwen客户端实例
    
    Args:
        model_type: 模型类型 ('qwen' 或 'kimi')
    
    Returns:
        QwenClient: Qwen客户端实例
    """
    global _qwen_client, _kimi_client
    
    if model_type == 'kimi':
        if _kimi_client is None:
            _kimi_client = QwenClient('kimi')
        return _kimi_client
    else:
        if _qwen_client is None:
            _qwen_client = QwenClient('qwen')
        return _qwen_client
