---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/config.py"]
tags: [config, server, python]
status: active
phase: 3
parent: []
children: []
related: ["scripts/server/settings.json", "scripts/server/rag_service.py", "scripts/server/knowledge_service.py", "scripts/server/llm_client.py"]
task: ["scripts/server/config.py # config.pyの構造とパス定義・設定読み込み処理の解析"]
summary: "scripts/server/config.py はプロジェクトのパス設定、環境設定ファイル(settings.json)の読み込み、APIキー取得などの基本設定を提供する。"
---

# config.py 解析ノート

## 1. 概要
`scripts/server/config.py` は、パーソナルナレッジベースのサーバーサイドスクリプト群における共通設定・パス解決・APIキー管理等を一元的に提供するモジュールです。

## 2. パス定義と定数
- **`PROJECT_ROOT`**: カレントスクリプト位置を基準に2階層上のルートディレクトリ絶対パスを算出します。
- **`CONFIG_PATH`**: `settings.json` の絶対パス。
- **`PRIVATE_DIR`**, **`RULES_DIR`**, **`RESOURCES_DIR`**, **`KNOWLEDGE_DIR`**: 各主要ディレクトリのパス。
- **`DB_PATH`**: `01-private/knowledge_index.db` のパス。
- **`OLLAMA_ENDPOINT`**, **`EMBED_MODEL`**: ローカルLLM/埋め込み用のデフォルト設定値。

## 3. 主要関数
### `load_config() -> dict`
- `settings.json` が存在する場合はJSON形式で読み込み、存在しない場合はデフォルト設定（`DEFAULT_CONFIG`）をファイルに書き出して返却します。

### `get_gemini_api_key() -> str`
- `01-private/` 配下の指定ファイル群（`gemini_api_key.txt`, `gemini-api-key`, `api_key.txt`）からAPIキーを探索して読み込みます。
- ファイルが見つからない場合は環境変数 `GEMINI_API_KEY` をフォールバックとして取得します。

## 4. 依存関係
- 標準ライブラリ: `os`, `json`
- 関連ファイル: `scripts/server/settings.json`, `scripts/server/rag_service.py`, `scripts/server/knowledge_service.py`, `scripts/server/llm_client.py`
