#!/usr/bin/env bash
# scripts/run-graphify.sh
# 指定された Git リポジトリ（clone 領域）に対して Graphify によるコード構造解析を実行し、
# 04-resources/git-repository/<Repository>/graph/<branch> に整理して出力する。
# 使い方: ./scripts/run-graphify.sh <リポジトリ名またはローカルcloneパス> [ブランチ名]

set -e

INPUT_TARGET="${1:?エラー: 解析対象のリポジトリ名またはパスを指定してください (例: KaMeToKo または 04-resources/git-repository/KaMeToKo/clone/dev_local)}"
BRANCH_NAME="${2:-main}"

PKM_ROOT=$(pwd)

# 前置チェック
if ! command -v graphify &> /dev/null; then
  echo "❌ エラー: graphify コマンドが見つかりません。'uv tool install graphifyy' 等でインストールしてください。"
  exit 1
fi

# パス判定およびターゲット・出力ディレクトリの解決
if [ -d "${INPUT_TARGET}" ]; then
  TARGET_DIR=$(cd "${INPUT_TARGET}" && pwd)
  BRANCH_NAME=$(basename "${TARGET_DIR}")
  REPO_NAME=$(basename "$(dirname "$(dirname "${TARGET_DIR}")")")
  if [ "${REPO_NAME}" = "." ] || [ "${REPO_NAME}" = "git-repository" ]; then
    REPO_NAME=$(basename "${TARGET_DIR}")
  fi
else
  REPO_NAME="${INPUT_TARGET}"
  TARGET_DIR="${PKM_ROOT}/04-resources/git-repository/${REPO_NAME}/clone/${BRANCH_NAME}"
fi

if [ ! -d "${TARGET_DIR}" ]; then
  echo "❌ エラー: 解析対象のディレクトリが存在しません: ${TARGET_DIR}"
  echo "先に ./scripts/fetch-git-log.sh を実行して clone を完了させてください。"
  exit 1
fi

OUTPUT_GRAPH_DIR="${PKM_ROOT}/04-resources/git-repository/${REPO_NAME}/graph/${BRANCH_NAME}"
mkdir -p "${OUTPUT_GRAPH_DIR}"

# 1. AST 抽出
echo "🔍 [${REPO_NAME}] Graphify によるソースコード構造解析を開始します..."
echo "  - 対象コード: ${TARGET_DIR}"
echo "  - 出力先:     ${OUTPUT_GRAPH_DIR}"

pushd "${TARGET_DIR}" > /dev/null
graphify extract . --code-only --output "${OUTPUT_GRAPH_DIR}"
popd > /dev/null

# 2. クラスタリング生成
echo "📊 [${REPO_NAME}] グラフクラスタリングおよびレポートの生成中..."
graphify cluster-only "${OUTPUT_GRAPH_DIR}" || true

# 3. 成果物の直下整理（命名明示化）
if [ -d "${OUTPUT_GRAPH_DIR}/graphify-out" ]; then
  cp "${OUTPUT_GRAPH_DIR}/graphify-out/graph.json" "${OUTPUT_GRAPH_DIR}/code-graph.json" 2>/dev/null || true
  cp "${OUTPUT_GRAPH_DIR}/graphify-out/GRAPH_REPORT.md" "${OUTPUT_GRAPH_DIR}/code-graph-report.md" 2>/dev/null || true
  cp "${OUTPUT_GRAPH_DIR}/graphify-out/graph.html" "${OUTPUT_GRAPH_DIR}/graph.html" 2>/dev/null || true
fi

echo "✅ コード解析・レポート整理完了:"
echo "  - code-graph.json        : AST依存データ"
echo "  - code-graph-report.md   : コード概要レポート"
echo "  - graph.html             : 可視化マップ"