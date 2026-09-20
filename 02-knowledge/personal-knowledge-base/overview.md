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
- [x] ルール・規約管理基盤 (`00-rules/`)
- [x] ナレッジ蓄積ストレージ (`02-knowledge/`)
- [x] 成果物・出力管理 (`03-output/`)
- [x] 一次情報リソース・Gitリポジトリ管理 (`04-resources/git-repository/`)
- [x] タスク・プロジェクト管理 (`05-todo/`)
- [x] 自動化・メンテナンススクリプト (`scripts/`, `.githooks/`)

## 2. インターフェース・トリガー別詳細トレース (Phase 2 必須)

### 機能1: ナレッジベース運用・自動化スクリプト
#### トリガー1: 「AIエージェント実行・スクリプト実行 (`scripts/`) / Git Commit」
- **入力・要求（Input/Request）**:
  - `AGENTS.md` および `00-rules/` に定義された絶対遵守ルール、リポジトリコード、スクリプトへの引数。
- **内部処理流転（Execution Flow）**:
  1. 絶対遵守ルール（機密保護・原本非破壊・ファイル移動ポリシー）のロード。
  2. `04-resources/git-repository/` 内コードの解析・スキャン。
  3. `02-knowledge/` への構造化Markdownの蓄積および `unexplored_domains` の消化。
  4. Gitコミットおよび `.githooks/` による検証。
- **出力・応答・状態変化（Output/Response/State Change）**:
  - **成功時**: `02-knowledge/` の更新、Gitリポジトリへのコミット完了、ログ出力。
  - **失敗時**: ルール違反検知時の処理中断、エラーログ出力。

## 3. モジュール間連携・例外ハンドリング・設計パターン (Phase 3)
- **コンポーネント間・ドメイン間の相互作用**: リソース層 (`04-resources/`) の読み取り専用原則を厳守しつつ、ナレッジ層 (`02-knowledge/`) を自動進化させるエージェント連携。
- **横断的関心事**: プライバシー・セキュリティ規約 (`00-rules/privacy-security.md`) による機密情報の完全排除。
