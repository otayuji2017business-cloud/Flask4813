"""ルートハンドラテスト

Flask ルートとHTTPレスポンスをテストしています。
シンプルなテストケースのみに集約し、基本的な GET テストを実施します。
"""

import logging
from flask.testing import FlaskClient

logger = logging.getLogger(__name__)


def test_get_index_returns_200(client: FlaskClient) -> None:
    """GET / でステータス 200 が返されることをテスト
    
    Args:
        client: Flask test client
    """
    response = client.get("/")
    
    assert response.status_code == 200
    logger.info("✓ GET / returned 200 status")


def test_get_index_contains_form(client: FlaskClient) -> None:
    """GET / でフォーム要素があることをテスト
    
    Args:
        client: Flask test client
    """
    response = client.get("/")
    
    assert response.status_code == 200
    assert "<form" in response.text.lower()
    logger.info("✓ Form element found in response")


def test_get_index_contains_input_name_field(client: FlaskClient) -> None:
    """GET / で入出力フィールド name が存在することをテスト
    
    Args:
        client: Flask test client
    """
    response = client.get("/")
    
    assert response.status_code == 200
    assert 'name="name"' in response.text or "name" in response.text.lower()
    logger.info("✓ Input field 'name' found in response")


def test_get_index_contains_submission_button(client: FlaskClient) -> None:
    """GET / で送信ボタンがあることをテスト
    
    Args:
        client: Flask test client
    """
    response = client.get("/")
    
    assert response.status_code == 200
    assert "<button" in response.text.lower() or 'type="submit"' in response.text.lower()
    logger.info("✓ Submit button found in response")
