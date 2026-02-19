import logging
from typing import Optional
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

logger = logging.getLogger(__name__)

engine: Optional[Engine] = None
SessionLocal: Optional[sessionmaker] = None
_initialized: bool = False


def init_engine(database_url: str) -> None:
    """SQLAlchemy エンジンを初期化

    アプリケーション起動時に1回のみ呼び出される。
    データベース接続プールを設定し、SessionLocal を初期化する。

    Args:
        database_url: データベース接続URL

    Raises:
        RuntimeError: エンジン初期化に失敗した場合
    """
    global engine, SessionLocal, _initialized

    if _initialized:
        logger.warning("Database engine already initialized, skipping")
        return

    try:
        logger.info(f"Initializing database engine with URL: {database_url[:50]}...")

        # SQLite の場合とそれ以外で設定を分ける
        if "sqlite://" in database_url:
            # SQLite では pool_size, max_overflow が使用不可
            engine = create_engine(database_url, echo=False, future=True)
        else:
            # MySQL など実サーバーの場合
            engine = create_engine(
                database_url,
                pool_size=5,
                max_overflow=2,
                pool_pre_ping=True,
                pool_recycle=1800,
                echo=False,
                future=True,
            )

        SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        _initialized = True
        logger.info("Database engine initialization completed successfully")

    except Exception as e:
        logger.error(f"Failed to initialize database engine: {e}")
        raise RuntimeError(f"Database initialization failed: {e}") from e


def get_session() -> Session:
    """SessionLocal インスタンスを取得

    SessionLocal が初期化されていない場合は RuntimeError を発生させます。
    ルートハンドラーはこのメソッドを使用して安全にセッションを取得します。

    Returns:
        SQLAlchemy Session インスタンス

    Raises:
        RuntimeError: SessionLocal が未初期化の場合
    """
    if SessionLocal is None:
        logger.error("SessionLocal is not initialized. Call init_engine() first.")
        raise RuntimeError(
            "Database session factory not initialized. Call init_engine() first."
        )

    return SessionLocal()
