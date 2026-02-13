from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = None
SessionLocal = None

def init_engine(database_url):
    global engine, SessionLocal

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
