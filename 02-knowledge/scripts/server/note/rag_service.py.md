---
title: "scripts/server/rag_service.py (Note)"
category: "scripts/server"
type: "note"
target: "scripts/server/rag_service.py"
summary: "scripts/server/rag_service.py の詳細解析ノート"
---

# scripts/server/rag_service.py (Note)

## 1. 目的と役割
`rag_service.py` は、パーソナルナレッジベース内のデータに対して高精度な検索を行うためのRAG（Retrieval-Augmented Generation）機能を提供します。OllamaのEmbedding APIを利用してクエリやドキュメントをベクトル化し、SQLiteに保存されたデータから近傍のドキュメントを抽出します。

## 2. 内部構造と主要処理
- **ベクトル生成 (`get_query_embedding`)**: Ollamaのエンドポイント (`/api/embeddings`) に対しHTTPリクエストを送り、テキストの数値ベクトルを取得。
- **類似度計算 (`cosine_similarity`)**: 数学的なコサイン類似度計算により、クエリと各ドキュメントの近縁度を評価。
- **検索処理 (`search_relevant_knowledge`)**: SQLiteデータベース (`knowledge.db`) にアクセスし、保存されたチャンク・ドキュメントのベクトルと比較して上位の関連情報を抽出。

## 3. 依存関係
- 外部・標準ライブラリ: `os`, `sqlite3`, `math`, `json`, `urllib.request`
- 内部モジュール: `config` (`DB_PATH`, `OLLAMA_ENDPOINT`, `EMBED_MODEL`)
