---
created: 2026-09-20
updated: 2026-09-20
tags: [personal-knowledge-base, spec, code-analysis]
phase: 3
status: active
unexplored_domains: []
---

# personal-knowledge-base リポジトリ 挙動・処理仕様ナレッジ

## 1. 識別された機能・インターフェース一覧 (Phase 1)
- [x] ルール・規約体系 (`00-rules/`: `workflow.md`, `classification.md`, `formatting.md`, `agent-behavior.md`, `privacy-security.md`)
- [x] エージェント運用ガイドライン (`AGENTS.md`, `CLAUDE.md`)
- [x] 自動化・同期スクリプト (`scripts/`: `fetch-git-log.sh`, `sync-rule.sh`, `sync-storage.sh`, `check-structure.sh`)
- [x] タスク管理・成果物ディレクトリ (`05-todo/`, `03-output/`)
- [x] ナレッジ蓄積ディレクトリ (`02-knowledge/`)

## 2. インターフェース・トリガー別詳細トレース (Phase 2)

### 機能1: Git履歴取得スクリプト
#### トリガー: 「`./scripts/fetch-git-log.sh <URL> <BRANCH>` の実行」
- **入力・要求（Input/Request）**:
  - 対象GitリポジトリのURLおよびブランチ名。
- **内部処理流転（Execution Flow）**:
  1. 指定リポジトリのクローンまたはfetchを実施。
  2. 統計情報、コントリビューター、ファイルツリー、コミットログを抽出。
  3. `04-resources/git-repository/<リポジトリ名>/history/` 配下に保存。
- **出力・応答・状態変化（Output/Response/State Change）**:
  - **成功時**: 履歴・ログファイルの生成 (`stats.txt`, `raw-git-log.txt` 等)。
  - **失敗時**: ネットワークエラーまたはURL不正時の終了コード返却。

### 機能2: 構造チェック・同期スクリプト
#### トリガー: 「`./scripts/check-structure.sh` / `sync-rule.sh` の実行」
- **入力・要求（Input/Request）**:
  - リポジトリ内のディレクトリ構成および規約ファイル。
- **内部処理流転（Execution Flow）**:
  1. 必須ディレクトリ・ファイルの存在確認。
  2. ルール間の整合性チェック。
- **出力・応答・状態変化（Output/Response/State Change）**:
  - **成功時**: チェック完了メッセージ、異常なしの確認。

## 3. モジュール間連携・例外ハンドリング・設計パターン (Phase 3)
- **コンポーネント間・ドメイン間の相互作用**:
  - 人間とAIエージェントが協調して `04-resources/`（一次情報）から `02-knowledge/`（知見）を経由して `03-output/`（成果物）を生み出す不変のライフサイクル・フロー。
- **横断的関心事**:
  - 機密情報の保護 (`01-private/` の除外)、原本非破壊の原則、厳格なディレクトリ編集ポリシーの徹底。
