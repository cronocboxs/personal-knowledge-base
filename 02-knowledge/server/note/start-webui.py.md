---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/start-webui.py"]
tags: [server, webui, streamlit, rag, knowledge-management, python]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/rag_service.py", "scripts/server/knowledge_service.py", "scripts/server/llm_client.py", "scripts/start-webui.md"]
task: ["scripts/server/start-webui.py # Streamlit WebUIサーバー起動スクリプトの静的解析"]
summary: "scripts/server/start-webui.py は Streamlit を用いたパーソナルナレッジベース統合 WebUI であり、ファイルエクスプローラー、AIモデル設定、一次データ保存・ナレッジ昇華フォーム、および RAG 検索・Q&A機能を提供します。"
---

# `scripts/server/start-webui.py` 解析ノート

## 1. 概要
`scripts/server/start-webui.py` は、パーソナルナレッジベースのフロントエンド・中核コントロールセンターである Streamlit WebUI アプリケーションです。ファイルの閲覧・編集、AIモデル（Ollama / Gemini）の切り替え、一次素材の保存とAIによるナレッジ昇華、およびローカルRAG検索を通じたQ&Aと自動昇華の全機能を統合しています。

## 2. 主要な機能とコンポーネント

### 2.1 サイドバー設定 & ファイルエクスプローラー
- **AIモデル設定**: Ollama（ローカルLLM）または Gemini（クラウドAPI）の選択、モデル名・エンドポイントの指定、APIキーの検証状態の表示。
- **エクスプローラーツリー**: `02-knowledge/` および `04-resources/` 配下のファイル構造を再帰的に展開し、クリックによってファイルをフォームに読み込んで編集可能にする機能。

### 2.2 Tab 1: 状況・データ入力・編集（一次保存 & ナレッジ昇華）
- **一次素材の保存**: `04-resources/` 配下へMarkdownやログを保存。
- **ナレッジ自動昇華**: 指定されたプロンプトテンプレート（指示書）とLLMを用いて、自動的にカテゴリ分類・メタデータ抽出・本文生成を行い、`head/` と `note/` の二層構造で保存。その後、インデックス更新スクリプトを呼び出してベクトルDBを同期。

### 2.3 Tab 2: ナレッジ検索・質問（RAG & 自動昇華）
- **RAG パイプライン**: ユーザーの質問に対するクエリベクトルを生成し、SQLite インデックスからコサイン類似度に基づいて関連ナレッジ（`top_k` 件）を検索・抽出。
- **回答生成**: 参照ナレッジを文脈コンテキストとしてLLMに渡し、正確な回答を生成。
- **回答のナレッジ昇華**: AIからの回答をそのまま新規ナレッジノートとして自動昇華・保存する機能。

## 3. 依存関係
- 設定・サービス: `config.py`, `rag_service.py`, `knowledge_service.py`, `llm_client.py`
- ドキュメント: `start-webui.md`
- 標準ライブラリ: `os`, `re`, `datetime`, `subprocess`
- 外部ライブラリ: `streamlit`
