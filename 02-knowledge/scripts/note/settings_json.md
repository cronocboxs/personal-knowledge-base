---
title: "settings_json"
source: "scripts/server/settings.json"
category: "scripts"
type: "note"
created_at: "2026-10-06"
---

# 詳細解析ノート: `scripts/server/settings.json`

## 1. 目的・役割
- `scripts/server/settings.json` の静的解析に基づく機能・役割の解説。

## 2. 内部構造・主要処理フロー
```python
# ソースコード内容抜粋・構造サマリ
```

## 3. ソースコード全文（リファレンス）
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
