---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/config.py"]
tags: [server, config, python, environment]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/settings.json", "scripts/server/start-webui.py", "scripts/server/rag_service.py", "scripts/server/knowledge_service.py", "scripts/server/llm_client.py"]
task: ["scripts/server/config.py # 設定・パス定義スクリプトの静的解析"]
summary: "scripts/server/config.py はプロジェクトルートや各種データベース・設定ファイルのパスを定義し、デフォルト設定のロードやAPIキーの取得ヘルパーを提供する設定モジュールです。"
---

# `scripts/server/config.py` 解析ノート

## 1. 概要
`scripts/server/config.py` は、パーソナルナレッジベースサーバー側の各種設定や絶対パスの定義、および外部設定ファイル (`settings.json`) の読み込み・デフォルト生成を行う中心的な設定モジュールです。

## 2. 主要なパス定義
- **`SCRIPT_DIR`**: スクリプトの存在ディレクトリ (`scripts/server/`)
- **`PROJECT_ROOT`**: プロジェクトのルートディレクトリ (`scripts/server/` から2階層上)
- **`CONFIG_PATH`**: 設定ファイルパス (`settings.json`)
- **`PRIVATE_DIR`**: 非公開情報ディレクトリ (`01-private`)
- **`RULES_DIR`**: 規約ディレクトリ (`00-rules`)
- **`RESOURCES_DIR`**: 一次資源ディレクトリ (`04-resources`)
- **`KNOWLEDGE_DIR`**: ナレッジディレクトリ (`02-knowledge`)
- **`DB_PATH`**: SQLite インデックスDB (`01-private/knowledge_index.db`)
- **Ollama 設定**: `OLLAMA_ENDPOINT` ("http://localhost:11434"), `EMBED_MODEL` ("nomic-embed-text")

## 3. 主要関数
- **`load_config() -> dict`**:
  - `settings.json` が存在する場合は `json.load` で読み込んで返す。
  - 存在しない場合は `DEFAULT_CONFIG`（GeminiやOllamaのデフォルトモデル設定）を `settings.json` に書き出して返す。
- **`get_gemini_api_key() -> str`**:
  - `01-private/` 配下の候補ファイル群 (`gemini_api_key.txt`, `gemini-api-key`, `api_key.txt`) や環境変数 (`GEMINI_API_KEY`) からAPIキーを安全に取得・返却する。
