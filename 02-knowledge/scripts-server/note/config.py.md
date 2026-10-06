---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/config.py"]
tags: [server, config, python, settings]
status: active
phase: 2
parent: []
children: []
related: ["scripts/server/settings.json"]
task: ["scripts/server/config.py # scripts/server/config.pyの静的解析・設定管理仕様ノート"]
summary: "scripts/server/config.py は、プロジェクトルートのパス定義、settings.jsonからの設定読み込み、およびGemini APIキーの取得を担当する設定管理モジュールです。"
---

# config.py 解析ノート

## 1. 概要
`scripts/server/config.py` は、パーソナルナレッジベース内のサーバーサイドスクリプト群（`scripts/server/`）に対して、共通のパス定数、設定ファイル（`settings.json`）の読み込み、および認証キー（Gemini APIキー等）の動的取得を提供するコア設定モジュールです。

## 2. 主要な定数とパス定義
- `SCRIPT_DIR`: 当該スクリプトが存在するディレクトリの絶対パス (`scripts/server/`)。
- `PROJECT_ROOT`: プロジェクトルートの絶対パス (`../../` を介して算出)。
- `CONFIG_PATH`: `settings.json` の絶対パス。
- `PRIVATE_DIR`: `01-private` ディレクトリの絶対パス。
- `RULES_DIR`: `00-rules` ディレクトリの絶対パス。
- `RESOURCES_DIR`: `04-resources` ディレクトリの絶対パス。
- `KNOWLEDGE_DIR`: `02-knowledge` ディレクトリの絶対パス。
- `DB_PATH`: SQLiteデータベースファイルのパス (`01-private/knowledge_index.db`)。
- `OLLAMA_ENDPOINT`: Ollama接続先エンドポイント (`http://localhost:11434`)。
- `EMBED_MODEL`: 埋め込み用モデル名 (`nomic-embed-text`)。

## 3. 主要関数・処理フロー
### `load_config() -> dict`
- **目的**: 設定ファイル `settings.json` を読み込む。存在しない場合は `DEFAULT_CONFIG` をファイルに書き込んで初期作成し、それを返却する。また、読み込み時に例外が発生した場合もデフォルト設定をフォールバックとして扱う堅牢な設計となっている。

### `get_gemini_api_key() -> str`
- **目的**: Gemini APIの認証キーを取得する。
- **探索順序**:
  1. `01-private/gemini_api_key.txt`
  2. `01-private/gemini-api-key`
  3. `01-private/api_key.txt`
  4. 環境変数 `GEMINI_API_KEY`
- 上記の優先順位に従って最初に見つかった有効なキー文字列を返す。

## 4. 依存関係
- 外部モジュール: `os`, `json`
- 関連ファイル: `scripts/server/settings.json`
