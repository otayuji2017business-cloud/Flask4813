# GitHub Secrets 設定後の完全ガイド

## 📌 概要

GitHub Secrets を設定した後、以下の流れで CI/CD パイプラインをテストします：

```
① テスト用ブランチを作成
   ↓
② GitHub にコードを push
   ↓
③ CI ワークフロー実行（Lint, Format, Type, Test）
   ↓
④ PR を作成して確認
   ↓
⑤ PR を approve して main にマージ
   ↓
⑥ デプロイワークフロー実行
   ↓
⑦ Cloud Run でアプリが起動確認
```

---

## 第1段階：テスト用ブランチを作成（ローカルPC）

### **Step 1: PowerShell を開く**

Windows キーを押して「PowerShell」と入力し、PowerShell を開きます。

```
スタート → 検索欄に「PowerShell」と入力 → 実行
```

### **Step 2: リポジトリディレクトリに移動**

```powershell
cd C:\Users\ota-yuji\Documents\GitHub\Flask4813
```

### **Step 3: 現在のブランチ確認**

```powershell
git branch
```

実行結果例：
```
* main
  (その他のブランチがあれば表示)
```

`*` が main についていることを確認します。

### **Step 4: テスト用ブランチを作成**

```powershell
git checkout -b test-ci-workflow
```

実行結果：
```
Switched to a new branch 'test-ci-workflow'
```

### **Step 5: 現在のブランチを確認**

```powershell
git branch
```

実行結果：
```
  main
* test-ci-workflow  ← ※ に切り替わっていることを確認
```

---

## 第2段階：GitHub にコードを push

### **Step 1: 現在の状態を確認**

```powershell
git status
```

実行結果例：
```
On branch test-ci-workflow
nothing to commit, working tree clean
```

変更がない場合は OK です。既に全て commit 済みです。

### **Step 2: GitHub に push**

```powershell
git push origin test-ci-workflow
```

実行結果例：
```
Enumerating objects: 5, done.
...
 * [new branch]      test-ci-workflow -> test-ci-workflow
```

---

## 第3段階：GitHub Actions の CI ワークフロー実行を確認

### **Step 1: GitHub Web UI を開く**

ブラウザで以下にアクセス：
```
https://github.com/YOUR_USERNAME/Flask4813
```

※ YOUR_USERNAME はあなたの GitHub ユーザー名に置き換えてください。

### **Step 2: "Actions" タブをクリック**

GitHub リポジトリページの上部にある **"Actions"** タブをクリック します。

```
[Code] [Issues] [Pull requests] [Actions] ← ここをクリック
```

### **Step 3: ワークフロー実行状況を確認**

画面に以下のように表示されます：

```
CI - Lint, Format, Type Check, Test
├─ 🔄 Running... （実行中）
└─ Workflow runs
   └─ test-ci-workflow - Merge pull request...
```

【確認ポイント】

- **🟡 黄色のアイコン** = 実行中
- **🟢 緑のアイコン** = 成功
- **🔴 赤のアイコン** = 失敗

### **Step 4: ワークフロー詳細を確認**

ワークフロー実行行をクリックすると、詳細画面が表示されます：

```
CI - Lint, Format, Type Check, Test
├─ Ruff Lint Check      ✅ (PASSED)
├─ Black Format Check   ✅ (PASSED)
├─ mypy Type Check      ✅ (PASSED)
├─ pytest Test Suite    ✅ (PASSED)
└─ All Checks Passed    ✅ (PASSED)
```

**全て ✅ (PASSED) であることを確認します。**

---

## 第4段階：PR（Pull Request）を作成

### **Step 1: GitHub 画面を確認**

GitHub リポジトリのトップページに戻ると、以下のメッセージが表示されます：

```
test-ci-workflow had recent pushes 1 minute ago

[Compare & pull request] ← クリック
```

### **Step 2: PR タイトルと説明を入力**

PR 作成画面で以下を入力：

**Title（タイトル）:**
```
Test: CI/CD workflow validation
```

**Description（説明）:**
```
GitHub Secrets 設定後の CI/CD パイプラインテスト

チェック内容：
- ✅ Ruff lint
- ✅ Black format
- ✅ mypy type check
- ✅ pytest tests (8/8 passing)
```

### **Step 3: "Create pull request" をクリック**

PR が作成されます。

### **Step 4: PR チェック状況を確認**

PR バージョンに以下のように表示されます：

```
Some checks are pending
├─ continuous-integration/github-actions/ci
   ✅ (PASSED - All checks passed)
└─ continuous-integration/github-actions/deploy
   ⏭️  (SKIPPED - Only run on main branch)
```

---

## 第5段階：PR を approve して main にマージ

### **Step 1: PR 画面で確認**

PR 画面で以下を確認：

```
✅ All checks have passed
✅ Mergeable - This branch has no conflicts
```

### **Step 2: "Approve" ボタンをクリック**

PR ページの右側に **"Approve"** ボタンがあります。クリックします。

### **Step 3: "Merge and commit" をクリック**

PR を approve した後、以下のメニューが表示されます：

```
[Merge and commit] (プルダウン)
├─ Create a merge commit
├─ Squash and merge
└─ Rebase and merge
```

**"Merge and commit"** を選択します。

### **Step 4: マージ完了**

マージすると以下のメッセージが表示されます：

```
✅ Pull request successfully merged and closed

You can now safely delete the test-ci-workflow branch.
[Delete branch] ← オプション
```

---

## 第6段階：デプロイワークフロー実行を確認

### **Step 1: Actions タブで確認**

GitHub の **"Actions"** タブをクリック します。

### **Step 2: デプロイワークフロー実行を待つ**

新しいワークフロー実行が開始されます：

```
Deploy - Build and Deploy to Cloud Run
├─ 🔄 Running... （実行中）
└─ Workflow runs
   └─ main - Merge pull request...
```

**⚠️ 注意:** デプロイは 2～5 分かかります。

### **Step 3: デプロイステップを確認**

ワークフロー実行行をクリックして詳細を確認：

```
Deploy - Build and Deploy to Cloud Run

① Run Tests Before Deploy  ✅ (PASSED)
   └─ Run pytest tests

② Build Docker Image and Deploy  🔄 (IN PROGRESS)
   ├─ Set up Cloud SDK
   ├─ Configure Docker authentication
   ├─ Build Docker image
   ├─ Push Docker image to Artifact Registry
   ├─ Deploy to Cloud Run
   └─ Get Cloud Run service URL
```

**全て ✅ (PASSED) で完了を待ちます。**

---

## 第7段階：Cloud Run でアプリが起動したか確認

### **Step 1: デプロイ完了を確認**

GitHub Actions で以下が表示されたら完了です：

```
✅ Deploy to Cloud Run service deployed successfully

Deployment completed. Service URL: 
https://flask4813-web-xxxxxxxxxxxx-an.a.run.app
```

### **Step 2: Google Cloud Console にアクセス**

ブラウザで以下にアクセス：
```
https://console.cloud.google.com/
```

### **Step 3: Cloud Run サービスを開く**

左サイドバーから以下をクリック：
```
① メニューアイコン ☰
  ↓
② "Cloud Run" を検索
  ↓
③ "flask4813-web" サービスをクリック
```

### **Step 4: デプロイ状況を確認**

Cloud Run サービスページで以下を確認：

```
flask4813-web

Status: ✅ Running
Revisions:
├─ [新しいリビジョン] - ACTIVE
│  └─ Deployed at 2026-02-19 12:00:00 UTC
└─ [古いリビジョン]  - TRAFFIC: 0%
```

### **Step 5: サービス URL にアクセス**

デプロイされたアプリにアクセス：

```
https://flask4813-web-xxxxxxxxxxxx-an.a.run.app
```

ブラウザで以下のような画面が表示されたら成功です：

```
Flask4813
名前が登録されました

【名前を登録】
┌─────────────────────┐
│ 入力欄              │
│ [   名前を入力     ] │
│ [登録]              │
└─────────────────────┘

【登録された名前一覧】
- 山田太郎
- 鈴木一郎
- （その他）
```

---

## 🎉 完全成功！チェックリスト

デプロイまで完了したら、以下をチェック：

| 項目 | 状態 | チェック |
|-----|------|--------|
| GitHub Secrets 設定 | ✅ 完了 | ✓  |
| CI ワークフロー実行 | ✅ 成功 | ✓  |
| テストすべて成功 | ✅ 8/8 | ✓  |
| PR 作成・マージ | ✅ 完了 | ✓  |
| デプロイワークフロー | ✅ 成功 | ✓  |
| Cloud Run 起動 | ✅ Running | ✓  |
| アプリにアクセス可能 | ✅ 200 OK | ✓  |

---

## � GitHub Artifacts のセットアップと使用方法

### 概要

**GitHub Artifacts** は、CI/CD ワークフロー内で生成されたファイル（テストレポート、カバレッジレポートなど）を保存・ダウンロードできる機能です。本プロジェクトでは、pytest の **カバレッジレポート（HTML形式）** を Artifacts として自動保存しています。

**特徴:**
- ✅ セットアップ不要（ワークフローで自動的に設定済み）
- ✅ テスト完了後、ブラウザで閲覧可能
- ✅ テストカバレッジの可視化
- ✅ 過去のテスト実行結果を比較可能

---

### セットアップ状況確認

#### Step 1: GitHub リポジトリにアクセス

https://github.com/otayuji2017business-cloud/Flask4813

#### Step 2: Actions タブを開く

```
GitHub リポジトリ → 上部メニュー
  ↓
[Actions] タブをクリック
```

画面例：
```
GitHub リポジトリ画面
┌─────────────────────────────────────┐
│ Code  Issues  Pull Requests  Actions │  ← ここ
└─────────────────────────────────────┘
```

#### Step 3: ワークフロー実行履歴を確認

```
Actions タブ内
  ↓
左側メニュー: "CI - Lint, Format, Type Check, Test"
  ↓
最新の実行（例：commit メッセージ表示）をクリック
```

画面例：
```
ワークフロー実行履歴
├─ ✅ Merge pull request #1 into main    2024-02-19 12:30 UTC
├─ ✅ test-ci-workflow branch push       2024-02-19 12:15 UTC
└─ ✅ Initial commit                     2024-02-19 11:45 UTC
```

#### Step 4: Artifacts を確認

最新のワークフロー実行を開くと、以下のように表示されます：

```
Artifacts
┌──────────────────────────────────────┐
│ 📦 coverage-report                   │
│    Size: 45 KB                       │
│    [Download] ボタン                 │
└──────────────────────────────────────┘
```

---

### Artifacts のダウンロードと閲覧

#### Step 1: Artifacts をダウンロード

ワークフロー実行ページで以下をクリック：

```
📦 coverage-report
  ↓
[Download] ボタンをクリック
```

自動的に `coverage-report.zip` がダウンロードされます。

#### Step 2: ZIP ファイルを解凍

ダウンロードフォルダから：

```powershell
# ZIP ファイルが保存されている場所に移動
cd Downloads

# ZIP ファイルを解凍
Expand-Archive coverage-report.zip -DestinationPath coverage-report
```

または、Windows エクスプローラーで右クリック → 「すべて展開」

#### Step 3: カバレッジレポートを閲覧

解凍されたフォルダを開く：

```
coverage-report/
  ├─ index.html          ← これをブラウザで開く
  ├─ app_models_py.html
  ├─ app__init___py.html
  ...
```

**ブラウザで開く:**

PowerShell：
```powershell
# coverage-report フォルダに移動
cd coverage-report

# index.html をブラウザで開く
Invoke-Item .\index.html
```

または、手動で：
1. `coverage-report` フォルダを開く
2. `index.html` を右クリック
3. 「プログラムから開く」→「Chrome」または「Edge」

#### Step 4: カバレッジレポートを確認

ブラウザに以下のように表示されます：

```
COVERAGE REPORT

statements: 64 / 100 (64%)
branches: 12 / 20 (60%)

modules              coverage  missing
====================================
app/__init__.py      100%      
app/routes.py        58%       85-90, 105
app/models.py        100%      
app/extensions.py    90%       45
config.py            85%       12-15
====================================

total                 64%
```

**見方:**
- **statements (ステートメント)**: コード行の実行比率
- **branches (分岐)**: if/else などの分岐カバレッジ
- **missing**: テストされていない行番号

---

### 🔍 CI ワークフロー内の Artifacts 生成設定

参考（ユーザーが修正することはありません）：

`.github/workflows/ci.yml` 内で以下のように設定されています：

```yaml
- name: Run pytest tests
  run: pytest tests/ -v --cov=app --cov-report=html

- name: Upload coverage to artifacts
  uses: actions/upload-artifact@v4
  with:
    name: coverage-report
    path: htmlcov/
  if: always()
```

**説明:**
- `--cov-report=html`: HTML形式のレポート生成
- `upload-artifact@v4`: GitHub Artifacts にアップロード
- `if: always()`: テスト失敗時もアップロード（除外含める）

---

### 📊 実用的な使用例

#### 例 1: テストカバレッジの改善を確認

**手順:**
1. ローカルでコードを修正
2. 新しいテストを追加
3. `git push` でアップロード
4. CI ワークフロー完了後、Artifacts をダウンロード
5. `index.html` で新しいカバレッジを確認
6. 前回のレポートと比較

#### 例 2: PR 時のテスト結果を確認

**手順:**
1. PR を作成
2. GitHub Actions の CI ワークフロー実行を待つ
3. PR ページの右側 "Checks" セクションで実行状況を確認
4. "CI - Lint, Format..." をクリック
5. Artifacts をダウンロードしてレポート確認

#### 例 3: 本番デプロイ前の品質確認

**チェックリスト:**
```
デプロイ前の品質確認
☐ CI ワークフローが ✅ All checks passed
☐ テストが 8/8 passing
☐ カバレッジが 60% 以上
☐ Lint エラーなし
☐ 型チェックエラーなし
```

---

### 💾 Artifacts の保持期間

**デフォルト**: 90日間保持

GitHub リポジトリ Settings → Actions → Artifacts の削除でカスタマイズ可能：

```
Settings → Actions → General
  ↓
Artifact and log retention
  ↓
Retention period: 90 days (デフォルト)
  ↓
更新をクリック
```

---

## �🐛 トラブルシューティング

### ❌ CI ワークフローが失敗した場合

**原因:** コードに Lint エラーやテスト失敗がある

**対処方法:**
1. GitHub Actions ログを確認
2. ローカルで修正
3. `git push` で再度試す

ローカル確認コマンド：
```powershell
# Lint チェック
python -m ruff check app/ config.py wsgi.py

# Format チェック
python -m black --check app/ config.py wsgi.py

# 型チェック
python -m mypy app/ config.py wsgi.py --ignore-missing-imports

# テスト実行
python -m pytest tests/ -v
```

### ❌ デプロイワークフローが失敗した場合

**原因:** GCP_SA_KEY または GCP_PROJECT_ID が違う可能性

**エラーメッセージ例:**
```
error getting credentials - err: exit status 1, out: `You do not currently have an active account selected.`
```

**対処方法:**

#### 1️⃣ GitHub Secrets を再確認

GitHub リポジトリ Settings → Secrets → Actions で以下を確認：

```
✅ GCP_PROJECT_ID が設定されているか
✅ GCP_SA_KEY が設定されているか
```

#### 2️⃣ GCP_SA_KEY の JSON 形式を確認

GCP SA Key JSON ファイルを確認：

```json
{
  "type": "service_account",
  "project_id": "platinum-linker-487308-t8",
  "private_key_id": "702b5b109b209ca92...",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG...",
  "client_email": "flask-run-sa@platinum-linker-487308-t8.iam.gserviceaccount.com",
  "client_id": "112201114201225977757",
  (その他のフィールド...)
}
```

**チェックポイント:**
- ✅ `private_key` に改行がある（`\n` で表現）
- ✅ JSON が完全で、末尾の } でクローズしている
- ✅ `project_id` と GCP_PROJECT_ID が一致している

#### 3️⃣ GitHub Secrets を再設定

古い値を削除して新規設定：

**GitHub 画面:**
```
Settings → Secrets and variables → Actions
  → GCP_SA_KEY を削除
  → New repository secret をクリック
  → GCP_SA_KEY を改めて貼り付け
```

**重要:** JSON ファイル全体を **1行で** コピー＆ペーストしてください（改行やスペースを入れない）

#### 4️⃣ GCP SA Key の権限確認

GCP Console で以下を確認：

```
IAM と管理 → IAM
  → サービスアカウント（flask-run-sa@...）
  → ロールが以下の3つ設定されているか確認：
     ✅ roles/artifactregistry.writer
     ✅ roles/run.developer
     ✅ roles/cloudsql.client
```

足りないロールがあれば追加してください。

#### 5️⃣ デプロイワークフローを再実行

修正後、以下で再実行：

**GitHub Web UI:**
```
Actions → Deploy ワークフロー
  → 右上の [Run workflow] をクリック
  → main ブランチを選択
  → [Run workflow] をクリック
```

または **PowerShell で再度 push:**

```powershell
cd C:\Users\ota-yuji\Documents\GitHub\Flask4813
git switch main
git pull origin main
$ (コードに変更がなければ) 
git commit --allow-empty -m "Retry deploy workflow"
git push origin main
```

### ❌ Cloud Run にアクセスできない場合

---

## 🔍 GCP 認証エラーの詳細診断

### エラーメッセージ
```
error getting credentials - err: exit status 1
You do not currently have an active account selected
```

### 診断チェックリスト

| 項目 | 確認方法 | 修正方法 |
|-----|--------|--------|
| **Secrets 存在確認** | GitHub Settings → Secrets で GCP_PROJECT_ID と GCP_SA_KEY が表示されているか | 表示されていなければ新規作成 |
| **JSON 形式確認** | `"private_key"` が改行なし（`\n`で表現）か | テキストエディタで確認、修正 |
| **Project ID 一致** | GCP_PROJECT_ID と SA Key の `project_id` が同じか | 異なればどちらかを修正 |
| **SA権限確認** | GCP Console で 3つのロールが付与されているか | 不足していれば付与 |

### デバッグ用ワークフロー（オプション）

`.github/workflows/debug-gcp.yml` を作成してデバッグ情報を取得：

```yaml
name: Debug GCP Setup

on: workflow_dispatch

jobs:
  debug:
    runs-on: ubuntu-latest
    steps:
      - uses: google-github-actions/setup-gcloud@v1
        with:
          project_id: ${{ secrets.GCP_PROJECT_ID }}
          service_account_key: ${{ secrets.GCP_SA_KEY }}
      
      - name: Check GCP authentication
        run: |
          echo "Project ID: $(gcloud config get-value project)"
          gcloud auth list
          gcloud config list
```

GitHub Actions で `Run workflow` ボタンからこのワークフローを実行すると、詳細情報が表示されます。

---

### ❌ Cloud Run にアクセスできない場合

**原因:** アプリケーションの起動エラー

**対処方法:**
1. Cloud Run のログを確認
   ```
   Cloud Run → サービス選択 → ログを表示
   ```
2. エラーメッセージを確認して修正
3. 修正後、再度 main にマージして自動デプロイ

---

## 📞 次のステップ

デプロイ完了後、以下を検討してください：

1. **データベース接続確認**
   - Cloud SQL（MySQL）に接続できるか確認

2. **環境変数設定確認**
   - Cloud Run → キー/値でデータベース情報を確認

3. **監視・ログ設定**
   - Stackdriver Logging でアプリログを確認

4. **本番運用準備**
   - カスタムドメイン設定
   - SSL/TLS 設定
   - バックアップ設定

---

## ✅ チェックリスト（完了確認）

セットアップ完了時に以下が全て ✅ であることを確認してください：

---

## 🛠️ ローカル環境での GCP SA Key 検証

GitHub にアップロード前に、ローカルで GCP SA Key が有効か検証できます：

### Step 1: JSON ファイルをダウンロード

GCP Console からダウンロードした SA Key ファイルを確認：

```
platinum-linker-487308-t8-702b5b109b20.json
```

### Step 2: JSON 形式を確認

PowerShell で検証：

```powershell
# JSON ファイルの内容確認
Get-Content platinum-linker-487308-t8-702b5b109b20.json

# 結果例（整形版）：
# {
#   "type": "service_account",
#   "project_id": "platinum-linker-487308-t8",
#   "private_key_id": "702b5b109b209ca92...",
#   "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG...",
#   ...
# }
```

**確認ポイント:**
- ✅ `private_key` に改行あり（`\n` で表現）
- ✅ JSON が完全でエラーなし

### Step 3: GitHub Secrets に貼り付け

**PowerShell で全内容をクリップボードにコピー:**

```powershell
Get-Content platinum-linker-487308-t8-702b5b109b20.json | Set-Clipboard
```

**または、手動でコピー:**
1. JSON ファイルをテキストエディタで開く
2. 全選択（Ctrl+A）
3. コピー（Ctrl+C）

**GitHub に貼り付け:**
1. GitHub Settings → Secrets → New repository secret
2. Name: `GCP_SA_KEY`
3. Value: **クリップボードの内容をペースト（Ctrl+V）**
4. Add secret

**重要:** JSON を複数行で貼り付けずに、そのまま貼り付けてください。GitHub が自動的に処理します。

---

## ✅ チェックリスト（完了確認）

セットアップ完了時に以下が全て ✅ であることを確認してください：

- [ ] GitHub Secrets 設定（GCP_PROJECT_ID, GCP_SA_KEY）
- [ ] テスト用ブランチ作成（test-ci-workflow）
- [ ] GitHub push 実行
- [ ] CI ワークフロー実行確認（8/8 passing）
- [ ] PR 作成・approve・マージ
- [ ] デプロイワークフロー実行確認
- [ ] Cloud Run サービス確認（Running ステータス）
- [ ] アプリケーション起動確認（ブラウザアクセス）

---

**次回からは、コードを修正して main にマージするだけで自動デプロイされます！** 🚀
