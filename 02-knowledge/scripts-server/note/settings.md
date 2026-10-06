---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/settings.json"]
tags: [config, json, server]
status: active
phase: 3
parent: []
children: []
related: ["scripts/server/config.py"]
task: ["scripts/server/settings.json # settings.jsonの設定項目とモデル定義の解析"]
summary: "scripts/server/settings.json は、WebUIサーバー等のデフォルトプロバイダやGemini/Ollamaのモデル設定を保持するJSON設定ファイル。"
---

# settings.json 解析ノート

## 1. 概要
`scripts/server/settings.json` は、サーバーアプリケーションの動作設定（デフォルトLLMプロバイダ、各AIバックエンドのモデル、エンドポイント等）を定義するJSONファイルです。

## 2. 設定パラメータ
- **`default_provider`**: サーバーがデフォルトで使用するLLMプロバイダ（例: `"Ollama (Local LLM)"`）。
- **`gemini`**:
  - `default_model`: `"gemini-3.5-flash-lite"`
  - `available_models`: 利用可能なGeminiモデルのリスト。
- **`ollama`**:
  - `default_model`: `"gemma4-agent"`
  - `endpoint`: `"http://localhost:11434"`

## 3. 依存関係
- 関連ファイル: `scripts/server/config.py`（本ファイルを読み込み・書き出しする）
