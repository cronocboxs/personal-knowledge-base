---
created: 2026-10-06
updated: 2026-10-06
source: ["04-resources/scripts/server/settings.json"]
tags: [server, settings, json, config]
status: active
phase: 3
parent: []
children: []
related: ["scripts/server/config.py"]
task: ["scripts/server/settings.json # サーバー設定JSONファイルの静的解析"]
summary: "WebUI等のサーバー機能におけるデフォルトLLMプロバイダーやGemini/Ollamaモデルの初期設定を定義するJSONファイル。"
---

# settings.json 解析ノート

## 1. 概要
`scripts/server/settings.json` は、パーソナルナレッジベースのローカルサーバーおよび WebUI アプリケーションにおけるデフォルトの LLM プロバイダーやモデル構成を保持する設定ファイルです。

## 2. 設定項目詳細
- `default_provider`: 起動時のデフォルトプロバイダー（例: `"Ollama (Local LLM)"`）
- `gemini`: Google Gemini に関する設定
  - `default_model`: デフォルトで使用するGeminiモデル名（例: `"gemini-3.5-flash-lite"`）
  - `available_models`: 利用可能なモデルのリスト
- `ollama`: ローカルLLM (Ollama) に関する設定
  - `default_model`: デフォルトのOllamaモデル名（例: `"gemma4-agent"`）
  - `endpoint`: Ollama の接続先エンドポイント (`http://localhost:11434`)

## 3. 関連モジュール
- `scripts/server/config.py`: 本 JSON ファイルを読み込み、存在しない場合は自動生成する。
