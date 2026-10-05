---
title: "scripts/server/rag_service.py (Head)"
category: "scripts/server"
type: "head"
target: "scripts/server/rag_service.py"
summary: "SQLiteとOllama埋め込みを用いたRAG類似度検索サービス"
---

# scripts/server/rag_service.py (Head)

## 概要
テキストの埋め込みベクトル（Embedding）生成、SQLiteデータベースをバックエンドにしたコサイン類似度に基づくナレッジ検索（RAG）機能を提供するモジュールです。

## 主要関数
- `get_query_embedding(text: str)`: テキストからベクトル埋め込みを取得
- `cosine_similarity(v1, v2)`: 2つのベクトル間のコサイン類似度計算
- `search_relevant_knowledge(query: str, limit: int)`: 関連ナレッジの類似度検索
