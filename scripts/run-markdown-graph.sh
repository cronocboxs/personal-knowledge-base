#!/usr/bin/env bash
# scripts/run-doc-graph.sh
# 使い方: ./scripts/run-doc-graph.sh <リポジトリ名またはパス> [ブランチ名]
set -e

PKM_ROOT=$(pwd)
chmod +x scripts/py3/extract-markdown-graph.py
python3 scripts/py3/extract-markdown-graph.py "$1" "$2"