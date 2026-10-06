---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/config.py"]
tags: ["server", "config", "python"]
status: active
phase: 2
parent: []
children: []
related: ["scripts/server/settings.json"]
task: []
summary: "scripts/server/config.pyの静的解析ノート: プロジェクト全体の絶対パス解決やOllama/Geminiの共通設定、設定ファイル読み込み・APIキー取得を行う。"
---

# scripts/server/config.py 解析ノート

## 1. 概要・目的
`scripts/server/config.py` は、パーソナルナレッジベースのバックエンドサーバー群（`scripts/server/` 配下の各スクリプト）で使用される共通設定ファイルおよびヘルパー関数群を提供します。
プロジェクトルートや主要ディレクトリの絶対パス解決、Ollama/Geminiのデフォルト設定、`settings.json` の自動読み込み・初期化、外部APIキーの自動探索などを一元管理します。

## 2. 主要な定数・パス定義
- **`SCRIPT_DIR`**: `scripts/server/` ディレクトリの絶対パス。
- **`PROJECT_ROOT`**: リポジトリルート（`scripts/server/` から2階層上）の絶対パス。
- **各種ディレクトリ/ファイルパス**:
  - `CONFIG_PATH`: `settings.json` のパス。
  - `PRIVATE_DIR`: `01-private` のパス。
  - `RULES_DIR`: `00-rules` のパス。
  - `RESOURCES_DIR`: `04-resources` のパス。
  - `KNOWLEDGE_DIR`: `02-knowledge` のパス。
  - `DB_PATH`: SQLite データベースファイルのパス（`01-private/knowledge_index.db`）。
- **Ollama 定数**:
  - `OLLAMA_ENDPOINT`: デフォルトエンドポイント (`http://localhost:11434`)。
  - `EMBED_MODEL`: 埋め込みモデル (`nomic-embed-text`)。

## 3. 主要関数・処理フロー
### 3.1 `load_config() -> dict`
- `settings.json` が存在する場合は `json.load()` で設定を読み込みます。
- 存在しない場合や読み込みエラー時は、デフォルト設定（`DEFAULT_CONFIG`）をファイルに書き込んで初期化し、それを返します。

### 3.2 `get_gemini_api_key() -> str`
- 以下の候補ファイルパスを順に探索し、最初に値が取得できたキーを返します。
  1. `01-private/gemini_api_key.txt`
  2. `01-private/gemini-api-key`
  3. `01-private/api_key.txt`
- ファイルが存在しない場合は環境変数 `GEMINI_API_KEY` をフォールバックとして取得します。

## 4. 依存関係
- 標準ライブラリ: `os`, `json`
- 連携モジュール: `scripts/server/settings.json`
