---
created: 2026-10-06
updated: 2026-10-06
source: ["04-resources/scripts/server/config.py"]
tags: [server, config, python, settings]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/settings.json", "scripts/server/llm_client.py"]
task: ["scripts/server/config.py"]
summary: "scripts/server/config.py は、パス定義、設定ファイルの読み込み、Gemini APIキーの取得などサーバー側の設定管理を担当します。"
---

# `scripts/server/config.py` 解析ノート

## 1. 概要
`scripts/server/config.py` は、パーソナルナレッジベースのサーバーサイド機能（WebUIやバックエンドサービス）における基本設定、パス定義、設定ファイル読込、および外部APIキーの管理を行う設定モジュールです。

## 2. 主要な変数とパス定義
- **`SCRIPT_DIR`**: スクリプトが存在するディレクトリ (`scripts/server/`) の絶対パス。
- **`PROJECT_ROOT`**: プロジェクトルートディレクトリの絶対パス（`scripts/server/` から2階層上）。
- **`CONFIG_PATH`**: `settings.json` の絶対パス。
- **`PRIVATE_DIR`**: `01-private` ディレクトリの絶対パス。
- **`RULES_DIR`**: `00-rules` ディレクトリの絶対パス。
- **`RESOURCES_DIR`**: `04-resources` ディレクトリの絶対パス。
- **`KNOWLEDGE_DIR`**: `02-knowledge` ディレクトリの絶対パス。
- **`DB_PATH`**: SQLiteのナレッジインデックスDB (`01-private/knowledge_index.db`) のパス。
- **`OLLAMA_ENDPOINT`**: Ollamaのデフォルトエンドポイント (`http://localhost:11434`)。
- **`EMBED_MODEL`**: 埋め込みモデル名 (`nomic-embed-text`)。

## 3. 主要関数

### `load_config() -> dict`
- **目的**: サーバー設定ファイル (`settings.json`) を読み込む。存在しない場合はデフォルト設定 (`DEFAULT_CONFIG`) を書き込んでそれを返す。
- **デフォルト設定内容**:
  - `default_provider`: "Ollama (Local LLM)"
  - `gemini`: デフォルトモデル等の設定
  - `ollama`: デフォルトモデル (`gemma4:e4b-it-q4_K_M`) とエンドポイント

### `get_gemini_api_key() -> str`
- **目的**: Gemini API キーを取得する。
- **探索順序**:
  1. `01-private/gemini_api_key.txt`
  2. `01-private/gemini-api-key`
  3. `01-private/api_key.txt`
  4. 環境変数 `GEMINI_API_KEY`
- 見つかった最初の有効なキー文字列をトリムして返す。

## 4. 依存関係・連携
- `settings.json`: 設定の永続化先。
- `llm_client.py` や各種サービス (`rag_service.py`, `knowledge_service.py`) からインポートされ、設定やパスの基準として利用される。
