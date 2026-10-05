---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/llm_client.py"]
tags: [server, llm, client, api, ollama, gemini]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/knowledge_service.py", "scripts/server/start-webui.py"]
task: ["scripts/server/llm_client.py # 汎用LLMクライアントモジュールの静的解析"]
summary: "scripts/server/llm_client.py は、Gemini Cloud APIおよびOllama Local LLMに対する統一的な呼び出しインターフェースを提供するクライアントモジュールです。"
---

# `scripts/server/llm_client.py` 解析ノート

## 1. 概要
`scripts/server/llm_client.py` は、パーソナルナレッジベースサーバーから外部のGemini Cloud APIやローカルのOllamaインスタンスへプロンプトを送信し、レスポンスを取得するための汎用LLMクライアントモジュールです。リトライ機構を備えており、ネットワークの一時的な揺らぎに強い設計になっています。

## 2. 主要関数
- **`call_llm(prompt: str, llm_provider: str = "Ollama (Local LLM)", gemini_model: str = "gemini-2.5-flash", api_key: str = "", ollama_model: str = "qwen2.5:1.5b", ollama_url: str = "http://localhost:11434") -> str`**:
  - `llm_provider` の値に応じて、Gemini API または Ollama API に対するHTTPリクエストを構築・送信する。
  - Ollamaの場合はコンテキスト長 (`num_ctx: 64000`) などのオプションを指定して実行する。
  - 最大3回のリトライ機構 (`max_retries = 3`) を内包する。
