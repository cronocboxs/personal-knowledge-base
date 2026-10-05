#!/usr/bin/env bash
# scripts/run-goose-task.sh
# Goose を使用した自律型ナレッジ昇華実行スクリプト (CLIオプション対応版)

set -e

PROJECT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
cd "${PROJECT_DIR}"

# デフォルト値の設定
TARGET_PATH="04-resources/"
INSTRUCTION="sublimation-agent"
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

実行例:
  # 1. 04-resources/ 全体を対象にデフォルトスキルで実行
  ./scripts/run-goose-task.sh

  # 2. 特定のディレクトリ配下を Goose で再昇華 (--force)
  ./scripts/run-goose-task.sh -t scripts/server/ -f

  # 3. 特定ファイル・指定カテゴリ・指示書で実行
  ./scripts/run-goose-task.sh -t 04-resources/app.py -i code-analysis -c "system-architecture"
EOF
  exit 0
}

# ---------------------------------------------------------
# CLI 引数のパース (getopts / 手動解析)
# ---------------------------------------------------------
while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help)
      show_help
      ;;
    -t|--target)
      TARGET_PATH="$2"
      shift 2
      ;;
    -i|--instruction)
      INSTRUCTION="$2"
      shift 2
      ;;
    -f|--force)
      FORCE_FLG="true"
      shift
      ;;
    -c|--category)
      CATEGORY="$2"
      shift 2
      ;;
    *)
      # 位置引数として指示書が直接渡された場合の互換性維持
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
# 指示書（スキルファイル）のパス解決
# ---------------------------------------------------------
if [ -f "${INSTRUCTION}" ]; then
  TASK_FILE="${INSTRUCTION}"
elif [ -f ".agents/skills/${INSTRUCTION}/SKILL.md" ]; then
  TASK_FILE=".agents/skills/${INSTRUCTION}/SKILL.md"
elif [ -f "00-rules/prompts/${INSTRUCTION}" ]; then
  TASK_FILE="00-rules/prompts/${INSTRUCTION}"
elif [ -f "00-rules/prompts/${INSTRUCTION}.md" ]; then
  TASK_FILE="00-rules/prompts/${INSTRUCTION}.md"
else
  echo "❌ タスク指示書が存在しません: ${INSTRUCTION}"
  echo "   (検索パス: ${INSTRUCTION}, .agents/skills/${INSTRUCTION}/SKILL.md, 00-rules/prompts/)"
  exit 1
fi

# cron環境用の PATH / 環境変数設定
export PATH="/usr/local/bin:/usr/bin:/bin:${HOME}/.local/bin:${PATH}"

# ログディレクトリ設定
LOG_DIR="${PROJECT_DIR}/04-resources/logs"
API_USAGE_DIR="${LOG_DIR}/api_usage"
mkdir -p "${API_USAGE_DIR}"

TMP_RUN_LOG="${LOG_DIR}/goose_last_run.log"
TMP_TASK_FILE="${LOG_DIR}/goose_active_task.md"

TODAY=$(date +"%Y-%m-%d")
DAILY_LOG_FILE="${API_USAGE_DIR}/${TODAY}.log"

# ---------------------------------------------------------
# Goose 実行用の一時指示書ファイルの作成 (動的パラメータ注入)
# ---------------------------------------------------------
cat << EOF > "${TMP_TASK_FILE}"
# 実行パラメータ context
- 解析対象パス (-t): ${TARGET_PATH}
- 強制再昇華フラグ (-f): ${FORCE_FLG}
- 保存カテゴリ指定 (-c): ${CATEGORY}

---

$(cat "${TASK_FILE}")
EOF

echo "=========================================="
echo "🤖 Goose タスク実行開始: ${TASK_FILE} ($(date))"
echo "  ・対象パス    : ${TARGET_PATH}"
echo "  ・強制再昇華  : ${FORCE_FLG}"
echo "  ・指定カテゴリ: ${CATEGORY}"
echo "=========================================="

# RUST_LOG=debug を付与して Goose を実行
set +e
RUST_LOG=debug goose run -i "${TMP_TASK_FILE}" 2>&1 | tee "${TMP_RUN_LOG}"
GOOSE_EXIT_CODE=${PIPESTATUS[0]}
set -e

# API 問い合わせ回数の集計ログ保存
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

# 一時指示書の削除
rm -f "${TMP_TASK_FILE}"

echo "------------------------------------------"
echo "📊 実行結果サマリー:"
echo "   ・ステータス: $( [ ${GOOSE_EXIT_CODE} -eq 0 ] && echo '成功 (0)' || echo "失敗 (${GOOSE_EXIT_CODE})" )"
echo "   ・今回 API 問い合わせ回数: ${API_CALL_COUNT} 回"
echo "   ・本日（${TODAY}）の総問い合わせ回数: ${NEW_TOTAL} 回"
echo "=========================================="
echo "✅ タスク完了: ${TASK_FILE} ($(date))"

exit ${GOOSE_EXIT_CODE}
