---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/rag_service.py"]
tags: [server, rag, sqlite, ollama, vector-search, python]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/knowledge_service.py", "scripts/server/llm_client.py", "scripts/server/start-webui.py"]
task: ["scripts/server/rag_service.py # RAGサービススクリプトの静的解析"]
summary: "scripts/server/rag_service.py は Ollama を用いたベクトル埋め込み生成、コサイン類似度計算、SQLite データベースからの高精度ナレッジ検索（RAG）を提供するサービスモジュールです。"
---

# `scripts/server/rag_service.py` 解析ノート

## 1. 概要
`scripts/server/rag_service.py` は、ローカルLLM（Ollama）の埋め込みAPIとSQLiteに格納されたナレッジインデックスを結合し、検索クエリに対する高精度なベクトル検索（RAG: Retrieval-Augmented Generation）機能を提供するサービスモジュールです。

## 2. 主要な関数

### `get_query_embedding(text: str) -> list[float]`
- **目的**: 入力テキストを Ollama の `/api/embeddings` エンドポイント（`EMBED_MODEL`: `nomic-embed-text`）に送信し、数値ベクトル（埋め込み表現）を取得する。
- **例外処理**: ネットワークエラーや Ollama 未起動時はエラーを表示し、空リストを返却。

### `cosine_similarity(v1: list[float], v2: list[float]) -> float`
- **目的**: 2つのベクトル間のコサイン類似度を計算する。
- **計算方法**: ドット積をそれぞれのノルム（L2ノルム）の積で割ることで算出。0除算や次元数不一致の場合は `0.0` を返す。

### `search_relevant_knowledge(query: str, top_k: int = 3, target_categories: list[str] = None) -> list[dict]`
- **目的**: ユーザーのクエリと SQLite データベース（`DB_PATH`）上の各ナレッジのベクトルを比較し、類似度の高い上位 `top_k` 件のドキュメントを取得する。
- **機能**:
  - `target_categories` によるカテゴリ絞り込み（"すべて" 以外の場合）。
  - 各ドキュメントのベクトルを `json.loads` で復元し、コサイン類似度を算出。
  - スコア降順にソートして上位を返却。

## 3. 依存関係
- 設定: `config.py` (`DB_PATH`, `OLLAMA_ENDPOINT`, `EMBED_MODEL`)
- 標準ライブラリ: `os`, `sqlite3`, `math`, `json`, `urllib.request`
- 関連ファイル: `knowledge_service.py`, `llm_client.py`, `start-webui.py`
