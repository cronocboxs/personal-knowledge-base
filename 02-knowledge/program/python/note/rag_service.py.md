---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/rag_service.py"]
tags: [python, server, rag-service]
status: active
phase: 3
parent: []
children: []
related: ["scripts/server/rag_service.py", "scripts/server/config.py"]
task: ["scripts/server/rag_service.py # RAG類似度検索サービスモジュール"]
summary: "scripts/server/rag_service.py の静的解析。Ollama埋め込みAPIを用いたクエリベクトル化、コサイン類似度計算、およびSQLiteインデックスからの関連ナレッジ検索機能を提供。"
---

# rag_service.py 解析ノート

## 1. 概要
`scripts/server/rag_service.py` は、パーソナルナレッジベースにおけるRAG（Retrieval-Augmented Generation）検索を担うサービスモジュールです。Ollamaの埋め込みモデル（`nomic-embed-text`）を活用してクエリをベクトル化し、SQLiteデータベースに保存されたナレッジとのコサイン類似度を算出します。

## 2. 主要関数・処理フロー

- **`get_query_embedding(text: str) -> list[float]`**
  - Ollama埋め込みエンドポイント（`http://localhost:11434/api/embeddings`）へテキストを送信し、ベクトルの配列を取得する。
- **`cosine_similarity(v1: list[float], v2: list[float]) -> float`**
  - 2つのベクトル間のコサイン類似度を数学的に計算する。
- **`search_relevant_knowledge(query: str, top_k: int, target_categories: list[str]) -> list[dict]`**
  - SQLiteデータベース（`knowledge_index.db`）から指定カテゴリのナレッジを抽出。
  - 各ナレッジの保存済みベクトルとクエリベクトルのコサイン類似度を算出し、スコア降順で上位 `top_k` 件を返却する。

## 3. 依存関係
- 標準ライブラリ: `os`, `sqlite3`, `math`, `json`, `urllib.request`
- 外部モジュール: `config`
