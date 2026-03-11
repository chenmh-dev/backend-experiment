import time
import uuid
import os
from flask import Flask, g, request
from .errors import register_error_handlers
from .db import init_db, close_db
from .logging_utils import setup_logging
from .config import ProductionConfig, DevelopmentConfig
def create_app():
    # 创建app
    app = Flask(__name__)

    # 加载配置文件
    env = os.getenv("APP_ENV", "development").lower()
    if env == "production":
        app.config.from_object(ProductionConfig)
    else:
        app.config.from_object(DevelopmentConfig)

    # 初始化日志
    setup_logging(app)
    
    # 初始化数据库（只做一次建表）
    init_db()

    @app.before_request
    def _start_timer_and_request_id():
        g.start_time = time.time()
        g.request_id = uuid.uuid4().hex[:12]

    @app.after_request
    def _log_request(response):
        duration_ms = int((time.time() - getattr(g, "start_time", time.time())) * 1000)
        user_id = None
        if hasattr(g, "user") and isinstance(g.user, dict):
            user_id = g.user.get("user_id")
        
        # 写入响应头，便于前端/接口调用方报错时带回
        response.headers["X-Request-Id"] = g.request_id

        app.logger.info(
            f'{request.method} {request.path} status={response.status_code} '
            f'duration_mc={duration_ms} user_id={user_id}',
            extra={"request_id": g.request_id}
        )
        return response

    app.teardown_appcontext(close_db)

    # 注册蓝图
    from .routes import main
    from .blueprints.auth_routes import bp as auth_bp
    from .blueprints.posts_routes import bp as posts_bp
    from .blueprints.user_routes import bp as user_bp
    from .blueprints.comments_routes import bp as comment_bp
    from .blueprints.debug_routes import bp as debug_bp

    app.register_blueprint(main)
    app.register_blueprint(auth_bp)
    app.register_blueprint(posts_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(comment_bp)

    if app.config.get("ENV_NAME") == "development":
        app.register_blueprint(debug_bp)

    # 注册错误处理
    register_error_handlers(app)
    
    return app 