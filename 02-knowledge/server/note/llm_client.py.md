---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/llm_client.py"]
tags: [server, llm-client, ollama, gemini, python]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/knowledge_service.py", "scripts/server/rag_service.py", "scripts/server/start-webui.py"]
task: ["scripts/server/llm_client.py # LLMクライアントサービスモジュールの静的解析"]
summary: "scripts/server/llm_client.py は Ollama（ローカルLLM）および Gemini（クラウドAPI）に対するリクエスト送信とエラー時のリトライ制御を行う汎用LLMクライアントモジュールです。"
---

# `scripts/server/llm_client.py` 解析ノート

## 1. 概要
`scripts/server/llm_client.py` は、パーソナルナレッジベースサーバーサイド群から呼び出される汎用LLMクライアントモジュールです。ローカル環境の Ollama API とクラウドの Gemini API の双方をサポートし、503エラーなどの一時的な障害に対する指数バックオフによるリトライ機構を備えています。

## 2. 主要な関数

### `call_llm(prompt: str, llm_provider: str = "Ollama (Local LLM)", gemini_model: str = "gemini-2.5-flash", api_key: str = "", ollama_model: str = "qwen2.5:1.5b", ollama_url: str = "http://localhost:11434") -> str`
- **目的**: 指定されたプロバイダ（Ollama または Gemini）に対してプロンプトを送信し、LLMからの生成テキスト応答を取得する。
- **機能**:
  - **Gemini (Cloud API)**: `api_key` の存在チェック後、Google Generative Language API (`v1beta`) の `generateContent` エンドポイントへリクエストを送信。
  - **Ollama (Local LLM)**: 指定された `ollama_url` の `/api/generate` エンドポイントへリクエストを送信。大きなコンテキスト窓（`num_ctx: 64000`）や無制限予測（`num_predict: -1`）を設定。
  - **リトライ制御**: HTTP 503 エラーが発生した際、最大3回まで指数バックオフ（2秒 ➔ 4秒）でリトライを実行。

## 3. 依存関係
- 標準ライブラリ: `json`, `time`, `urllib.request`, `urllib.error`
- 関連ファイル: `config.py`, `knowledge_service.py`, `rag_service.py`, `start-webui.py`
