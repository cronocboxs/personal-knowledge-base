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
ERROR_STATE_FILE="${LOG_DIR}/consecutive_error_count.txt"

# 日付別集計ファイルのパス (例: 04-resources/logs/api_usage/2026-09-20.log)
TODAY=$(date +"%Y-%m-%d")
DAILY_LOG_FILE="${API_USAGE_DIR}/${TODAY}.log"

# 現在の連続エラーカウントを取得
CONSECUTIVE_ERRORS=0
if [ -f "${ERROR_STATE_FILE}" ]; then
  CONSECUTIVE_ERRORS=$(cat "${ERROR_STATE_FILE}")
  if ! [[ "${CONSECUTIVE_ERRORS}" =~ ^[0-9]+$ ]]; then
    CONSECUTIVE_ERRORS=0
  fi
fi

echo "=========================================="
echo "🤖 Goose タスク実行開始: ${TASK_FILE} ($(date))"
echo "=========================================="

# RUST_LOG=debug を付与して Goose を実行し、ログを取得
set +e
RUST_LOG=debug goose run -i "${TASK_FILE}" 2>&1 | tee "${TMP_RUN_LOG}"
GOOSE_EXIT_CODE=${PIPESTATUS[0]}
set -e

# ----------------------------------------------------
# 🔍 検知機能 1: APIエラー・レートリミットの解析
# ----------------------------------------------------
# ログ内から明確なエラーレスポンス（HTTP 429/500/503 等）を検出
API_ERROR_DETECTED=$(grep -i -c -E "status:\s*(429|500|503)|HTTP/(1\.1|2)\s+(429|500|503)|rate\s*limit\s*exceeded|quota\s*exceeded|resourceexhausted" "${TMP_RUN_LOG}" || true)

# 1. Gooseプロセスが正常終了 (exit 0) した場合 ➔ ログの内容にかかわらず「完全成功」
if [ ${GOOSE_EXIT_CODE} -eq 0 ]; then
  CONSECUTIVE_ERRORS=0
  echo 0 > "${ERROR_STATE_FILE}"

# 2. Gooseプロセスが異常終了 (exit non-zero) し、かつ明確なAPIエラーが検知された場合
else
  CONSECUTIVE_ERRORS=$((CONSECUTIVE_ERRORS + 1))
  echo "${CONSECUTIVE_ERRORS}" > "${ERROR_STATE_FILE}"
  echo "⚠️ [警告] APIエラーまたはプロセス異常を検知しました (連続 ${CONSECUTIVE_ERRORS} 回目)"
fi

# ----------------------------------------------------
# 📊 集計機能: 今回の API 問い合わせ回数
# ----------------------------------------------------
API_CALL_COUNT=$(grep -i -c -E "generate_content|generativelanguage|google" "${TMP_RUN_LOG}" || true)

PREV_TOTAL=0
if [ -f "${DAILY_LOG_FILE}" ]; then
  PREV_TOTAL=$(tail -n 1 "${DAILY_LOG_FILE}" | awk '{print $NF}')
  if ! [[ "${PREV_TOTAL}" =~ ^[0-9]+$ ]]; then
    PREV_TOTAL=0
  fi
fi

NEW_TOTAL=$((PREV_TOTAL + API_CALL_COUNT))
echo "$(date +'%Y-%m-%d %H:%M:%S') - 今回: ${API_CALL_COUNT} 回 | 日別累計: ${NEW_TOTAL} | 連続エラー: ${CONSECUTIVE_ERRORS}" >> "${DAILY_LOG_FILE}"

echo "------------------------------------------"
echo "📊 実行結果サマリー:"
echo "   ・ステータス: $( [ ${GOOSE_EXIT_CODE} -eq 0 ] && echo '成功 (0)' || echo "失敗 (${GOOSE_EXIT_CODE})" )"
echo "   ・APIエラー検知数: ${API_ERROR_DETECTED} 件"
echo "   ・連続エラーカウント: ${CONSECUTIVE_ERRORS} / 5 回"
echo "   ・今回 API 問い合わせ回数: ${API_CALL_COUNT} 回"
echo "   ・本日（${TODAY}）の総問い合わせ回数: ${NEW_TOTAL} 回"
echo "=========================================="

# ----------------------------------------------------
# 🛑 検知機能 2: 5回連続エラー時の安全停止ガード
# ----------------------------------------------------
if [ ${CONSECUTIVE_ERRORS} -ge 5 ]; then
  echo "❌ 【安全停止】5回連続でAPIエラーが発生したため、コスト保護のため処理を完全停止します。"
  echo "   (状態リセットが必要な場合は '${ERROR_STATE_FILE}' を削除してください)"
  exit 99
fi

echo "✅ タスク完了: ${TASK_FILE} ($(date))"
exit ${GOOSE_EXIT_CODE}