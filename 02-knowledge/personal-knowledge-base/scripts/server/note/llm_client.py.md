---
created: 2026-10-02
updated: 2026-10-02
source: ["scripts/server/llm_client.py"]
tags: ["llm", "python", "api-client", "ollama", "gemini"]
status: draft
phase: 1
parent: []
children: []
related: ["01-private/gemini_api_key.txt"]
task: []
summary: "本コードは、ローカルのOllama環境とクラウドベースのGemini APIの両方に対応する、汎用的なLLM呼び出しラッパー関数（call_llm）を定義するPythonクライアントライブラリである。"
---

---
created: 2026-10-02
updated: 2026-10-02
source: ["scripts/server/llm_client-py.py"]
tags: [code-analysis, llm, api-client]
status: draft
phase: 1
parent: []
children: []
related: [Gemini (Cloud API), Ollama, urllib.request, json]
task: []
summary: "外部のLLMプロバイダー（GeminiまたはOllama）に対して汎用的なプロンプト送信および応答取得を行うためのPythonクライアント関数を定義している。"
---

# llm_client-py 解析ノート

## 1. 概要・目的

本ファイルは、複数の異なる大規模言語モデル（LLM）プロバイダー（具体的にはGoogle Gemini Cloud APIとローカルのOllama）へ、単一の関数インターフェースからアクセスし、テキスト生成を行うための汎用的なクライアントコードを実装しています。

主な目的は、利用するLLMの環境や認証方法（クラウドAPIキーを持つか、ローカルサーバーに依存するか）の違いを、呼び出し側から隠蔽し、単一のエンドポイントで管理することです。

## 2. 主要コンポーネント・関数

### `call_llm` 関数
*   **責務**: 指定された`llm_provider`に基づいて、LLMとの通信を試み、結果の文字列を返す。
*   **引数**:
    *   `prompt` (str): LLMに渡す入力プロンプト。
    *   `llm_provider` (str, default: "Ollama (Local LLM)")：使用するLLMのプロバイダー名（"Gemini (Cloud API)"またはその他）。
    *   `gemini_model` (str)：Geminiで使用するモデル名。
    *   `api_key` (str)：Geminiを利用するためのAPIキー。
    *   `ollama_model` (str)：Ollamaで使用するモデル名。
    *   `ollama_url` (str)：ローカルのOllama APIのエンドポイント。

## 3. 処理フローと重要実装ポイント

### 🌐 プロバイダー分岐ロジック
関数内部では、`if llm_provider == "Gemini (Cloud API)"` の分岐により、実行するHTTPリクエストの構造（URL、ペイロード）が切り替えられています。

### 🔄 リトライ機構の実装 (Resilience)
*   **目的**: API接続が不安定な場合に備え、指数バックオフ（Exponential Backoff）に基づいたリトライ処理を実装しています。
*   **ロジック**:
    *   最大試行回数は3回に制限されています。
    *   HTTPエラーコード`503`（Service Unavailable）を受け取った場合のみリトライが発生します。
    *   リトライするたびに待機時間 (`retry_delay`) が2倍に増加します（2秒 → 4秒）。これにより、サービス負荷を考慮した待機が実現されています。

### 🔑 Gemini Cloud API接続
1.  APIキーの存在確認が必須であり、キーがない場合は`ValueError`を発生させることが規約されています。
2.  GeminiのエンドポイントURLを構築し、プロンプトをJSON形式のペイロードに格納します。
3.  `urllib.request`を使用してPOSTリクエストを送信し、応答JSONから結果を抽出して返却します。

### 🐳 Ollama Local LLM接続
1.  Ollamaの`/api/generate`エンドポイントを使用します。
2.  プロンプトと共に、モデル名、ストリーム制御、コンテキストウィンドウサイズ (`num_ctx: 64000`) などの詳細なオプションをペイロードに含めて送信しています。
3.  応答JSONの`response`キーから最終的な生成テキストを抽出して返却します。
