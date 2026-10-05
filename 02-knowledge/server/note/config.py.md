---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/config.py"]
tags: [server, config, python]
status: active
phase: 3
parent: []
children: []
related: ["scripts/server/settings.json"]
task: ["scripts/server/config.py # サーバ設定・パス管理スクリプトの静的解析"]
summary: "プロジェクト共通のパス定義、設定ファイルの読み込み、およびGemini APIキー取得のヘルパー関数を提供する設定モジュール。"
---

# `scripts/server/config.py` 解析ノート

## 1. 概要
`scripts/server/config.py` は、パーソナルナレッジベースサーバ群（`scripts/server/`）において、プロジェクトルートの絶対パス算出、各種データ・ルール・リソースディレクトリのパス定義、`settings.json` の自動生成・読み込み、および環境変数やプライベートファイルからの Gemini API キー取得を行う共通設定モジュールです。

## 2. 主要な定数・パス定義
- `SCRIPT_DIR`: スクリプト自身の配置ディレクトリ絶対パス (`scripts/server/`)
- `PROJECT_ROOT`: リポジトリルートの絶対パス (`../../` 経由)
- `CONFIG_PATH`: `settings.json` の絶対パス
- `PRIVATE_DIR`: `01-private/` の絶対パス
- `RULES_DIR`: `00-rules/` の絶対パス
- `RESOURCES_DIR`: `04-resources/` の絶対パス
- `KNOWLEDGE_DIR`: `02-knowledge/` の絶対パス
- `DB_PATH`: `01-private/knowledge_index.db` の絶対パス
- `OLLAMA_ENDPOINT`: Ollama ローカルエンドポイント (`http://localhost:11434`)
- `EMBED_MODEL`: 埋め込みモデル名 (`nomic-embed-text`)

## 3. 関数・主要処理フロー

### `load_config() -> dict`
1. `settings.json`（`CONFIG_PATH`）の存在を確認する。
2. 存在する場合は JSON として読み込んで返す。失敗した場合はデフォルト設定にフォールバックする。
3. 存在しない場合は `DEFAULT_CONFIG` をファイルに書き込み、初期設定を生成した上で返す。

### `get_gemini_api_key() -> str`
1. 以下のプライベートディレクトリ内の候補ファイルから API キーの読み込みを試みる:
   - `01-private/gemini_api_key.txt`
   - `01-private/gemini-api-key`
   - `01-private/api_key.txt`
2. ファイルが見つからない、または空の場合は環境変数 `GEMINI_API_KEY` を参照する。
3. 有効な文字列が得られればそれを返す。

## 4. 依存関係
- 外部モジュール: `os`, `json`
- 関連ファイル: `scripts/server/settings.json`
