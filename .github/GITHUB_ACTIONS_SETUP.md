# GitHub Actions セットアップガイド

## 概要

Flask4813 アプリケーションの CI/CD パイプラインを GitHub Actions で自動化しています。

### ワークフロー一覧

| ワークフロー | トリガー | 実行内容 |
|-----------|--------|--------|
| **CI** | すべてのブランチへの push / PR | Lint → Format → Type Check → Test |
| **Deploy** | main ブランチへのマージ | テスト → ビルド → Artifact Registry → Cloud Run |

---

## 📋 ワークフロー詳細

### 1️⃣ CI ワークフロー（`.github/workflows/ci.yml`）

**トリガー:**
- すべてのブランチへの push
- PR 作成時

**実行ステップ:**

1. **Ruff Lint** - コードの品質チェック
   ```bash
   ruff check app/ config.py wsgi.py
   ```

2. **Black Format** - コードフォーマットの確認
   ```bash
   black --check app/ config.py wsgi.py
   ```

3. **mypy Type Check** - 型チェック
   ```bash
   mypy app/ config.py wsgi.py --ignore-missing-imports
   ```

4. **pytest Tests** - ユニット・統合テスト
   ```bash
   pytest tests/ -v --cov=app --cov-report=html
   ```

5. **Coverage Report** - テストカバレッジレポート生成

**失敗時の動作:**
- PR マージをブロック
- ログに詳細情報を出力
- 開発者に修正を通知

---

### 2️⃣ Deploy ワークフロー（`.github/workflows/deploy.yml`）

**トリガー:**
- `main` ブランチへのマージ

**前提条件:**
- CI ワークフローが成功すること（テスト 8/8 合格）

**実行ステップ:**

1. **テスト実行** - 本番デプロイ前の確認
   ```bash
   pytest tests/ -v
   ```

2. **Docker ビルド**
   ```bash
   docker build -t asia-northeast1-docker.pkg.dev//flask4813/web:latest .
   ```{GCP_PROJECT_ID}

3. **Artifact Registry へ Push**
   ```bash
   docker push asia-northeast1-docker.pkg.dev/{GCP_PROJECT_ID}/flask4813/web:latest
   ```

4. **Cloud Run へデプロイ**
   ```bash
   gcloud run deploy flask4813-web \
     --image asia-northeast1-docker.pkg.dev/{GCP_PROJECT_ID}/flask4813/web:latest \
     --region asia-northeast1
   ```

5. **デプロイ成功確認** - サービス URL を出力

---

## 🔐 GitHub Secrets セットアップ

Deploy ワークフローを有効化するには、以下の Secrets を GitHub に設定してください。

### セットアップ手順

1. **GitHub リポジトリ** → **Settings** → **Secrets and variables** → **Actions** を開く

2. **以下の Secrets を作成:**

| Secret 名 | 説明 | 例 |
|----------|------|-----|
| `GCP_PROJECT_ID` | Google Cloud Platform のプロジェクト ID | `platinum-linker-487308-t8` |
| `GCP_SA_KEY` | GCP サービスアカウントキー（JSON） | JSON キーの全内容 |

### GCP サービスアカウントキーの取得

```bash
# GCP コンソールで以下を実行
# 1. Google Cloud Console へログイン
# 2. プロジェクト選択
# 3. IAM と管理 → サービスアカウント
# 4. サービスアカウント作成または既存を選択
# 5. キー → JSON ファイルをダウンロード
# 6. ダウンロードした JSON 全体を GCP_SA_KEY に貼り付け
```

### 必要な GCP 権限

サービスアカウントに以下のロールを付与してください：

- `roles/artifactregistry.writer` - Artifact Registry への push
- `roles/run.developer` - Cloud Run へのデプロイ
- `roles/cloudsql.client` - Cloud SQL への接続（本番環境）

---

## 🚀 ローカルでのテスト

GitHub から実行する前に、ローカルで CI 要件を満たしているか確認してください：

### 1. Lint チェック
```bash
ruff check app/ config.py wsgi.py
```

### 2. Format チェック
```bash
black --check app/ config.py wsgi.py
```

### 3. 型チェック
```bash
mypy app/ config.py wsgi.py --ignore-missing-imports
```

### 4. テスト実行
```bash
pytest tests/ -v --cov=app
```

---

## 📊 ワークフロー実行状況の確認

### GitHub Web UI での確認

1. リポジトリの **Actions** タブを開く
2. ワークフロー名をクリック
3. 実行ログ詳細を確認

### 各ステップのログ確認

各ステップを展開して、詳細なログを確認できます：

```
✓ Set up Python
✓ Install dependencies
✓ Run Ruff lint
✓ Check format with Black
✓ Run mypy type check
✓ Run pytest tests
```

---

## 🔄 デプロイフロー

```
① main ブランチにマージ
   ↓
② GitHub Actions 自動トリガー
   ↓
③ テスト実行（8/8 成功確認）
   ↓
④ Docker イメージビルド
   ↓
⑤ Artifact Registry へ push
   ↓
⑥ Cloud Run へデプロイ
   ↓
⑦ デプロイ完了（URL 表示）
```

---

## 🐛 トラブルシューティング

### Deploy ワークフローが失敗する場合

1. **Secrets の設定確認**
   ```bash
   # Settings → Secrets の GCP_PROJECT_ID と GCP_SA_KEY が設定されているか確認
   ```

2. **GCP 権限確認**
   ```bash
   # サービスアカウントが適切なロールを持っているか確認
   gcloud projects get-iam-policy {GCP_PROJECT_ID} \
     --flatten="bindings[].members" \
     --filter="bindings.members:serviceAccounts/*"
   ```

3. **Cloud Run リソースの確認**
   ```bash
   # Cloud Run サービスが存在するか確認
   gcloud run services list --region asia-northeast1
   ```

### テストが失敗する場合

1. ローカルで `pytest tests/ -v` を実行
2. 失敗したテスト詳細をログで確認
3. GitHub Actions ログとの比較

---

## ✅ チェックリスト

デプロイを実行する前に、以下の項目を確認してください：

- [ ] CI ワークフロー成功（Lint, Format, Type, Test）
- [ ] GCP Secrets 設定完了
- [ ] GCP サービスアカウント権限確認
- [ ] Cloud Run リソース作成済み
- [ ] データベース環境変数設定済み
- [ ] Dockerfile 動作確認済み

---

## 📚 参考資料

- [GitHub Actions ドキュメント](https://docs.github.com/ja/actions)
- [Google Cloud Run ドキュメント](https://cloud.google.com/run/docs)
- [pytest ドキュメント](https://docs.pytest.org/)
- [mypy ドキュメント](https://mypy.readthedocs.io/)
