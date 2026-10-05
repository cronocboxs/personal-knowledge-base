---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/knowledge_service.py"]
tags: [server, knowledge-service, sqlite, python, markdown]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/llm_client.py", "scripts/server/rag_service.py", "scripts/server/start-webui.py"]
task: ["scripts/server/knowledge_service.py # ナレッジ生成・管理サービスモジュールの静的解析"]
summary: "scripts/server/knowledge_service.py は指示書テンプレートや規約ドキュメントを読み込み、LLMと連携して二層構造（head/note）のナレッジファイルおよびメタデータ（JSON Frontmatter）を自動生成するサービスモジュールです。"
---

# `scripts/server/knowledge_service.py` 解析ノート

## 1. 概要
`scripts/server/knowledge_service.py` は、パーソナルナレッジベースにおけるナレッジの生成・管理を行うコアサービスモジュールです。規約の読み込み、指示書プロンプトの解決、LLM（`call_llm`）を利用した2パス生成（メタデータ抽出と本文生成）、およびRAG回答の自動昇華機能を統合しています。

## 2. 主要な関数

### `resolve_prompt_path(prompt_input: str) -> str`
- **目的**: プロンプトや指示書名の入力を、`00-rules/prompts/` や `.agents/skills/` 内の絶対パスに解決する。

### `get_available_prompts() -> list[str]`
- **目的**: `00-rules/prompts/` 配下にある Markdown プロンプト一覧を取得する。

### `load_rule_docs() -> str`
- **目的**: リポジトリの各種規約（`AGENTS.md`, `formatting.md`, `workflow.md`, `agent-behavior.md`）を読み込んで結合し、LLMにコンテキストとして提供する。

### `get_existing_notes_context(category_filter: str = None) -> str`
- **目的**: SQLite インデックスから既存ノートの一覧や概要を取得し、関連ノートや親子のリレーション抽出用コンテキストを作成する。

### `clean_and_parse_json(json_str: str) -> dict`
- **目的**: LLMが生成した不正なエスケープを含むJSON文字列を頑健にパースする。

### `generate_knowledge_files(...) -> dict`
- **目的**: 2パス処理によりナレッジファイルを生成する。
  - **PASS 1**: 規約・既存ノートを踏まえてカテゴリやタグ、概要、リレーション（`parent`, `children`, `related`）をJSONで抽出。
  - **PASS 2**: 選択されたプロンプトテンプレートとテキストを基に構造化されたMarkdown本文を生成。
  - **戻り値**: 判定カテゴリ、`head_content` (Frontmatter)、`note_content` (Frontmatter + 本文) を辞書で返す。

### `auto_sublimate_rag_answer(...) -> dict`
- **目的**: RAGを用いたQ&Aのやり取りを自動でナレッジノート（Frontmatter付き）に昇華するためのデータを生成する。

## 3. 依存関係
- 設定・LLM: `config.py`, `llm_client.py`
- 標準ライブラリ: `os`, `re`, `json`, `sqlite3`, `pathlib`
- 外部ライブラリ: `streamlit`
- 関連ファイル: `rag_service.py`, `start-webui.py`
