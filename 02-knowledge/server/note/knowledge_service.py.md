---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/knowledge_service.py"]
tags: [server, knowledge, llm, sublimation, python]
status: active
phase: 3
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/llm_client.py", "scripts/server/rag_service.py"]
task: ["scripts/server/knowledge_service.py # scripts/server/knowledge_service.pyの静的解析・ナレッジ生成"]
summary: "scripts/server/knowledge_service.py は、プロンプトテンプレートの解決、プロジェクト規約および既存ノートのコンテキスト統合、およびLLMを用いた二層ナレッジ（head / note）の自動生成とRAG回答の昇華機能を提供します。"
---

# knowledge_service.py - ナレッジ昇華サービスモジュール

## 1. 概要
`scripts/server/knowledge_service.py` は、パーソナルナレッジベースにおける「二層ナレッジ生成（head/note）」の中核を担うサービスモジュールです。指示書テンプレートの解決、プロジェクト規約（`AGENTS.md`や`00-rules/`）および既存ノート情報のコンテキスト統合、LLMを用いたメタデータ（YAML Frontmatter）と本文の2パス生成ロジック、およびRAG回答の自動昇華機能を提供します。

## 2. 主要な関数・処理ロジック

### `resolve_prompt_path(prompt_input: str) -> str`
- **目的**: 指定されたプロンプト名やパスを `00-rules/prompts/` や `.agents/skills/` から検索し、実際の絶対パスに解決する。

### `load_rule_docs() -> str`
- **目的**: リポジトリ直下の `AGENTS.md` や `00-rules/` 配下の規約ファイルを読み込み、LLMへのコンテキストとして統合する。

### `get_existing_notes_context(category_filter: str = None) -> str`
- **目的**: SQLite インデックス（`knowledge_index.db`）から既存ノートのタイトル、パス、概要を読み込み、リレーション構築用のコンテキストを作成する。

### `clean_and_parse_json(json_str: str) -> dict`
- **目的**: LLMが生成した JSON 文字列のエスケープ文字や不正なフォーマットを正規表現で補正し、安全にパースする。

### `generate_knowledge_files(...) -> dict`
- **目的**: 入力データと指示書テンプレートを元に、2パス（メタデータ抽出と本文生成）で二層ナレッジファイルを生成する。
- **Pass 1**: カテゴリ、サマリー、タグ、リレーション等の YAML Frontmatter 属性を JSON で抽出。
- **Pass 2**: 選択された指示書テンプレートに沿った解析本文 Markdown を生成。

### `auto_sublimate_rag_answer(...) -> dict`
- **目的**: RAG 検索・対話の回答結果から、メタデータを抽出し新たなナレッジドキュメントとして昇華・フォーマットする。

## 3. 依存関係
- 設定: `config.py`
- LLMクライアント: `llm_client.py`
- 標準ライブラリ: `os`, `re`, `json`, `sqlite3`, `pathlib`
- 連携先: `start-webui.py`
