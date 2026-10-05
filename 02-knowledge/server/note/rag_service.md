---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/rag_service.py"]
tags: [server, rag, sqlite, ollama, python]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/knowledge_service.py", "scripts/server/llm_client.py"]
task: ["scripts/server/rag_service.py # scripts/server/rag_service.pyの静的解析完了"]
summary: "OllamaとSQLiteを利用したベクトル埋め込みによるコサイン類似度検索・RAG検索ロジックを提供するサービスモジュール。"
---

# rag_service.py 解析ノート

## 1. 概要
`rag_service.py` は、ユーザーの質問文を Ollama の埋め込みモデル（Embed Model）を用いてベクトル化し、SQLite データベース（`knowledge_index` テーブル）に保存されているドキュメント群のベクトルとコサイン類似度を計算して、関連度の高いドキュメントを抽出する RAG（Retrieval-Augmented Generation）検索サービスモジュールです。

## 2. 依存関係
- **インポートモジュール**: `os`, `sqlite3`, `math`, `json`, `urllib.request`
- **内部設定依存**: `config.py` から `DB_PATH`, `OLLAMA_ENDPOINT`, `EMBED_MODEL` をインポート。

## 3. 主要関数・処理フロー

### `get_query_embedding(text: str) -> list[float]`
- **目的**: 入力されたテキスト（質問文など）を Ollama の `/api/embeddings` エンドポイントに送信し、数値ベクトル（埋め込み表現）を取得する。
- **処理フロー**:
  1. `OLLAMA_ENDPOINT` と `EMBED_MODEL` を用いてリクエストペイロードを作成。
  2. `urllib.request` を使用して Ollama API を同期呼び出し。
  3. レスポンスから `"embedding"` リストを取得して返す。エラー時は空リストを返しつつ `st.error` で通知。

### `cosine_similarity(v1: list[float], v2: list[float]) -> float`
- **目的**: 2つの数値ベクトル間のコサイン類似度を算出する。
- **処理フロー**:
  1. ベクトルの存在確認と次元数の一致を確認（不一致時は `0.0` を返す）。
  2. 内積、それぞれのノルムを計算し、コサイン類似度（`-1.0`〜`1.0`）を算出する。

### `search_relevant_knowledge(query: str, top_k: int = 3, target_categories: list[str] = None) -> list[dict]`
- **目的**: 指定された質問に関連する知識ベース内のドキュメントを検索する。
- **処理フロー**:
  1. データベースファイルの存在確認（存在しない場合は空リスト）。
  2. `get_query_embedding(query)` でクエリのベクトルを取得。
  3. SQLite に接続し、必要に応じてカテゴリフィルタ (`target_categories`) を適用して `knowledge_index` からレコードを取得。
  4. 各レコードの `embedding`（JSON文字列）をパースし、クエリベクトルとのコサイン類似度を計算。
  5. 類似度の高い順にソートし、上位 `top_k` 件を辞書のリストとして返却。
