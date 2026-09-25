#!/usr/bin/env bash
# 使い方: ./scripts/run-markdown-index.sh <path>
set -e

PKM_ROOT=$(pwd)
chmod +x scripts/py3/generate-knowledge-index.py
python3 scripts/py3/generate-knowledge-index.py "$1"