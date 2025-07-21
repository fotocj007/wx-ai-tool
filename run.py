#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
启动脚本
用于启动VX Tool应用
"""

import os
import sys
import argparse
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from app import VXToolApp
from core.logger import get_logger, cleanup_old_logs
from core.config import get_config


def check_dependencies():
    """
    检查依赖是否安装
    """
    required_packages = [
        'flask',
        'flask_cors',
        'google.generativeai',
        'markdown',
        'bs4',
        'requests',
        'configparser'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print("❌ 缺少以下依赖包:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\n请运行以下命令安装依赖:")
        print("pip install -r requirements.txt")
        return False
    
    return True


def check_config():
    """
    检查配置文件
    """
    config_file = "config.ini"
    if not os.path.exists(config_file):
        print(f"❌ 配置文件不存在: {config_file}")
        print("请确保config.ini文件存在并包含正确的配置信息")
        return False
    
    try:
        config = get_config()
        # 检查关键配置
        gemini_key = config.get_gemini_api_key()
        wechat_config = config.get_wechat_config()
        
        if not gemini_key:
            print("❌ Gemini API Key未配置")
            return False
        
        if not all([wechat_config['appid'], wechat_config['appsecret']]):
            print("❌ 微信配置不完整")
            return False
        
        print("✅ 配置文件检查通过")
        return True
        
    except Exception as e:
        print(f"❌ 配置文件检查失败: {e}")
        return False


def create_directories():
    """
    创建必要的目录
    """
    directories = ['logs', 'articles', 'templates']
    
    for directory in directories:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(f"✅ 创建目录: {directory}")


def main():
    """
    主函数
    """
    parser = argparse.ArgumentParser(description='VX Tool - 微信公众号热点文章AI生成与发布系统')
    parser.add_argument('--host', default='0.0.0.0', help='服务器主机地址 (默认: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000, help='服务器端口 (默认: 5000)')
    parser.add_argument('--debug', action='store_true',default=False, help='启用调试模式')
    parser.add_argument('--check-only', action='store_true', help='仅检查环境，不启动服务')
    
    args = parser.parse_args()
    
    print("🚀 VX Tool - 微信公众号热点文章AI生成与发布系统")
    print("=" * 60)
    
    # 1. 检查依赖
    print("📦 检查依赖包...")
    if not check_dependencies():
        sys.exit(1)
    print("✅ 依赖包检查通过")
    
    # 2. 创建必要目录
    print("📁 创建必要目录...")
    create_directories()
    
    # 3. 检查配置
    print("⚙️ 检查配置文件...")
    if not check_config():
        sys.exit(1)
    
    # 4. 清理旧日志
    print("🧹 清理旧日志文件...")
    try:
        cleanup_old_logs()
        print("✅ 日志清理完成")
    except Exception as e:
        print(f"⚠️ 日志清理失败: {e}")
    
    if args.check_only:
        print("\n✅ 环境检查完成，所有组件正常！")
        return
    
    # 5. 启动应用
    try:
        print(f"\n🌟 启动VX Tool服务...")
        print(f"📍 服务地址: http://{args.host}:{args.port}")
        print(f"🔧 调试模式: {'开启' if args.debug else '关闭'}")
        print("\n按 Ctrl+C 停止服务")
        print("=" * 60)
        
        app = VXToolApp()
        app.run(host=args.host, port=args.port, debug=args.debug)
        
    except KeyboardInterrupt:
        print("\n\n👋 服务已停止")
    except Exception as e:
        logger = get_logger()
        logger.error(f"启动失败: {e}")
        print(f"❌ 启动失败: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()