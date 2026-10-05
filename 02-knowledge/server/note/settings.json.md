---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/settings.json"]
tags: [server, config, json]
status: active
phase: 3
parent: []
children: []
related: ["scripts/server/config.py"]
task: ["scripts/server/settings.json # サーバ設定JSONファイルの静的解析"]
summary: "WebUIおよびLLMサービスで使用するデフォルトプロバイダ、Gemini、Ollamaのモデル設定を保持するJSON設定ファイル。"
---

# `scripts/server/settings.json` 解析ノート

## 1. 概要
`scripts/server/settings.json` は、`scripts/server/` 配下のアプリケーション（WebUIやLLMクライアント）が参照する構成設定ファイルを定義する JSON ファイルです。

## 2. 設定構造と内容
- `default_provider`: 既定の LLM プロバイダ（例: `"Ollama (Local LLM)"`）
- `gemini`:
  - `default_model`: Gemini の既定モデル (`"gemini-3.5-flash-lite"`)
  - `available_models`: 利用可能な Gemini モデルのリスト
- `ollama`:
  - `default_model`: Ollama の既定モデル (`"gemma4-agent"`)
  - `endpoint`: Ollama の API エンドポイント (`"http://localhost:11434"`)

## 3. 関連ファイル
- `scripts/server/config.py`: 本設定ファイルを読み込み・フォールバック生成するモジュール。
