---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/llm_client.py"]
tags: [server, llm, client, ollama, gemini, python]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/knowledge_service.py", "scripts/server/start-webui.py"]
task: ["scripts/server/llm_client.py # scripts/server/llm_client.pyの静的解析完了"]
summary: "Ollama（ローカルLLM）およびGemini（クラウドAPI）に対するプロンプト送信とレスポンス取得を抽象化・統一する汎用LLMクライアントモジュール。"
---

# llm_client.py 解析ノート

## 1. 概要
`llm_client.py` は、パーソナルナレッジベースのサーバーサイド機能（WebUI やナレッジ自動昇華など）から呼び出される、LLM プロバイダ抽象化クライアントモジュールです。Ollama（ローカル LLM）および Gemini（Google Cloud API）の両方に対応し、HTTP リクエストの送信、例外処理、および一時的な 503 エラーに対する指数バックオフによるリトライ処理をカプセル化しています。

## 2. 依存関係
- **インポートモジュール**: `json`, `time`, `urllib.request`, `urllib.error`
- **内部モジュール依存**: なし（他のサーバーモジュールからインポートして使用される基盤モジュール）

## 3. 主要関数・処理フロー

### `call_llm(prompt: str, llm_provider: str = "Ollama (Local LLM)", gemini_model: str = "gemini-2.5-flash", api_key: str = "", ollama_model: str = "qwen2.5:1.5b", ollama_url: str = "http://localhost:11434") -> str`
- **目的**: 指定されたプロバイダ（Ollama または Gemini）に対してプロンプトを送信し、生成されたテキスト応答を取得する。
- **処理フロー**:
  1. 最大リトライ回数（`max_retries = 3`）に基づくループを実行。
  2. **Gemini (Cloud API) の場合**:
     - `api_key` の存在を確認（未設定時は `ValueError`）。
     - Google Generative Language API のエンドポイント (`generateContent`) へ JSON ペイロードを送信。
     - レスポンスから `"candidates"][0]["content"]["parts"][0]["text"` を抽出して返す。
  3. **Ollama (Local LLM) の場合**:
     - Ollama の `/api/generate` エンドポイントへリクエスト送信。
     - コンテキスト長(`num_ctx: 64000`)や `keep_alive` などのオプションを指定。
     - レスポンスの `"response"` フィールドを抽出して返す。
  4. **例外処理・リトライ**:
     - HTTP 503 エラー等の過負荷時、待機時間を倍増（2秒 ➔ 4秒）させながらリトライを実行。その他のエラーはそのまま送出。
