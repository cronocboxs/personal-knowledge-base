---
created: 2026-09-20
updated: 2026-09-20
tags: [personal-knowledge-base, spec, code-analysis]
phase: 3
status: active
unexplored_domains: []
---

# personal-knowledge-base 挙動・処理仕様ナレッジ

## 1. 識別された機能・インターフェース一覧 (Phase 1)
- [x] ルール定義 (`00-rules/`: ワークフロー、分類、フォーマット、エージェント行動規範、セキュリティ)
- [x] 自動化メンテナンススクリプト (`scripts/`: ログ取得、ルール同期、ストレージ同期、構造チェック)
- [x] Gitフック設定 (`.githooks/pre-commit`) および Gitleeks セキュリティスキャン設定 (`.gitleeks.toml`)
- [x] ナレッジベースディレクトリ構造管理 (`01-private/`, `02-knowledge/`, `03-output/`, `04-resources/`, `05-todo/`, `06-storage/`, `99-trash/`)

## 2. インターフェース・トリガー別詳細トレース (Phase 2)
### 機能1: メンテナンススクリプトの実行
#### トリガー: 「シェルコマンドまたはGitコミット時のフック実行」
- **入力・要求（Input/Request）**:
  - `scripts/` 配下のシェルスクリプト群 (`check-structure.sh`, `sync-rule.sh`, `fetch-git-log.sh` 等)。
- **内部処理流転（Execution Flow）**:
  1. ディレクトリ構造の整合性確認 (`check-structure.sh`)。
  2. ルールおよびストレージの同期・検証。
  3. Gitログの自動取得とインデックス更新。
- **出力・応答・状態変化（Output/Response/State Change）**:
  - **成功時**: 正常終了ステータス、ログ出力、コミットの許可。
  - **失敗時**: 構造エラーやポリシー違反の検知によるコミットのブロック。

## 3. モジュール間連携・例外ハンドリング・設計パターン (Phase 3)
- **コンポーネント間・ドメイン間の相互作用**: AIエージェントと人間が協調してナレッジを育成・管理するための構造化リポジトリシステム。厳格なセキュリティ・プライバシー規約と自動化スクリプトが連携。
- **横断的関心事**: 機密情報の保護 (`.gitignore`, `01-private/`), 原本の非破壊維持, 自動化による品質担保。
