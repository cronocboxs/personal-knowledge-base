---
created: 2026-09-20
tags: [knowledge-base, architecture, git, hooks, scripts]
status: active
---

# personal-knowledge-base アーキテクチャ仕様

本リポジトリは、人間とAIエージェントが安全かつ効率的にナレッジを蓄積・共有するための階層型ディレクトリ構造を採用しています。

## ディレクトリ設計

- `00-rules/`: システム規約・フォーマット（参照専用）
- `01-private/`: 最高機密・個人情報（`.gitignore` 対象）
- `02-knowledge/`: 構造化された知見・概念ノート（AI・人間による蓄積先）
- `03-output/`: 生成物・成果物・ドラフト
- `04-resources/`: 参照一次情報原本（読み取り専用・非破壊）
- `05-todo/`: タスク・プロジェクト管理
- `06-storage/`: 大容量バイナリ・動画・PDF等（`.gitignore` 対象）
- `99-trash/`: 一時廃棄退避場所（直接削除禁止）
- `scripts/`: 自動化シェルスクリプト
- `.agents/skills/`: エージェントスキル定義

## 品質・安全管理

- Git pre-commit フック (`.githooks/pre-commit`) および Gitleeks 設定 (`.gitleeks.toml`) による機密情報の漏洩防止。
