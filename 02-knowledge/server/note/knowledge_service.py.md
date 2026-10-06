---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/knowledge_service.py"]
tags: [server, knowledge-service, python]
status: active
phase: 3
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/llm_client.py"]
task: ["scripts/server/knowledge_service.py # 知識生成・プロンプト解決・メタデータ抽出サービスモジュールの静的解析ノート"]
summary: "プロンプトテンプレートの解決、ルール・既存ノートコンテキストの読み込み、LLMを用いた二層ナレッジ（YAML Frontmatter＋本文）の自動生成・カテゴリ判定を行うサービスモジュール。"
---

# knowledge_service.py 解析ノート

## 1. 概要
`scripts/server/knowledge_service.py` は、サーバーサイドでLLMやSQLite、プロジェクト規約を組み合わせて、外部資料やコード群からパーソナルナレッジ（二層ノート形式: `head/` および `note/`）を自動生成・推論するコアサービスモジュールです。

## 2. 主要関数

### `resolve_prompt_path(prompt_input: str) -> str`
- **目的**: 指示書指定（ファイル名、パス、スキル名）を適切な絶対パスへ解決する。
- **検索先**: `00-rules/prompts/`, `.agents/skills/`, `00-rules/skills/`。

### `get_available_prompts() -> list[str]`
- **目的**: `00-rules/prompts/` 内の `.md` ファイル一覧を取得する。

### `load_rule_docs() -> str`
- **目的**: `AGENTS.md`, `formatting.md`, `workflow.md`, `agent-behavior.md` などの主要規約ファイルを結合してコンテキスト文字列として返す。

### `get_existing_notes_context(category_filter: str = None) -> str`
- **目的**: SQLite (`knowledge_index.db`) から既存ノートのタイトル・パス・概要を取得し、LLMへの参照コンテキストとして整形する。

### `clean_and_parse_json(json_str: str) -> dict`
- **目的**: LLM出力の不完全なJSON文字列やエスケープミスを自動修復してパースする。

### `generate_knowledge_files(...) -> dict`
- **目的**: 2パス方式でナレッジノートを生成する。
  - **PASS 1**: カテゴリ判定 & YAMLメタデータの抽出 (JSON出力)
  - **PASS 2**: 選択された指示書テンプレートに基づく本文解析の生成 (Raw Markdown)
- **戻り値**: 推察されたカテゴリ、ヘッドコンテンツ、ノートコンテンツを含む辞書。

### `auto_sublimate_rag_answer(...) -> dict`
- **目的**: RAGの質問と回答の対話内容から、自動的にナレッジノート（タイトル・カテゴリ・概要・メタデータ）を昇華生成する。

## 3. 依存関係
- 標準ライブラリ: `os`, `re`, `json`, `sqlite3`, `pathlib`
- 外部パッケージ: `streamlit`
- 内部モジュール: `config`, `llm_client`
