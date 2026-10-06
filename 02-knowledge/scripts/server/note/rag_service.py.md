---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/rag_service.py"]
tags: [server, rag, sqlite, embedding, ollama, python]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/knowledge_service.py"]
task:
  - "scripts/server/rag_service.py # RAG検索サービスモジュール"
summary: "Ollama Embeddings APIを用いたクエリのベクトル化、コサイン類似度計算、およびSQLite上のナレッジベース検索を提供するRAGサービスモジュール"
---

# scripts/server/rag_service.py 解析ノート

## 1. 概要・責務
`scripts/server/rag_service.py` は、パーソナルナレッジベースにおけるRAG（Retrieval-Augmented Generation）検索の中核を担うモジュールです。クエリテキストのベクトル化（Ollama API経由）、コサイン類似度の算出、SQLiteデータベース（`knowledge_index.db`）からの上位関連ドキュメント検索を提供します。

## 2. 主要関数・処理フロー

### `get_query_embedding(text: str) -> list[float]`
1. Ollama のエンドポイント (`/api/embeddings`) に対し、`EMBED_MODEL`（`nomic-embed-text`）とプロンプトを指定してPOSTリクエストを送信する。
2. レスポンスから埋め込みベクトル（浮動小数点数リスト）を抽出して返す。失敗時は空リストを返す。

### `cosine_similarity(v1: list[float], v2: list[float]) -> float`
1. 2つのベクトルの内積と各ノルム（L2ノルム）を計算し、コサイン類似度（0.0〜1.0）を算出する。
2. 次元数不一致やゼロノルムの場合は `0.0` を返す。

### `search_relevant_knowledge(query: str, top_k: int = 3, target_categories: list[str] = None) -> list[dict]`
1. `DB_PATH` の存在を確認する。存在しない場合は空リストを返す。
2. `get_query_embedding(query)` でクエリベクトルを取得する。
3. SQLite データベースから指定されたカテゴリ（未指定または「すべて」の場合は全件）に合致するレコード（`rel_path`, `category`, `title`, `summary`, `content`, `embedding`）を取得する。
4. 各ドキュメントのベクトルをJSONパースし、クエリベクトルとのコサイン類似度を算出する。
5. スコアの降順でソートし、上位 `top_k` 件の辞書リストを返す。

## 3. 依存関係
- `os`, `sqlite3`, `math`, `json`, `urllib.request`
- インポート元/設定: `scripts/server/config.py`
