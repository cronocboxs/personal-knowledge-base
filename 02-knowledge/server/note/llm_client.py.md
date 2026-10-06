---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/llm_client.py"]
tags: [server, llm-client, python]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/knowledge_service.py", "scripts/server/rag_service.py", "scripts/server/start-webui.py"]
task: ["scripts/server/llm_client.py # llm_client.pyの静的解析"]
summary: "Ollama (ローカルLLM) および Gemini (クラウドAPI) に対応した、リトライ機構付きの汎用LLM呼び出しクライアントモジュール。"
---

# llm_client.py 解析ノート

## 概要
`scripts/server/llm_client.py` は、パーソナルナレッジベースのサーバーサイドスクリプト群において、複数のLLMプロバイダー（Ollama および Gemini）へ統一されたインターフェースでプロンプトを送信し、レスポンスを取得するためのクライアントモジュールです。

## 主要な関数と処理フロー

### 1. 汎用LLM呼び出し (`call_llm`)
- 引数:
  - `prompt`: 送信するプロンプト文字列。
  - `llm_provider`: プロバイダー選択（`"Ollama (Local LLM)"` または `"Gemini (Cloud API)"`）。
  - `gemini_model`: 使用する Gemini モデル名。
  - `api_key`: Gemini API キー。
  - `ollama_model`: 使用する Ollama モデル名。
  - `ollama_url`: Ollama エンドポイント URL。

### 2. プロバイダー別の処理
- **Gemini (Cloud API)**:
  - API キーの存在チェックを行い、Google Generative Language API のエンドポイント（`generateContent`）へ `urllib.request` を用いて POST リクエストを送信します。
  - レスポンス JSON から `candidates[0].content.parts[0].text` を抽出して返します。
- **Ollama (Local LLM)**:
  - Ollama のエンドポイント（`/api/generate`）へ JSON ペイロード（モデル名、プロンプト、ストリーミング無効、コンテキスト長 `num_ctx: 64000` 等の設定を含む）を POST 送信します。
  - レスポンス JSON から `response` フィールドを抽出して返します。

### 3. リトライ機構
- HTTP 503 エラーなどの一時的なサーバー負荷・過負荷エラーが発生した場合、最大3回までリトライを行います。
- リトライ間隔は指数バックオフ方式（初回2秒、次4秒）で待機時間を延長します。

## 依存関係
- 標準ライブラリ: `json`, `time`, `urllib.request`, `urllib.error`
- 被依存モジュール: `knowledge_service.py`, `rag_service.py`, `start-webui.py`
