---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/config.py"]
tags: [server, config, python]
status: active
phase: 3
parent: []
children: []
related: ["scripts/server/settings.json", "scripts/server/knowledge_service.py", "scripts/server/llm_client.py", "scripts/server/rag_service.py", "scripts/server/start-webui.py"]
task: ["scripts/server/config.py # 設定管理モジュールの静的解析ノート"]
summary: "プロジェクトルートやプライベートディレクトリのパス定義、設定ファイル(settings.json)のロード、Gemini APIキーの取得などサーバー全体の設定管理を行うモジュール。"
---

# config.py 解析ノート

## 1. 概要
`scripts/server/config.py` は、パーソナルナレッジベースサーバー全体で使用される共通パス、デフォルト設定、および設定ファイルやAPIキーの読み込み処理を提供するモジュールです。

## 2. 定数・パス定義
- `SCRIPT_DIR`: 当該ファイルが存在するディレクトリ (`scripts/server/`) の絶対パス。
- `PROJECT_ROOT`: リポジトリルート (`../../`) の絶対パス。
- `CONFIG_PATH`: `settings.json` の絶対パス。
- `PRIVATE_DIR`: プライベートデータ格納先 (`01-private`) の絶対パス。
- `RULES_DIR`, `RESOURCES_DIR`, `KNOWLEDGE_DIR`: 各種ディレクトリの絶対パス。
- `DB_PATH`: `knowledge_index.db` の絶対パス (`01-private/knowledge_index.db`)。
- `OLLAMA_ENDPOINT`, `EMBED_MODEL`: Ollama連携用定数。

## 3. 主要関数

### `load_config() -> dict`
- **目的**: `settings.json` からサーバー設定を読み込む。ファイルが存在しない場合は `DEFAULT_CONFIG` を書き込んでから返す。
- **戻り値**: 設定情報を保持する辞書型オブジェクト。

### `get_gemini_api_key() -> str`
- **目的**: Gemini APIキーを取得する。
- **探索順序**:
  1. `01-private/gemini_api_key.txt`
  2. `01-private/gemini-api-key`
  3. `01-private/api_key.txt`
  4. 環境変数 `GEMINI_API_KEY`
- **戻り値**: 取得したAPIキー文字列。

## 4. 依存関係
- `os`, `json`: 標準ライブラリのみ使用。外部パッケージ依存なし。
