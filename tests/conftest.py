"""テスト共通設定

pytest が実行するテスト全体で使用されるフィクスチャと設定を定義します。
"""

import logging
from typing import Generator, Any
import pytest
from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app import create_app
from app.extensions import init_engine
from app.models import Base

logger = logging.getLogger(__name__)


@pytest.fixture
def test_app() -> Flask:
    """テスト用 Flask アプリケーション
    
    SQLite in-memory データベースを使用し、
    本番環境に依存しないテスト環境を提供します。
    
    テスト時も呼ばれるため、init_db=False でデータベース初期化をスキップします。
    実際の DB 初期化は client フィクスチャで行います。
    
    Returns:
        テスト用に設定された Flask アプリケーション
    """
    # テスト用に DB 環境変数を設定（create_app 前に設定）
    import os
    os.environ["FLASK_ENV"] = "test"
    
    # init_db=False でデータベース初期化をスキップ
    app = create_app(init_db=False)
    app.config["TESTING"] = True
    app.config["SECRET_KEY"] = "test-secret-key"
    
    logger.info("Test Flask app created with test configuration (DB init skipped)")
    
    return app


@pytest.fixture
def test_db(test_app: Flask) -> Generator[Session, None, None]:
    """テスト用データベースセッション（モデルテスト専用）
    
    各テストケースの前に：
    1. SQLite in-memory エンジンを初期化
    2. テーブルを作成
    
    テスト終了後：
    1. セッションをクローズ
    2. テーブルをドロップ（ロールバック）
    
    このフィクスチャはモデルテストで使用します。
    ルートテストですては、client フィクスチャを使用してください。
    
    Yields:
        SQLAlchemy Session オブジェクト
    """
    with test_app.app_context():
        # SQLite in-memory エンジン初期化
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        
        SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        db = SessionLocal()
        
        logger.info("Test database session created (model tests)")
        
        yield db
        
        db.close()
        Base.metadata.drop_all(engine)
        logger.info("Test database session closed and tables dropped")


@pytest.fixture
def client(test_app: Flask) -> Any:
    """テスト用 Flask test client
    
    HTTP リクエストをシミュレートしてルートをテストするために使用します。
    テスト用の in-memory SQLite データベースを設定し、
    各テスト終了後には自動でクリーンアップします。
    
    Args:
        test_app: テスト用 Flask アプリケーション
    
    Yields:
        Flask test client
    """
    import app.extensions as ext
    from app.models import Base
    
    # テスト用 in-memory DB を初期化
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    
    # SessionLocal を設定
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    
    # グローバル extensions に設定
    ext.engine = engine
    ext.SessionLocal = SessionLocal
    
    logger.info("Flask test client initialized with in-memory database")
    
    test_client = test_app.test_client()
    
    yield test_client
    
    # クリーンアップ
    logger.info("Cleaning up test database")
    engine.dispose()
    ext.engine = None
    ext.SessionLocal = None
    logger.info("Flask test client cleaned up")
