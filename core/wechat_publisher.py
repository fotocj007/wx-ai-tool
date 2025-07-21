# -*- coding: utf-8 -*-
"""
微信公众号发布模块
负责与微信公众号API交互，发布文章草稿
"""

import requests
import json
import time
import os
import mimetypes
import re
from io import BytesIO
from datetime import datetime, timedelta
from typing import Optional, Tuple
from core.config import get_config
from core.logger import get_logger


class WeChatPublisher:
    """
    微信公众号发布器
    """
    
    BASE_URL = "https://api.weixin.qq.com/cgi-bin"
    
    def __init__(self):
        """
        初始化微信发布器
        """
        self.config = get_config()
        self.logger = get_logger()
        self.access_token_data = None
        
        # 获取微信配置
        wechat_config = self.config.get_wechat_config()
        self.app_id = wechat_config['appid']
        self.app_secret = wechat_config['appsecret']
        self.author = wechat_config['author']
        
        self.logger.info("微信发布器初始化完成")
    
    def _ensure_access_token(self) -> Optional[str]:
        """
        确保access_token有效
        
        Returns:
            str: access_token，失败返回None
        """
        try:
            # 检查是否需要刷新token
            if self._is_token_expired():
                self.logger.info("access_token已过期，正在刷新...")
                if not self._refresh_access_token():
                    return None
            
            return self.access_token_data['access_token']
            
        except Exception as e:
            self.logger.error(f"获取access_token失败: {e}")
            return None
    
    def _is_token_expired(self) -> bool:
        """
        检查token是否过期
        
        Returns:
            bool: 是否过期
        """
        if not self.access_token_data:
            return True
        
        # 提前5分钟刷新token
        expire_time = self.access_token_data.get('expire_time', 0)
        return time.time() >= (expire_time - 300)
    
    def _refresh_access_token(self) -> bool:
        """
        刷新access_token
        
        Returns:
            bool: 是否成功
        """
        url = f"{self.BASE_URL}/token"
        params = {
            'grant_type': 'client_credential',
            'appid': self.app_id,
            'secret': self.app_secret
        }
        
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if 'access_token' not in result:
                error_msg = result.get('errmsg', '未知错误')
                self.logger.error(f"获取access_token失败: {error_msg}")
                return False
            
            # 保存token信息
            self.access_token_data = {
                'access_token': result['access_token'],
                'expire_time': time.time() + result.get('expires_in', 7200)
            }
            
            self.logger.info("access_token刷新成功")
            return True
            
        except Exception as e:
            self.logger.error(f"刷新access_token失败: {e}")
            return False
    
    def _get_cache_file_path(self, image_url: str) -> str:
        """
        获取缓存文件路径
        
        Args:
            image_url: 图片路径
        
        Returns:
            str: 缓存文件路径
        """
        return os.path.join(os.path.dirname(image_url), "bg.txt")
    
    def _read_image_cache(self, cache_file_path: str) -> Tuple[Optional[str], Optional[str]]:
        """
        从缓存文件读取图片信息
        
        Args:
            cache_file_path: 缓存文件路径
        
        Returns:
            Tuple[str, str]: (media_id, url) 如果缓存无效则返回 (None, None)
        """
        if not os.path.exists(cache_file_path):
            return None, None
        
        try:
            with open(cache_file_path, "r", encoding="utf-8") as f:
                cache_data = json.load(f)
                cached_media_id = cache_data.get("media_id")
                cached_url = cache_data.get("url")
                if cached_media_id:
                    self.logger.info(f"从缓存读取图片media_id: {cached_media_id}")
                    return cached_media_id, cached_url
                return None, None
        except (json.JSONDecodeError, KeyError, FileNotFoundError) as e:
            self.logger.warning(f"读取缓存文件失败: {e}，将重新上传图片")
            return None, None
    
    def _save_image_cache(self, cache_file_path: str, media_id: str, url: Optional[str], file_name: str) -> None:
        """
        保存图片信息到缓存文件
        
        Args:
            cache_file_path: 缓存文件路径
            media_id: 微信媒体ID
            url: 图片URL
            file_name: 文件名
        """
        try:
            cache_data = {
                "media_id": media_id,
                "url": url,
                "upload_time": time.time(),
                "file_name": file_name
            }
            with open(cache_file_path, "w", encoding="utf-8") as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
            self.logger.info(f"图片上传成功并已缓存: {media_id}")
        except Exception as cache_error:
            self.logger.warning(f"保存缓存文件失败: {cache_error}")
    
    def upload_image(self, image_url: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        上传图片到微信服务器（带缓存机制）
        
        Args:
            image_url: 图片路径
        
        Returns:
            Tuple[str, str, str]: (media_id, url, error_message)
        """
        # 尝试从缓存读取
        cache_file_path = self._get_cache_file_path(image_url)
        cached_media_id, cached_url = self._read_image_cache(cache_file_path)
        if cached_media_id:
            return cached_media_id, cached_url, None

        if not image_url:
            # 如果图片URL为空，则返回一个默认的图片ID
            return None, None, f"本地图片未找到: {image_url}"

        try:
            # 处理本地图片
            if not os.path.exists(image_url):
                return None, None, f"本地图片未找到: {image_url}"
            print("---上传新图片-------------")
            # 缓存未命中，执行上传
            with open(image_url, "rb") as f:
                image_buffer = BytesIO(f.read())

            # 动态确定 MIME 类型和文件名后缀
            mime_type, _ = mimetypes.guess_type(image_url)
            if not mime_type:
                mime_type = "image/jpeg"  # 默认值
            file_name = os.path.basename(image_url)

            token = self._ensure_access_token()
            if not token:
                return None, None, "获取access_token失败"
            
            # 检查是否已认证来决定使用哪个接口
            if self.is_verified():
                url = f"{self.BASE_URL}/material/add_material?access_token={token}&type=image"
            else:
                url = f"{self.BASE_URL}/media/upload?access_token={token}&type=image"
                self.logger.error(f"未认证,上传零时封面素材: {url}")
                
            files = {"media": (file_name, image_buffer, mime_type)}
            response = requests.post(url, files=files, timeout=30)
            response.raise_for_status()
            data = response.json()

            if "errcode" in data and data.get("errcode") != 0:
                return None, None, f"图片上传失败: {data.get('errmsg')}"
            elif "media_id" not in data:
                return None, None, "图片上传失败: 响应中缺少 media_id"
            else:
                # 上传成功，保存到缓存
                media_id = data.get("media_id")
                url_result = data.get("url")
                self._save_image_cache(cache_file_path, media_id, url_result, file_name)
                return media_id, url_result, None

        except requests.exceptions.RequestException as e:
            return None, None, f"图片上传失败: {e}"
        except Exception as e:
            return None, None, f"图片上传失败: {e}"
    
    def _clean_title(self, title: str) -> str:
        """
        清理标题，去掉前面的时间戳格式
        
        Args:
            title: 原始标题
        
        Returns:
            str: 清理后的标题
        """
        # 去掉开头的时间戳格式，如：20250718_155640_ 或 20250718 155640 
        cleaned_title = re.sub(r'^\d{8}[_\s]\d{6}[_\s]', '', title)
        # 去掉开头的纯日期格式，如：20250718_
        cleaned_title = re.sub(r'^\d{8}_', '', cleaned_title)
        return cleaned_title.strip()
    
    def add_draft(self, title: str, content_html: str, digest: str = "") -> Tuple[Optional[str], Optional[str]]:
        """
        创建并上传草稿
        
        Args:
            title: 文章标题
            content_html: 文章HTML内容
            digest: 文章摘要
        
        Returns:
            Tuple[str, str]: (media_id, error_message)
        """
        try:
            self.logger.info(f"开始创建草稿: {title}")
            
            # 确保access_token有效
            access_token = self._ensure_access_token()
            if not access_token:
                return None, "获取access_token失败"
            
            # 上传本地图片作为封面
            image_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "img", "bg.png")
            thumb_media_id, _, upload_error = self.upload_image(image_path)
            
            if upload_error:
                self.logger.warning(f"上传封面图片失败: {upload_error}")
                # 如果上传失败，使用配置中的默认图片ID
                return None, f"上传草稿失败,上传封面图片失败: {upload_error}"
            
            # 清理标题，去掉时间戳前缀
            clean_title = self._clean_title(title)
            
            # 构建请求URL
            url = f"{self.BASE_URL}/draft/add?access_token={access_token}"
            
            # 构建文章数据
            article_data = {
                "title": clean_title[:60],  # 标题限制64字符
                "author": self.author,
                "digest": digest[:80] if digest else "",  # 摘要限制120字符
                "content": content_html,
                "thumb_media_id": thumb_media_id,
                "content_source_url": "",  # 原文链接
                "need_open_comment": 1,  # 开启评论
                "only_fans_can_comment": 0  # 所有人可评论
            }
            
            # 构建请求数据
            data = {"articles": [article_data]}
            json_data = json.dumps(data, ensure_ascii=False).encode("utf-8")
            # print(json_data)
            
            # 发送请求
            response = requests.post(
                url, 
                data=json_data,
                headers={'Content-Type': 'application/json; charset=utf-8'},
                timeout=30
            )
            response.raise_for_status()
            
            result = response.json()
            
            # 检查响应结果
            if result.get("errcode", 0) != 0:
                error_msg = result.get('errmsg', '未知错误')
                self.logger.error(f"上传草稿失败: {error_msg}")
                return None, f"上传草稿失败: {error_msg}"
            
            media_id = result.get("media_id")
            if not media_id:
                self.logger.error("上传草稿失败: 响应中缺少media_id")
                return None, "上传草稿失败: 响应中缺少media_id"
            
            self.logger.info(f"草稿创建成功！Media ID: {media_id}")
            return media_id, None
            
        except requests.RequestException as e:
            error_msg = f"上传微信草稿网络请求失败: {e}"
            self.logger.error(error_msg)
            return None, error_msg
        except Exception as e:
            error_msg = f"上传草稿失败: {e}"
            self.logger.error(error_msg)
            return None, error_msg
    
    def get_draft_list(self, offset: int = 0, count: int = 20) -> Optional[dict]:
        """
        获取草稿列表
        
        Args:
            offset: 偏移量
            count: 数量
        
        Returns:
            dict: 草稿列表数据
        """
        try:
            access_token = self._ensure_access_token()
            if not access_token:
                return None
            
            url = f"{self.BASE_URL}/draft/batchget?access_token={access_token}"
            data = {
                "offset": offset,
                "count": count,
                "no_content": 1  # 不返回content字段
            }
            
            response = requests.post(url, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("errcode", 0) != 0:
                error_msg = result.get('errmsg', '未知错误')
                self.logger.error(f"获取草稿列表失败: {error_msg}")
                return None
            
            return result
            
        except Exception as e:
            self.logger.error(f"获取草稿列表失败: {e}")
            return None
    
    def delete_draft(self, media_id: str) -> bool:
        """
        删除草稿
        
        Args:
            media_id: 草稿媒体ID
        
        Returns:
            bool: 是否成功
        """
        try:
            access_token = self._ensure_access_token()
            if not access_token:
                return False
            
            url = f"{self.BASE_URL}/draft/delete?access_token={access_token}"
            data = {"media_id": media_id}
            
            response = requests.post(url, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if result.get("errcode", 0) != 0:
                error_msg = result.get('errmsg', '未知错误')
                self.logger.error(f"删除草稿失败: {error_msg}")
                return False
            
            self.logger.info(f"草稿删除成功: {media_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"删除草稿失败: {e}")
            return False
    
    def is_verified(self) -> bool:
        """
        检查公众号是否已认证
        
        Returns:
            bool: 是否已认证
        """
        try:
            access_token = self._ensure_access_token()
            if not access_token:
                return False
            
            # 尝试调用需要认证的接口
            url = f"{self.BASE_URL}/draft/batchget?access_token={access_token}"
            data = {"offset": 0, "count": 1, "no_content": 1}
            
            response = requests.post(url, json=data, timeout=30)
            result = response.json()
            
            # 如果返回错误码61004，表示未认证
            if result.get("errcode") == 61004:
                self.logger.warning("公众号未认证，无法使用草稿功能")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"检查认证状态失败: {e}")
            return False
    
    def test_connection(self) -> bool:
        """
        测试微信API连接
        
        Returns:
            bool: 连接是否成功
        """
        try:
            access_token = self._ensure_access_token()
            if access_token:
                self.logger.info("微信API连接测试成功")
                return True
            else:
                self.logger.error("微信API连接测试失败")
                return False
                
        except Exception as e:
            self.logger.error(f"微信API连接测试失败: {e}")
            return False


# 全局微信发布器实例
_global_wechat_publisher = None


def get_wechat_publisher() -> WeChatPublisher:
    """
    获取全局微信发布器实例
    
    Returns:
        WeChatPublisher: 微信发布器实例
    """
    global _global_wechat_publisher
    if _global_wechat_publisher is None:
        _global_wechat_publisher = WeChatPublisher()
    return _global_wechat_publisher