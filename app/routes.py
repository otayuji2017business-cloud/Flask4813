import logging
from typing import Dict, Any
from flask import Blueprint, request, redirect, render_template
from . import extensions
from .models import Item

logger = logging.getLogger(__name__)

bp = Blueprint("main", __name__)

@bp.route("/", methods=["GET", "POST"])
def index() -> Dict[str, Any] | str:
    """名前の登録と一覧表示
    
    GET: 登録フォームと名前一覧を表示
    POST: 名前を登録し、GETにリダイレクト
    
    Returns:
        レンダリングされたHTMLまたはリダイレクトレスポンス
    """
    # SessionLocal をリアルタイムで参照（extensions モジュールから直接）
    db = extensions.SessionLocal()

    try:
        if request.method == "POST":
            name = request.form.get("name", "").strip()
            
            if not name:
                logger.warning("Empty name submitted")
                return redirect("/")
            
            item = Item(name=name)
            db.add(item)
            db.commit()
            logger.info(f"Item created: {name}")
            return redirect("/")

        items = db.query(Item).all()
        return render_template("index.html", items=items)
    
    except Exception as e:
        logger.error(f"Error in index route: {e}")
        db.rollback()
        raise
    finally:
        db.close()
