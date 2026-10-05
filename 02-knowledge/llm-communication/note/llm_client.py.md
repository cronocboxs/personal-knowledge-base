---
created: 2026-10-05
updated: 2026-10-05
source: ["scripts/server/llm_client.py"]
tags: [llm, backend, communication]
status: active
phase: 2
parent: []
children: []
related: [config.py]
task: []
summary: "Gemini APIおよびOllamaへの抽象化された呼び出しロジックを提供するクライアントモジュール。"
---

# 🤖 llm_client.py - 外部LLMとの通信レイヤー

## 🧠 役割と目的
`llm_client.py` は、本プロジェクトが依存する全ての外部大規模言語モデル（LLM）とのインターフェースを一元管理する役割を担うクライアントモジュールである。特定のLLM（Gemini または Ollama）に依存せず、共通の `call_llm` 関数を通じてプロンプト（指示書）を送信し、テキスト応答を受け取る抽象化レイヤーを提供することが目的である。

## 🛠️ 主要機能とロジック解説

### 1. 共通インターフェース (`call_llm`)
メインの処理を行う関数。引数として`prompt`、使用する`llm_provider`、および各モデル固有のパラメータ（`gemini_model`, `ollama_model`, `api_key`など）を受け取る。
- **Provider Switching:** `llm_provider`の値に基づき、内部で呼び出すAPIのロジック（Gemini経由か、Ollama経由か）を決定する。
- **Retry Mechanism:** 外部サービスの不安定性に対応するため、HTTPエラー（特に503 Service Unavailable）が発生した場合に備え、最大3回のリトライと指数バックオフ（2초 ➔ 4초...）が実装されている。

### 2. Gemini (Cloud API) 連携
- **認証:** プロジェクトルートの `01-private/gemini_api_key.txt` からAPIキーを読み込む。
- **通信:** `urllib.request` を使用し、指定された `gemini_model` に対してREST APIコールを行う。
- **安全考慮:** APIキーの取り扱いに配慮し、特別なエラーハンドリングが含まれている。

### 3. Ollama連携
- **通信:** ローカルホストのOllamaエンドポイント (`http://localhost:11434`) にPOSTリクエストを送信する。
- **Payload:** モデル名、プロンプト、ストリームフラグ (`"stream": False`) を含むJSONボディを構築する。
- **効率:** JSON構造を正確に構築し、`urllib.request`を通じて呼び出すことができている。

## 🔄 依存関係とシステム統合
- **依存:** `config.py` から提供されるグローバルな設定（`ollama_url`, モデル名など）に完全に依存している。
- **役割:** システムコンポーネント（`knowledge_service.py`など）が「LLMを使いたい」という要求をこのクライアント層に投げ、具体的なAPI通信の実装を任せる。
- **技術的深み:** このレイヤーのお陰で、後からGoogle GeminiからOpenAIなどの別モデルに切り替えても、呼び出し元のロジック（`knowledge_service.py`）を変更する必要が大幅に減る、高い疎結合性が実現されている。