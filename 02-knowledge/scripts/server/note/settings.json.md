---
title: "scripts/server/settings.json (Note)"
category: "scripts/server"
type: "note"
target: "scripts/server/settings.json"
summary: "scripts/server/settings.json の詳細解析ノート"
---

# scripts/server/settings.json (Note)

## 1. 目的と役割
`settings.json` は、`scripts/server/` 配下のアプリケーションやLLM呼び出しで使用する各種デフォルト設定（プロバイダー、モデル名、エンドポイント等）を一元管理するための設定ファイルです。

## 2. 構造とパラメータ
- **`default_provider`**: 使用するデフォルトのLLMバックエンド（例: `"Ollama (Local LLM)"`）。
- **`gemini`**: Gemini API 用の設定（`default_model`, `available_models`）。
- **`ollama`**: ローカルの Ollama 用設定（`default_model`, `endpoint`）。

## 3. 利用箇所
`config.py` を経由してロードされ、WebUIやLLMクライアント、RAGサービスでの初期設定値として利用されます。
