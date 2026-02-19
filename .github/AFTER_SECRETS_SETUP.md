# GitHub Secrets 設定後の完全ガイド

## 📌 概要

GitHub Secrets（`GCP_PROJECT_ID`, `GCP_SA_KEY`）を設定した後、以下の流れで CI/CD パイプラインをテストします：

```
① テスト用ブランチを作成 → push
② CI ワークフロー実行確認（Ruff, Black, mypy, pytest）
③ PR 作成・approve・マージ
④ デプロイワークフロー実行（Docker → Artifact Registry → Cloud Run）
⑤ Cloud Run でアプリ起動確認
```

**所要時間:** 全体で 15～20 分

---

## ⚡ 実行ステップ

### Step 1: テスト用ブランチを作成して push

PowerShell で実行：

```powershell
cd C:\Users\ota-yuji\Documents\GitHub\Flask4813
git checkout -b test-ci-workflow
git push origin test-ci-workflow
```

---

### Step 2: CI ワークフロー実行確認

GitHub Actions で自動で以下がチェックされます：

```
✅ Ruff Lint Check
✅ Black Format Check
✅ mypy Type Check
✅ pytest Test Suite (8/8 passing)
```

**確認方法:**
- GitHub リポジトリ → [Actions] タブ
- 「CI - Lint, Format, Type Check, Test」をクリック
- 全て ✅ PASSED になるまで待つ（約 3～5 分）

---

### Step 3: PR（Pull Request）を作成・マージ

**GitHub Web UI で：**

1. GitHub リポジトリ → [Compare & pull request]
2. PR タイトル：`Test: CI/CD workflow validation`
3. [Create pull request]
4. CI 完了後 → [Approve] → [Merge and commit]

---

### Step 4: デプロイワークフロー実行確認

main ブランチマージを検出すると、自動でデプロイ開始：

```
① Run Tests Before Deploy  ✅ (1 min)
② Build Docker Image  ✅ (2 min)
③ Push to Artifact Registry  ✅ (1 min)
④ Deploy to Cloud Run  ✅ (1-2 min)
```

**確認方法:**
- GitHub Actions → [Deploy - Build and Deploy to Cloud Run]
- 全て ✅ PASSED になるまで待つ（約 5～10 分）

---

### Step 5: Cloud Run で起動確認

**Google Cloud Console で確認：**

1. ブラウザで `https://console.cloud.google.com/` を開く
2. メニュー → 「Cloud Run」を検索 → 「flask4813-web」をクリック
3. Status が ✅ Running を確認

**アプリにアクセス：**

GitHub Actions のデプロイ完了メッセージから Service URL をコピーしてアクセス：

```
https://flask4813-web-xxxxxxxxxxxx-an.a.run.app
```

以下が表示されたら成功：

```
Flask4813
【名前を登録】
[入力欄] [登録ボタン]

【登録された名前一覧】
- 山田太郎
- 鈴木一郎
```

---

## ✅ 完全成功チェックリスト

| 項目 | 状態 |
|-----|------|
| CI ワークフロー | ✅ すべて PASSED |
| PR 作成・マージ | ✅ 完了 |
| デプロイワークフロー | ✅ すべて PASSED |
| Cloud Run Status | ✅ Running |
| ブラウザアクセス | ✅ 200 OK |

---

## 📦 GitHub Artifacts（テストカバレッジレポート）

### ダウンロード方法

1. GitHub Actions → ワークフロー実行
2. 下部 [Artifacts] → `coverage-report` をクリック
3. ZIP ファイルをダウンロード・解凍
4. `coverage-report/index.html` をブラウザで開く

### 見方

- **statements**: コード実行比率
- **branches**: if/else などの分岐カバレッジ
- **missing**: テストされていない行番号

推奨ターゲット：**60% 以上**

---

## 📦 Artifact Registry（Docker イメージ管理）

### 確認方法

1. Google Cloud Console → Artifact Registry
2. `flask4813` リポジトリ → `web` イメージを確認
3. タグ：`latest`（最新）、`v1.0.0`（バージョン）など

### ストレージコスト削減

古いイメージを定期的に削除：

```
Artifact Registry → リポジトリ設定 → Cleanup policies
→ 最新10件のみ保持、30日以上前は削除
```

---

## 🐛 トラブルシューティング

### CI ワークフローが失敗

**原因:** Lint エラーまたはテスト失敗

**対処:**
1. GitHub Actions ログを確認
2. ローカルで修正：
   ```powershell
   python -m ruff check app/ config.py wsgi.py
   python -m black --check app/ config.py wsgi.py
   python -m mypy app/ config.py wsgi.py --ignore-missing-imports
   python -m pytest tests/ -v
   ```
3. `git push` で再度試す

---

### デプロイワークフローが失敗

**エラー:** `error getting credentials - You do not currently have an active account selected`

**原因:** GCP_SA_KEY または GCP_PROJECT_ID が違う

**対処:**

#### 1. GitHub Secrets を再確認

```
GitHub Setting → Secrets and variables → Actions
→ GCP_PROJECT_ID と GCP_SA_KEY が存在を確認
```

#### 2. JSON 形式を確認

GCP SA Key JSON ファイルを確認：

```json
{
  "type": "service_account",
  "project_id": "platinum-linker-487308-t8",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  ...
}
```

**チェック:**
- ✅ `private_key` に改行あり（`\n` で表現）
- ✅ JSON が完全（末尾の }）
- ✅ `project_id` と GCP_PROJECT_ID が一致

#### 3. GitHub Secrets を再設定

```
Settings → Secrets → GCP_SA_KEY を削除
→ New repository secret → JSON 全体をペースト
```

**重要:** JSON を複数行で貼り付けずに1行でペースト

#### 4. GCP SA Key の権限確認

GCP Console で確認：

```
IAM と管理 → IAM
→ サービスアカウント（flask-run-sa@...）
→ 以下3つのロールが付与されているか確認：
   ✅ roles/artifactregistry.writer
   ✅ roles/run.developer
   ✅ roles/cloudsql.client
```

不足していれば追加

#### 5. デプロイワークフローを再実行

GitHub Web UI：

```
Actions → Deploy ワークフロー
→ [Run workflow] → main ブランチ → [Run workflow]
```

または PowerShell：

```powershell
cd C:\Users\ota-yuji\Documents\GitHub\Flask4813
git switch main
git pull origin main
git commit --allow-empty -m "Retry deploy"
git push origin main
```

---

### Cloud Run にアクセスできない

**原因:** アプリケーション起動エラー

**対処:**
1. Cloud Run ログを確認：`Cloud Run → サービス → ログを表示`
2. エラーメッセージを確認して修正
3. main にマージして再デプロイ

---

## ローカル環境での GCP 認証確認

### GCP ログイン状態確認

```powershell
gcloud auth list
```

**出力例:**
```
        Credentialed Accounts
ACTIVE  ACCOUNT
*       otayuji2017business@gmail.com
```

### GCP 設定確認

```powershell
gcloud config list
```

**出力例:**
```
[core]
account = otayuji2017business@gmail.com
project = platinum-linker-487308-t8
```

**確認ポイント:**
- ✅ ACTIVE に自分のメールアドレス
- ✅ `project` が `platinum-linker-487308-t8`

### 初回実行時の警告

以下のメッセージが出る場合がありますが、**エラーではありません**：

```
API [cloudresourcemanager.googleapis.com] not enabled...
Would you like to enable and retry (y/N)? y
```

→ `y` を入力して有効化を許可

```
Project lacks an 'environment' tag...
```

→ オプション設定。本番運用時に後から設定可能

---

## 📞 次のステップ

デプロイ完了後：

1. **データベース接続確認**
   - Cloud SQL（MySQL）に接続できるか確認

2. **環境変数設定確認**
   - Cloud Run → デプロイ詳細 → 環境変数を確認

3. **ログ監視**
   - Cloud Logging でアプリログ確認

4. **本番運用準備**
   - カスタムドメイン設定
   - SSL/TLS 設定
   - バックアップ設定

---

**次回からは、コードを修正して main にマージするだけで自動デプロイされます！** 🚀
