---
created: 2026-10-01
updated: 2026-10-01
source: ["scripts/server/rag_service.py"]
tags: ["rag", "python", "sqlite", "embedding", "retrieval", "system-architecture"]
status: draft
phase: 1
parent: []
children: []
related: []
task: []
summary: "本サービスは、RAG（Retrieval-Augmented Generation）のためのコアヘルパー関数群を提供する。Ollamaを用いたベクトル埋め込み生成と、SQLiteデータベースに対するコサイン類似度検索を実行することで、知識検索層を実装する。"
---

# rag_service-py 解析ノート

## 1. システム概要・目的
本スクリプト（`rag_service-py.py`）は、**RAG (Retrieval-Augmented Generation)** の「検索 (Retrieval)」フェーズを担うコアなユーティリティサービスです。

目的は、与えられた自然言語クエリ（質問）に対し、事前に構造化され、ベクトル埋め込みが格納された大規模な知識データベース（SQLite）から、最も関連性の高い知識の断片（コンテキスト）を効率的に検索し、取得することです。

このサービスは、単なるキーワード検索ではなく、「意味」に基づいた類似度検索（セマンティック検索）を可能にすることで、LLM（大規模言語モデル）の回答精度を向上させるために設計されています。

## 2. 主要コンポーネント・関数

### 🔹 `get_query_embedding(text: str)`
**役割**: テキストクエリを数学的なベクトル表現（埋め込みベクトル）に変換します。
**実装ポイント**:
1. 外部サービスであるLLMの埋め込みAPIエンドポイント（`OLLAMA_ENDPOINT`）を利用します。
2. `urllib.request` を使用して、JSON形式のペイロード（プロンプトと使用モデル名）をPOSTし、埋め込みベクトルをJSONとして受信しています。
3. 処理が成功しなかった場合（例：Ollamaが稼働していない場合）、エラーを記録し、空のリストを返します。

### 🔹 `cosine_similarity(v1: list[float], v2: list[float])`
**役割**: 2つの埋め込みベクトルがどれだけ同じ方向を指しているか（つまり、どれだけ類似しているか）を測定します。
**数学的原理**: コサイン類似度を計算します。これは、内積をそれぞれのベクトルのL2ノルム（長さ）で割ることで算出されます。
**重要性**: ベクトル埋め込み空間において、この値が大きいほど、入力された二つのクエリ・ドキュメント間の「意味的な近さ」が高いことを示します。

### 🔹 `search_relevant_knowledge(query: str, top_k: int = 3, target_categories: list[str] = None)`
**役割**: 検索のメインロジックを担う関数です。
**処理フロー**:
1. **データベース接続**: 最初にSQLiteデータベース（`DB_PATH`）に接続します。
2. **クエリベクトル化**: 入力された`query`を`get_query_embedding`に通し、検索に使用するクエリベクトル（`query_vec`）を取得します。
3. **SQL検索の実行**:
    * `target_categories`が指定されている場合、`WHERE category IN (...)`句を使用して、検索範囲を絞り込んだSQLを実行します。
    * 指定がなければ、すべての知識ノードを対象に検索します。
4. **類似度計算（コア処理）**:
    * データベースから取得した各知識ノードの埋め込み文字列（`emb_str`）をJSONとしてデコードし、`cosine_similarity`関数を用いて`query_vec`と比較します。
    * 計算結果（`score`）を各知識ノードのデータに追加します。
5. **結果の集約とソート**: 取得した全結果を、計算された`score`（類似度）が高い順（`reverse=True`）にソートします。
6. **出力**: トップK件の結果（`rel_path`, `title`, `summary`, `score`など）を辞書のリストとして返します。

## 3. 処理フローと実装ポイント

**構造化のポイント**:
この設計の最大の特徴は、ベクトル検索の計算処理（`cosine_similarity`）をPythonコード側で行っている点です。

**技術的なボトルネックと改善点**:
1. **データベースの制限**: 知識の参照と類似度計算のメインループがPythonコード（`for` ループ）内に存在します。データ量が非常に大きくなる場合、このPython側の処理がボトルネックとなる可能性があります。理想的には、SQLiteではなく、PineconeやFaissのような専用のベクトルデータベースを利用し、DB側で類似度計算（ベクトル検索）を完結させるべきです。
2. **埋め込みAPIの依存性**: 埋め込みベクトル生成が外部API（Ollama）に完全に依存しています。このAPIの可用性やレイテンシが、サービスのパフォーマンスに直結します。

**総合的な処理フロー**:
クエリ入力 $\rightarrow$ **Embedding生成** (Ollama API) $\rightarrow$ **データベースからの候補取得** (SQLite WHERE句) $\rightarrow$ **類似度計算** (Python $V_{query}$ vs $V_{doc}$) $\rightarrow$ **ソート・フィルタリング** $\rightarrow$ 検索結果出力。
