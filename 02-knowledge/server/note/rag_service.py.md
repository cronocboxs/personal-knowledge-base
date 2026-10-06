---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/rag_service.py"]
tags: [server, rag-service, python]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/knowledge_service.py", "scripts/server/llm_client.py", "scripts/server/start-webui.py"]
task: ["scripts/server/rag_service.py # rag_service.pyの静的解析"]
summary: "Ollama Embeddings APIを用いたクエリベクトル化、コサイン類似度計算、SQLiteインデックスからの高度なセマンティック検索を行うRAGサービスモジュール。"
---

# rag_service.py 解析ノート

## 概要
`scripts/server/rag_service.py` は、パーソナルナレッジベースにおいて、ユーザーの質問クエリに対するセマンティック検索（RAG: Retrieval-Augmented Generation）を実現するためのサービスモジュールです。

## 主要な関数と処理フロー

### 1. クエリベクトル化 (`get_query_embedding`)
- 指定されたテキストクエリを Ollama の Embeddings API（`{OLLAMA_ENDPOINT}/api/embeddings`）へ送信し、モデル（`nomic-embed-text`）を用いたベクトル表現（浮動小数点数リスト）を取得します。

### 2. コサイン類似度計算 (`cosine_similarity`)
- 2つのベクトル間のコサイン類似度を計算し、方向の一致度（0.0 〜 1.0）を算出します。
- ゼロ除算や次元数不一致に対する安全なガード処理が含まれています。

### 3. ナレッジ類似度検索 (`search_relevant_knowledge`)
- SQLite データベース（`DB_PATH`）から、指定されたカテゴリフィルター条件に従ってインデックスデータ（パス、カテゴリ、タイトル、概要、本文、ベクトル）を取得します。
- 各ドキュメントのベクトル (`emb_str`) を JSON パースし、クエリベクトルとのコサイン類似度を計算します。
- 類似度スコアの降順でソートし、上位 `top_k` 件の関連ドキュメント情報を抽出して返却します。

## 依存関係
- 標準ライブラリ: `os`, `sqlite3`, `math`, `json`, `urllib.request`
- 内部モジュール: `config` (`DB_PATH`, `OLLAMA_ENDPOINT`, `EMBED_MODEL`)
- 被依存モジュール: `start-webui.py`
