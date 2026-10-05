---
title: "scripts/server/knowledge_service.py (Note)"
category: "scripts/server"
type: "note"
target: "scripts/server/knowledge_service.py"
summary: "scripts/server/knowledge_service.py の詳細解析ノート"
---

# scripts/server/knowledge_service.py (Note)

## 1. 目的と役割
`knowledge_service.py` は、パーソナルナレッジベースの核心である「データ入力からナレッジへの昇華（Sublimation）」プロセスを自動化・管理するバックエンドサービスです。

## 2. 内部構造と主要処理
- **プロンプト管理 (`resolve_prompt_path`)**: `00-rules/prompts/` やスキルディレクトリからプロンプトや指示書を正確に特定・ロードする。
- **ファイル生成 (`generate_knowledge_files`)**: LLM等を活用し、生テキストやリソースからメタデータ付きのHead/Note構造ファイルを構築して `02-knowledge/` に配置。
- **自動昇華 (`auto_sublimate_rag_answer`)**: チャットやRAGでのやり取りから得られた知見を自動的に知識ベースへと取り込むパイプライン。

## 3. 依存関係
- 標準/外部ライブラリ: `os`, `re`, `json`, `sqlite3`, `pathlib`, `streamlit`
- 内部モジュール: `config`, `llm_client`
