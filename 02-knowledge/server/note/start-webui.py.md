---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/start-webui.py"]
tags: [server, webui, streamlit, python]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/knowledge_service.py", "scripts/server/rag_service.py", "scripts/server/llm_client.py"]
task: ["scripts/server/start-webui.py # start-webui.pyの静的解析"]
summary: "Streamlitを用いた個人用ナレッジベースのWebUIアプリケーション。ファイルエクスプローラー、一階層・二層ノート昇華、RAG質問検索機能を提供。"
---

# start-webui.py 解析ノート

## 概要
`scripts/server/start-webui.py` は、Streamlit フレームワークをベースにしたパーソナルナレッジベース用の WebUI アプリケーションです。ファイルの閲覧・編集、AIによる二層ナレッジ昇華（`04-resources` ➔ `02-knowledge`）、RAGを活用した質問応答（セマンティック検索 ＋ LLM回答生成 ＋ 自動ナレッジ化）を統合的に提供します。

## 主要なコンポーネントと機能

### 1. サイドバー設定
- **AIモデル設定**: Ollama (ローカルLLM) と Gemini (クラウドAPI) の切り替え、モデル選択（Ollamaモデルは動的取得）、APIキーの確認機能。
- **ファイルエクスプローラー**: `02-knowledge` および `04-resources` ディレクトリの階層構造をツリー状（再帰的エクスパンダー）に描画し、クリックによってファイルをフォームにロードする機能。

### 2. Tab 1: 状況・データ入力・編集 (`tab1`)
- **一次素材の保存**: 入力されたテキストを `04-resources/` 配下に保存。
- **ナレッジの新規登録・AI自動昇華**:
  - `04-resources` への保存と同時に、選択されたプロンプトテンプレート（指示書）を用いて LLM がメタデータと本文を生成。
  - `02-knowledge/<category>/head/` および `note/` へ二層出力。
  - インデックス更新スクリプト（`scripts/index/update-index.py`）を呼び出して SQLite ベクトルインデックスを同期。

### 3. Tab 2: ナレッジ検索・質問 (RAG) (`tab2`)
- **セマンティック検索**: 入力されたクエリをベクトル化し、SQLite インデックスからコサイン類似度上位の関連ナレッジを抽出。
- **回答生成**: 関連ナレッジをコンテキストとして LLM に渡し、回答を生成。
- **回答のナレッジ昇華**: AIからの回答をワンクリックで新しいナレッジノート（`02-knowledge`）として自動昇華・保存。

## 依存関係
- 標準ライブラリ: `os`, `re`, `datetime`, `subprocess`
- 外部ライブラリ: `streamlit`
- 内部モジュール: `config`, `rag_service`, `knowledge_service`, `llm_client`
