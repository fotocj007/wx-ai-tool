# -*- coding: utf-8 -*-
"""
微信路由模块
包含微信公众号相关的路由，如草稿管理、发布等
"""

from flask import request
from typing import Dict, Any
import os


def register_wechat_routes(app, vx_app):
    """
    注册微信相关路由
    
    Args:
        app: Flask应用实例
        vx_app: VXToolApp实例
    """
    
    @app.route('/api/drafts', methods=['GET'])
    def get_drafts():
        """获取草稿列表"""
        return _get_drafts(vx_app)
    
    @app.route('/api/publish-wechat/<filename>', methods=['POST'])
    def publish_wechat(filename):
        """发布文章到微信公众号"""
        return _publish_to_wechat(vx_app, filename)


def _get_drafts(vx_app) -> Dict[str, Any]:
    """
    获取草稿列表
    
    Args:
        vx_app: VXToolApp实例
        
    Returns:
        dict: API响应
    """
    try:
        offset = int(request.args.get('offset', 0))
        count = int(request.args.get('count', 20))
        
        drafts_data = vx_app.wechat_publisher.get_draft_list(offset, count)
        
        if not drafts_data:
            return {
                'success': False,
                'error': '获取草稿列表失败'
            }
        
        return {
            'success': True,
            'data': drafts_data
        }
        
    except Exception as e:
        vx_app.logger.error(f"获取草稿列表失败: {e}")
        return {
            'success': False,
            'error': f'获取草稿列表失败: {str(e)}'
        }


def _publish_to_wechat(vx_app, filename: str) -> Dict[str, Any]:
    """
    发布文章到微信公众号
    
    Args:
        vx_app: VXToolApp实例
        filename: 文件名
        
    Returns:
        dict: API响应
    """
    try:
        # 检查HTML文件是否存在
        articles_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'articles')
        html_dir = os.path.join(articles_dir, 'html')
        html_filename = filename.replace('.md', '.html')
        html_file_path = os.path.join(html_dir, html_filename)
        
        if not os.path.exists(html_file_path):
            return {
                'success': False,
                'error': 'HTML文件不存在，请先转换Markdown为HTML'
            }
        
        # 读取HTML内容
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # 从文件名提取标题
        title = filename.replace('.md', '').replace('_', ' ')
        if title.startswith('2'):
            # 如果以日期开头，去掉日期部分
            parts = title.split('_', 2)
            if len(parts) >= 3:
                title = parts[2]
        
        # 生成摘要
        digest = vx_app.html_converter.extract_digest(html_content)
        
        # 发布到微信
        media_id, error = vx_app.wechat_publisher.add_draft(title, html_content, digest)
        if error:
            return {
                'success': False,
                'error': error
            }
        
        vx_app.logger.info(f"文章已发布到微信: {title}, Media ID: {media_id}")
        
        return {
            'success': True,
            'data': {
                'title': title,
                'media_id': media_id,
                'digest': digest,
                'message': '文章已成功发布到微信公众号！'
            }
        }
        
    except Exception as e:
        vx_app.logger.error(f"发布到微信失败: {str(e)}")
        return {
            'success': False,
            'error': f'发布到微信失败: {str(e)}'
        }