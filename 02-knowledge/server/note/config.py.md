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
`scripts/server/config.py` は、パーソナルナレッジベースサーバーサイド群の共通設定およびパス定義を行うPythonモジュールです。プロジェクトルートの自動検出、各種ディレクトリ（`01-private`, `00-rules`, `04-resources`, `02-knowledge`）のパス解決、設定ファイル（`settings.json`）の読み込み・初期化、および外部APIキーの安全な取得を行います。

## 2. 主要な変数と定数

- **`SCRIPT_DIR`**: 現在のスクリプト（`scripts/server/`）の絶対パス。
- **`PROJECT_ROOT`**: プロジェクトルート（`SCRIPT_DIR` から2階層上）の絶対パス。
- **`CONFIG_PATH`**: 設定ファイルパス（`settings.json`）。
- **`PRIVATE_DIR`**: プライベートデータ格納ディレクトリ（`01-private`）。
- **`RULES_DIR`**: ルールディレクトリ（`00-rules`）。
- **`RESOURCES_DIR`**: リソースディレクトリ（`04-resources`）。
- **`KNOWLEDGE_DIR`**: ナレッジディレクトリ（`02-knowledge`）。
- **`DB_PATH`**: SQLite インデックスデータベースのパス（`01-private/knowledge_index.db`）。
- **`OLLAMA_ENDPOINT`**: ローカルOllamaエンドポイント（デフォルト: `http://localhost:11434`）。
- **`EMBED_MODEL`**: 埋め込みモデル名（デフォルト: `nomic-embed-text`）。

## 3. 主要な関数

### `load_config() -> dict`
- **目的**: `settings.json` から設定を読み込む。ファイルが存在しない場合や破損している場合は、`DEFAULT_CONFIG` をファイルに書き込んでデフォルト値を返します。

### `get_gemini_api_key() -> str`
- **目的**: Gemini API キーを取得する。
- **検索順序**:
  1. `01-private/gemini_api_key.txt`
  2. `01-private/gemini-api-key`
  3. `01-private/api_key.txt`
  4. 環境変数 `GEMINI_API_KEY`

## 4. 依存関係
- 標準ライブラリ: `os`, `json`
- 関連ファイル: `scripts/server/settings.json`, `scripts/server/start-webui.py`, `scripts/server/rag_service.py`, `scripts/server/knowledge_service.py`, `scripts/server/llm_client.py`
