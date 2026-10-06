---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/config.py"]
tags: [server, config, python]
status: draft
phase: 1
parent: []
children: []
related: ["scripts/server/knowledge_service.py", "scripts/server/llm_client.py"]
task: []
summary: "scripts/server/config.pyの絶対パス定義、設定ファイルの読み込み、APIキー取得等の設定管理機能。"
---

# config.py

## 概要
`scripts/server/config.py` は、パーソナルナレッジベースのサーバーサイド機能における基本設定およびパス定義、環境変数の管理を行うモジュールです。プロジェクトルートの自動検出や、`settings.json` の読み込み・初期化、Gemini APIキーの探索処理を提供します。

## 主要な定義・関数

### 1. パス定義
- `SCRIPT_DIR`: 当該ファイルが存在するディレクトリの絶対パス。
- `PROJECT_ROOT`: `scripts/server/` から2階層上のプロジェクトルート絶対パス。
- `CONFIG_PATH`: 設定ファイル (`settings.json`) の絶対パス。
- `PRIVATE_DIR`: プライベートデータ格納ディレクトリ (`01-private`) の絶対パス。
- `RULES_DIR`: ルール規約ディレクトリ (`00-rules`) の絶対パス。
- `RESOURCES_DIR`: 一次素材ディレクトリ (`04-resources`) の絶対パス。
- `KNOWLEDGE_DIR`: ナレッジディレクトリ (`02-knowledge`) の絶対パス。
- `DB_PATH`: データベースファイル (`knowledge_index.db`) の絶対パス。
- `OLLAMA_ENDPOINT`: Ollamaのデフォルトエンドポイント (`http://localhost:11434`)。
- `EMBED_MODEL`: 埋め込みモデル名 (`nomic-embed-text`)。

### 2. `load_config() -> dict`
- **目的**: `settings.json` から設定データを読み込む。
- **動作**:
  - ファイルが存在する場合は JSON として読み込んで返す。
  - 存在しない場合や例外発生時は、デフォルト設定（`DEFAULT_CONFIG`）を `settings.json` に書き込んで返す。

### 3. `get_gemini_api_key() -> str`
- **目的**: Gemini API キーをプライベートディレクトリまたは環境変数から取得する。
- **動作**:
  - 以下の候補ファイルを順に探索し、最初に見つかった非空の文字列を返す：
    - `01-private/gemini_api_key.txt`
    - `01-private/gemini-api-key`
    - `01-private/api_key.txt`
  - ファイルが存在しない場合は、環境変数 `GEMINI_API_KEY` の値を確認して返す。
