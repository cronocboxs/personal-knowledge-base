---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/rag_service.py"]
tags: [server, rag, sqlite, ollama, python]
status: active
phase: 3
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/knowledge_service.py", "scripts/server/start-webui.py"]
task: ["scripts/server/rag_service.py # scripts/server/rag_service.pyの静的解析・ナレッジ生成"]
summary: "scripts/server/rag_service.py は Ollama API を用いたベクトル化処理と、SQLite データベース（knowledge_index.db）を用いたコサイン類似度による高精度 RAG 検索機能を提供します。"
---

# rag_service.py - RAG (Retrieval-Augmented Generation) 検索サービスモジュール

## 1. 概要
`scripts/server/rag_service.py` は、ユーザーからの検索クエリを Ollama (`nomic-embed-text`) でベクトル化し、SQLite インデックスデータベース（`knowledge_index.db`）に蓄積されたナレッジとのコサイン類似度計算を行って関連度の高いドキュメントを抽出する RAG 検索のコアサービスです。

## 2. 主要な関数

### `get_query_embedding(text: str) -> list[float]`
- **目的**: 入力されたテキスト（クエリ）を Ollama 埋め込みエンドポイント（`/api/embeddings`）に送信し、数値ベクトル（`list[float]`）を取得する。
- **エラーハンドリング**: 失敗時はエラーメッセージを表示し空リストを返す。

### `cosine_similarity(v1: list[float], v2: list[float]) -> float`
- **目的**: 2つのベクトル間のコサイン類似度を計算する。
- **計算方法**: ドット積をそれぞれのベクトルのノルムの積で割った値を算出。ゼロ除算や長さ不一致時は `0.0` を返す。

### `search_relevant_knowledge(query: str, top_k: int = 3, target_categories: list[str] = None) -> list[dict]`
- **目的**: クエリに合致する関連ナレッジを SQLite から検索・スコアリングし、スコア降順で上位 `top_k` 件を返す。
- **処理フロー**:
  1. データベースファイルの存在確認。
  2. `get_query_embedding` でクエリのベクトルを取得。
  3. SQLite に接続し、カテゴリフィルタに応じてクエリ実行。
  4. 取得した各レコードの保存済みベクトルとクエリベクトルのコサイン類似度を計算。
  5. スコア順にソートし上位件数を抽出。

## 3. 依存関係
- 設定モジュール: `config.py`（`DB_PATH`, `OLLAMA_ENDPOINT`, `EMBED_MODEL`）
- 標準ライブラリ: `os`, `sqlite3`, `math`, `json`, `urllib.request`
- 連携先: `start-webui.py`, `knowledge_service.py`
