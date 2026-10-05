---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/llm_client.py"]
tags: [llm, ollama, gemini, python, client]
status: active
phase: 2
parent: []
children: []
related: ["scripts/server/config.py"]
task: ["scripts/server/llm_client.py # Python製LLMクライアント（OllamaおよびGemini対応）の静的解析"]
summary: "Ollama (ローカルLLM) および Gemini (クラウドAPI) に対応した、リトライ・エラーハンドリング付き汎用LLM呼び出しクライアントの静的解析。"
---

# llm_client.py の技術解析ノート

## 1. 概要
`scripts/server/llm_client.py` は、パーソナルナレッジベース内の各サービスから呼び出される統合LLMクライアントモジュールです。
外部依存パッケージに極力頼らず、Python標準ライブラリ（`urllib.request`）を用いて、ローカルのOllama APIおよびGoogle Gemini Cloud APIへ安全にプロンプトを送信し、応答を取得する機能を提供します。

## 2. 主要機能と処理フロー

### 2.1 `call_llm` 関数
- **プロバイダ分岐**:
  - `llm_provider == "Gemini (Cloud API)"`:
    - APIキーの存在チェックを行い、Google Generative Language API（`v1beta/models/{gemini_model}:generateContent`）に対してPOSTリクエストを送信。
    - レスポンスの `candidates[0].content.parts[0].text` から生成テキストを抽出して返却。
  - `llm_provider == "Ollama (Local LLM)"` (デフォルト):
    - 指定された `ollama_url`（デフォルト `http://localhost:11434`）の `/api/generate` エンドポイントに対してJSONペイロードを送信。
    - コンテキスト長（`num_ctx: 64000`）や無制限予測（`num_predict: -1`）、`keep_alive` パラメータを設定。
    - レスポンスの `response` フィールドから生成テキストを抽出して返却。

### 2.2 リトライとエラーハンドリング
- 最大3回のリトライロジックを実装。
- HTTP 503エラー（過負荷・一時的利用不可）検知時には、指数バックオフ（2秒 ➔ 4秒）で再試行を実施。

## 3. 依存関係
- 標準ライブラリ: `json`, `time`, `urllib.request`, `urllib.error`
