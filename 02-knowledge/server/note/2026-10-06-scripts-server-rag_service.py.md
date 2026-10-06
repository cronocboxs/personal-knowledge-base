---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/rag_service.py"]
tags: ["server", "rag", "sqlite", "vector-search", "python"]
status: active
phase: 2
parent: ["scripts/server/config.py"]
children: []
related: ["scripts/index/update-index.py"]
task: []
summary: "scripts/server/rag_service.pyの静的解析ノート: SQLiteとOllama埋め込みモデルを利用したベクトル類似度検索（RAG）機能を提供する。"
---

# scripts/server/rag_service.py 解析ノート

## 1. 概要・目的
`scripts/server/rag_service.py` は、パーソナルナレッジベースにおけるRAG（Retrieval-Augmented Generation）の中核サービスモジュールです。
ユーザーの質問文をOllamaの埋め込みモデル（`nomic-embed-text`）でベクトル化し、SQLiteデータベース（`01-private/knowledge_index.db`）に保存されている既存ナレッジのベクトルとのコサイン類似度を計算して関連度の高いドキュメントを抽出します。

## 2. 主要関数・処理フロー
### 2.1 `get_query_embedding(text: str) -> list[float]`
- Ollamaの `/api/embeddings` エンドポイントに対し、質問文と埋め込みモデル名をPOSTリクエストし、数値ベクトルリストを取得します。エラー時はエラーメッセージを表示し空リストを返します。

### 2.2 `cosine_similarity(v1: list[float], v2: list[float]) -> float`
- 2つのベクトル間のコサイン類似度を計算します。
- ゼロ除算や次元数不一致の安全チェックを行い、内積と各ベクトルのノルムから類似度（0.0〜1.0）を算出します。

### 2.3 `search_relevant_knowledge(query: str, top_k: int = 3, target_categories: list[str] = None) -> list[dict]`
1. データベースファイルの存在確認を行い、存在しない場合は空リストを返します。
2. `get_query_embedding(query)` で質問文のベクトルを取得します。
3. SQLite（`DB_PATH`）に接続し、指定されたカテゴリ条件（フィルタ）がある場合は `WHERE category IN (...)` で絞り込んで `knowledge_index` テーブルからドキュメントを取得します。
4. 各ドキュメントの埋め込みJSON文字列をデコードし、質問ベクトルとのコサイン類似度スコアを計算します。
5. スコアの降順でソートし、上位 `top_k` 件の辞書リストを返します。

## 3. 依存関係
- 標準ライブラリ: `os`, `sqlite3`, `math`, `json`, `urllib.request`
- 内部モジュール: `scripts/server/config.py` (`DB_PATH`, `OLLAMA_ENDPOINT`, `EMBED_MODEL`)
- 連携インデクサ: `scripts/index/update-index.py`
