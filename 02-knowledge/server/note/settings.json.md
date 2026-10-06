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
task: ["scripts/server/settings.json # scripts/server/settings.json の静的解析完了"]
summary: "scripts/server/settings.json は、バックエンドサーバーおよびWebUIで使用されるLLMプロバイダーやデフォルトモデルの設定値を保持するJSONファイルです。"
---

# settings.json 解析ノート

## 1. 概要
`scripts/server/settings.json` は、パーソナルナレッジベースサーバーの挙動を設定する JSON 設定ファイルです。`scripts/server/config.py` を通じて読み込まれます。

## 2. 設定構造と内容
- `default_provider`: 起動時等のデフォルトLLMプロバイダー（例: `"Ollama (Local LLM)"`）。
- `gemini`: Gemini APIに関する設定
  - `default_model`: デフォルトモデル（例: `"gemini-3.5-flash-lite"`）
  - `available_models`: 利用可能なモデルのリスト
- `ollama`: Ollamaに関する設定
  - `default_model`: デフォルトのローカルモデル（例: `"gemma4-agent"`）
  - `endpoint`: Ollamaの接続先エンドポイント（例: `"http://localhost:11434"`）
