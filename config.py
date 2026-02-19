import os
from dotenv import load_dotenv

load_dotenv()

class ProdConfig:
    """本番環境の設定"""
    DB_PASSWORD = os.environ.get("DB_PASSWORD")

    if not DB_PASSWORD:
        raise RuntimeError("DB_PASSWORD environment variable not set")

    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY environment variable not set")

    DATABASE_URL = (
        f"mysql+pymysql://appuser:{DB_PASSWORD}"
        f"@/appdb"
        f"?unix_socket=/cloudsql/platinum-linker-487308-t8:asia-northeast1:flask-mysql"
    )

class DevelopmentConfig:
    """開発環境の設定"""
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    DATABASE_URL = "sqlite:///app.db"

def get_config():
    """環境に応じた設定を返す"""
    env = os.environ.get("FLASK_ENV", "development")
    if env == "production":
        return ProdConfig
    return DevelopmentConfig
