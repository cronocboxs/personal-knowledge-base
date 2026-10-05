---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/config.py"]
tags: [server, config, python]
status: active
phase: 3
parent: []
children: []
related: ["scripts/server/settings.json", "scripts/server/rag_service.py", "scripts/server/knowledge_service.py", "scripts/server/llm_client.py"]
task: ["scripts/server/config.py # scripts/server/config.pyの静的解析・ナレッジ生成"]
summary: "scripts/server/config.py はプロジェクト全体のパス定義、設定ファイル(settings.json)のロード機構、およびGemini APIキー取得ヘルパーを提供する設定モジュールです。"
---

# config.py - サーバー設定管理モジュール

## 1. 概要
`scripts/server/config.py` は、パーソナルナレッジベースサーバーサイドスクリプト群において共通して利用されるパス定数、デフォルト設定値、および設定ファイルやAPIキーのロードロジックを提供するコアモジュールです。

## 2. 主要な定数・パス定義
- **`SCRIPT_DIR`**: スクリプトが配置されているディレクトリ（`scripts/server/`）の絶対パス。
- **`PROJECT_ROOT`**: プロジェクトルートディレクトリの絶対パス（`scripts/server/` から2階層上）。
- **`CONFIG_PATH`**: `settings.json` の絶対パス。
- **`PRIVATE_DIR`**: プライベートデータ格納ディレクトリ（`01-private/`）の絶対パス。
- **`RULES_DIR`**: ルールディレクトリ（`00-rules/`）の絶対パス。
- **`RESOURCES_DIR`**: リソースディレクトリ（`04-resources/`）の絶対パス。
- **`KNOWLEDGE_DIR`**: ナレッジベースディレクトリ（`02-knowledge/`）の絶対パス。
- **`DB_PATH`**: SQLiteインデックスデータベースのパス（`01-private/knowledge_index.db`）。
- **`OLLAMA_ENDPOINT`**: OllamaローカルLLMのエンドポイント（デフォルト: `http://localhost:11434`）。
- **`EMBED_MODEL`**: 埋め込みモデル名（デフォルト: `nomic-embed-text`）。

## 3. 主要な関数

### `load_config() -> dict`
- **目的**: `settings.json` から設定データをロードする。ファイルが存在しない場合は、`DEFAULT_CONFIG` を書き込んでからデフォルト設定を返す。エラー発生時もフォールバックとしてデフォルト設定を返す。

### `get_gemini_api_key() -> str`
- **目的**: Gemini APIキーを取得する。
- **検索順序**:
  1. `01-private/gemini_api_key.txt`
  2. `01-private/gemini-api-key`
  3. `01-private/api_key.txt`
  4. 環境変数 `GEMINI_API_KEY`

## 4. 依存関係
- 標準ライブラリ: `os`, `json`
- 被依存モジュール: `rag_service.py`, `knowledge_service.py`, `llm_client.py`, `start-webui.py` 等
