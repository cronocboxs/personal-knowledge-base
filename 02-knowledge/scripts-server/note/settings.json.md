---
title: "scripts/server/settings.json Note"
date: 2026-10-06
tags: [server, settings]
category: scripts-server
description: "サーバー設定JSONファイルの詳細解析"
---

# Note: scripts/server/settings.json

## 1. 目的と役割
本ファイル `settings.json` は `サーバー設定JSONファイル` として動作し、システム全体の中で重要な役割を果たします。

## 2. 主要な構成要素・処理フロー
- ファイル種別: `json`
- 責務: サーバー設定JSONファイル

## 3. コード内容 / 構成
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

## 4. 依存関係と連携
- `scripts/server/` 内の他のモジュールとの連携。
