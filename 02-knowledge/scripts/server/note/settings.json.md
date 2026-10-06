---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/settings.json"]
tags: [server, settings, json, config]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py"]
task:
  - "scripts/server/settings.json # サーバー設定ファイル"
summary: "WebUIサーバーおよびLLMプロバイダー（Gemini, Ollama）のデフォルトモデルやエンドポイントを定義するJSON設定ファイル"
---

# scripts/server/settings.json 解析ノート

## 1. 概要・責務
`scripts/server/settings.json` は、パーソナルナレッジベースのWebUIおよびLLM連携において使用される設定パラメータ（デフォルトプロバイダー、モデル名、エンドポイントURL等）を保持するJSON設定ファイルです。

## 2. 設定項目の構造
- **`default_provider`**: 使用するデフォルトのLLMプロバイダー（例: `"Ollama (Local LLM)"`）
- **`gemini`**: Google Gemini API用の設定
  - `default_model`: デフォルトモデル名（`"gemini-3.5-flash-lite"`）
  - `available_models`: 利用可能なモデルリスト
- **`ollama`**: ローカルOllama用の設定
  - `default_model`: デフォルトモデル名（`"gemma4-agent"`）
  - `endpoint`: Ollama API接続エンドポイント (`"http://localhost:11434"`)

## 3. 連携関係
- `scripts/server/config.py` の `load_config()` 関数によりロードされ、各サービスモジュール（`llm_client.py` 等）の初期設定として利用されます。
