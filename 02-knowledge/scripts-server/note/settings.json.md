---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/settings.json"]
tags: [server, config, json, settings]
status: active
phase: 2
parent: []
children: []
related: ["scripts/server/config.py"]
task: ["scripts/server/settings.json # サーバー設定JSONファイルの解析"]
summary: "LLMプロバイダーやデフォルトモデル（Gemini / Ollama）の設定を保持するJSON設定ファイル。"
---

# settings.json - サーバー設定ファイル

## 概要
`scripts/server/settings.json` は、ナレッジベースサーバーにおけるデフォルトのLLMプロバイダー、および各プロバイダー（Gemini, Ollama）の利用モデルやエンドポイントを定義するJSONファイルです。

## 構造
- `default_provider`: デフォルトで使用するLLMプロバイダー（例: `"Ollama (Local LLM)"`）
- `gemini`: Google Gemini APIの設定
  - `default_model`: デフォルトモデル (`"gemini-3.5-flash-lite"`)
  - `available_models`: 利用可能なモデルリスト
- `ollama`: ローカルOllamaの設定
  - `default_model`: デフォルトモデル (`"gemma4-agent"` など)
  - `endpoint`: Ollama APIエンドポイント (`"http://localhost:11434"`)
