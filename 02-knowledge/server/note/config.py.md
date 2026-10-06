---
created: 2026-10-06
updated: 2026-10-06
source: ["04-resources/scripts/server/config.py"]
tags: [server, config, python]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/settings.json"]
task: ["scripts/server/config.py # 設定管理モジュール"]
summary: "scripts/server/config.py は、パーソナルナレッジベースのサーバ用設定管理モジュールであり、プロジェクトルートの絶対パス解決、設定ファイル(settings.json)のロード機能、および機密ディレクトリからのGemini APIキー取得やOllamaエンドポイントの設定を提供する。"
---

# config.py 解析ノート

## 1. 概要
`scripts/server/config.py` は、パーソナルナレッジベースの Web UI やバックエンドサービスが共通で利用する設定管理モジュールです。
プロジェクトルートの絶対パスを動的に算出するとともに、ローカル設定ファイルや機密情報を安全に取得・管理する機能を提供します。

## 2. 主要変数・定数
- `SCRIPT_DIR`: このスクリプトが存在するディレクトリの絶対パス。
- `PROJECT_ROOT`: プロジェクトルートディレクトリの絶対パス（`scripts/server/` から2階層上）。
- `CONFIG_PATH`: 設定ファイル `settings.json` のパス。
- `PRIVATE_DIR`: 機密情報格納ディレクトリ (`01-private`) のパス。
- `RULES_DIR`: 規約ディレクトリ (`00-rules`) のパス。
- `RESOURCES_DIR`: 一時・一次資料ディレクトリ (`04-resources`) のパス。
- `KNOWLEDGE_DIR`: ナレッジディレクトリ (`02-knowledge`) のパス。
- `DB_PATH`: データベースファイル (`knowledge_index.db`) のパス。
- `OLLAMA_ENDPOINT`: Ollama のデフォルト接続先 (`http://localhost:11434`)。
- `EMBED_MODEL`: 埋め込みモデル名 (`nomic-embed-text`)。
- `DEFAULT_CONFIG`: デフォルトのプロバイダ設定（Gemini, Ollama のモデル情報等）。

## 3. 主要関数
### `load_config() -> dict`
- 設定ファイル `settings.json` が存在する場合は読み込んで辞書として返します。
- 存在しない場合は、デフォルト設定を `settings.json` に書き出した上でその辞書を返します。

### `get_gemini_api_key() -> str`
- 機密ディレクトリ (`01-private/`) 内の `gemini_api_key.txt`, `gemini-api-key`, `api_key.txt` から API キーの読み込みを試みます。
- ファイルが見つからない場合や空の場合は、環境変数 `GEMINI_API_KEY` の値フォールバックします。
