---
created: 2026-09-20
updated: 2026-09-21
tags: [personal-knowledge-base, spec, code-analysis]
phase: 1
status: active
unexplored_domains: 
- "ルール定義 (`00-rules/`: ワークフロー、分類、フォーマット、エージェント行動規範、セキュリティ)"
- "自動化メンテナンススクリプト (`scripts/`: ログ取得、ルール同期、ストレージ同期、構造チェック)"
- "Gitフック設定 (`.githooks/pre-commit`) および Gitleeks セキュリティスキャン設定 (`.gitleeks.toml`)"
- "ナレッジベースディレクトリ構造管理 (`01-private/`, `02-knowledge/`, `03-output/`, `04-resources/`, `05-todo/`, `06-storage/`, `99-trash/`)"
- "ナレッジベースディレクトリの構造の仕様"
---

# personal-knowledge-base 挙動・処理仕様ナレッジ

## 1. 識別された機能・インターフェース一覧 (Phase 1)
- [x] ルール定義 (`00-rules/`: ワークフロー、分類、フォーマット、エージェント行動規範、セキュリティ)
- [x] 自動化メンテナンススクリプト (`scripts/`: ログ取得、ルール同期、ストレージ同期、構造チェック)
- [x] Gitフック設定 (`.githooks/pre-commit`) および Gitleeks セキュリティスキャン設定 (`.gitleeks.toml`)
- [x] ナレッジベースディレクトリ構造管理 (`01-private/`, `02-knowledge/`, `03-output/`, `04-resources/`, `05-todo/`, `06-storage/`, `99-trash/`)
- [x] ナレッジベースディレクトリの構造の仕様

## 2. インターフェース・トリガー別詳細トレース (Phase 2)
### 機能1: メンテナンススクリプトの実行
#### トリガー: 「シェルコマンドまたはGitコミット時のフック実行」
- **入力・要求（Input/Request）**:
  - `scripts/` 配下のシェルスクリプト群 (`check-structure.sh`, `sync-rule.sh`, `fetch-git-log.sh` 等)。
- **内部処理流転（Execution Flow）**:
  1. ディレクトリ構造の整合性確認 (`check-structure.sh`)。
  2. サニタイズ（日付・人名・URLのリーク検証）の実行。
  3. Git ignoreの検証（`01-private/`, `03-output/` の日付ディレクトリ）。
- **出力・応答・状態変化（Output/Response/State Change）**:
  - **成功時**: 検査パスのメッセージ出力、正常終了 (`exit 0`)。
  - **失敗時**: 該当箇所のレポート出力、エラー終了 (`exit 1`)。

### 機能2: ルール同期スクリプトの実行
#### トリガー: 「`scripts/sync-rule.sh` の実行」
- **入力・要求（Input/Request）**:
  - テンプレートブランチ (`template`)。
- **内部処理流転（Execution Flow）**:
  1. `template` ブランチから `AGENTS.md`, `CLAUDE.md`, `00-rules/`, `.agents/`, `scripts/`, `.gitleeks.toml`, `.githooks` をチェックアウト。
- **出力・応答・状態変化（Output/Response/State Change）**:
  - 最新のルール・エージェント設定に一括更新される。

### 機能3: Gitログ取得スクリプトの実行
#### トリガー: 「`scripts/fetch-git-log.sh` の実行」
- **入力・要求（Input/Request）**:
  - 対象リポジトリの URL またはローカルパス、任意でブランチ名。
- **内部処理流転（Execution Flow）**:
  1. 対象のクローン/フェッチ/プル。
  2. 前回保存したコミットハッシュとの差分検出。
  3. 差分がない場合はスキップ、ある場合は `--name-status` 付きのコミットログを抽出して既存ログの先頭にマージ。
- **出力・応答・状態変化（Output/Response/State Change）**:
  - `04-resources/git-history/<リポジトリ名>/raw-git-log.txt` と `.last_commit` の更新。

---

## 3. モジュール間連携・例外ハンドリング・設計パターン (Phase 3)
- **コンポーネント間・ドメイン間の相互作用**:
  - スクリプト群 (`scripts/`) はリポジトリの運用保守、規約維持、外部リポジトリの履歴追跡を担う。
  - Git フック（`.githooks/pre-commit`）が `check-structure.sh` を呼び出すことで、コミット時の安全性を担保する自動フィードバックループを構築している。
- **横断的関心事**:
  - **セキュリティ・プライバシー**: `01-private/` の厳格な除外、機密情報リークの自動検知（`check-structure.sh` 内の正規表現パターンマッチ）。
  - **原本非破壊**: `04-resources/` は読み取り専用とし、歴史的・一次情報は直接改変しない設計。
  2. ルールおよびストレージの同期・検証。
  3. Gitログの自動取得とインデックス更新。
- **出力・応答・状態変化（Output/Response/State Change）**:
  - **成功時**: 正常終了ステータス、ログ出力、コミットの許可。
  - **失敗時**: 構造エラーやポリシー違反の検知によるコミットのブロック。

## 3. モジュール間連携・例外ハンドリング・設計パターン (Phase 3)
- **コンポーネント間・ドメイン間の相互作用**: AIエージェントと人間が協調してナレッジを育成・管理するための構造化リポジトリシステム。厳格なセキュリティ・プライバシー規約と自動化スクリプトが連携。
- **横断的関心事**: 機密情報の保護 (`.gitignore`, `01-private/`), 原本の非破壊維持, 自動化による品質担保。
