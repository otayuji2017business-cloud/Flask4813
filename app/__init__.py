import logging
from flask import Flask, jsonify, Response
from flask_wtf.csrf import CSRFProtect, CSRFError
from .extensions import init_engine
from .routes import bp

logger = logging.getLogger(__name__)
csrf = CSRFProtect()


def create_app(init_db: bool = True) -> Flask:
    """Flask アプリケーションファクトリ

    Args:
        init_db: データベースエンジンを初期化するか（テスト時は False）

    Returns:
        Flask: 初期化された Flask アプリケーション
    """
    app = Flask(__name__)

    from config import get_config

    app.config.from_object(get_config())

    # CSRF 保護を初期化
    csrf.init_app(app)

    # Engine 初期化（起動時 1 回）
    # テスト時は init_db=False で init_engine の呼び出しをスキップ
    if init_db:
        init_engine(app.config["DATABASE_URL"])

    # Blueprint 登録
    app.register_blueprint(bp)

    # エラーハンドラーを登録
    _register_error_handlers(app)

    return app


def _register_error_handlers(app: Flask) -> None:
    """エラーハンドラーを登録

    Args:
        app: Flask アプリケーション
    """

    @app.errorhandler(400)
    def bad_request(error: Exception) -> tuple[Response, int]:
        """400 Bad Request エラーハンドラー"""
        logger.warning(f"Bad request: {error}")
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(404)
    def not_found(error: Exception) -> tuple[Response, int]:
        """404 Not Found エラーハンドラー"""
        logger.warning(f"Resource not found: {error}")
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(CSRFError)
    def handle_csrf_error(error: CSRFError) -> tuple[Response, int]:
        """CSRF エラーハンドラー

        CSRF トークンが無効または欠落している場合
        """
        logger.warning(f"CSRF validation failed: {error.description}")
        return (
            jsonify({"error": "CSRF validation failed", "message": error.description}),
            400,
        )

    @app.errorhandler(500)
    def internal_error(error: Exception) -> tuple[Response, int]:
        """500 Internal Server Error エラーハンドラー

        予期しないサーバーエラーが発生した場合
        """
        logger.error(f"Internal server error: {error}", exc_info=True)
        return (
            jsonify(
                {
                    "error": "Internal server error",
                    "message": "An unexpected error occurred. Please try again later.",
                }
            ),
            500,
        )

    @app.errorhandler(Exception)
    def handle_exception(error: Exception) -> tuple[Response, int]:
        """汎用例外ハンドラー

        キャッチされない例外をログに記録し、500 エラーを返す
        """
        logger.error(f"Unhandled exception: {error}", exc_info=True)
        return (
            jsonify(
                {
                    "error": "Server error",
                    "message": "An unexpected error occurred. Please contact support.",
                }
            ),
            500,
        )
