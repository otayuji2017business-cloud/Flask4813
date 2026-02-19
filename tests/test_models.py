"""モデルユニットテスト

SQLAlchemy のモデル定義をテストします。
"""

import logging
from typing import Generator
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.models import Base, Item

logger = logging.getLogger(__name__)


@pytest.fixture
def db_session() -> Generator[Session, None, None]:
    """モデルテスト用データベースセッション
    
    コンテキストマネージャなしで SQLAlchemy を使用するテストケーション
    """
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = SessionLocal()
    
    yield session
    
    session.close()
    Base.metadata.drop_all(engine)


class TestItemModel:
    """Item モデルのテストクラス"""
    
    def test_item_creation(self, db_session: Session) -> None:
        """新規アイテムを作成できることをテスト
        
        Args:
            db_session: テスト用データベースセッション
        """
        item = Item(name="Test Name")
        db_session.add(item)
        db_session.commit()
        
        assert item.id is not None
        assert item.name == "Test Name"
        logger.info(f"Item created successfully: id={item.id}, name={item.name}")
    
    def test_item_retrieval(self, db_session: Session) -> None:
        """データベースに保存したアイテムを取得できることをテスト
        
        Args:
            db_session: テスト用データベースセッション
        """
        item = Item(name="Retrieval Test")
        db_session.add(item)
        db_session.commit()
        
        retrieved = db_session.query(Item).filter_by(name="Retrieval Test").first()
        
        assert retrieved is not None
        assert retrieved.name == "Retrieval Test"
        logger.info("Item retrieved successfully from database")
    
    def test_item_list(self, db_session: Session) -> None:
        """複数のアイテムをクエリできることをテスト
        
        Args:
            db_session: テスト用データベースセッション
        """
        items_data = ["Alice", "Bob", "Charlie"]
        for name in items_data:
            item = Item(name=name)
            db_session.add(item)
        db_session.commit()
        
        items = db_session.query(Item).all()
        
        assert len(items) == 3
        names = [item.name for item in items]
        assert names == items_data
        logger.info(f"Listed {len(items)} items from database")
    
    def test_item_name_field(self, db_session: Session) -> None:
        """アイテムの name フィールドが正しく保存されることをテスト
        
        Args:
            db_session: テスト用データベースセッション
        """
        name = "Field Test" * 10  # 110文字（最大255）
        item = Item(name=name)
        db_session.add(item)
        db_session.commit()
        
        retrieved = db_session.query(Item).filter_by(id=item.id).first()
        
        assert retrieved is not None
        assert retrieved.name == name
        logger.info("Item name field preserved correctly")
