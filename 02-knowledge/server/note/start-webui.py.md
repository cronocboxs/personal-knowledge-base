---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/start-webui.py"]
tags: [server, webui, streamlit, python, ui]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/rag_service.py", "scripts/server/knowledge_service.py", "scripts/server/llm_client.py"]
task: ["scripts/server/start-webui.py # Streamlit WebUIアプリケーションスクリプトの静的解析"]
summary: "scripts/server/start-webui.py は、Streamlitを用いたパーソナルナレッジベース用のインタラクティブWebUIであり、ナレッジ登録・RAG質問応答・自動昇華機能を提供します。"
---

# `scripts/server/start-webui.py` 解析ノート

## 1. 概要
`scripts/server/start-webui.py` は、Streamlitフレームワークをベースにしたパーソナルナレッジベースの統合WebUIです。ユーザーはブラウザ経由で、ナレッジの新規登録（一次データ保存＋AI自動昇華）、RAGを用いた質問応答、プロンプト指示書の管理、インデックスの再構築などを直感的に操作できます。

## 2. 主要機能・ヘルパー
- **`get_knowledge_categories() -> list[str]`**:
  - `02-knowledge/` 配下のディレクトリからカテゴリ一覧を取得する（`head`/`note` を除く）。
- **`get_ollama_models() -> list[str]`**:
  - `ollama list` コマンドを実行し、利用可能なOllamaローカルモデルの一覧を取得する。
- **UIレイアウトとサイドバー設定**:
  - プロバイダー選択（Ollama / Gemini）、モデル選択、エンドポイント設定、各種管理タブ（RAG質問、ナレッジ登録、設定確認など）を構成。
