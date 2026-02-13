from flask import Blueprint, request, redirect, render_template_string
from .extensions import SessionLocal
from .models import Item

bp = Blueprint("main", __name__)

@bp.route("/", methods=["GET", "POST"])
def index():
    db = SessionLocal()

    if request.method == "POST":
        name = request.form["name"]
        item = Item(name=name)
        db.add(item)
        db.commit()
        return redirect("/")

    items = db.query(Item).all()
    db.close()

    return render_template_string("""
    <form method="post">
        <input name="name">
        <button type="submit">Save</button>
    </form>
    <ul>
    {% for item in items %}
        <li>{{ item.name }}</li>
    {% endfor %}
    </ul>
    """, items=items)
