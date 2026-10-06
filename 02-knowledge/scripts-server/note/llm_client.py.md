---
title: "scripts/server/llm_client.py Note"
date: 2026-10-06
tags: [server, llm_client]
category: scripts-server
description: "LLMクライアント通信モジュールの詳細解析"
---

# Note: scripts/server/llm_client.py

## 1. 目的と役割
本ファイル `llm_client.py` は `LLMクライアント通信モジュール` として動作し、システム全体の中で重要な役割を果たします。

## 2. 主要な構成要素・処理フロー
- ファイル種別: `py`
- 責務: LLMクライアント通信モジュール

## 3. コード内容 / 構成
```
import json
import time
import urllib.request
import urllib.error

# ---------------------------------------------------------
# 汎用LLM呼び出し関数
# ---------------------------------------------------------
def call_llm(
    prompt: str,
    llm_provider: str = "Ollama (Local LLM)",
    gemini_model: str = "gemini-2.5-flash",
    api_key: str = "",
    ollama_model: str = "qwen2.5:1.5b",
    ollama_url: str = "http://localhost:11434"
) -> str:
    max_retries = 3
    retry_delay = 2  # 初回待機時間（秒）
    
    for attempt in range(max_retries):
        try:
            if llm_provider == "Gemini (Cloud API)":
                if not api_key:
                    raise ValueError("Gemini API キーが取得できませんでした。`01-private/gemini_api_key.txt` を配置してください。")
                
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}:generateContent?key={api_key}"
                payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
                req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
                
                with urllib.request.urlopen(req) as res:
                    res_data = json.loads(res.read().decode("utf-8"))
                    return res_data["candidates"][0]["content"]["parts"][0]["text"]

            else:
                url = f"{ollama_url.rstrip('/')}/api/generate"
                payload = json.dumps({
                    "model": ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "keep_alive": "5m",
                        "num_ctx": 64000,
                        "num_predict": -1
                    }
                }).encode("utf-8")
                req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
                
                with urllib.request.urlopen(req) as res:
                    res_data = json.loads(res.read().decode("utf-8"))
                    return res_data["response"]
                    
        except urllib.error.HTTPError as e:
            if e.code == 503 and attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2  # 2秒 ➔ 4秒 と待機時間を倍増
                continue
            raise e
        except Exception as e:
            raise e

```

## 4. 依存関係と連携
- `scripts/server/` 内の他のモジュールとの連携。
