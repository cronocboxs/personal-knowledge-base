---
title: "scripts/server/start-webui.py (Note)"
category: "scripts/server"
type: "note"
target: "scripts/server/start-webui.py"
summary: "scripts/server/start-webui.py の詳細解析ノート"
---

# scripts/server/start-webui.py (Note)

## 1. 目的と役割
`start-webui.py` は、ユーザーがナレッジベースに対して手軽に資料やテキストを追加し、AI（RAG）を通じてそれらの内容に基づいた質問・回答を行えるようにするためのStreamlitアプリです。

## 2. 内部構造と主要処理
- **UI構築**: Streamlitによるサイドバー設定、タブ切り替え（データ登録、チャット、管理等）。
- **データ連携**: `knowledge_service.py` を呼び出してアップロードされたデータの一次保存および自動昇華処理を実行。
- **RAG検索**: `rag_service.py` を用いて、チャットの質問に関連するドキュメントを検索し、LLMにコンテキストとして提供。
- **LLM呼び出し**: `llm_client.py` を通じて選択されたモデル（OllamaまたはGemini）で回答を生成。

## 3. 依存関係
- 外部ライブラリ: `streamlit`, `os`, `re`, `datetime`, `subprocess`
- 内部モジュール: `config`, `rag_service`, `knowledge_service`, `llm_client`
