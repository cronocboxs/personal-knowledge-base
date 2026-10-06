---
created: 2026-10-06
updated: 2026-10-06
source: ["04-resources/scripts/server/rag_service.py"]
tags: [server, rag, vector, sqlite, python]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py"]
task: ["scripts/server/rag_service.py # RAG検索サービスモジュール"]
summary: "scripts/server/rag_service.py は、Ollamaを用いた質問文のベクトル化、コサイン類似度の算出、およびSQLiteナレッジインデックスDBを活用した高精度なRAG（検索拡張生成）の検索サービスを提供するモジュールである。"
---

# rag_service.py 解析ノート

## 1. 概要
`scripts/server/rag_service.py` は、ナレッジベース内からユーザーの質問に対して関連性の高いドキュメントを検索・抽出する RAG (Retrieval-Augmented Generation) のバックエンドロジックを提供します。

## 2. 主要関数
### `get_query_embedding(text: str) -> list[float]`
- 引数のテキストを Ollama の埋め込みモデル（`nomic-embed-text`）に送信し、数値ベクトル（埋め込み表現）を取得・返却します。
- 接続エラーが発生した場合はエラーを出力し、空リストを返します。

### `cosine_similarity(v1: list[float], v2: list[float]) -> float`
- 2つのベクトル間のコサイン類似度（余弦類似度）を計算します。
- ベクトルの次元数が異なる場合やノルムが 0 の場合は安全に `0.0` を返します。

### `search_relevant_knowledge(query: str, top_k: int = 3, target_categories: list[str] = None) -> list[dict]`
- SQLite データベース (`knowledge_index.db`) からナレッジ情報を取得します。
- 指定されたカテゴリ（`target_categories`）がある場合はフィルタリングを行います。
- クエリのベクトルと各ドキュメントのベクトル間のコサイン類似度を計算し、類似度スコアが高い順に上位 `top_k` 件のドキュメント（パス、カテゴリ、タイトル、概要、本文、スコア）を返却します。
