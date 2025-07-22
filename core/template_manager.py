# -*- coding: utf-8 -*-
"""
模板管理器
负责管理所有HTML样式模板
"""

class TemplateManager:
    """
    模板管理器类
    负责提供和管理各种HTML样式模板
    """
    
    def __init__(self):
        """
        初始化模板管理器
        """
        pass
    
    def get_style_templates(self) -> dict:
        """
        获取多种样式模板
        
        Returns:
            dict: 包含多种样式模板的字典
        """
        return {
            # 科技蓝色主题 - 现代科技感
            'tech_blue': {
                'name': '科技蓝色主题',
                'container': 'max-width: 100%; margin: 0 auto; padding: 5px; font-family: "Microsoft YaHei", "PingFang SC", sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #ffffff; line-height: 1.6; border-radius: 10px;',
                'styles': {
                    'h1': 'font-size: 28px; font-weight: bold; color: #00d4ff; margin: 30px 0 20px; padding: 15px; background: rgba(0, 212, 255, 0.1); border-radius: 8px; text-align: center; border: 2px solid #00d4ff;',
                    'h2': 'font-size: 22px; font-weight: bold; color: #00d4ff; margin: 25px 0 15px; padding-left: 15px; border-left: 4px solid #00d4ff; background: rgba(0, 212, 255, 0.05);',
                    'h3': 'font-size: 20px; font-weight: bold; color: #66d9ff; margin: 20px 0 10px; padding-left: 10px; border-left: 3px solid #66d9ff;',
                    'h4': 'font-size: 18px; font-weight: bold; color: #99e6ff; margin: 15px 0 8px;',
                    'p': 'font-size: 16px; color: #000000; line-height: 1.8; margin-bottom: 15px; text-align: justify;',
                    'strong': 'color: #00ff88; font-weight: bold; text-shadow: 0 0 5px rgba(0, 255, 136, 0.3);',
                    'em': 'color: #ffaa00; font-style: italic;',
                    'ul': 'padding-left: 20px; margin: 15px 0;',
                    'ol': 'padding-left: 20px; margin: 15px 0;',
                    'li': 'margin-bottom: 8px; line-height: 1.6; color: #000000;',
                    'blockquote': 'border-left: 4px solid #00d4ff; padding: 15px; color: #b3ecff; font-style: italic; margin: 15px 0; background: rgba(0, 212, 255, 0.1); border-radius: 5px;',
                    'code': 'background: rgba(0, 0, 0, 0.3); padding: 3px 6px; border-radius: 4px; font-family: "Consolas", "Monaco", monospace; color: #00ff88; border: 1px solid #00d4ff;',
                    'pre': 'background: rgba(0, 0, 0, 0.4); padding: 20px; border-radius: 8px; border: 1px solid #00d4ff; overflow-x: auto; margin: 15px 0; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);',
                    'a': 'color: #00ff88; text-decoration: none; border-bottom: 1px dotted #00ff88;',
                    'img': 'max-width: 100%; height: auto; display: block; margin: 15px auto; border-radius: 8px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);',
                    'table': 'border-collapse: collapse; width: 100%; margin: 15px 0; background: rgba(255, 255, 255, 0.1); border-radius: 8px; overflow: hidden;',
                    'th': 'border: 1px solid #00d4ff; padding: 12px; background: rgba(0, 212, 255, 0.2); font-weight: bold; text-align: center; color: #00d4ff;',
                    'td': 'border: 1px solid #66d9ff; padding: 10px; text-align: left; color: #000000;',
                    'hr': 'border: none; height: 2px; background: linear-gradient(90deg, #00d4ff, #66d9ff, #00d4ff); margin: 20px 0; border-radius: 1px;'
                }
            },
            
            # 温馨橙色主题 - 温暖亲和
            'warm_orange': {
                'name': '温馨橙色主题',
                'container': 'max-width: 100%; margin: 0 auto; padding: 5px; font-family: "Microsoft YaHei", "PingFang SC", serif; background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%); color: #5d4037; line-height: 1.7; border-radius: 15px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);',
                'styles': {
                    'h1': 'font-size: 26px; font-weight: bold; color: #d84315; margin: 30px 0 20px; padding: 20px; background: #fff3e0; border-radius: 12px; text-align: center; border: 3px solid #ff8a65; box-shadow: 0 4px 8px rgba(216, 67, 21, 0.2);',
                    'h2': 'font-size: 22px; font-weight: bold; color: #e65100; margin: 25px 0 15px; padding: 12px 20px; background: #fff8f5; border-radius: 8px; border-left: 5px solid #ff8a65;',
                    'h3': 'font-size: 20px; font-weight: bold; color: #f57c00; margin: 20px 0 10px; padding-left: 15px; border-left: 4px solid #ffab40;',
                    'h4': 'font-size: 18px; font-weight: bold; color: #ff9800; margin: 15px 0 8px;',
                    'p': 'font-size: 16px; color: #5d4037; line-height: 1.8; margin-bottom: 16px; text-align: justify;',
                    'strong': 'color: #d84315; font-weight: bold; background: rgba(255, 138, 101, 0.2); padding: 2px 4px; border-radius: 3px;',
                    'em': 'color: #f57c00; font-style: italic; background: rgba(255, 171, 64, 0.2); padding: 1px 3px; border-radius: 2px;',
                    'ul': 'padding-left: 25px; margin: 15px 0;',
                    'ol': 'padding-left: 25px; margin: 15px 0;',
                    'li': 'margin-bottom: 10px; line-height: 1.7; color: #5d4037;',
                    'blockquote': 'border-left: 5px solid #ff8a65; padding: 20px; color: #6d4c41; font-style: italic; margin: 20px 0; background: #fff8f5; border-radius: 8px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);',
                    'code': 'background: #fff3e0; padding: 4px 8px; border-radius: 4px; font-family: "Consolas", "Monaco", monospace; color: #d84315; border: 1px solid #ffcc80;',
                    'pre': 'background: #fff8f5; padding: 20px; border-radius: 10px; border: 2px solid #ffcc80; overflow-x: auto; margin: 20px 0; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);',
                    'a': 'color: #d84315; text-decoration: none; border-bottom: 2px solid #ff8a65; transition: all 0.3s ease;',
                    'img': 'max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 12px; box-shadow: 0 6px 20px rgba(0, 0, 0, 0.15);',
                    'table': 'border-collapse: collapse; width: 100%; margin: 20px 0; background: #fff8f5; border-radius: 10px; overflow: hidden; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);',
                    'th': 'border: 1px solid #ffcc80; padding: 15px; background: #fff3e0; font-weight: bold; text-align: center; color: #d84315;',
                    'td': 'border: 1px solid #ffcc80; padding: 12px; text-align: left; color: #5d4037;',
                    'hr': 'border: none; height: 3px; background: linear-gradient(90deg, #ff8a65, #ffab40, #ff8a65); margin: 25px 0; border-radius: 2px;'
                }
            },
            
            # 商务灰色主题 - 专业商务
            'business_gray': {
                'name': '商务灰色主题',
                'container': 'max-width: 100%; margin: 0 auto; padding: 5px; font-family: "Microsoft YaHei", "Helvetica Neue", Arial, sans-serif; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); color: #2c3e50; line-height: 1.6; border-radius: 8px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);',
                'styles': {
                    'h1': 'font-size: 28px; font-weight: 700; color: #2c3e50; margin: 35px 0 25px; padding: 25px; background: #ffffff; border-radius: 6px; text-align: center; border-top: 4px solid #3498db; box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);',
                    'h2': 'font-size: 24px; font-weight: 600; color: #34495e; margin: 30px 0 20px; padding: 15px 25px; background: #ecf0f1; border-radius: 4px; border-left: 4px solid #3498db;',
                    'h3': 'font-size: 20px; font-weight: 600; color: #34495e; margin: 25px 0 15px; padding-left: 20px; border-left: 3px solid #95a5a6;',
                    'h4': 'font-size: 18px; font-weight: 500; color: #7f8c8d; margin: 20px 0 10px;',
                    'p': 'font-size: 16px; color: #2c3e50; line-height: 1.8; margin-bottom: 18px; text-align: justify;',
                    'strong': 'color: #e74c3c; font-weight: 600; background: rgba(231, 76, 60, 0.1); padding: 2px 4px; border-radius: 2px;',
                    'em': 'color: #3498db; font-style: italic; background: rgba(52, 152, 219, 0.1); padding: 1px 3px; border-radius: 2px;',
                    'ul': 'padding-left: 30px; margin: 20px 0;',
                    'ol': 'padding-left: 30px; margin: 20px 0;',
                    'li': 'margin-bottom: 10px; line-height: 1.7; color: #2c3e50;',
                    'blockquote': 'border-left: 4px solid #3498db; padding: 20px 25px; color: #7f8c8d; font-style: italic; margin: 25px 0; background: #ffffff; border-radius: 4px; box-shadow: 0 2px 5px rgba(0, 0, 0, 0.05);',
                    'code': 'background: #ecf0f1; padding: 4px 8px; border-radius: 3px; font-family: "Consolas", "Monaco", monospace; color: #e74c3c; border: 1px solid #bdc3c7;',
                    'pre': 'background: #ffffff; padding: 25px; border-radius: 6px; border: 1px solid #bdc3c7; overflow-x: auto; margin: 25px 0; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);',
                    'a': 'color: #3498db; text-decoration: none; border-bottom: 1px solid #3498db; transition: all 0.3s ease;',
                    'img': 'max-width: 100%; height: auto; display: block; margin: 25px auto; border-radius: 6px; box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);',
                    'table': 'border-collapse: collapse; width: 100%; margin: 25px 0; background: #ffffff; border-radius: 6px; overflow: hidden; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);',
                    'th': 'border: 1px solid #bdc3c7; padding: 15px; background: #ecf0f1; font-weight: 600; text-align: center; color: #2c3e50;',
                    'td': 'border: 1px solid #bdc3c7; padding: 12px; text-align: left; color: #2c3e50;',
                    'hr': 'border: none; height: 2px; background: linear-gradient(90deg, #3498db, #95a5a6, #3498db); margin: 30px 0; border-radius: 1px;'
                }
            },
            
            # 娱乐粉色主题 - 活泼时尚
            'entertainment_pink': {
                'name': '娱乐粉色主题',
                'container': 'max-width: 100%; margin: 0 auto; padding: 5px; font-family: "Microsoft YaHei", "Comic Sans MS", cursive; background: linear-gradient(135deg, #ffeef8 0%, #f8d7da 100%); color: #6f2c91; line-height: 1.7; border-radius: 20px; box-shadow: 0 8px 25px rgba(255, 105, 180, 0.2);',
                'styles': {
                    'h1': 'font-size: 26px; font-weight: bold; color: #e91e63; margin: 30px 0 20px; padding: 20px; background: linear-gradient(45deg, #ff69b4, #ff1493); color: white; border-radius: 15px; text-align: center; box-shadow: 0 6px 15px rgba(233, 30, 99, 0.3); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);',
                    'h2': 'font-size: 22px; font-weight: bold; color: #c2185b; margin: 25px 0 15px; padding: 15px 20px; background: #fce4ec; border-radius: 12px; border: 2px solid #f48fb1; box-shadow: 0 3px 8px rgba(196, 24, 91, 0.2);',
                    'h3': 'font-size: 20px; font-weight: bold; color: #ad1457; margin: 20px 0 10px; padding-left: 15px; border-left: 5px solid #f48fb1; background: linear-gradient(90deg, #fce4ec, transparent);',
                    'h4': 'font-size: 18px; font-weight: bold; color: #880e4f; margin: 15px 0 8px;',
                    'p': 'font-size: 16px; color: #6f2c91; line-height: 1.8; margin-bottom: 16px; text-align: justify;',
                    'strong': 'color: #e91e63; font-weight: bold; background: linear-gradient(45deg, #ff69b4, #ff1493); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0 0 10px rgba(233, 30, 99, 0.5);',
                    'em': 'color: #9c27b0; font-style: italic; background: rgba(156, 39, 176, 0.1); padding: 2px 4px; border-radius: 4px;',
                    'ul': 'padding-left: 25px; margin: 15px 0;',
                    'ol': 'padding-left: 25px; margin: 15px 0;',
                    'li': 'margin-bottom: 10px; line-height: 1.7; color: #6f2c91; position: relative;',
                    'blockquote': 'border-left: 5px solid #f48fb1; padding: 20px; color: #8e24aa; font-style: italic; margin: 20px 0; background: linear-gradient(135deg, #fce4ec, #f3e5f5); border-radius: 12px; box-shadow: 0 4px 12px rgba(244, 143, 177, 0.3);',
                    'code': 'background: linear-gradient(45deg, #fce4ec, #f3e5f5); padding: 4px 8px; border-radius: 6px; font-family: "Consolas", "Monaco", monospace; color: #e91e63; border: 2px solid #f48fb1;',
                    'pre': 'background: linear-gradient(135deg, #fce4ec, #f3e5f5); padding: 20px; border-radius: 15px; border: 2px solid #f48fb1; overflow-x: auto; margin: 20px 0; box-shadow: 0 6px 15px rgba(244, 143, 177, 0.3);',
                    'a': 'color: #e91e63; text-decoration: none; border-bottom: 2px dotted #f48fb1; transition: all 0.3s ease;',
                    'img': 'max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 15px; box-shadow: 0 8px 20px rgba(233, 30, 99, 0.2); border: 3px solid #f48fb1;',
                    'table': 'border-collapse: collapse; width: 100%; margin: 20px 0; background: linear-gradient(135deg, #fce4ec, #f3e5f5); border-radius: 12px; overflow: hidden; box-shadow: 0 6px 15px rgba(244, 143, 177, 0.2);',
                    'th': 'border: 2px solid #f48fb1; padding: 15px; background: linear-gradient(45deg, #ff69b4, #ff1493); font-weight: bold; text-align: center; color: white; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);',
                    'td': 'border: 1px solid #f48fb1; padding: 12px; text-align: left; color: #6f2c91;',
                    'hr': 'border: none; height: 4px; background: linear-gradient(90deg, #ff69b4, #ff1493, #9c27b0, #ff69b4); margin: 25px 0; border-radius: 2px; box-shadow: 0 2px 4px rgba(233, 30, 99, 0.3);'
                }
            },
            
            # 自然绿色主题 - 清新自然
            'nature_green': {
                'name': '自然绿色主题',
                'container': 'max-width: 100%; margin: 0 auto; padding: 5px; font-family: "Microsoft YaHei", "Georgia", serif; background: linear-gradient(135deg, #e8f5e8 0%, #c8e6c9 100%); color: #2e7d32; line-height: 1.7; border-radius: 12px; box-shadow: 0 8px 25px rgba(76, 175, 80, 0.2);',
                'styles': {
                    'h1': 'font-size: 26px; font-weight: bold; color: #1b5e20; margin: 30px 0 20px; padding: 20px; background: linear-gradient(45deg, #4caf50, #8bc34a); color: white; border-radius: 10px; text-align: center; box-shadow: 0 6px 15px rgba(27, 94, 32, 0.3); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);',
                    'h2': 'font-size: 22px; font-weight: bold; color: #2e7d32; margin: 25px 0 15px; padding: 15px 20px; background: #f1f8e9; border-radius: 8px; border: 2px solid #81c784; box-shadow: 0 3px 8px rgba(46, 125, 50, 0.2);',
                    'h3': 'font-size: 20px; font-weight: bold; color: #388e3c; margin: 20px 0 10px; padding-left: 15px; border-left: 5px solid #81c784; background: linear-gradient(90deg, #f1f8e9, transparent);',
                    'h4': 'font-size: 18px; font-weight: bold; color: #43a047; margin: 15px 0 8px;',
                    'p': 'font-size: 16px; color: #2e7d32; line-height: 1.8; margin-bottom: 16px; text-align: justify;',
                    'strong': 'color: #1b5e20; font-weight: bold; background: rgba(76, 175, 80, 0.2); padding: 2px 4px; border-radius: 3px;',
                    'em': 'color: #689f38; font-style: italic; background: rgba(139, 195, 74, 0.2); padding: 1px 3px; border-radius: 2px;',
                    'ul': 'padding-left: 25px; margin: 15px 0;',
                    'ol': 'padding-left: 25px; margin: 15px 0;',
                    'li': 'margin-bottom: 10px; line-height: 1.7; color: #2e7d32;',
                    'blockquote': 'border-left: 5px solid #81c784; padding: 20px; color: #558b2f; font-style: italic; margin: 20px 0; background: linear-gradient(135deg, #f1f8e9, #e8f5e8); border-radius: 8px; box-shadow: 0 4px 12px rgba(129, 199, 132, 0.3);',
                    'code': 'background: #f1f8e9; padding: 4px 8px; border-radius: 4px; font-family: "Consolas", "Monaco", monospace; color: #2e7d32; border: 1px solid #a5d6a7;',
                    'pre': 'background: #f1f8e9; padding: 20px; border-radius: 10px; border: 2px solid #a5d6a7; overflow-x: auto; margin: 20px 0; box-shadow: 0 6px 15px rgba(165, 214, 167, 0.3);',
                    'a': 'color: #2e7d32; text-decoration: none; border-bottom: 2px solid #81c784; transition: all 0.3s ease;',
                    'img': 'max-width: 100%; height: auto; display: block; margin: 20px auto; border-radius: 10px; box-shadow: 0 8px 20px rgba(46, 125, 50, 0.2); border: 2px solid #a5d6a7;',
                    'table': 'border-collapse: collapse; width: 100%; margin: 20px 0; background: #f1f8e9; border-radius: 10px; overflow: hidden; box-shadow: 0 6px 15px rgba(129, 199, 132, 0.2);',
                    'th': 'border: 1px solid #a5d6a7; padding: 15px; background: linear-gradient(45deg, #4caf50, #8bc34a); font-weight: bold; text-align: center; color: white; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);',
                    'td': 'border: 1px solid #a5d6a7; padding: 12px; text-align: left; color: #2e7d32;',
                    'hr': 'border: none; height: 3px; background: linear-gradient(90deg, #4caf50, #8bc34a, #4caf50); margin: 25px 0; border-radius: 2px; box-shadow: 0 2px 4px rgba(76, 175, 80, 0.3);'
                }
            },
            
            # 数字序列主题 - 1、2、3连续标题
            'numbered_sequence': {
                'name': '数字序列主题',
                'container': 'max-width: 100%; margin: 0 auto; padding: 5px; font-family: "Microsoft YaHei", "Arial", sans-serif; background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); color: #2c3e50; line-height: 1.7; border-radius: 15px; box-shadow: 0 10px 30px rgba(240, 147, 251, 0.3); counter-reset: section;',
                'styles': {
                    'h1': 'font-size: 28px; font-weight: bold; color: #ffffff; margin: 30px 0 25px; padding: 25px; background: linear-gradient(45deg, #667eea, #764ba2); border-radius: 12px; text-align: center; box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2); text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3); position: relative;',
                    'h2': 'font-size: 24px; font-weight: bold; color: #2c3e50; margin: 25px 0 20px; padding: 20px 20px 20px 70px; background: rgba(255, 255, 255, 0.9); border-radius: 10px; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1); position: relative; counter-increment: section; border-left: 5px solid #667eea;',
                    'h3': 'font-size: 20px; font-weight: bold; color: #34495e; margin: 20px 0 15px; padding: 15px 15px 15px 60px; background: rgba(255, 255, 255, 0.8); border-radius: 8px; position: relative; counter-increment: subsection; border-left: 4px solid #f5576c;',
                    'h4': 'font-size: 18px; font-weight: bold; color: #7f8c8d; margin: 15px 0 10px; padding: 10px 10px 10px 50px; background: rgba(255, 255, 255, 0.7); border-radius: 6px; position: relative; counter-increment: subsubsection; border-left: 3px solid #f093fb;',
                    'p': 'font-size: 16px; color: #2c3e50; line-height: 1.8; margin-bottom: 18px; text-align: justify; background: rgba(255, 255, 255, 0.6); padding: 15px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);',
                    'strong': 'color: #e74c3c; font-weight: bold; background: rgba(231, 76, 60, 0.2); padding: 3px 6px; border-radius: 4px;',
                    'em': 'color: #9b59b6; font-style: italic; background: rgba(155, 89, 182, 0.2); padding: 2px 4px; border-radius: 3px;',
                    'ul': 'padding-left: 30px; margin: 20px 0; background: rgba(255, 255, 255, 0.5); padding: 15px; border-radius: 8px;',
                    'ol': 'padding-left: 30px; margin: 20px 0; background: rgba(255, 255, 255, 0.5); padding: 15px; border-radius: 8px;',
                    'li': 'margin-bottom: 12px; line-height: 1.7; color: #2c3e50; position: relative;',
                    'blockquote': 'border-left: 5px solid #667eea; padding: 25px; color: #34495e; font-style: italic; margin: 25px 0; background: rgba(255, 255, 255, 0.8); border-radius: 10px; box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);',
                    'code': 'background: rgba(255, 255, 255, 0.9); padding: 5px 10px; border-radius: 6px; font-family: "Consolas", "Monaco", monospace; color: #e74c3c; border: 1px solid #bdc3c7;',
                    'pre': 'background: rgba(255, 255, 255, 0.9); padding: 25px; border-radius: 12px; border: 2px solid #bdc3c7; overflow-x: auto; margin: 25px 0; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);',
                    'a': 'color: #667eea; text-decoration: none; border-bottom: 2px solid #667eea; transition: all 0.3s ease;',
                    'img': 'max-width: 100%; height: auto; display: block; margin: 25px auto; border-radius: 12px; box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2); border: 3px solid #f5576c;',
                    'table': 'border-collapse: collapse; width: 100%; margin: 25px 0; background: rgba(255, 255, 255, 0.9); border-radius: 12px; overflow: hidden; box-shadow: 0 8px 25px rgba(0, 0, 0, 0.1);',
                    'th': 'border: 1px solid #bdc3c7; padding: 18px; background: linear-gradient(45deg, #667eea, #764ba2); font-weight: bold; text-align: center; color: #ffffff; text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.3);',
                    'td': 'border: 1px solid #bdc3c7; padding: 15px; text-align: left; color: #2c3e50;',
                    'hr': 'border: none; height: 4px; background: linear-gradient(90deg, #f093fb, #f5576c, #667eea, #f093fb); margin: 30px 0; border-radius: 2px; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);'
                }
            }
        }
    
    def get_available_templates(self) -> list:
        """
        获取可用的模板列表
        
        Returns:
            list: 包含模板信息的列表，每个元素包含name和description字段
        """
        templates = self.get_style_templates()
        return [
            {
                'name': key,
                'description': template['name']
            }
            for key, template in templates.items()
        ]
    
    def get_template_preview(self, template_name: str) -> dict:
        """
        获取模板预览信息
        
        Args:
            template_name: 模板名称
        
        Returns:
            dict: 模板预览信息
        """
        templates = self.get_style_templates()
        if template_name in templates:
            template = templates[template_name]
            return {
                'name': template['name'],
                'container_style': template['container'],
                'sample_styles': {
                    'h1': template['styles'].get('h1', ''),
                    'h2': template['styles'].get('h2', ''),
                    'p': template['styles'].get('p', '')
                }
            }
        return {}