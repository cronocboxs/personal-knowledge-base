---
title: "scripts/server/start-webui.py (Head)"
category: "scripts/server"
type: "head"
target: "scripts/server/start-webui.py"
summary: "Streamlitを用いたデータ保存・RAG質問回答WebUIアプリケーション"
---

# scripts/server/start-webui.py (Head)

## 概要
Streamlitフレームワークをベースにした、ナレッジの登録・管理およびRAGを活用したAIチャット／質問回答インターフェースを提供するWebUIアプリケーションのエントリポイントです。

## 主要機能
- ナレッジの新規登録および自動昇華パイプラインの実行
- RAG検索を活用したインタラクティブなLLMチャット
- 各種プロバイダー（Ollama / Gemini）の切り替え設定
