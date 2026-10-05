---
created: 2026-10-06
updated: 2026-10-06
source: ["04-resources/scripts/server/config.py"]
tags: [server, config, python, backend]
status: active
phase: 3
parent: []
children: []
related: ["scripts/server/settings.json", "scripts/server/rag_service.py", "scripts/server/knowledge_service.py", "scripts/server/llm_client.py"]
task: ["scripts/server/config.py # 設定管理モジュールの静的解析"]
summary: "プロジェクトルートやプライベートディレクトリのパス定義、settings.jsonのロード機能、Gemini APIキーの取得機能を提供するサーバー設定管理モジュール。"
---

# config.py 解析ノート

## 1. 概要
`scripts/server/config.py` は、パーソナルナレッジベースのサーバーサイド機能（WebUI や各種サービス）で使用される共通設定ファイルおよびパス解決モジュールです。

## 2. 主要な定数とパス定義
- `SCRIPT_DIR`: スクリプト自身のディレクトリ (`scripts/server`)
- `PROJECT_ROOT`: プロジェクトルートディレクトリ (`../../`)
- `CONFIG_PATH`: 設定ファイル (`scripts/server/settings.json`)
- `PRIVATE_DIR`: 非公開データ保存用ディレクトリ (`01-private`)
- `RULES_DIR`: ルール定義ディレクトリ (`00-rules`)
- `RESOURCES_DIR`: リソースディレクトリ (`04-resources`)
- `KNOWLEDGE_DIR`: ナレッジディレクトリ (`02-knowledge`)
- `DB_PATH`: SQLite データベースパス (`01-private/knowledge_index.db`)
- `OLLAMA_ENDPOINT`: Ollama のローカルエンドポイント (`http://localhost:11434`)
- `EMBED_MODEL`: 埋め込みモデル名 (`nomic-embed-text`)

## 3. 主要関数

### `load_config() -> dict`
- `settings.json` の存在を確認し、存在すれば JSON としてロードして返す。
- 存在しない場合、デフォルトの設定構造（`DEFAULT_CONFIG`）をファイルに書き出して初期作成し、それを返す。

### `get_gemini_api_key() -> str`
- 以下の候補ファイルから Gemini API キーの読み込みを試みる:
  1. `01-private/gemini_api_key.txt`
  2. `01-private/gemini-api-key`
  3. `01-private/api_key.txt`
- ファイルが存在しない場合や空の場合は、環境変数 `GEMINI_API_KEY` をフォールバックとして取得する。

## 4. 依存関係
- `os`, `json` 標準ライブラリのみに依存。
- `settings.json` および `01-private/` などのファイルシステム構造に強く依存している。
