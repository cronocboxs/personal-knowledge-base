---
created: 2026-09-20
tags: [knowledge-base, agents, automation, rules, workflow]
status: active
---

# personal-knowledge-base 概要

本リポジトリ (`personal-knowledge-base`) は、AIエージェント（Goose, Claude, Cursor等）および自動化スクリプトとの協調運用を前提とした構造化ナレッジベースです。

## コアコンセプト

- **完全な規約駆動開発 (`00-rules/`)**:
  - 情報ライフサイクル、ファイル分類、フォーマット、行動規範、プライバシー保護の厳格なルール定義。
- **エージェントスキル連携 (`.agents/skills/`)**:
  - `ingest-repo-knowledge` や `generate-docs-git` などの自律型スキル定義。
- **自動化スクリプト (`scripts/`)**:
  - Gitログ取得、構造チェック、ストレージ同期等の運用自動化シェルスクリプト群。
