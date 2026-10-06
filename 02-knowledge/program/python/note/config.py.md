---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/config.py"]
tags: [python, server, config]
status: active
phase: 3
parent: []
children: []
related: ["scripts/server/config.py"]
task: ["scripts/server/config.py # 設定・パス管理モジュール"]
summary: "scripts/server/config.py の静的解析。プロジェクトルートの絶対パス解決、設定ファイルの読み込み、および Gemini API キー取得のヘルパー機能を提供。"
---

# config.py 解析ノート

## 1. 概要
`scripts/server/config.py` は、パーソナルナレッジベースのサーバーサイド機能（WebUIや各種サービス）で共有される共通設定、パス定義、および認証情報の読み込みを担当するモジュールです。

## 2. 主な構成要素と処理フロー

### パス定義
- **`SCRIPT_DIR`**: 現在のスクリプト（`scripts/server/`）の絶対パス。
- **`PROJECT_ROOT`**: プロジェクトルートの絶対パス（`SCRIPT_DIR` から2階層上）。
- **ディレクトリパス**: `01-private/`, `00-rules/`, `04-resources/`, `02-knowledge/`, `01-private/knowledge_index.db` などの絶対パスを定数として定義。
- **外部サービス接続デフォルト**: Ollamaエンドポイント（`http://localhost:11434`）や埋め込みモデル（`nomic-embed-text`）を定義。

### `load_config()`
- `settings.json` の存在を確認し、存在する場合は JSON として読み込んで返却する。
- 存在しない場合やエラー時は、デフォルト設定（`DEFAULT_CONFIG`）を `settings.json` に書き込んで新規作成し返却する。

### `get_gemini_api_key()`
- `01-private/` 配下の複数の候補ファイル（`gemini_api_key.txt`, `gemini-api-key`, `api_key.txt`）を走査して API キーを取得する。
- ファイルが存在しないか空の場合は環境変数 `GEMINI_API_KEY` をフォールバックとして取得する。

## 3. 依存関係
- 標準ライブラリ: `os`, `json`
