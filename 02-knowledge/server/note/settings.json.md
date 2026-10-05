---
created: 2026-10-06
updated: 2026-10-06
source: ["04-resources/scripts/server/settings.json"]
tags: [server, settings, json, configuration]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py"]
task: ["scripts/server/settings.json"]
summary: "scripts/server/settings.json は、LLMプロバイダーやモデルのデフォルト設定を保持するJSON設定ファイルです。"
---

# `scripts/server/settings.json` 解析ノート

## 1. 概要
`scripts/server/settings.json` は、サーバーサイドで利用されるLLMのデフォルトプロバイダー、モデル選択、エンドポイント等の設定を保持するJSONファイルです。`config.py` を通じて読み込まれます。

## 2. 設定パラメータ構造
- **`default_provider`**: 使用するデフォルトのLLMプロバイダー（例: `"Ollama (Local LLM)"`）。
- **`gemini`**: Google Gemini API関連の設定。
  - `default_model`: デフォルトで使用するGeminiモデル名（例: `"gemini-3.5-flash-lite"`）。
  - `available_models`: 利用可能なGeminiモデルのリスト。
- **`ollama`**: ローカルOllama関連の設定。
  - `default_model`: 使用するモデル名（例: `"gemma4-agent"`）。
  - `endpoint`: Ollama APIサーバーのエンドポイントURL（例: `"http://localhost:11434"`）。

## 3. 連携関係
- `config.py`: ファイルが存在しない場合のデフォルト生成および読み込み処理の対象。
- 各種LLMクライアント (`llm_client.py`) やサービスから参照され、動作時のプロバイダーやモデル選択に反映されます。
