---
title: "scripts/server/settings.json (Head)"
category: "scripts/server"
type: "head"
target: "scripts/server/settings.json"
summary: "サーバー・LLM機能用の設定定義ファイル"
---

# scripts/server/settings.json (Head)

## 概要
サーバーサイドスクリプトおよびLLMクライアント・RAG機能で利用されるデフォルトプロバイダー、Geminiモデル、Ollamaモデル・エンドポイントなどの設定を保持するJSONファイルです。

## 主要設定項目
- `default_provider`: デフォルトのLLMプロバイダー
- `gemini`: Google Gemini のモデル設定
- `ollama`: Ollama (ローカルLLM) のモデルおよびエンドポイント設定
