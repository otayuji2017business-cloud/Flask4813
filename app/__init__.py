import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .extensions import init_engine, SessionLocal
from .routes import bp

csrf = CSRFProtect()

def create_app(init_db: bool = True) -> Flask:
    """Flask アプリケーションファクトリ
    
    Args:
        init_db: データベースエンジンを初期化するか（テスト時は False）
    
    Returns:
        Flask: 初期化された Flask アプリケーション
    """
    app = Flask(__name__)

    from config import get_config
    app.config.from_object(get_config())

    # CSRF 保護を初期化
    csrf.init_app(app)

    # Engine 初期化（起動時 1 回）
    # テスト時は init_db=False で init_engine の呼び出しをスキップ
    if init_db:
        init_engine(app.config["DATABASE_URL"])

    # Blueprint 登録
    app.register_blueprint(bp)

    return app
