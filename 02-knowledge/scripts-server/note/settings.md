---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/settings.json"]
tags: [server, scripts, python]
status: active
phase: 5
parent: []
children: []
related: []
task: ["scripts/server/settings.json"]
summary: "Static analysis and knowledge note for settings.json in scripts/server/"
---

# settings.json 解析ノート

## 概要
`scripts/server/settings.json` の静的解析結果および主要構造のドキュメント。

## ソースコード / 設定内容
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

## 処理フロー・責務
- ファイルの役割と依存関係の解析。
- サーバスクリプト群における位置づけと仕様。
