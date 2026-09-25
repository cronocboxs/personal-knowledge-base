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

# 実行ログ・集計ファイルの設定（04-resources/logs 配下）
LOG_DIR="${PROJECT_DIR}/04-resources/logs"
API_USAGE_DIR="${LOG_DIR}/api_usage"
mkdir -p "${API_USAGE_DIR}"

TMP_RUN_LOG="${LOG_DIR}/goose_last_run.log"

# 日付別集計ファイルのパス (例: 04-resources/logs/api_usage/2026-09-20.log)
TODAY=$(date +"%Y-%m-%d")
DAILY_LOG_FILE="${API_USAGE_DIR}/${TODAY}.log"

echo "=========================================="
echo "🤖 Goose タスク実行開始: ${TASK_FILE} ($(date))"
echo "=========================================="

# RUST_LOG=debug を付与して Goose を実行し、ログを取得
set +e
RUST_LOG=debug goose run -i "${TASK_FILE}" 2>&1 | tee "${TMP_RUN_LOG}"
GOOSE_EXIT_CODE=${PIPESTATUS[0]}
set -e

# 今回の実行での API 問い合わせ回数を集計
API_CALL_COUNT=$(grep -i -c -E "generate_content|generativelanguage|google" "${TMP_RUN_LOG}" || true)

# 日別の累計カウント計算
PREV_TOTAL=0
if [ -f "${DAILY_LOG_FILE}" ]; then
  PREV_TOTAL=$(tail -n 1 "${DAILY_LOG_FILE}" | awk '{print $NF}')
  # 数値として扱えない場合のガード
  if ! [[ "${PREV_TOTAL}" =~ ^[0-9]+$ ]]; then
    PREV_TOTAL=0
  fi
fi

NEW_TOTAL=$((PREV_TOTAL + API_CALL_COUNT))

# 日別ログファイルに追記記録
echo "$(date +'%Y-%m-%d %H:%M:%S') - 今回: ${API_CALL_COUNT} 回 | 日別累計: ${NEW_TOTAL}" >> "${DAILY_LOG_FILE}"

echo "------------------------------------------"
echo "📊 実行結果サマリー:"
echo "   ・ステータス: $( [ ${GOOSE_EXIT_CODE} -eq 0 ] && echo '成功 (0)' || echo "失敗 (${GOOSE_EXIT_CODE})" )"
echo "   ・今回 API 問い合わせ回数: ${API_CALL_COUNT} 回"
echo "   ・本日（${TODAY}）の総問い合わせ回数: ${NEW_TOTAL} 回"
echo "=========================================="
echo "✅ タスク完了: ${TASK_FILE} ($(date))"

exit ${GOOSE_EXIT_CODE}