---
title: "scripts/server/knowledge_service.py (Head)"
category: "scripts/server"
type: "head"
target: "scripts/server/knowledge_service.py"
summary: "ナレッジファイルの生成・自動昇華・プロンプト解決サービス"
---

# scripts/server/knowledge_service.py (Head)

## 概要
アップロードされた生データから `02-knowledge/` 配下に二層構造のナレッジドキュメント（Head/Note）を自動生成するパイプラインや、プロンプトパスの解決処理を提供するサービスモジュールです。

## 主要機能
- `resolve_prompt_path()`: 指定された指示書・プロンプトのパス解決
- `generate_knowledge_files()`: 生データから二層ナレッジファイルを生成
- `auto_sublimate_rag_answer()`: RAG結果に基づく自動昇華処理
