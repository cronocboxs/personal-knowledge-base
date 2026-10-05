---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/llm_client.py"]
tags: [server, llm, ollama, gemini, python]
status: active
phase: 3
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/knowledge_service.py", "scripts/server/rag_service.py", "scripts/server/start-webui.py"]
task: ["scripts/server/llm_client.py # scripts/server/llm_client.pyの静的解析・ナレッジ生成"]
summary: "scripts/server/llm_client.py は、Ollama（ローカルLLM）およびGemini（クラウドAPI）の双方に対応した堅牢な汎用LLM呼び出しクライアント（リトライ機構付き）を提供します。"
---

# llm_client.py - 汎用 LLM クライアントモジュール

## 1. 概要
`scripts/server/llm_client.py` は、パーソナルナレッジベースサーバーサイドにおける LLM 呼び出しを抽象化・一元化するモジュールです。Ollama（ローカル LLM）と Gemini（Google Cloud API）の両プロバイダをサポートし、HTTP リクエストエラー（503 Service Unavailable 等）に対する指数バックオフによる自動リトライ機構（最大3回）を備えています。

## 2. 主要な関数

### `call_llm(prompt: str, llm_provider: str = "Ollama (Local LLM)", gemini_model: str = "gemini-2.5-flash", api_key: str = "", ollama_model: str = "qwen2.5:1.5b", ollama_url: str = "http://localhost:11434") -> str`
- **目的**: 指定されたプロバイダとモデル設定に従い、プロンプトを送信して LLM からの応答テキストを取得する。
- **処理ロジック**:
  - **Gemini (Cloud API)**:
    - APIキーの存在チェック。
    - Google Generative Language API (`/v1beta/models/{model}:generateContent`) へ `urllib.request` でリクエスト送信。
    - レスポンスからテキスト抽出。
  - **Ollama (Local LLM)**:
    - Ollama エンドポイント (`/api/generate`) へ `model`, `prompt`, `stream=False`, `options`（コンテキストサイズやkeep_alive等）を設定したペイロードを送信。
    - レスポンスの `response` フィールドを返す。
- **リトライ機構**: HTTP 503 エラー発生時は、待機時間（2秒、4秒…）を倍増させながら最大3回まで再試行する。

## 3. 依存関係
- 設定モジュール: `config.py` から間接的に利用されるほか、各サービスから直接呼び出される。
- 標準ライブラリ: `json`, `time`, `urllib.request`, `urllib.error`
- 連携先: `knowledge_service.py`, `start-webui.py`
