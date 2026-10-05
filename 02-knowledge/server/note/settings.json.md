---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/settings.json"]
tags: [server, settings, json, configuration]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/start-webui.py"]
task: ["scripts/server/settings.json # サーバー設定JSONファイルの静的解析"]
summary: "scripts/server/settings.json は、デフォルトLLMプロバイダーやGemini・Ollamaのデフォルトモデル・エンドポイントURLを定義するJSON設定ファイルです。"
---

# `scripts/server/settings.json` 解析ノート

## 1. 概要
`scripts/server/settings.json` は、パーソナルナレッジベースサーバーの挙動を制御するJSON形式の設定ファイルです。`config.py` の `load_config()` によって読み込まれ、存在しない場合はデフォルト値から自動生成されます。

## 2. 設定内容
- **`default_provider`**: デフォルトで使用するLLMプロバイダー (`"Ollama (Local LLM)"`)
- **`gemini`**:
  - `default_model`: `"gemini-3.5-flash-lite"`
  - `available_models`: 利用可能なGeminiモデルリスト
- **`ollama`**:
  - `default_model`: `"gemma4-agent"`
  - `endpoint`: `"http://localhost:11434"`
