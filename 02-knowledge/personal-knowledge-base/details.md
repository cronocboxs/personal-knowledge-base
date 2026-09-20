---
title: "personal-knowledge-base リポジトリ詳細実装仕様"
type: "specification"
repository: "personal-knowledge-base"
created_at: "2026-09-20"
---

# personal-knowledge-base 詳細実装仕様

## 1. 概要
AIエージェントおよび自動化スクリプトとの協調運用を前提とした構造化ナレッジベースです。

## 2. ディレクトリ設計とポリシー
- `00-rules/`: システム規約・フォーマット（参照専用）
- `01-private/`: プライベート情報・機密情報（`.gitignore` 対象）
- `02-knowledge/`: 体系化された知見・概念ノート
- `03-output/`: 生成物・成果物・ドラフト
- `04-resources/`: 一次情報原本（読み取り専用）
- `05-todo/`: タスク管理・ロードマップ
- `06-storage/`: バイナリ等の大容量ファイル
- `99-trash/`: 一時廃棄場所（直接削除禁止）
- `scripts/`: 自動化・メンテナンススクリプト
- `.agents/`: エージェントスキル・手順書

## 3. 自動化とエージェント連携
AGENTS.mdの絶対遵守ルールに基づき、インジェストやナレッジ更新、git commitの自動化が組み込まれています。
