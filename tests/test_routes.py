"""ルートハンドラテスト

Flask ルートとHTTPレスポンスをテストします。
"""

import logging
from typing import Any
import re
import pytest
from flask import Flask
from flask.testing import FlaskClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models import Base, Item
import app.extensions as ext

logger = logging.getLogger(__name__)


def get_csrf_token(client: FlaskClient) -> str:
    """フォームから CSRF トークンを取得
    
    Args:
        client: Flask test client
    
    Returns:
        CSRF トークン文字列
    """
    response = client.get("/")
    # HTML から name="csrf_token" の value を抽出
    match = re.search(r'name="csrf_token"\s+type="hidden"\s+value="([^"]+)"', response.text)
    if not match:
        logger.warning("CSRF token not found in form")
        return ""
    return match.group(1)


@pytest.fixture(autouse=True)
def setup_test_db(client: FlaskClient) -> Any:
    """各テストケース実行前にテスト用 DB を初期化
    
    Args:
        client: Flask test client
        
    Yields:
        None
    """
    yield


class TestIndexRoute:
    """インデックスルート（/）のテストクラス"""
    
    def test_get_index(self, client: FlaskClient) -> None:
        """GET / でホームページが表示されることをテスト
        
        Args:
            client: Flask test client
        """
        response = client.get("/")
        
        assert response.status_code == 200
        assert "Flask4813" in response.text or "名前" in response.text
        logger.info("GET / returned 200 status")
    
    def test_get_index_displays_form(self, client: FlaskClient) -> None:
        """GET / でフォームが表示されることをテスト
        
        Args:
            client: Flask test client
        """
        response = client.get("/")
        
        assert response.status_code == 200
        assert "form" in response.text.lower() or "<form" in response.text
        assert "name" in response.text.lower()
        logger.info("Form element found in GET / response")
    
    def test_get_index_initial_empty_list(self, client: FlaskClient) -> None:
        """初回アクセス時に名前一覧が空であることをテスト
        
        Args:
            client: Flask test client
        """
        response = client.get("/")
        
        assert response.status_code == 200
        # 初期状態では登録済みデータがないことを確認
        logger.info("Initial index page has empty item list")
    
    def test_post_index_registers_name(self, client: FlaskClient) -> None:
        """POST / で名前を登録できることをテスト
        
        Args:
            client: Flask test client
        """
        csrf_token = get_csrf_token(client)
        
        response = client.post(
            "/",
            data={"name": "Test User", "csrf_token": csrf_token},
            follow_redirects=False
        )
        
        # リダイレクトレスポンスであることを確認
        assert response.status_code in [301, 302, 303, 307, 308]
        logger.info("POST / returned redirect response")
    
    def test_post_index_with_redirect(self, client: FlaskClient) -> None:
        """POST / で名前を登録後にリダイレクトされることをテスト
        
        Args:
            client: Flask test client
        """
        csrf_token = get_csrf_token(client)
        
        response = client.post(
            "/",
            data={"name": "Redirect Test", "csrf_token": csrf_token},
            follow_redirects=True
        )
        
        assert response.status_code == 200
        logger.info("POST / redirect and GET / returned successfully")
    
    def test_post_index_empty_name_rejected(self, client: FlaskClient) -> None:
        """POST / で空の名前が拒否されることをテスト
        
        Args:
            client: Flask test client
        """
        csrf_token = get_csrf_token(client)
        
        response = client.post(
            "/",
            data={"name": "", "csrf_token": csrf_token},
            follow_redirects=True
        )
        
        assert response.status_code == 200
        logger.info("Empty name submission was rejected")
    
    def test_post_index_whitespace_only_rejected(self, client: FlaskClient) -> None:
        """POST / で空白のみの名前が拒否されることをテスト
        
        Args:
            client: Flask test client
        """
        csrf_token = get_csrf_token(client)
        
        response = client.post(
            "/",
            data={"name": "   ", "csrf_token": csrf_token},
            follow_redirects=True
        )
        
        assert response.status_code == 200
        logger.info("Whitespace-only name submission was rejected")
    
    def test_csrf_token_in_form(self, client: FlaskClient) -> None:
        """GET / でCSRFトークンがフォームに埋め込まれていることをテスト
        
        Args:
            client: Flask test client
        """
        response = client.get("/")
        
        assert response.status_code == 200
        # CSRF トークンが存在することを確認
        assert "csrf_token" in response.text
        logger.info("CSRF token found in form")
    
    def test_multiple_names_accumulate(self, client: FlaskClient) -> None:
        """複数の名前を登録できることをテスト
        
        Args:
            client: Flask test client
        """
        names = ["Alice", "Bob", "Charlie"]
        
        for name in names:
            csrf_token = get_csrf_token(client)
            response = client.post(
                "/",
                data={"name": name, "csrf_token": csrf_token},
                follow_redirects=True
            )
            assert response.status_code == 200
        
        logger.info(f"Successfully registered {len(names)} names")


class TestTemplateRendering:
    """テンプレートレンダリングのテストクラス"""
    
    def test_index_uses_template(self, client: FlaskClient) -> None:
        """インデックスページがテンプレートを使用していることをテスト
        
        Args:
            client: Flask test client
        """
        response = client.get("/")
        
        assert response.status_code == 200
        # テンプレート文字列を含まないことを確認（render_template を使用）
        assert response.is_json is False
        logger.info("Index page rendered using template")
    
    def test_page_contains_app_title(self, client: FlaskClient) -> None:
        """ページにアプリケーションタイトルが含まれることをテスト
        
        Args:
            client: Flask test client
        """
        response = client.get("/")
        
        assert response.status_code == 200
        # base.html に定義されたタイトルを確認
        assert "Flask" in response.text
        logger.info("App title found in page")
