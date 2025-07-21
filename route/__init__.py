# Route module initialization
from .main_routes import register_main_routes
from .api_routes import register_api_routes
from .article_routes import register_article_routes
from .wechat_routes import register_wechat_routes

__all__ = [
    'register_main_routes',
    'register_api_routes', 
    'register_article_routes',
    'register_wechat_routes'
]