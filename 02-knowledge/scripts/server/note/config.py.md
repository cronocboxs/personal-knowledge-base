---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/config.py"]
tags: [server, config, python, settings]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/settings.json"]
task:
  - "scripts/server/config.py # 設定管理モジュール"
summary: "プロジェクト共通のパス定義、設定ファイルの読み込み、およびGemini APIキー取得等の共通設定機能を提供するモジュール"
---

# scripts/server/config.py 解析ノート

## 1. 概要・責務
`scripts/server/config.py` は、パーソナルナレッジベースのサーバーサイド処理における共通の設定定数、ディレクトリパスの定義、および `settings.json` のロード機能、Gemini APIキーの探索機能を提供する基盤モジュールです。

## 2. 主要な定数とパス定義
- **`SCRIPT_DIR`**: スクリプトの格納ディレクトリ (`scripts/server`)
- **`PROJECT_ROOT`**: プロジェクトのルートディレクトリ (`../../`)
- **`CONFIG_PATH`**: `settings.json` の絶対パス
- **`PRIVATE_DIR`**: 非公開情報用ディレクトリ (`01-private`)
- **`RULES_DIR`**: 規約ディレクトリ (`00-rules`)
- **`RESOURCES_DIR`**: 一次資料ディレクトリ (`04-resources`)
- **`KNOWLEDGE_DIR`**: 知識ベースディレクトリ (`02-knowledge`)
- **`DB_PATH`**: SQLite インデックスデータベースのパス (`01-private/knowledge_index.db`)
- **`OLLAMA_ENDPOINT`**: Ollama接続用エンドポイント (`http://localhost:11434`)
- **`EMBED_MODEL`**: ベクトル埋め込みモデル (`nomic-embed-text`)

## 3. 主要関数・処理フロー

### `load_config() -> dict`
1. `settings.json` の存在を確認する。
2. 存在する場合はJSONとしてロードして辞書を返す。読込失敗時はデフォルト設定にフォールバックする。
3. 存在しない場合は `DEFAULT_CONFIG` を JSON として新規書き込みして返す。

### `get_gemini_api_key() -> str`
1. 以下の候補ファイルを順に探索し、存在かつ非空であればキー文字列を返す：
   - `01-private/gemini_api_key.txt`
   - `01-private/gemini-api-key`
   - `01-private/api_key.txt`
2. ファイルが見つからない場合は環境変数 `GEMINI_API_KEY` を参照する。

## 4. 依存関係
- `os`, `json`
- 連携先: `scripts/server/settings.json`
