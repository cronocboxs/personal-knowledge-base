---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/rag_service.py"]
tags: [server, rag, vector, sqlite, search]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/start-webui.py"]
task: ["scripts/server/rag_service.py # RAGサービス・類似度検索スクリプトの静的解析"]
summary: "scripts/server/rag_service.py は、Ollama embeddings APIを用いた質問文のベクトル化とSQLiteインデックスに対するコサイン類似度検索・RAG検索処理を提供するモジュールです。"
---

# `scripts/server/rag_service.py` 解析ノート

## 1. 概要
`scripts/server/rag_service.py` は、パーソナルナレッジベースにおけるRAG（Retrieval-Augmented Generation）検索の中核を担うモジュールです。質問文を `nomic-embed-text` モデルでベクトル化し、SQLiteに格納された既存のナレッジベクトルとの間でコサイン類似度を計算して関連ドキュメントを抽出します。

## 2. 主要関数
- **`get_query_embedding(text: str) -> list[float]`**:
  - `OLLAMA_ENDPOINT/api/embeddings` に対して `EMBED_MODEL` (`nomic-embed-text`) でプロンプトを送信し、浮動小数点数のベクトル表現を取得する。
- **`cosine_similarity(v1: list[float], v2: list[float]) -> float`**:
  - 2つのベクトル間のコサイン類似度を計算する（0.0 〜 1.0）。
- **`search_relevant_knowledge(query: str, top_k: int = 3, target_categories: list[str] = None) -> list[dict]`**:
  - SQLiteデータベース (`knowledge_index.db`) からナレッジデータを取得し、クエリベクトルとのコサイン類似度が高い上位 `top_k` 件を抽出して返却する。
