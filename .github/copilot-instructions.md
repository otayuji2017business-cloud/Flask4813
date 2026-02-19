
# Copilot Instructions for Flask4813 App (Web)

## このドキュメントについて

- 本ドキュメントは、GitHub Copilot や各種 AI ツールが本リポジトリのコンテキストを理解しやすくするためのガイドです。
- 新機能の追加・既存コードの修正を行う場合は、必ず本ドキュメントの方針を前提としてください。
- 不確かな点がある場合は、リポジトリのファイルを探索し、ユーザーに「こういうことですか?」と確認をするようにしてください。

## 前提条件

- 回答は必ず日本語で行う
- コードの変更をする際、変更量が200行を超える可能性が高い場合は、事前に「この指示では変更量が200行を超える可能性がありますが、実行しますか?」とユーザーに確認をとるようにしてください。
- 何か大きい変更を加える場合、まず何をするのか計画を立てた上で、ユーザーに「このような計画で進めようと思います。」と提案してください。この時、ユーザーから計画の修正を求められた場合は計画を修正して、再提案をしてください。

## アプリ概要

Flask4813 App (Web) は、利用者が名前を入力し、その一覧を表示するシンプルなWebアプリケーションである。


### 主な機能

- **利用者が名前を入力できるフォーム**: ユーザーは自分の名前を入力できるフォームを提供し、入力された名前はアプリ内で管理される
- **その一覧を表示する機能**: 入力された名前の一覧を表示する機能を提供し、ユーザーは自分が入力した名前や他のユーザーが入力した名前を見ることができる


## 技術スタック概要

- **言語**: Python 3.12
- **フレームワーク**: Flask 3.1.2
- **テンプレートエンジン**: Jinja2 3.1.6
- **ORM**: SQLAlchemy 2.0.46
- **DB**: Cloud SQL (MySQL 8系)
- **DB Driver**: pymysql 1.1.1
- **ビルドツール**: Docker（Cloud Run デプロイ用）
- **パッケージマネージャー**: pip
- **状態管理**: Flask session + Cloud SQL（MySQL 8系）
- **UI構成**: Flaskテンプレートベース（base.html継承）
- **マイグレーション**: Alembic
- **テスト**: pytest + Flask test client
- **リンター**: Ruff
- **フォーマッター**: Black
- **型チェック**: mypy
- **CI/CD**: GitHub Actions + Docker build → Cloud Run
- **WSGI Server**: Gunicorn 21.2.0

フロントエンド分離構成（React等）は採用しない。


## プロジェクト構成と役割

本アプリは機能ベースのディレクトリ構成を採用し、関心の分離とスケーラビリティを実現しています。

Flask4813/
│
├── app/
│   ├── __init__.py
│   ├── models.py
│   ├── routes.py
│   └── extensions.py
│
├── .github/
│   └── copilot-instructions.md
│
├── config.py
├── wsgi.py
├── requirements.txt
├── Dockerfile
├── .gcloudignore
├── .dockerignore
└── .env


- **app/**: アプリケーションのコアコードを格納
  - `__init__.py`: Flask アプリケーションのファクトリ関数を定義
  - `models.py`: SQLAlchemy のモデル定義
  - `routes.py`: Flask のルートハンドラーを定義
  - `extensions.py`: db, migrate等の初期化
- **.github/**: GitHub関連の設定やドキュメントを格納
   - `copilot-instructions.md`: GitHub Copilot や AIツール向けの指示書（このファイル）
- **config.py**: 環境ごとの設定を定義
- **wsgi.py**: WSGIサーバー（Gunicorn）用のエントリポイント
- **requirements.txt**: Pythonの依存関係を管理
- **Dockerfile**: Dockerイメージのビルド定義
- **.gcloudignore**: Cloud Buildで無視するファイルを指定
- **.dockerignore**: Dockerビルドで無視するファイルを指定
- **.env**: 環境変数を定義（ローカル開発用、Git管理外）



## アーキテクチャ指針

## 設計原則

- 小規模のため単一Blueprintと明記
- Cloud Run前提のステートレス設計を徹底
- MVC構造を明確に保つ  
  - Model: SQLAlchemyモデル  
  - View: Jinja2テンプレート   


# 状態管理方針

- **ローカル状態**: Flask session
- **永続データ**: Cloud SQL（MySQL）
- **リクエストスコープ変数**: Flask `g` オブジェクト使用
- **グローバル変数による状態保持は禁止（Cloud Run非対応）**

Flask標準の署名付きCookieセッションを使用する。
サーバーサイドセッションストアは使用しない。


# ルーティング設計

- REST原則に従う
- HTTPメソッドを適切に使い分ける（GET / POST / PUT / DELETE）
- URL設計はリソース指向

例：
GET     /users
POST    /users
GET     /users/<id>
PUT     /users/<id>
DELETE  /users/<id>

HTTPメソッドを正しく使い分ける。


---

# テンプレート設計

- base.html を作成し共通レイアウトを定義
- コンポーネント的にテンプレートを分割


---

# セキュリティ指針

- **環境変数**: API キーは `.env` で管理し、`.gitignore` に追加
- **機密情報**: DBパスワードなどの機密情報は Secret Manager で管理し、コードベースには含めない
- **CSRF対策**: フォームにはCSRFトークンを埋め込む（Flask-WTFの導入を検討）
- **HTTPS**: 本番環境ではCloud RunのHTTPSを利用し、通信の暗号化を確保


# Cloud Run制約

- アプリは完全ステートレスであること
- ローカルファイル保存を前提にしない
- 長時間処理は禁止（リクエストタイムアウト考慮）


# テスト戦略

- モデルテスト
- ルートテスト
- テストは SQLite in-memory を使用する。
  本番DBには依存しない。

# ロギング方針
- Python標準のloggingモジュールを使用
- print文は禁止
- ログレベルを適切に設定（DEBUG, INFO, WARNING, ERROR, CRITICAL）

# アンチパターン(やってはいけないこと)

- app.py に全ての処理を書く
- グローバル変数で状態管理
- SQLの直書き（ORMを使用）
- ビジネスロジックをテンプレートに書く
- 200行超の巨大関数


# コーディング規約

- 型ヒント必須
- docstring記述
- asyncは使用しない（Flask同期設計）
- import順序を統一
- 例外は必ず捕捉しログ出力


# CI/CD方針
- Lint → Format check → Type check → Test → Docker build
- GitHub ActionsでCI/CDを構築
- プッシュ時に自動でテストとリンティングを実行
- mainブランチへのマージでDockerイメージをビルドし、Cloud Runへデプロイ
- デプロイ前に必ずテストが成功することを条件とする
- デプロイ後はCloud Runのログを確認し、問題がないかモニタリングする
- デプロイのロールバック手順も用意しておく（Cloud Runのリビジョン管理を活用）
- デプロイの際は、環境変数やシークレットの管理に注意し、必要な設定が正しく行われていることを確認する

# デプロイ方針

- Dockerでビルド
- Artifact Registryへpush
- Cloud Runへdeploy
- 環境変数はCloud Run側で設定

---

# まとめ

このドキュメントを常に最新に保ち、新しい技術選定や設計変更があった場合は適宜更新してください。GitHub Copilot や AI ツールは、このドキュメントを参照することで、プロジェクトのコンテキストを正確に理解し、より適切なコード提案を行うことができます。

本プロジェクトは、Flask + SQLAlchemy + Cloud Run によるシンプルかつ拡張可能な構成を採用する。
React や Firebase を前提としたフロント分離構成は、採用しない.







