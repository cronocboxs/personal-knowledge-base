---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/settings.json"]
tags: ["scripts", "server", "config"]
status: active
phase: 5
parent: []
children: []
related: []
task: ["scripts/server/settings.json # 解析対象ファイル"]
summary: "スクリプトサーバーの実行設定・パラメータ定義ファイル"
---

# server-settings

## 概要
スクリプトサーバーの実行設定・パラメータ定義ファイル

## ソースコード内容
```
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
