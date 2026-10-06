---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/config.py"]
tags: [server, config, python]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/settings.json", "scripts/server/knowledge_service.py", "scripts/server/rag_service.py", "scripts/server/llm_client.py", "scripts/server/start-webui.py"]
task: ["scripts/server/config.py # config.pyの静的解析"]
summary: "プロジェクト共通のパス定義、環境変数、Ollama/Geminiの設定読み込み、APIキー取得を行うサーバー設定モジュール。"
---

# config.py 解析ノート

## 概要
`scripts/server/config.py` は、パーソナルナレッジベースのサーバーサイドスクリプト群（`scripts/server/`）で使用される共通のパス定義、設定読み込み、および外部APIキー取得機能を提供するモジュールです。

## 主要な処理とデータ構造

### 1. パス定義
- `SCRIPT_DIR`: 現在のスクリプトディレクトリ（`scripts/server/`）の絶対パス。
- `PROJECT_ROOT`: プロジェクトルートディレクトリの絶対パス（`SCRIPT_DIR` から2階層上）。
- 各種サブディレクトリの絶対パス:
  - `CONFIG_PATH`: `settings.json` のパス。
  - `PRIVATE_DIR`: `01-private` ディレクトリのパス。
  - `RULES_DIR`: `00-rules` ディレクトリのパス。
  - `RESOURCES_DIR`: `04-resources` ディレクトリのパス。
  - `KNOWLEDGE_DIR`: `02-knowledge` ディレクトリのパス。
  - `DB_PATH`: SQLiteデータベース（`01-private/knowledge_index.db`）のパス。

### 2. LLM / 埋め込みモデル定数
- `OLLAMA_ENDPOINT`: Ollama の接続先エンドポイント（デフォルト: `http://localhost:11434`）。
- `EMBED_MODEL`: 埋め込みモデル名（`nomic-embed-text`）。

### 3. 設定ファイル管理 (`load_config`)
- `settings.json` の存在を確認し、存在する場合は JSON として読み込んで返します。
- 存在しない場合、または読み込みに失敗した場合は、デフォルト設定 (`DEFAULT_CONFIG`) を `settings.json` に書き出して返します。
- デフォルト設定には、Gemini や Ollama のプロバイダー情報、デフォルトモデル情報が含まれます。

### 4. APIキー取得 (`get_gemini_api_key`)
- `01-private/` 配下の複数の候補ファイル（`gemini_api_key.txt`, `gemini-api-key`, `api_key.txt`）を順に走査し、最初に見つかった非空のキー文字列を返します。
- ファイルが存在しない場合は、環境変数 `GEMINI_API_KEY` の値をフォールバックとして取得します。

## 依存関係
- 標準ライブラリ: `os`, `json`
- 被依存モジュール: `knowledge_service.py`, `rag_service.py`, `llm_client.py`, `start-webui.py`
