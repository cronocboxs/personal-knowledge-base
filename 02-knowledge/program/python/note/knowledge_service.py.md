---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/knowledge_service.py"]
tags: [python, server, knowledge-service]
status: active
phase: 3
parent: []
children: []
related: ["scripts/server/knowledge_service.py", "scripts/server/config.py", "scripts/server/llm_client.py"]
task: ["scripts/server/knowledge_service.py # ナレッジ生成・管理サービスモジュール"]
summary: "scripts/server/knowledge_service.py の静的解析。プロンプトパス解決、ルール・既存ノートコンテキスト読込、LLMを用いた二層ナレッジ（head/note）自動生成およびRAG回答昇華機能を提供。"
---

# knowledge_service.py 解析ノート

## 1. 概要
`scripts/server/knowledge_service.py` は、パーソナルナレッジベースにおけるナレッジの自動生成、プロンプト解決、規約読み込み、およびSQLiteインデックス連携を担う中核サービスモジュールです。

## 2. 主要関数・処理フロー

- **`resolve_prompt_path(prompt_input: str) -> str`**
  - 入力されたプロンプト名やパスを、`00-rules/prompts/` や `.agents/skills/` などの実在パスに解決する。
- **`get_available_prompts() -> list[str]`**
  - `00-rules/prompts/` 内の利用可能な `.md` プロンプトファイル一覧を取得する。
- **`load_rule_docs() -> str`**
  - `AGENTS.md`, `formatting.md`, `workflow.md`, `agent-behavior.md` などの主要規約を読み込み、LLMへのコンテキストとして連結する。
- **`get_existing_notes_context(category_filter: str) -> str`**
  - SQLiteデータベース（`knowledge_index.db`）から既存のナレッジ一覧を取得し、リレーション抽出用のコンテキストを提供する。
- **`clean_and_parse_json(json_str: str) -> dict`**
  - LLMが生成した不完全なJSON文字列を正規表現等でエスケープ補正しパースする。
- **`generate_knowledge_files(...)`**
  - 2パス方式（Pass 1: JSONによるメタデータ・カテゴリ・サマリ抽出、Pass 2: 指示書に基づく Markdown 本文解析生成）を実行し、二層構造（`head/` および `note/`）のナレッジを構築する。
- **`auto_sublimate_rag_answer(...)`**
  - RAGの対話や回答内容から自動でナレッジノート（タイトル・カテゴリ・メタデータ・本文）を構築・昇華する。

## 3. 依存関係
- 標準ライブラリ: `os`, `re`, `json`, `sqlite3`, `pathlib`
- 外部ライブラリ: `streamlit`
- 内部モジュール: `config`, `llm_client`
