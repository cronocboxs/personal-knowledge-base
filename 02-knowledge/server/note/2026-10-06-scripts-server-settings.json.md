---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/settings.json"]
tags: ["server", "settings", "json", "config"]
status: active
phase: 2
parent: ["scripts/server/config.py"]
children: []
related: ["scripts/server/config.py"]
task: []
summary: "scripts/server/settings.jsonの静的解析ノート: バックエンドサーバーのデフォルトLLMプロバイダ、Gemini/Ollamaのモデル設定を定義するJSON設定ファイル。"
---

# scripts/server/settings.json 解析ノート

## 1. 概要・目的
`scripts/server/settings.json` は、パーソナルナレッジベースのサーバーおよびWebUIにおけるデフォルトのLLMプロバイダ、クラウドAPI（Gemini）やローカルLLM（Ollama）のモデル設定を保持するJSONファイルです。
`scripts/server/config.py` の `load_config()` を通じて読み込まれ、設定のカスタマイズ基盤として機能します。

## 2. 構造・主要パラメータ
```json
{
  "default_provider": "Ollama (Local LLM)",
  "gemini": {
    "default_model": "gemini-3.5-flash-lite",
    "available_models": [
      "gemini-3.5-flash-lite"
    ]
  },
  "ollama": {
    "default_model": "gemma4-agent",
    "endpoint": "http://localhost:11434"
  }
}
```

- **`default_provider`**: 初期選択されるLLMプロバイダ（例: `"Ollama (Local LLM)"`）。
- **`gemini`**: クラウドAPIの設定。
  - `default_model`: デフォルトのGeminiモデル名。
  - `available_models`: 利用可能なモデル一覧。
- **`ollama`**: ローカルLLMの設定。
  - `default_model`: デフォルトのOllamaモデル名。
  - `endpoint`: OllamaのAPIエンドポイントURL。

## 3. 依存関係
- 読み込み元: `scripts/server/config.py`
