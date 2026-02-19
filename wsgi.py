"""WSGI アプリケーション エントリポイント

Gunicorn などのWSGIサーバーがこのモジュールを読み込み、
app オブジェクトを通じてリクエストを処理します。
"""

from flask import Flask
from app import create_app

app: Flask = create_app()
"""WSGI対応の Flask アプリケーション"""
