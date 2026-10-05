---
title: "config_py"
source: "scripts/server/config.py"
category: "scripts"
type: "note"
created_at: "2026-10-06"
---

# 詳細解析ノート: `scripts/server/config.py`

## 1. 目的・役割
- `scripts/server/config.py` の静的解析に基づく機能・役割の解説。

## 2. 内部構造・主要処理フロー
```python
# ソースコード内容抜粋・構造サマリ
```

## 3. ソースコード全文（リファレンス）
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
