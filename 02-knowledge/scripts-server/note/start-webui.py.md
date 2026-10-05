---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/start-webui.py"]
tags: ["scripts", "server", "webui", "streamlit"]
status: active
phase: 2
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/rag_service.py", "scripts/server/knowledge_service.py", "scripts/server/llm_client.py"]
task: []
summary: "scripts/server/start-webui.py の静的解析ノート"
---

# `scripts/server/start-webui.py` 解析ノート

## 概要
`scripts/server/start-webui.py` は、Streamlit を用いたパーソナルナレッジベースの統合 WebUI アプリケーションのエントリーポイントです。
データ保存、AI自動昇華、ファイルエクスプローラー、RAG検索・質問応答機能を提供します。

## 主な機能と構成
1. **サイドバー（設定とエクスプローラー）**:
   - LLM プロバイダ（Ollama / Gemini）の切り替えとモデル選択。
   - `02-knowledge/` および `04-resources/` のツリー構造表示とファイル読み込み。
2. **タブ1: 解析対象データの配置 & ナレッジ昇華・編集**:
   - 一次素材としての保存 (`04-resources/`)。
   - ナレッジの新規登録および AI による自動昇華 (`02-knowledge/` の `head/` と `note/` への二層出力 ＋ SQLite インデックス更新)。
3. **タブ2: ナレッジ検索・質問 (RAG)**:
   - ユーザーからの質問に対して関連ナレッジをベクトル検索（RAG）。
   - LLM による回答生成と、その回答のナレッジ化（自動昇華）。
