---
created: 2026-10-06
updated: 2026-10-06
source: ["04-resources/scripts/server/llm_client.py"]
tags: [server, llm, client, ollama, gemini, python]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py"]
task: ["scripts/server/llm_client.py # 汎用LLMクライアントモジュール"]
summary: "scripts/server/llm_client.py は、Ollama(ローカルLLM)およびGemini(クラウドAPI)の双方に対応した統一的なLLM呼び出しインターフェースを提供し、リトライ機構やパラメータ設定を内包するクライアントモジュールである。"
---

# llm_client.py 解析ノート

## 1. 概要
`scripts/server/llm_client.py` は、パーソナルナレッジベース内の各サービスから呼び出される汎用 LLM クライアントモジュールです。
Ollama（ローカル LLM）および Google Gemini（クラウド API）の両方に対応し、HTTP リクエスト、エラーハンドリング、およびエクスポネンシャルバックオフによるリトライ機構を提供します。

## 2. 主要関数
### `call_llm(prompt: str, llm_provider: str = "Ollama (Local LLM)", gemini_model: str = "gemini-2.5-flash", api_key: str = "", ollama_model: str = "qwen2.5:1.5b", ollama_url: str = "http://localhost:11434") -> str`
- **Gemini (Cloud API) モード**:
  - 指定された `api_key` を用いて Google Generative Language API (`v1beta/models/{model}:generateContent`) へリクエストを送信し、生成テキストを取得します。
- **Ollama (Local LLM) モード**:
  - 指定された `ollama_url`（デフォルト `http://localhost:11434`）の `/api/generate` エンドポイントに対し、コンテキスト長やストリーム無効化などのオプションを指定してリクエストを送信し、応答テキストを取得します。
- **リトライ機構**:
  - HTTP 503 エラーなどの一時的な過負荷・サービス利用不可エラーが発生した際、最大3回までエクスポネンシャルバックオフ（待機時間を倍増: 2秒 → 4秒）で自動リトライを行います。
