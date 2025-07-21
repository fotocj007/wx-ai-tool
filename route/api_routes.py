# -*- coding: utf-8 -*-
"""
API路由模块
包含热点话题、平台列表、系统状态等基础API路由
"""

from flask import request
from typing import Dict, Any
from tools.hotnews import get_platform_news, PLATFORMS


def register_api_routes(app, vx_app):
    """
    注册API路由
    
    Args:
        app: Flask应用实例
        vx_app: VXToolApp实例
    """
    
    @app.route('/api/hot-topics', methods=['GET'])
    def get_hot_topics():
        """获取热点话题列表"""
        return _get_hot_topics(vx_app)

    
    @app.route('/api/status', methods=['GET'])
    def system_status():
        """系统状态检查"""
        return _system_status(vx_app)


def _get_hot_topics(vx_app) -> Dict[str, Any]:
    """
    获取热点话题列表
    
    Args:
        vx_app: VXToolApp实例
        
    Returns:
        dict: API响应
    """
    try:
        platform = request.args.get('platform', '微博')
        count = int(request.args.get('count', 30))
        
        vx_app.logger.info(f"获取热点话题: 平台={platform}, 数量={count}")
        
        # 获取热点新闻数据
        news_data = get_platform_news(platform, count)
        
        if not news_data:
            return {
                'success': False,
                'error': f'无法获取{platform}的热点话题',
                'data': []
            }
        
        return {
            'success': True,
            'data': {
                'platform': platform,
                'topics': news_data,  # 返回完整的新闻数据，包含name, rank, lastCount, url
                'count': len(news_data)
            }
        }
        
    except Exception as e:
        vx_app.logger.error(f"获取热点话题失败: {e}")
        return {
            'success': False,
            'error': f'获取热点话题失败: {str(e)}',
            'data': []
        }

def _system_status(vx_app) -> Dict[str, Any]:
    """
    系统状态检查
    
    Args:
        vx_app: VXToolApp实例
        
    Returns:
        dict: API响应
    """
    try:
        # 检查AI API
        ai_model = vx_app.config.get_ai_model()
        ai_status = vx_app.ai_client.test_connection()
        
        status = {
            f'{ai_model}_api': ai_status,
            'wechat_api': vx_app.wechat_publisher.test_connection(),
            'wechat_verified': vx_app.wechat_publisher.is_verified()
        }
        
        # 判断整体状态
        if ai_status and status['wechat_api']:
            overall = 'healthy'
            message = f'所有服务运行正常 (AI模型: {ai_model.upper()})'
        elif ai_status or status['wechat_api']:
            overall = 'partial'
            message = f'部分服务可用 (AI模型: {ai_model.upper()})'
        else:
            overall = 'error'
            message = f'服务异常，请检查配置 (AI模型: {ai_model.upper()})'
        
        return {
            'success': True,
            'data': {
                'status': status,
                'overall': overall,
                'message': message
            }
        }
        
    except Exception as e:
        vx_app.logger.error(f"系统状态检查失败: {e}")
        return {
            'success': False,
            'error': f'系统状态检查失败: {str(e)}'
        }