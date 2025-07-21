# -*- coding: utf-8 -*-
"""
微信公众号热点文章AI生成与发布系统 - 主应用
提供Web API接口服务
"""

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import os
import sys
import threading
import uuid
from typing import Dict, Any

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.config import get_config
from core.logger import get_logger, cleanup_old_logs
from core.html_converter import get_html_converter
from core.wechat_publisher import get_wechat_publisher
from aicore.gemini_client import get_gemini_client
from aicore.qwen_client import get_qwen_client
from route import register_main_routes, register_api_routes, register_article_routes, register_wechat_routes


class VXToolApp:
    """
    VX Tool 主应用类
    """

    def __init__(self):
        """
        初始化应用
        """
        self.app = Flask(__name__)
        CORS(self.app)  # 启用跨域支持

        # 初始化SocketIO
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")

        # 任务状态管理
        self.task_status = {}  # 存储任务状态

        # 初始化组件
        self.config = get_config()
        self.logger = get_logger()
        self.html_converter = get_html_converter()
        self.wechat_publisher = get_wechat_publisher()

        # 根据配置选择AI客户端
        ai_model = self.config.get_ai_model()
        if ai_model == 'qwen':
            self.ai_client = get_qwen_client()
            self.logger.info("使用Qwen AI客户端")
        else:
            self.ai_client = get_gemini_client()
            self.logger.info("使用Gemini AI客户端")

        # 注册路由
        self._register_routes()

        # 清理旧日志
        cleanup_old_logs(keep_days=self.config.get_max_log_files())

        self.logger.info("VX Tool 应用初始化完成")

    def _register_routes(self):
        """
        注册路由
        """
        # 注册各个模块的路由
        register_main_routes(self.app)
        register_api_routes(self.app, self)
        register_article_routes(self.app, self)
        register_wechat_routes(self.app, self)

        # 注册SocketIO事件
        self._register_socketio_events()

    def _register_socketio_events(self):
        """
        注册SocketIO事件
        """

        @self.socketio.on('connect')
        def handle_connect():
            self.logger.info('客户端已连接')

        @self.socketio.on('disconnect')
        def handle_disconnect():
            self.logger.info('客户端已断开连接')

    def generate_article_async(self, title: str, task_id: str, use_catchy_title: bool = True, ai_model: str = 'qwen'):
        """
        异步生成文章
        
        Args:
            title: 原始标题
            task_id: 任务ID
            use_catchy_title: 是否生成爆款标题
            ai_model: AI模型选择 ('qwen' 或 'gemini')
        """
        try:
            # 根据ai_model参数选择AI客户端
            if ai_model == 'gemini':
                ai_client = get_gemini_client()
                self.logger.info(f"使用Gemini AI客户端生成文章: {title}")
            else:
                ai_client = get_qwen_client()
                self.logger.info(f"使用Qwen AI客户端生成文章: {title}")
            
            # 更新任务状态
            self.task_status[task_id] = {
                'status': 'generating_title',
                'message': f'正在使用{ai_model.upper()}生成爆款标题...',
                'progress': 20
            }
            self.socketio.emit('task_update', {
                'task_id': task_id,
                'status': 'generating_title',
                'message': f'正在使用{ai_model.upper()}生成爆款标题...',
                'progress': 20
            })

            # 生成文章和标题
            content, final_title = ai_client.generate_article_from_title(title, use_catchy_title)

            # 更新任务状态：开始生成文章
            self.task_status[task_id] = {
                'status': 'generating_article',
                'message': '正在生成文章内容...',
                'progress': 50
            }
            self.socketio.emit('task_update', {
                'task_id': task_id,
                'status': 'generating_article',
                'title': final_title if final_title else title,
                'message': '正在生成文章内容...',
                'progress': 50
            })

            if content and final_title:
                # 更新任务状态
                self.task_status[task_id] = {
                    'status': 'saving',
                    'message': '正在保存文章...',
                    'progress': 80
                }
                self.socketio.emit('task_update', {
                    'task_id': task_id,
                    'status': 'saving',
                    'message': '正在保存文章...',
                    'progress': 80
                })

                # 保存文章
                articles_dir = os.path.join(os.path.dirname(__file__), 'articles')
                if not os.path.exists(articles_dir):
                    os.makedirs(articles_dir)

                from datetime import datetime
                import re

                # 生成安全的文件名
                safe_title = re.sub(r'[<>:"/\\|?*]', '_', final_title)
                safe_title = re.sub(r'[\s]+', '_', safe_title)
                if len(safe_title) > 50:
                    safe_title = safe_title[:50]

                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{safe_title}.md"
                file_path = os.path.join(articles_dir, filename)

                # 写入文件
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                # 任务完成
                self.task_status[task_id] = {
                    'status': 'completed',
                    'message': '文章生成完成！',
                    'progress': 100,
                    'data': {
                        'title': final_title,
                        'original_title': title,
                        'filename': filename,
                        'file_path': file_path
                    }
                }
                self.socketio.emit('task_update', {
                    'task_id': task_id,
                    'status': 'completed',
                    'message': '文章生成完成！',
                    'progress': 100,
                    'original_title': title,
                    'final_title': final_title,
                    'filename': filename,
                    'file_path': file_path
                })

                self.logger.info(f"文章生成完成: {final_title}")
            else:
                # 任务失败
                self.task_status[task_id] = {
                    'status': 'failed',
                    'message': 'AI文章生成失败',
                    'progress': 0
                }
                self.socketio.emit('task_update', {
                    'task_id': task_id,
                    'status': 'error',
                    'error': 'AI文章生成失败',
                    'progress': 0
                })

        except Exception as e:
            # 任务异常
            self.task_status[task_id] = {
                'status': 'failed',
                'message': f'生成文章失败: {str(e)}',
                'progress': 0
            }
            self.socketio.emit('task_update', {
                'task_id': task_id,
                'status': 'error',
                'error': f'生成文章失败: {str(e)}',
                'progress': 0
            })
            self.logger.error(f"异步生成文章失败: {e}")

    def start_article_generation(self, title: str, use_catchy_title: bool = True, ai_model: str = 'qwen') -> str:
        """
        启动文章生成任务
        
        Args:
            title: 原始标题
            use_catchy_title: 是否生成爆款标题
            ai_model: AI模型选择 ('qwen' 或 'gemini')
            
        Returns:
            str: 任务ID
        """
        task_id = str(uuid.uuid4())

        # 初始化任务状态
        self.task_status[task_id] = {
            'status': 'started',
            'message': '任务已启动...',
            'progress': 10
        }

        # 启动异步任务
        thread = threading.Thread(
                target=self.generate_article_async,
                args=(title, task_id, use_catchy_title, ai_model)
        )
        thread.daemon = True
        thread.start()

        return task_id

    def run(self, host='0.0.0.0', port=5000, debug=False):
        """
        运行应用
        
        Args:
            host: 主机地址
            port: 端口号
            debug: 调试模式
        """
        self.logger.info(f"启动VX Tool服务: http://{host}:{port}")
        self.socketio.run(self.app, host=host, port=port, debug=debug, allow_unsafe_werkzeug=True)


def create_app() -> Flask:
    """
    创建Flask应用实例
    
    Returns:
        Flask: Flask应用实例
    """
    vx_app = VXToolApp()
    return vx_app.app


if __name__ == '__main__':
    # 创建应用实例
    vx_app = VXToolApp()

    # 运行应用
    vx_app.run(debug=True)
