# -*- coding: utf-8 -*-
"""
文章路由模块
包含文章生成、编辑、转换等相关路由
"""

from flask import request, send_file, abort
from typing import Dict, Any
import os
import glob
from datetime import datetime
import re


def register_article_routes(app, vx_app):
    """
    注册文章相关路由
    
    Args:
        app: Flask应用实例
        vx_app: VXToolApp实例
    """

    @app.route('/api/generate-article', methods=['POST'])
    def generate_article():
        """仅生成文章（不发布）"""
        return _generate_article(vx_app)

    @app.route('/api/articles', methods=['GET'])
    def articles_list():
        """获取文章列表"""
        return _get_articles_list(vx_app)

    @app.route('/api/articles/<filename>', methods=['GET'])
    def article_detail(filename):
        """获取文章内容"""
        return _get_article_content(vx_app, filename)

    @app.route('/api/articles/<filename>', methods=['PUT'])
    def article_update(filename):
        """更新文章内容"""
        return _update_article_content(vx_app, filename)

    @app.route('/api/convert-html/<filename>', methods=['POST'])
    def convert_html(filename):
        """将Markdown转换为HTML"""
        return _convert_to_html(vx_app, filename)

    @app.route('/preview/<filename>', methods=['GET'])
    def preview_html(filename):
        """预览HTML文件"""
        return _preview_html(vx_app, filename)
    
    @app.route('/api/templates', methods=['GET'])
    def get_templates():
        """获取可用的样式模板列表"""
        return _get_templates(vx_app)


def _generate_article(vx_app) -> Dict[str, Any]:
    """
    仅生成文章（不发布）- 异步版本
    
    Args:
        vx_app: VXToolApp实例
        
    Returns:
        dict: API响应
    """
    try:
        data = request.get_json()
        if not data or 'title' not in data:
            return {
                'success': False,
                'error': '缺少必要参数: title'
            }

        title = data['title']
        use_catchy_title = data.get('use_catchy_title', True)

        vx_app.logger.info(f"开始异步生成文章: {title}")

        # 启动异步任务
        task_id = vx_app.start_article_generation(title, use_catchy_title)

        return {
            'success': True,
            'data': {
                'task_id': task_id,
                'message': '文章生成任务已启动，请通过WebSocket监听进度'
            }
        }

    except Exception as e:
        vx_app.logger.error(f"启动文章生成任务失败: {e}")
        return {
            'success': False,
            'error': f'启动文章生成任务失败: {str(e)}'
        }


def _get_articles_list(vx_app) -> Dict[str, Any]:
    """
    获取文章列表
    
    Args:
        vx_app: VXToolApp实例
        
    Returns:
        dict: API响应
    """
    try:
        articles_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'articles')
        if not os.path.exists(articles_dir):
            os.makedirs(articles_dir)

        md_files = glob.glob(os.path.join(articles_dir, '*.md'))
        files = []

        for file_path in md_files:
            filename = os.path.basename(file_path)
            stat = os.stat(file_path)
            modified = datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S')

            files.append({
                'name': filename,
                'modified': modified,
                'size': stat.st_size
            })

        # 按修改时间倒序排列
        files.sort(key=lambda x: x['modified'], reverse=True)

        return {
            'success': True,
            'data': {
                'files': files,
                'total': len(files)
            }
        }

    except Exception as e:
        vx_app.logger.error(f"获取文章列表失败: {str(e)}")
        return {
            'success': False,
            'error': f'获取文章列表失败: {str(e)}'
        }


def _get_article_content(vx_app, filename: str) -> Dict[str, Any]:
    """
    获取文章内容
    
    Args:
        vx_app: VXToolApp实例
        filename: 文件名
        
    Returns:
        dict: API响应
    """
    try:
        articles_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'articles')
        file_path = os.path.join(articles_dir, filename)

        if not os.path.exists(file_path):
            return {
                'success': False,
                'error': '文件不存在'
            }

        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        return {
            'success': True,
            'data': {
                'filename': filename,
                'content': content
            }
        }

    except Exception as e:
        vx_app.logger.error(f"读取文章内容失败: {str(e)}")
        return {
            'success': False,
            'error': f'读取文章内容失败: {str(e)}'
        }


def _update_article_content(vx_app, filename: str) -> Dict[str, Any]:
    """
    更新文章内容
    
    Args:
        vx_app: VXToolApp实例
        filename: 文件名
        
    Returns:
        dict: API响应
    """
    try:
        data = request.get_json()
        content = data.get('content', '')

        articles_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'articles')
        file_path = os.path.join(articles_dir, filename)

        if not os.path.exists(file_path):
            return {
                'success': False,
                'error': '文件不存在'
            }

        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        vx_app.logger.info(f"文章已更新: {filename}")

        return {
            'success': True,
            'data': {
                'filename': filename,
                'message': '文件保存成功'
            }
        }

    except Exception as e:
        vx_app.logger.error(f"更新文章内容失败: {str(e)}")
        return {
            'success': False,
            'error': f'更新文章内容失败: {str(e)}'
        }


def _convert_to_html(vx_app, filename: str) -> Dict[str, Any]:
    """
    将Markdown转换为HTML
    
    Args:
        vx_app: VXToolApp实例
        filename: 文件名
        
    Returns:
        dict: API响应
    """
    try:
        # 获取请求参数
        data = request.get_json() if request.is_json else {}
        template_name = data.get('template_name') if data else request.args.get('template_name')
        
        articles_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'articles')
        md_file_path = os.path.join(articles_dir, filename)

        if not os.path.exists(md_file_path):
            return {
                'success': False,
                'error': '文件不存在'
            }

        # 读取Markdown内容
        with open(md_file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # 从文件名提取标题
        title = filename.replace('.md', '').replace('_', ' ')
        if title.startswith('2'):
            # 如果以日期开头，去掉日期部分
            parts = title.split('_', 2)
            if len(parts) >= 3:
                title = parts[2]

        # 转换为HTML，支持指定模板
        html_content = vx_app.html_converter.markdown_to_styled_html(md_content, title, template_name)
        
        # 获取使用的模板信息
        available_templates = vx_app.html_converter.get_available_templates()
        template_names = [t['name'] for t in available_templates]
        
        if template_name and template_name in template_names:
            # 找到对应的模板描述
            used_template = next(t['description'] for t in available_templates if t['name'] == template_name)
        else:
            # 如果没有指定模板或模板不存在，则是随机选择的
            used_template = "随机选择"

        # 保存HTML文件
        html_dir = os.path.join(articles_dir, 'html')
        if not os.path.exists(html_dir):
            os.makedirs(html_dir)

        html_filename = filename.replace('.md', '.html')
        html_file_path = os.path.join(html_dir, html_filename)

        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        vx_app.logger.info(f"HTML文件已生成: {html_file_path}，使用模板: {used_template}")

        return {
            'success': True,
            'data': {
                'html_path': html_file_path,
                'html_filename': html_filename,
                'template_used': used_template,
                'message': f'HTML转换成功，使用模板: {used_template}'
            }
        }

    except Exception as e:
        vx_app.logger.error(f"转换HTML失败: {str(e)}")
        return {
            'success': False,
            'error': f'转换HTML失败: {str(e)}'
        }


def _get_templates(vx_app) -> Dict[str, Any]:
    """
    获取可用的样式模板列表
    
    Args:
        vx_app: VXToolApp实例
        
    Returns:
        dict: API响应
    """
    try:
        templates = vx_app.html_converter.get_available_templates()
        
        return {
            'success': True,
            'data': {
                'templates': templates,
                'count': len(templates)
            }
        }
        
    except Exception as e:
        vx_app.logger.error(f"获取模板列表失败: {str(e)}")
        return {
            'success': False,
            'error': f'获取模板列表失败: {str(e)}'
        }


def _preview_html(vx_app, filename: str):
    """
    预览HTML文件
    
    Args:
        vx_app: VXToolApp实例
        filename: 文件名
        
    Returns:
        Flask response
    """
    try:
        articles_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'articles')
        html_dir = os.path.join(articles_dir, 'html')
        html_file_path = os.path.join(html_dir, filename)

        if not os.path.exists(html_file_path):
            vx_app.logger.warning(f"HTML文件不存在: {html_file_path}")
            return abort(404)  # 返回HTTP 404状态码

        return send_file(html_file_path, mimetype='text/html')

    except Exception as e:
        vx_app.logger.error(f"预览HTML失败: {str(e)}")
        abort(500)  # 返回HTTP 500状态码
