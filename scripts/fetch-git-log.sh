#!/usr/bin/env bash
# scripts/fetch-git-log.sh
# 指定された Git リポジトリから clone/fetch してログおよびメタデータを取得
# ./scripts/fetch-git-log.sh <GitHub_URL> <ブランチ名>

set -e

INPUT_TARGET="${1:?エラー: GitHub URL またはローカルパスを指定してください (例: git@github.com:user/repo.git)}"
BRANCH_NAME="${2:-main}" # ブランチ指定（未指定の場合は main）

PKM_ROOT=$(pwd)

# --------------------------------------------------
# パス決定処理
# --------------------------------------------------
if [[ "${INPUT_TARGET}" =~ ^(https://|git@github\.com:) ]]; then
  REPO_NAME=$(basename "${INPUT_TARGET}" .git)
else
  TARGET_REPO_ABS=$(cd "${INPUT_TARGET}" && pwd)
  REPO_NAME=$(basename "$(git -C "${TARGET_REPO_ABS}" rev-parse --show-toplevel)")
fi

BASE_DIR="${PKM_ROOT}/04-resources/git-repository/${REPO_NAME}"
CLONE_DIR="${BASE_DIR}/clone/${BRANCH_NAME}"
HISTORY_DIR="${BASE_DIR}/history"

mkdir -p "${CLONE_DIR}" "${HISTORY_DIR}"

# --------------------------------------------------
# Clone / Fetch 処理
# --------------------------------------------------
if [[ "${INPUT_TARGET}" =~ ^(https://|git@github\.com:) ]]; then
  if [ ! -d "${CLONE_DIR}/.git" ]; then
    echo "📥 GitHub からリポジトリを clone しています (${BRANCH_NAME}): ${INPUT_TARGET}"
    git clone --branch "${BRANCH_NAME}" "${INPUT_TARGET}" "${CLONE_DIR}"
  else
    echo "🔄 既存の clone 領域を最新化しています: ${REPO_NAME} (${BRANCH_NAME})"
    git -C "${CLONE_DIR}" fetch origin "${BRANCH_NAME}"
    git -C "${CLONE_DIR}" checkout "${BRANCH_NAME}"
    git -C "${CLONE_DIR}" pull origin "${BRANCH_NAME}"
  fi
fi

TARGET_REPO="${CLONE_DIR}"

# --------------------------------------------------
# Git ログ・各種メタデータ解析データの取得
# --------------------------------------------------
echo "🔍 [${REPO_NAME}] Gitログおよび解析用メタデータを取得中..."

STATE_FILE="${HISTORY_DIR}/.last_commit"
RAW_LOG_FILE="${HISTORY_DIR}/raw-git-log.txt"

pushd "${TARGET_REPO}" > /dev/null

# 1. フルコミットログ（差分追跡対応）
if [ ! -f "${STATE_FILE}" ]; then
  echo "🚀 初回実行: 全コミットログを取得します。"
  git log --name-status --pretty=format:"---%nCommit: %H%nAuthor: %an%nDate: %ad%nSubject: %s%n" > "${RAW_LOG_FILE}"
else
  LAST_COMMIT=$(cat "${STATE_FILE}")
  CURRENT_HEAD=$(git rev-parse HEAD)

  if [ "${LAST_COMMIT}" != "${CURRENT_HEAD}" ]; then
    TMP_LOG=$(mktemp)
    git log "${LAST_COMMIT}..HEAD" --name-status --pretty=format:"---%nCommit: %H%nAuthor: %an%nDate: %ad%nSubject: %s%n" > "${TMP_LOG}"
    cat "${TMP_LOG}" "${RAW_LOG_FILE}" > "${RAW_LOG_FILE}.tmp"
    mv "${RAW_LOG_FILE}.tmp" "${RAW_LOG_FILE}"
    rm -f "${TMP_LOG}"
  fi
fi

git rev-parse HEAD > "${STATE_FILE}"

# 2. 追加の解析用メタデータ生成
echo "📂 ファイルツリー（追跡ファイル一覧）を出力中..."
git ls-files > "${HISTORY_DIR}/file-tree.txt"

echo "👥 開発者貢献一覧を出力中..."
git shortlog -sn --all > "${HISTORY_DIR}/contributors.txt" || true

echo "🌿 リモート/ローカルブランチ一覧を出力中..."
git branch -a -v > "${HISTORY_DIR}/active-branches.txt" || true

echo "📊 ファイル別コミット頻度ランキングを出力中..."
git log --format="" --name-only | sort | uniq -c | sort -nr | head -n 50 > "${HISTORY_DIR}/stats.txt" || true

popd > /dev/null

echo "✅ 取得完了:"
echo "  - ソースコード: ${CLONE_DIR}"
echo "  - 解析データ:   ${HISTORY_DIR}"