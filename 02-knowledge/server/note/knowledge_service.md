---
created: 2026-10-06
updated: 2026-10-06
source: ["04-resources/scripts/server/knowledge_service.py"]
tags: [server, knowledge, service, python]
status: active
phase: 3
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/llm_client.py"]
task: ["scripts/server/knowledge_service.py"]
summary: "scripts/server/knowledge_service.pyの静的解析ノート（本文付き）"
---

# `scripts/server/knowledge_service.py` 解析ノート

## 1. 概要・責務
`scripts/server/knowledge_service.py` は、パーソナルナレッジベースにおけるナレッジ生成・昇華処理を担うサービスモジュールです。プロンプトや規約ドキュメントの解決・読み込み、既存ナレッジコンテキストの SQLite からの取得、LLM出力のJSONパース補正、二層構造（`head/` および `note/`）のメタデータ・本文生成処理を提供します。

## 2. 主要な関数・処理フロー
### `resolve_prompt_path(prompt_input: str) -> str`
- 指定されたプロンプト名やパスを、`00-rules/prompts/` や `.agents/skills/` などの実際の絶対パスへと解決します。

### `get_available_prompts() -> list[str]`
- `00-rules/prompts/` 配下に存在する `.md` ファイルの一覧を取得して返します。

### `load_rule_docs() -> str`
- リポジトリ直下の `AGENTS.md` および `00-rules/` 配下の主要規約ファイル群を読み込み、コンテキストとして結合します。

### `get_existing_notes_context(category_filter: str = None) -> str`
- SQLite データベース (`01-private/knowledge_index.db`) から既存のナレッジ一覧（タイトル、パス、概要）を取得し、文字列コンテキストとしてまとめます。

### `clean_and_parse_json(json_str: str) -> dict`
- LLMが生成した不正なエスケープ文字を含む JSON 文字列をクレンジングし、安全にパースします。

### `generate_knowledge_files(...) -> dict`
1. 規約と既存ノートのコンテキストをロード。
2. **PASS 1**: LLMを用いてカテゴリ・メタデータ（tags, summary, related等）を JSON 形式で抽出。
3. **PASS 2**: 選択された指示書テンプレートに基づいて、本文の解説 Markdown を生成。
4. 二層構造（head と note）のコンテンツを辞書形式で返却します。

### `auto_sublimate_rag_answer(...) -> dict`
- RAGのQ&Aセッションの結果から、自動的にナレッジノートのタイトル、カテゴリ、メタデータおよびノート本文を生成・構造化します。
