---
created: 2026-09-19
tags: [scripts, automation, maintenance]
status: active
---

# 自動化スクリプト仕様

`personal-knowledge-base` のリポジトリには、維持管理やタスク実行を自動化するための各種スクリプトが `scripts/` 配下に用意されています。

## scripts/ 配下の主なスクリプト

1. **`check-structure.sh`**:
   - リポジトリのディレクトリ構造や必須ファイルの存在、規約違反がないかをチェックするバリデーションスクリプト。
2. **`fetch-git-log.sh`**:
   - Gitログの取得や分析を自動化するためのヘルパースクリプト。
3. **`sync-rule.sh`**:
   - ルールや規約の同期・適用を行うスクリプト。
4. **`sync-storage.sh`**:
   - `06-storage/` 等の外部ストレージ同期を管理するスクリプト。
5. **`run-goose-task.sh`**:
   - AIエージェント（Goose）によるタスク実行を呼び出すための自動化スクリプト。

## 運用上のポイント

- 定型作業や一括メンテナンスを行う際は、手動でのファイル操作を行わず、原則として `scripts/` 内のスクリプトを活用、または新規作成して実行すること（`scripts/` 内での検証）。
