import logging
from typing import Dict, Any, Union
from flask import Blueprint, request, redirect, render_template, flash
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from . import extensions
from .models import Item

logger = logging.getLogger(__name__)

bp = Blueprint("main", __name__)

@bp.route("/", methods=["GET", "POST"])
def index() -> Union[Dict[str, Any], str]:
    """名前の登録と一覧表示
    
    GET: 登録フォームと名前一覧を表示
    POST: 名前を登録し、GETにリダイレクト
    
    Returns:
        レンダリングされたHTMLまたはリダイレクトレスポンス
        
    Raises:
        RuntimeError: データベースセッションの初期化に失敗した場合
    """
    # SessionLocal をリアルタイムで参照（extensions モジュールから直接）
    try:
        db = extensions.get_session()
    except RuntimeError as e:
        logger.critical(f"Failed to get database session: {e}")
        flash("データベースエラーが発生しました。後でもう一度お試しください。", "error")
        raise

    try:
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            
            if not name:
                logger.warning("Empty name submitted")
                flash("名前を入力してください。", "warning")
                return redirect("/")
            
            try:
                item = Item(name=name)
                db.add(item)
                db.commit()
                logger.info(f"Item created: {name}")
                flash(f"'{name}' を登録しました。", "success")
                return redirect("/")
            
            except IntegrityError as e:
                # 重複エラーなどの制約違反
                db.rollback()
                logger.warning(f"Database integrity error: {e}")
                flash("その名前は既に登録されています。", "error")
                return redirect("/")
            
            except SQLAlchemyError as e:
                # その他のデータベースエラー
                db.rollback()
                logger.error(f"Database error: {e}")
                flash("データベースエラーが発生しました。後でもう一度お試しください。", "error")
                return redirect("/")

        items = db.query(Item).all()
        return render_template("index.html", items=items)
    
    except SQLAlchemyError as e:
        # クエリ実行中のエラー
        logger.error(f"Database error in index route: {e}")
        flash("データベースエラーが発生しました。", "error")
        raise
    
    except Exception as e:
        logger.error(f"Unexpected error in index route: {e}")
        raise
    
    finally:
        db.close()
