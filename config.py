"""Flask アプリケーション設定

環境（開発/本番）に応じた設定を管理します。
"""

import os
from typing import Type, Union
from dotenv import load_dotenv

load_dotenv()


class ProdConfig:
    """本番環境の設定

    Cloud Run での本番運用を想定した設定。
    機密情報は環境変数から取得します。
    """

    DB_PASSWORD: str = os.environ.get("DB_PASSWORD", "")

    if not DB_PASSWORD:
        raise RuntimeError("DB_PASSWORD environment variable not set")

    SECRET_KEY: str = os.environ.get("SECRET_KEY", "")
    if not SECRET_KEY:
        raise RuntimeError("SECRET_KEY environment variable not set")

    DATABASE_URL: str = (
        f"mysql+pymysql://appuser:{DB_PASSWORD}"
        f"@/appdb"
        f"?unix_socket=/cloudsql/platinum-linker-487308-t8:asia-northeast1:flask-mysql"
    )


class DevelopmentConfig:
    """開発環境の設定

    ローカル開発用の設定。
    SQLite in-memory を使用してテストします。
    """

    SECRET_KEY: str = os.environ.get(
        "SECRET_KEY", "dev-secret-key-change-in-production"
    )
    DATABASE_URL: str = "sqlite:///app.db"


class TestConfig:
    """テスト環境の設定

    pytest 実行時の設定。
    SQLite in-memory を使用してテストします。
    """

    SECRET_KEY: str = "test-secret-key"
    DATABASE_URL: str = "sqlite:///:memory:"


def get_config() -> Union[Type[ProdConfig], Type[DevelopmentConfig], Type[TestConfig]]:
    """環境に応じた設定クラスを返す

    FLASK_ENV 環境変数により以下のように判定します：
    - "production": ProdConfig
    - "test": TestConfig
    - その他: DevelopmentConfig（デフォルト）

    Returns:
        設定クラス（ProdConfig、TestConfig または DevelopmentConfig）
    """
    env = os.environ.get("FLASK_ENV", "development")
    if env == "production":
        return ProdConfig
    elif env == "test":
        return TestConfig
    return DevelopmentConfig
