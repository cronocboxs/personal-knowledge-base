#!/usr/bin/env bash
# scripts/fetch-git-log.sh
# 指定された Git リポジトリ（GitHub URL または ローカルパス）から clone/fetch してログを取得

set -e

INPUT_TARGET="${1:?エラー: GitHub URL またはローカルパスを指定してください (例: git@github.com:user/repo.git)}"
BRANCH_NAME="${2}" # ブランチ指定（未指定の場合はデフォルトブランチ）

PKM_ROOT=$(pwd)
CLONE_BASE_DIR="${PKM_ROOT}/04-resources/git-clone"

# 引数が URL かローカルパスかを判定して対象ディレクトリを決定
if [[ "${INPUT_TARGET}" =~ ^(https://|git@github\.com:) ]]; then
  # URL からリポジトリ名を抽出 (例: repo.git -> repo)
  REPO_NAME=$(basename "${INPUT_TARGET}" .git)
  TARGET_REPO_ABS="${CLONE_BASE_DIR}/${REPO_NAME}"

  mkdir -p "${CLONE_BASE_DIR}"

  if [ ! -d "${TARGET_REPO_ABS}" ]; then
    echo "📥 GitHub からリポジトリを clone しています: ${INPUT_TARGET}"
    git clone "${INPUT_TARGET}" "${TARGET_REPO_ABS}"
  else
    echo "🔄 既存の clone 領域を最新化 (fetch/pull) しています: ${REPO_NAME}"
    git -C "${TARGET_REPO_ABS}" fetch --all --prune
  fi

  # ブランチ指定がある場合は切り替え
  if [ -n "${BRANCH_NAME}" ]; then
    echo "🔀 ブランチを切り替えます: ${BRANCH_NAME}"
    git -C "${TARGET_REPO_ABS}" checkout "${BRANCH_NAME}"
    git -C "${TARGET_REPO_ABS}" pull origin "${BRANCH_NAME}"
  else
    # 最新の標準ブランチを反映
    git -C "${TARGET_REPO_ABS}" pull
  fi
else
  # 従来のローカルパス指定
  TARGET_REPO_ABS=$(cd "${INPUT_TARGET}" && pwd)
  REPO_NAME=$(basename "$(git -C "${TARGET_REPO_ABS}" rev-parse --show-toplevel)")
fi

OUTPUT_DIR="${PKM_ROOT}/04-resources/git-history/${REPO_NAME}"
STATE_FILE="${OUTPUT_DIR}/.last_commit"
RAW_LOG_FILE="${OUTPUT_DIR}/raw-git-log.txt"

mkdir -p "${OUTPUT_DIR}"

echo "🔍 [${REPO_NAME}] Gitログの取得を開始します... (対象: ${TARGET_REPO_ABS})"

pushd "${TARGET_REPO_ABS}" > /dev/null

if [ ! -f "${STATE_FILE}" ]; then
  echo "🚀 初回実行: すべてのGitコミットログを取得します。"
  git log --name-status --pretty=format:"---%nCommit: %H%nAuthor: %an%nDate: %ad%nSubject: %s%n" > "${RAW_LOG_FILE}"
else
  LAST_COMMIT=$(cat "${STATE_FILE}")
  CURRENT_HEAD=$(git rev-parse HEAD)

  if [ "${LAST_COMMIT}" = "${CURRENT_HEAD}" ]; then
    echo "✅ 新しいコミットはありません。スキップします。"
    popd > /dev/null
    exit 0
  fi

  TMP_LOG=$(mktemp)
  git log "${LAST_COMMIT}..HEAD" --name-status --pretty=format:"---%nCommit: %H%nAuthor: %an%nDate: %ad%nSubject: %s%n" > "${TMP_LOG}"

  cat "${TMP_LOG}" "${RAW_LOG_FILE}" > "${RAW_LOG_FILE}.tmp"
  mv "${RAW_LOG_FILE}.tmp" "${RAW_LOG_FILE}"
  rm -f "${TMP_LOG}"
fi

git rev-parse HEAD > "${STATE_FILE}"

popd > /dev/null

echo "✅ 取得完了: ${RAW_LOG_FILE} にログを保存しました。"
