import logging
from typing import Optional
from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session

logger = logging.getLogger(__name__)

engine: Optional[Engine] = None
SessionLocal: Optional[sessionmaker] = None

def init_engine(database_url: str) -> None:
    """SQLAlchemy エンジンを初期化
    
    アプリケーション起動時に1回のみ呼び出される。
    データベース接続プールを設定し、SessionLocal を初期化する。
    
    Args:
        database_url: データベース接続URL
        
    Raises:
        RuntimeError: エンジン初期化に失敗した場合
    """
    global engine, SessionLocal
    
    try:
        logger.info(f"Initializing database engine with URL: {database_url[:50]}...")
        
        engine = create_engine(
            database_url,
            pool_size=5,
            max_overflow=2,
            pool_pre_ping=True,
            pool_recycle=1800,
            echo=False,
            future=True
        )
        
        SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
        logger.info("Database engine initialization completed successfully")
        
    except Exception as e:
        logger.error(f"Failed to initialize database engine: {e}")
        raise RuntimeError(f"Database initialization failed: {e}") from e
