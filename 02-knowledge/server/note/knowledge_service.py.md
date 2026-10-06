---
created: 2026-10-06
updated: 2026-10-06
source: ["04-resources/scripts/server/knowledge_service.py"]
tags: [server, knowledge, llm, prompt, python]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/llm_client.py"]
task: ["scripts/server/knowledge_service.py # ナレッジ生成・管理サービスモジュール"]
summary: "scripts/server/knowledge_service.py は、LLMを活用したナレッジファイルの二層出力(head/note)生成、プロンプトパス解決、既存規約・ノートのコンテキスト統合、およびJSONレスポンスの頑健なパース機能を提供する中核サービスモジュールである。"
---

# knowledge_service.py 解析ノート

## 1. 概要
`scripts/server/knowledge_service.py` は、パーソナルナレッジベース内における LLM を用いたテキスト/コードの自動昇華・ナレッジファイル生成を行うサービスモジュールです。

## 2. 主要関数
### `resolve_prompt_path(prompt_input: str) -> str`
- プロンプトの指定名やファイルパスを、`00-rules/prompts/` や `.agents/skills/` などの実在するファイルパスへ柔軟に解決・変換します。

### `get_available_prompts() -> list[str]`
- `00-rules/prompts/` 配下にある Markdown プロンプトファイル一覧を取得します。

### `load_rule_docs() -> str`
- リポジトリの基本規約ファイル（`AGENTS.md`, `formatting.md`, `workflow.md`, `agent-behavior.md`）のコンテンツを読み込み、LLM のシステムコンテキスト用に結合します。

### `get_existing_notes_context(category_filter: str = None) -> str`
- SQLite ナレッジインデックス DB から既存ノートのタイトル・パス・概要を取得し、LLM がリレーション（関連ノート）を把握するためのコンテキスト文字列を生成します。

### `clean_and_parse_json(json_str: str) -> dict`
- LLM が出力した不安定な JSON 文字列に対し、エスケープ漏れや構文エラーの自動補正（`json.loads` のフォールバック）を行い安全にパースします。

### `generate_knowledge_files(...) -> dict`
- **PASS 1**: カテゴリの自動推察と Frontmatter メタデータ（`summary`, `tags`, `parent`, `children`, `related` 等）を LLM で JSON 抽出。
- **PASS 2**: 選択されたプロンプトテンプレートと規約に基づいて、詳細な解析 Markdown 本文を生成。
- 最終的に `head` 用 Frontmatter と `note` 用フルコンテンツを辞書として返却します。

### `auto_sublimate_rag_answer(...) -> dict`
- RAG の質疑応答結果を基に、新規ナレッジノートの Frontmatter と本文（質問・回答内容）を自動構成して返却します。
