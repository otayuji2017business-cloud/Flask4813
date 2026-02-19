"""SQLAlchemy モデル定義

このモジュールはアプリケーションで使用するデータベーステーブルの
ORM モデルを定義します。
"""

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer

class Base(DeclarativeBase):
    """SQLAlchemy ORM の基底クラス
    
    すべてのモデルはこのクラスを継承します。
    """
    pass

class Item(Base):
    """名前を登録するためのアイテムモデル
    
    ユーザーが入力した名前を保存するテーブルに対応します。
    
    Attributes:
        id: プライマリキー（自動採番）
        name: ユーザーが入力した名前（255文字以下）
    """
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
