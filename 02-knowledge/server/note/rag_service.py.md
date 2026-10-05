---
created: 2026-10-06
updated: 2026-10-06
source: ["04-resources/scripts/server/rag_service.py"]
tags: [server, rag, vector-search, sqlite, ollama, python]
status: active
phase: 3
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/knowledge_service.py", "scripts/server/llm_client.py"]
task: ["scripts/server/rag_service.py # RAGベクトル検索サービスの静的解析"]
summary: "Ollama Embeddings APIを用いたクエリベクトル化と、SQLiteに格納されたナレッジとのコサイン類似度に基づくRAG検索機能を提供するモジュール。"
---

# rag_service.py 解析ノート

## 1. 概要
`scripts/server/rag_service.py` は、パーソナルナレッジベース内を対象とした RAG（Retrieval-Augmented Generation）検索機能を提供するサービスモジュールです。

## 2. 主要関数詳細

### `get_query_embedding(text: str) -> list[float]`
- Ollama エンドポイント (`/api/embeddings`) に対して HTTP リクエストを送信し、入力テキストの埋め込みベクトル（リスト形式）を取得する。

### `cosine_similarity(v1: list[float], v2: list[float]) -> float`
- 2つのベクトル間のコサイン類似度を計算する。
- ベクトルの次元不一致やゼロベクトルの場合は `0.0` を返す。

### `search_relevant_knowledge(query: str, top_k: int = 3, target_categories: list[str] = None) -> list[dict]`
- SQLite データベース (`knowledge_index.db`) からナレッジデータを取得する。
- カテゴリ指定がある場合はフィルタリングを実施。
- 各ドキュメントのベクトル (`embedding`) とクエリベクトルのコサイン類似度を計算し、スコアが高い順にソートして上位 `top_k` 件を返す。

## 3. 依存関係
- `config.py` から `DB_PATH`, `OLLAMA_ENDPOINT`, `EMBED_MODEL` をインポート。
- 標準ライブラリ (`os`, `sqlite3`, `math`, `json`, `urllib.request`) を使用。
