---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/config.py"]
tags: [server, config, python, settings]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/knowledge_service.py", "scripts/server/llm_client.py", "scripts/server/rag_service.py", "scripts/server/start-webui.py"]
task: ["scripts/server/config.py # 設定管理スクリプト"]
summary: "scripts/server/config.py はプロジェクトの各種絶対パス、Ollama/Geminiのデフォルト設定、設定ファイル読み込み、APIキー取得などの基本定数・設定管理を提供する。"
---

# `config.py` 解析ノート

## 1. 概要
`scripts/server/config.py` は、パーソナルナレッジベースサーバー (`scripts/server/`) における共通のパス設定、デフォルト設定値、設定ファイル (`settings.json`) のロード、および Gemini API キーの自動検出・取得ロジックを提供する設定管理モジュールです。

## 2. 主要な定数とパス定義
- **`PROJECT_ROOT`**: `scripts/server/` から2階層上のリポジトリルート絶対パス。
- **ディレクトリ定義**:
  - `PRIVATE_DIR`: `01-private/` (非公開・機密データ、`knowledge_index.db`、APIキー用)
  - `RULES_DIR`: `00-rules/`
  - `RESOURCES_DIR`: `04-resources/`
  - `KNOWLEDGE_DIR`: `02-knowledge/`
- **モデル設定**:
  - `OLLAMA_ENDPOINT`: `"http://localhost:11434"`
  - `EMBED_MODEL`: `"nomic-embed-text"`

## 3. 主要関数

### `load_config() -> dict`
- **概要**: `settings.json` の存在を確認し、存在すれば JSON としてパースして返す。存在しない場合は `DEFAULT_CONFIG` をファイルに書き込んで保存し、それを返す。

### `get_gemini_api_key() -> str`
- **概要**: 以下の候補パスを順番に走査して Gemini API キーをファイルから読み込む。
  1. `01-private/gemini_api_key.txt`
  2. `01-private/gemini-api-key`
  3. `01-private/api_key.txt`
- 上記ファイルが存在しない、またはキーが空の場合は環境変数 `GEMINI_API_KEY` の値を取得して返す。

## 4. 依存関係
- `os`, `json` 標準ライブラリを使用。
- `scripts/server/` 内の他モジュール（`knowledge_service.py`, `llm_client.py`, `rag_service.py`, `start-webui.py`）からインポートされて参照される基盤モジュール。
