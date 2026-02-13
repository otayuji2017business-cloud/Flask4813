import os
from flask import Flask
from .extensions import init_engine, SessionLocal
from .routes import bp

def create_app():
    app = Flask(__name__)

    from config import get_config
    app.config.from_object(get_config())

    # Engine初期化（起動時1回）
    init_engine(app.config["DATABASE_URL"])

    # Blueprint登録
    app.register_blueprint(bp)

    return app
