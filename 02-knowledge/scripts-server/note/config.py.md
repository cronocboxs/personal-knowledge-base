---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/config.py"]
tags: [server, config, python, path]
status: active
phase: 2
parent: []
children: []
related: ["scripts/server/settings.json"]
task: ["scripts/server/config.py # 設定管理とパス定義モジュールの解析"]
summary: "プロジェクトルートや各ディレクトリの絶対パス、設定ファイル（settings.json）の読み込み、およびGemini APIキーの取得機能を提供する設定モジュール。"
---

# config.py - 設定管理とパス定義モジュール

## 概要
`scripts/server/config.py` は、パーソナルナレッジベースサーバーにおけるパス定義、`settings.json` の読み込み・初期化、および外部APIキー（Geminiなど）の解決を行う基礎モジュールです。

## 主要な定数・パス定義
- `SCRIPT_DIR`: 当該ファイルが存在するディレクトリ (`scripts/server/`)
- `PROJECT_ROOT`: リポジトリルート (`../../`)
- `CONFIG_PATH`: 設定ファイルパス (`settings.json`)
- `PRIVATE_DIR`: プライベートデータ用ディレクトリ (`01-private`)
- `RULES_DIR`: ルール定義ディレクトリ (`00-rules`)
- `RESOURCES_DIR`: 一次資料ディレクトリ (`04-resources`)
- `KNOWLEDGE_DIR`: ナレッジ格納ディレクトリ (`02-knowledge`)
- `DB_PATH`: データベースパス (`01-private/knowledge_index.db`)
- `OLLAMA_ENDPOINT`: Ollama接続先 (`http://localhost:11434`)
- `EMBED_MODEL`: 埋め込み用モデル名 (`nomic-embed-text`)

## 関数仕様
### `load_config() -> dict`
- `settings.json` が存在する場合は JSON として読み込んで返します。
- 存在しない場合はデフォルト設定 (`DEFAULT_CONFIG`) を `settings.json` に書き込んでから返します。

### `get_gemini_api_key() -> str`
- `01-private/` 配下の複数の候補ファイル (`gemini_api_key.txt`, `gemini-api-key`, `api_key.txt`) からキーの読み込みを試みます。
- ファイルが存在しない場合や空の場合は環境変数 `GEMINI_API_KEY` をフォールバックとして取得します。
