---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/rag_service.py"]
tags: ["scripts", "server", "rag", "search"]
status: active
phase: 2
parent: []
children: []
related: ["scripts/server/config.py"]
task: []
summary: "scripts/server/rag_service.py の静的解析ノート"
---

# `scripts/server/rag_service.py` 解析ノート

## 概要
`scripts/server/rag_service.py` は、パーソナルナレッジベースにおける RAG（Retrieval-Augmented Generation）のコアロジック（ベクトル埋め込み生成、コサイン類似度計算、SQLite データベースからの類似度検索）を提供するモジュールです。

## 主な関数と処理フロー
### 1. `get_query_embedding(text: str) -> list[float]`
- Ollama の埋め込み API (`/api/embeddings`) を呼び出し、入力テキスト（質問文など）のベクトル表現（埋め込み）を取得します。

### 2. `cosine_similarity(v1: list[float], v2: list[float]) -> float`
- 2つのベクトル間のコサイン類似度を計算します。

### 3. `search_relevant_knowledge(query: str, top_k: int = 3, target_categories: list[str] = None) -> list[dict]`
- SQLite データベース (`01-private/knowledge_index.db`) に接続します。
- 必要に応じてカテゴリフィルタを適用し、ナレッジのタイトル、概要、本文、ベクトルを取得します。
- クエリのベクトルと各ドキュメントのベクトル間でコサイン類似度を計算し、スコアが高い順にソートして上位 `top_k` 件のドキュメント情報を返します。
