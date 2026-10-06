---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/llm_client.py"]
tags: [python, server, llm-client]
status: active
phase: 3
parent: []
children: []
related: ["scripts/server/llm_client.py", "scripts/server/config.py"]
task: ["scripts/server/llm_client.py # 汎用LLMクライアントモジュール"]
summary: "scripts/server/llm_client.py の静的解析。Gemini Cloud APIおよびローカルOllamaエンドポイントに対応したリトライ機能付き汎用LLM呼び出しクライアントを提供。"
---

# llm_client.py 解析ノート

## 1. 概要
`scripts/server/llm_client.py` は、パーソナルナレッジベース内の各サービスから呼び出される汎用LLMクライアントモジュールです。標準ライブラリ（`urllib`）のみを使用して、Gemini Cloud APIおよびローカルのOllamaサーバーへリクエストを送信します。

## 2. 主要関数・処理フロー

- **`call_llm(...) -> str`**
  - **Gemini (Cloud API)**:
    - APIキーの存在を確認し、Google Generative Language API (`v1beta/models/{gemini_model}:generateContent`) へリクエストを送信。
    - レスポンスの `candidates[0].content.parts[0].text` を返却する。
  - **Ollama (Local LLM)**:
    - 指定された `ollama_url`（デフォルト `http://localhost:11434`）の `/api/generate` エンドポイントへ JSON ペイロードを送信。
    - コンテキスト長 (`num_ctx: 64000`) や無制限予測 (`num_predict: -1`) などのオプションを設定。
    - レスポンスの `response` フィールドを返却する。
  - **リトライ機構**:
    - HTTP 503エラー発生時、最大3回までエクスポネンシャルバックオフ（2秒、4秒）を挟んで自動リトライを実行する。

## 3. 依存関係
- 標準ライブラリ: `json`, `time`, `urllib.request`, `urllib.error`
