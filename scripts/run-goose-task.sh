#!/usr/bin/env bash
# scripts/run-goose-task.sh
# 指定されたスキル名（またはタスク指示書パス）を受け取り、Goose を非対話実行する汎用スクリプト

set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "${PROJECT_DIR}"

INPUT_TARGET="${1:?エラー: スキル名またはタスク指示書のパスを指定してください (例: ingest-repo-knowledge)}"

# 1. 渡された引数がファイルパスそのものかチェック
if [ -f "${INPUT_TARGET}" ]; then
  TASK_FILE="${INPUT_TARGET}"
# 2. ディレクトリ名指定の場合: .agents/skills/<スキル名>/SKILL.md を検索
elif [ -f ".agents/skills/${INPUT_TARGET}/SKILL.md" ]; then
  TASK_FILE=".agents/skills/${INPUT_TARGET}/SKILL.md"
else
  echo "❌ タスク指示書が存在しません: ${INPUT_TARGET}"
  echo "   (検索パス: .agents/skills/${INPUT_TARGET}/SKILL.md)"
  exit 1
fi

# cron環境用の PATH / 環境変数設定
export PATH="/usr/local/bin:/usr/bin:/bin:${HOME}/.local/bin:${PATH}"

echo "=========================================="
echo "🤖 Goose タスク実行開始: ${TASK_FILE} ($(date))"
echo "=========================================="

# -i オプションで指示書ファイルを指定して実行
goose run -i "${TASK_FILE}"

echo "✅ タスク完了: ${TASK_FILE} ($(date))"