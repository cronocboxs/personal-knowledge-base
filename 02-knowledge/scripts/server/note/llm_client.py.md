---
title: "scripts/server/llm_client.py (Note)"
category: "scripts/server"
type: "note"
target: "scripts/server/llm_client.py"
summary: "scripts/server/llm_client.py の詳細解析ノート"
---

# scripts/server/llm_client.py (Note)

## 1. 目的と役割
`llm_client.py` は、アプリケーション内から各種LLM（Ollama, Gemini等）を統一的なインターフェースで呼び出すためのクライアント実装です。ネットワークの一時的なエラーに対する自動リトライ機能を備えています。

## 2. 内部構造と主要処理
- **リトライ機構**: 接続エラーやタイムアウト時に備え、指数バックオフや指定回数のリトライ (`max_retries`, `retry_delay`) を実装。
- **プロバイダー分岐**: 選択されたプロバイダー（Ollama / Gemini）に応じたHTTPリクエストボディの構築とAPIエンドポイントへの送信。
- **エラーハンドリング**: `urllib.error.URLError` などの例外をキャッチし、安全にエラーログを出力またはフォールバック。

## 3. 依存関係
- 標準ライブラリ: `json`, `time`, `urllib.request`, `urllib.error`
