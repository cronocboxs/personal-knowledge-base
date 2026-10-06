---
created: 2026-10-06
updated: 2026-10-06
source: ["04-resources/scripts/server/start-webui.py"]
tags: [server, webui, streamlit, dashboard, python]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/rag_service.py", "scripts/server/knowledge_service.py", "scripts/server/llm_client.py"]
task: ["scripts/server/start-webui.py # Streamlit WebUIダッシュボードメインスクリプト"]
summary: "scripts/server/start-webui.py は、パーソナルナレッジベースの統合ダッシュボードを提供する Streamlit アプリケーションであり、ファイルエクスプローラー、一次データ保存、AI自動昇華機能、およびベクトル検索を活用したRAG質問応答機能を提供する。"
---

# start-webui.py 解析ノート

## 1. 概要
`scripts/server/start-webui.py` は、パーソナルナレッジベースの操作・検索・管理を行うための Streamlit 製 WebUI アプリケーションのエントリーポイントです。

## 2. 主要機能・タブ構成
- **サイドバー (AIモデル設定 & エクスプローラー)**:
  - LLM プロバイダーの切り替え（Ollama ローカル LLM または Gemini クラウド API）およびモデルの動的選択。
  - `02-knowledge/` および `04-resources/` 配下のファイル構造をツリー状に表示し、ワンクリックでフォームへの読み込み・編集をサポート。
- **タブ 1 (状況・データ入力・編集)**:
  - 一次素材の保存（`04-resources/`）。
  - AI による自動解析昇華（指定プロンプトを用いた `head`/`note` の二層生成と SQLite インデックス更新）。
- **タブ 2 (ナレッジ検索・質問 - RAG)**:
  - `rag_service.py` を用いたベクトル類似度検索による高精度 RAG 検索。
  - AI による回答生成と、その回答を新しいナレッジノートとして自動昇華・保存する機能。
