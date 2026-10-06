#!/usr/bin/env bash
# scripts/run-goose-task.sh
# Goose を使用した自律型ナレッジ昇華実行スクリプト (外部ファイル構成版)

set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "${PROJECT_DIR}"

# デフォルト値の設定
TARGET_PATH="04-resources/"
INSTRUCTION="agent"
FORCE_FLG="false"
CATEGORY="auto"

# ヘルプメッセージを表示する関数
show_help() {
  cat << 'EOF'
usage: run-goose-task.sh [-h] [-t PATH] [-i NAME_OR_PATH] [-f] [-c CATEGORY]

🤖 Goose 自律型ナレッジ昇華スクリプト
Goose エージェントを起動し、指定された条件・指示書に従って自律的にナレッジ昇華・リレーション構築・Gitコミットを実行します。

options:
  -h, --help            ヘルプメッセージを表示して終了します
  -t PATH, --target PATH
                        解析対象のファイルパスまたはディレクトリパス (デフォルト: 04-resources/)
  -i NAME_OR_PATH, --instruction NAME_OR_PATH
                        使用する指示書（スキル名、ファイル名、またはパス / デフォルト: sublimation-agent）
  -f, --force           昇華済みノートが存在する場合でも強制的に再昇華（上書き）します
  -c CATEGORY, --category CATEGORY
                        保存先カテゴリ名 ('auto' の場合はAIが自動判別 / デフォルト: auto)
EOF
  exit 0
}

# ---------------------------------------------------------
# CLI 引数のパース
# ---------------------------------------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) show_help ;;
    -t|--target) TARGET_PATH="$2"; shift 2 ;;
    -i|--instruction) INSTRUCTION="$2"; shift 2 ;;
    -f|--force) FORCE_FLG="true"; shift ;;
    -c|--category) CATEGORY="$2"; shift 2 ;;
    *)
      if [[ -z "${USER_POSITIONAL_INST}" ]]; then
        USER_POSITIONAL_INST="$1"
        INSTRUCTION="$1"
        shift
      else
        echo "⚠️ 未知のオプション: $1"
        show_help
      fi
      ;;
  esac
done

# ---------------------------------------------------------
# 指示書（スキルファイル）および Agent 名の判定
# ---------------------------------------------------------
if [ -f "${INSTRUCTION}" ]; then
  TASK_FILE="${INSTRUCTION}"
  AGENT_NAME=$(basename "${INSTRUCTION}" .md)
elif [ -f ".agents/skills/${INSTRUCTION}/SKILL.md" ]; then
  TASK_FILE=".agents/skills/${INSTRUCTION}/SKILL.md"
  AGENT_NAME="${INSTRUCTION}"
elif [ -f "00-rules/prompts/${INSTRUCTION}" ]; then
  TASK_FILE="00-rules/prompts/${INSTRUCTION}"
  AGENT_NAME=$(basename "${INSTRUCTION}" .md)
elif [ -f "00-rules/prompts/${INSTRUCTION}.md" ]; then
  TASK_FILE="00-rules/prompts/${INSTRUCTION}.md"
  AGENT_NAME="${INSTRUCTION}"
else
  echo "❌ タスク指示書が存在しません: ${INSTRUCTION}"
  exit 1
fi

export PATH="/usr/local/bin:/usr/bin:/bin:${HOME}/.local/bin:${PATH}"

LOG_DIR="${PROJECT_DIR}/04-resources/logs"
API_USAGE_DIR="${LOG_DIR}/api_usage"
mkdir -p "${API_USAGE_DIR}"

TMP_RUN_LOG="${LOG_DIR}/goose_last_run.log"
TMP_TASK_FILE="${LOG_DIR}/goose_active_task.md"

TODAY=$(date +"%Y-%m-%d")
DAILY_LOG_FILE="${API_USAGE_DIR}/${TODAY}.log"

# ---------------------------------------------------------
# TODOファイルパス決定 & Python外部スクリプトの呼び出し
# ---------------------------------------------------------
SAFE_TARGET_NAME=$(echo "${TARGET_PATH}" | sed 's/[^a-zA-Z0-9]/--/g' | sed 's/----*/-/g' | sed 's/^-//;s/-$//')
[ -z "${SAFE_TARGET_NAME}" ] && SAFE_TARGET_NAME="root"

TODO_DIR="05-todo/${AGENT_NAME}"
TODO_FILE="${TODO_DIR}/${SAFE_TARGET_NAME}-todo.md"

export PY_TODO_FILE="${TODO_FILE}"
export PY_TARGET_PATH="${TARGET_PATH}"
export PY_FORCE_FLG="${FORCE_FLG}"
export PY_AGENT_NAME="${AGENT_NAME}"
export PY_TODAY="${TODAY}"

# 外部スクリプトを実行
python3 scripts/init_todo_list.py

# ---------------------------------------------------------
# テンプレートからのアクティブタスク指示書の生成
# ---------------------------------------------------------
EXISTING_CATEGORIES=$(ls -d 02-knowledge/*/ 2>/dev/null | sed 's|02-knowledge/||;s|/||' | grep -v -E '^(head|note)$' | tr '\n' ', ')
TEMPLATE_FILE="00-rules/templates/goose_task_context.md"

if [ -f "${TEMPLATE_FILE}" ]; then
  # sed を使用してテンプレートの変数を置換
  sed -e "s|{{AGENT_NAME}}|${AGENT_NAME}|g" \
      -e "s|{{TARGET_PATH}}|${TARGET_PATH}|g" \
      -e "s|{{TODO_FILE}}|${TODO_FILE}|g" \
      -e "s|{{FORCE_FLG}}|${FORCE_FLG}|g" \
      -e "s|{{CATEGORY}}|${CATEGORY}|g" \
      -e "s|{{EXISTING_CATEGORIES}}|${EXISTING_CATEGORIES}|g" \
      "${TEMPLATE_FILE}" > "${TMP_TASK_FILE}"
  
  # 本文指示書を末尾に結合
  echo "" >> "${TMP_TASK_FILE}"
  cat "${TASK_FILE}" >> "${TMP_TASK_FILE}"
else
  # テンプレートが存在しない場合のフォールバック
  cat "${TASK_FILE}" > "${TMP_TASK_FILE}"
fi

echo "=========================================="
echo "🤖 Goose タスク実行開始: ${TASK_FILE} ($(date))"
echo "  ・Agent名     : ${AGENT_NAME}"
echo "  ・対象パス    : ${TARGET_PATH}"
echo "  ・TODOファイル: ${TODO_FILE}"
echo "  ・指定カテゴリ: ${CATEGORY}"
echo "=========================================="


# ---------------------------------------------------------
# Goose 実行 & ログ集計
# ---------------------------------------------------------
set +e
RUST_LOG=debug goose run -i "${TMP_TASK_FILE}" 2>&1 | tee "${TMP_RUN_LOG}"
GOOSE_EXIT_CODE=${PIPESTATUS[0]}
set -e

API_CALL_COUNT=$(grep -i -c -E "generate_content|generativelanguage|google" "${TMP_RUN_LOG}" || true)

PREV_TOTAL=0
if [ -f "${DAILY_LOG_FILE}" ]; then
  PREV_TOTAL=$(tail -n 1 "${DAILY_LOG_FILE}" | awk '{print $NF}')
  if ! [[ "${PREV_TOTAL}" =~ ^[0-9]+$ ]]; then
    PREV_TOTAL=0
  fi
fi

NEW_TOTAL=$((PREV_TOTAL + API_CALL_COUNT))
echo "$(date +'%Y-%m-%d %H:%M:%S') - 今回: ${API_CALL_COUNT} 回 | 日別累計: ${NEW_TOTAL}" >> "${DAILY_LOG_FILE}"

rm -f "${TMP_TASK_FILE}"

echo "------------------------------------------"
echo "📊 実行結果サマリー:"
echo "   ・ステータス: $( [ ${GOOSE_EXIT_CODE} -eq 0 ] && echo '成功 (0)' || echo "失敗 (${GOOSE_EXIT_CODE})" )"
echo "   ・今回 API 問い合わせ回数: ${API_CALL_COUNT} 回"
echo "   ・本日（${TODAY}）の総問い合わせ回数: ${NEW_TOTAL} 回"
echo "=========================================="
echo "✅ タスク完了: ${TASK_FILE} ($(date))"

exit ${GOOSE_EXIT_CODE}