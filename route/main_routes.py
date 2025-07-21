# -*- coding: utf-8 -*-
"""
主页面路由模块
包含主页和编辑器页面的路由
"""

from flask import render_template


def register_main_routes(app):
    """
    注册主页面路由
    
    Args:
        app: Flask应用实例
    """
    
    @app.route('/')
    def index():
        """主页"""
        return render_template('index.html')
    
    @app.route('/editor')
    def editor():
        """编辑器页面"""
        return render_template('editor.html')