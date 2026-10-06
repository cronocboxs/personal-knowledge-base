---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/start-webui.py"]
tags: [python, server, streamlit, webui]
status: active
phase: 3
parent: []
children: []
related: ["scripts/server/start-webui.py", "scripts/server/config.py", "scripts/server/knowledge_service.py", "scripts/server/rag_service.py", "scripts/server/llm_client.py"]
task: ["scripts/server/start-webui.py # Streamlit WebUI ダッシュボードアプリケーション"]
summary: "scripts/server/start-webui.py の静的解析。Streamlit を用いた対話型 WebUI ダッシュボード。エクスプローラー風ツリー表示、一次データ保存、LLMによる二層ナレッジ自動昇華、およびRAG検索機能を提供。"
---

# start-webui.py 解析ノート

## 1. 概要
`scripts/server/start-webui.py` は、パーソナルナレッジベースの操作インターフェースを提供する Streamlit ベースの WebUI アプリケーションです。エクスプローラー風のツリーからファイルを閲覧・編集できるほか、LLMを用いた二層ナレッジ昇華機能、RAG検索機能、およびSQLiteインデックスの自動更新機能を統合しています。

## 2. 主要機能・処理フロー

- **サイドバー設定・エクスプローラー**
  - **AIモデル設定**: Ollama (Local LLM) または Gemini (Cloud API) の切り替え、モデル選択、APIキー確認。
  - **ファイルエクスプローラー**: `02-knowledge/` および `04-resources/` 配下のディレクトリ・ファイルを再帰的にツリー表示。ボタン押下でフォームに読み込み編集可能。
- **Tab 1: 状況・データ入力・編集 (一次保存 ＆ ナレッジ昇華)**
  - 一次素材（`04-resources/`）の保存。
  - ナレッジの新規登録・AI自動昇華（指定プロンプトに基づく二層 `head/` & `note/` 生成、およびインデックス更新）。
- **Tab 2: ナレッジ検索・質問 (RAG)**
  - ユーザーの質問に対するベクトル類似度検索（`rag_service`）とLLMによる回答生成。
  - 生成された回答をワンクリックでナレッジベースへ自動昇華・保存する機能。

## 3. 依存関係
- 標準ライブラリ: `os`, `re`, `datetime`, `subprocess`
- 外部ライブラリ: `streamlit`
- 内部モジュール: `config`, `rag_service`, `knowledge_service`, `llm_client`
