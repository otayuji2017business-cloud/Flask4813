"""テスト共通設定

pytest が実行するテスト全体で使用されるフィクスチャと設定を定義します。
"""

import logging
from typing import Generator
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
    
    Yields:
        テスト用に設定された Flask アプリケーション
    """
    app = create_app()
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["SECRET_KEY"] = "test-secret-key"
    
    logger.info("Test Flask app created with in-memory SQLite database")
    
    return app


@pytest.fixture
def test_db(test_app: Flask) -> Generator[Session, None, None]:
    """テスト用データベースセッション
    
    各テストケースの前に：
    1. SQLite in-memory エンジンを初期化
    2. テーブルを作成
    
    テスト終了後：
    1. セッションをクローズ
    2. テーブルをドロップ（ロールバック）
    
    Yields:
        SQLAlchemy Session オブジェクト
    """
    with test_app.app_context():
        # SQLite in-memory エンジン初期化
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        
        SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        db = SessionLocal()
        
        logger.info("Test database session created")
        
        yield db
        
        db.close()
        Base.metadata.drop_all(engine)
        logger.info("Test database session closed and tables dropped")


@pytest.fixture
def client(test_app: Flask, test_db: Session):
    """テスト用 Flask test client
    
    HTTP リクエストをシミュレートしてルートをテストするために使用します。
    
    Args:
        test_app: テスト用 Flask アプリケーション
        test_db: テスト用データベースセッション
    
    Returns:
        Flask test client
    """
    # test_db をアプリケーションに注入（routes.py から利用可能にする）
    with test_app.app_context():
        # グローバル engine と SessionLocal を設定
        from app.extensions import engine as global_engine, SessionLocal as global_session
        import app.extensions as ext
        
        ext.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(ext.engine)
        ext.SessionLocal = sessionmaker(bind=ext.engine, autoflush=False, autocommit=False)
        
        yield test_app.test_client()
        
        ext.engine.dispose()
