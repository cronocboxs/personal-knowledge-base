#!/usr/bin/env bash
# scripts/sync-rule.sh
# template ブランチからシステム規約・エージェント定義のみを選択的に同期するスクリプト

set -e

SOURCE_BRANCH="template"

echo "🔄 Syncing rules and agent configs from '${SOURCE_BRANCH}'..."

# template ブランチから定義ファイルのみをチェックアウト
git checkout "${SOURCE_BRANCH}" -- \
  AGENTS.md \
  CLAUDE.md \
  README.md \
  .gitignore \
  .gitleeks.toml \
  .agents/ \
  .githooks \
  00-rules/ \
  04-resources/rules \
  scripts/

echo "✅ Rules updated successfully from ${SOURCE_BRANCH}."
echo "💡 Run 'git status' and commit the updated rules if needed."