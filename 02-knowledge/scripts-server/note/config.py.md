---
title: "scripts/server/config.py Note"
date: 2026-10-06
tags: [server, config]
category: scripts-server
description: "サーバー設定管理モジュールの詳細解析"
---

# Note: scripts/server/config.py

## 1. 目的と役割
本ファイル `config.py` は `サーバー設定管理モジュール` として動作し、システム全体の中で重要な役割を果たします。

## 2. 主要な構成要素・処理フロー
- ファイル種別: `py`
- 責務: サーバー設定管理モジュール

## 3. コード内容 / 構成
```
import os
import json

# ---------------------------------------------------------
# パス定義: プロジェクトルートの絶対パスを取得 (scripts/server/ から2階層上)
# ---------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../"))

# 各種ファイル・ディレクトリの絶対パス
CONFIG_PATH = os.path.join(SCRIPT_DIR, "settings.json")
PRIVATE_DIR = os.path.join(PROJECT_ROOT, "01-private")
RULES_DIR = os.path.join(PROJECT_ROOT, "00-rules")
RESOURCES_DIR = os.path.join(PROJECT_ROOT, "04-resources")
KNOWLEDGE_DIR = os.path.join(PROJECT_ROOT, "02-knowledge")
DB_PATH = os.path.join(PRIVATE_DIR, "knowledge_index.db")

OLLAMA_ENDPOINT = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"

# ---------------------------------------------------------
# 設定ファイルの読み込み
# ---------------------------------------------------------
DEFAULT_CONFIG = {
    "default_provider": "Ollama (Local LLM)",
    "gemini": {
        "default_model": "gemini-3.5-flash-lite",
        "available_models": [
            "gemini-3.5-flash-lite"
        ]
    },
    "ollama": {
        "default_model": "gemma4:e4b-it-q4_K_M",
        "endpoint": "http://localhost:11434"
    }
}

def load_config() -> dict:
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2, ensure_ascii=False)
    return DEFAULT_CONFIG

# ---------------------------------------------------------
# ヘルパー関数: ルート基準での Gemini API キー読み込み
# ---------------------------------------------------------
def get_gemini_api_key() -> str:
    candidate_files = [
        os.path.join(PRIVATE_DIR, "gemini_api_key.txt"),
        os.path.join(PRIVATE_DIR, "gemini-api-key"),
        os.path.join(PRIVATE_DIR, "api_key.txt")
    ]
    for file_path in candidate_files:
        if os.path.exists(file_path):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    key = f.read().strip()
                    if key:
                        return key
            except Exception:
                pass
    return os.environ.get("GEMINI_API_KEY", "").strip()

```

## 4. 依存関係と連携
- `scripts/server/` 内の他のモジュールとの連携。
