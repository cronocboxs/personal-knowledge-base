---
created: 2026-10-06
updated: 2026-10-06
source: ["04-resources/scripts/server/config.py"]
tags: [server, config, python]
status: active
phase: 3
parent: []
children: []
related: ["scripts/server/settings.json", "scripts/server/llm_client.py"]
task: ["scripts/server/config.py"]
summary: "scripts/server/config.pyの静的解析ノート（本文付き）"
---

# `scripts/server/config.py` 解析ノート

## 1. 概要・責務
`scripts/server/config.py` は、パーソナルナレッジベースのサーバーサイドスクリプト群（WebUI、RAG、ナレッジ検索など）共通で使用される設定管理モジュールです。プロジェクトルートのパス計算、ディレクトリ定数の定義、JSON設定ファイルの自動ロード・デフォルト生成、および Gemini API キーの安全な読み込み機能を提供します。

## 2. 主要な定数・パス定義
- **`SCRIPT_DIR`**: スクリプトが配置されているディレクトリ（`scripts/server/`）の絶対パス。
- **`PROJECT_ROOT`**: プロジェクトルートディレクトリの絶対パス（`SCRIPT_DIR` から2階層上）。
- **ディレクトリ・ファイル定数**:
  - `CONFIG_PATH`: `settings.json` の絶対パス。
  - `PRIVATE_DIR`: `01-private` ディレクトリの絶対パス。
  - `RULES_DIR`: `00-rules` ディレクトリの絶対パス。
  - `RESOURCES_DIR`: `04-resources` ディレクトリの絶対パス。
  - `KNOWLEDGE_DIR`: `02-knowledge` ディレクトリの絶対パス。
  - `DB_PATH`: `01-private/knowledge_index.db` の絶対パス。
- **LLM関連定数**:
  - `OLLAMA_ENDPOINT`: デフォルトの Ollama エンドポイント（`http://localhost:11434`）。
  - `EMBED_MODEL`: 埋め込みモデル名（`nomic-embed-text`）。

## 3. 主要関数・処理フロー
### `load_config() -> dict`
1. `settings.json` (`CONFIG_PATH`) が存在するか確認する。
2. 存在する場合は JSON としてロードし辞書型で返す。読み込み失敗時はデフォルト設定を使用する。
3. 存在しない場合は、`DEFAULT_CONFIG`（Gemini と Ollama のデフォルトプロバイダ・モデル設定）を JSON 形式でファイルに書き込み、それを返す。

### `get_gemini_api_key() -> str`
1. `01-private/` 配下の候補ファイル（`gemini_api_key.txt`, `gemini-api-key`, `api_key.txt`）を順番に走査する。
2. ファイルが存在し、中身が空でない場合はその文字列を API キーとして返す。
3. ファイルが見つからない場合は環境変数 `GEMINI_API_KEY` の値を取得して返す。
