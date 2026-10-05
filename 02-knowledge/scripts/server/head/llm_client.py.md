---
title: "scripts/server/llm_client.py (Head)"
category: "scripts/server"
type: "head"
target: "scripts/server/llm_client.py"
summary: "OllamaおよびGemini API向けの汎用LLMクライアントモジュール"
---

# scripts/server/llm_client.py (Head)

## 概要
Ollama（ローカルLLM）およびGoogle Gemini APIなどの複数プロバイダーに対して、リトライ処理やエラーハンドリングを内包した共通のテキスト生成・LLM呼び出し関数を提供するモジュールです。

## 主要関数
- `call_llm(...)`: 指定されたプロバイダーとモデルに応じてLLMへプロンプトを送信し、テキスト出力を取得する共通クライアント
