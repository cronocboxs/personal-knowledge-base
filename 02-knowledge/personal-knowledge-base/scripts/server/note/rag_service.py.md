---
created: 2026-10-02
updated: 2026-10-02
source: ["scripts/server/rag_service.py"]
tags: ["RAG", "Python", "VectorSearch", "Embedding", "Ollama", "SQLite"]
status: draft
phase: 1
parent: []
children: []
related: ["config.py", "sqlite3", "Ollama API", "knowledge_index"]
task: []
summary: "RAGシステムの中核となるベクトル検索および類似度計算を提供するサービス層のロジック。Ollama APIを使用した埋め込み生成とSQLiteデータベースからの知識検索を実行する。"
---

---
# rag_service-py 解析ノート

## 1. 概要・目的
このモジュールは、RAG（Retrieval-Augmented Generation）システムにおいて、与えられたクエリ（質問文）に基づいて、構造化されたナレッジベース（SQLite DB）から最も関連性の高い情報を検索し、取り出す役割を担うコアサービスです。

単にキーワードマッチングを行うのではなく、クエリと知識ドキュメントの両方をベクトル化し、その間の**コサイン類似度**を計算することで、意味的な近さに基づいて情報を「検索」することが目的です。これにより、より高度で文脈を理解した知識の提供が可能になります。

## 2. 主要コンポーネント・関数

### 🚀 `get_query_embedding(text: str)`
* **役割**: 入力されたテキスト（クエリ）を、AIモデル（Ollama経由）を用いて高次元のベクトル（埋め込み）に変換します。
* **処理**: `OLLAMA_ENDPOINT`を指定されたエンドポイントにJSONペイロードを送り、ベクトル表現をリクエストします。
* **重要点**: この関数がダウンすると、すべての検索機能が停止するため、Ollamaの稼働状況確認が必須です。

### 📐 `cosine_similarity(v1: list[float], v2: list[float])`
* **役割**: 2つのベクトル間の角度の近さ（類似度）を計算します。値が1に近いほど類似していると判断されます。
* **処理**: 内積（Dot Product）を、それぞれのベクトルのノルム（大きさ）の積で割る標準的な計算式を採用しています。
* **重要点**: ベクトル検索の成否を決定する最も重要な数学的計算です。

### 🔍 `search_relevant_knowledge(query: str, top_k: int = 3, target_categories: list[str] = None)`
* **役割**: メインのエントリポイント。クエリをベクトル化し、データベース内の全ドキュメントと比較し、最も類似度の高い結果をリストとして返します。
* **処理**:
    1. **ベクトル生成**: まず、クエリを`get_query_embedding`でベクトル化します。
    2. **DB検索**: SQLiteデータベース（`knowledge_index`）に対し、指定された条件（`target_categories`）でドキュメント群をフェッチします。
    3. **類似度計算**: フェッチした各ドキュメントの埋め込みベクトルと、クエリのベクトルを用いて`cosine_similarity`を計算します。
    4. **ソート＆フィルタリング**: 計算したスコアに基づいて結果を降順にソートし、指定された`top_k`の件数だけを返します。

## 3. 処理フローと実装ポイント

### ⚙️ 全体処理フロー
1. **入力受付**: ユーザーからのクエリを受け取る。
2. **埋め込み生成**: クエリをOllama API経由でベクトルA（`query_vec`）に変換する。
3. **データ取得**: SQLite DBから関連するドキュメント群（各ドキュメントに対応するベクトルBの配列）を取得する。
4. **スコアリング**: ベクトルAと、取得した各ベクトルBを`cosine_similarity`で比較し、類似度スコアを算出する。
5. **結果出力**: スコアの高い順に上位K件のドキュメント情報（パス、タイトル、要約など）を返却する。

### ✨ 重要実装ポイント
* **ベクトル処理の分離**: クエリベクトル生成、類似度計算、DB操作の3要素が独立した関数に分かれているため、可読性が高く、デバッグや単位テストが容易です。
* **SQLiteの活用と制限**: 知識データの保存・管理にSQLiteを使用していますが、**本コードの仕組み上、類似度計算（ベクトルマッチング）はPythonメモリ上で実行されています**。もしドキュメント数が極めて膨大になる場合は、本処理をPgVectorなどのベクトルDBレイヤーに移行することが検討課題となります。
* **柔軟な検索範囲指定**: `target_categories`パラメータが存在することで、特定ドメイン（例: 「認証関連」「API仕様」など）に絞った検索実行が可能となっています。

---
**【メタデータ（YAML Frontmatter）】**

```yaml
---
created: 2026-10-02
updated: 2026-10-02
source: ["scripts/server/rag_service-py"]
tags: [code-analysis, RAG, sqlite, embedding, vector-search]
status: draft
phase: 1
parent: []
children: []
related: [knowledge_index]
task: []
summary: "RAGシステムにおける埋め込み検索と知識ベース照会を行うコアサービス。"
---
```
