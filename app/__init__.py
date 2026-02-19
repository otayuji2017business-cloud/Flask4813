import os
from flask import Flask
from flask_wtf.csrf import CSRFProtect
from .extensions import init_engine, SessionLocal
from .routes import bp

csrf = CSRFProtect()

def create_app() -> Flask:
    """Flaskアプリケーションファクトリ
    
    Returns:
        Flask: 初期化されたFlaskアプリケーション
    """
    app = Flask(__name__)

    from config import get_config
    app.config.from_object(get_config())

    # CSRF保護を初期化
    csrf.init_app(app)

    # Engine初期化（起動時1回）
    init_engine(app.config["DATABASE_URL"])

    # Blueprint登録
    app.register_blueprint(bp)

    return app
