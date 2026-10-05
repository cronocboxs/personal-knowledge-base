---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/knowledge_service.py"]
tags: [server, knowledge, service, ollama, gemini, python]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/llm_client.py"]
task: ["scripts/server/knowledge_service.py # scripts/server/knowledge_service.pyの静的解析完了"]
summary: "プロンプトテンプレートの解決、規約読み込み、LLMを用いた二層ナレッジ生成（メタデータ・本文抽出）、およびRAG回答の自動昇華を行うサービスモジュール。"
---

# knowledge_service.py 解析ノート

## 1. 概要
`knowledge_service.py` は、パーソナルナレッジベースの中核となるナレッジ生成・昇華ロジックを提供するサービスモジュールです。プロンプトテンプレートの解決、規約ドキュメント（`AGENTS.md` や `00-rules/`）の動的読み込み、LLM を活用した 2 パス（メタデータ抽出 ＋ 本文解析生成）による二層ノート（`head` および `note`）の生成、さらに RAG の質問・回答結果の自動昇華機能を担当します。

## 2. 依存関係
- **インポートモジュール**: `os`, `re`, `json`, `sqlite3`, `pathlib.Path`, `streamlit as st`
- **内部モジュール・設定依存**: `config.py` (`PROJECT_ROOT`, `RULES_DIR`, `KNOWLEDGE_DIR`, `DB_PATH`), `llm_client.py` (`call_llm`)

## 3. 主要関数・処理フロー

### `resolve_prompt_path(prompt_input: str) -> str`
- **目的**: 指定された指示書名やパス（例: `code-analysis.md`, `sublimation-agent`）を、リポジトリ内の適切な絶対パス（`00-rules/prompts/` や `.agents/skills/` 等）に解決する。

### `get_available_prompts() -> list[str]`
- **目的**: `00-rules/prompts/` 配下に格納されている利用可能なプロンプトテンプレートのファイル名一覧を取得する。

### `load_rule_docs() -> str`
- **目的**: `AGENTS.md` や `00-rules/formatting.md` などの主要な規約ファイルを読み込み、LLMのシステムプロンプトやコンテキストとして注入可能な文字列として結合する。

### `get_existing_notes_context(category_filter: str = None) -> str`
- **目的**: SQLite ベクトルデータベース (`DB_PATH`) から既存のノートタイトル・パス・概要のリストを取得し、リレーション（`parent`, `children`, `related`）参照用のコンテキストを作成する。

### `clean_and_parse_json(json_str: str) -> dict`
- **目的**: LLM が出力した JSON 文字列のエスケープミスや不正な記法を補正し、安全に `json.loads` でパースする。

### `generate_knowledge_files(...) -> dict`
- **目的**: 入力データとタイトルをもとに、規約に完全に準拠した二層ナレッジファイルを生成する。
- **処理フロー**:
  1. 規約ドキュメントと既存ノート情報を読み込み。
  2. **PASS 1**: LLM を用いてカテゴリ・タグ・概要・リレーションを JSON 形式で抽出（または自動推察）。
  3. 規約に準拠した YAML Frontmatter テキストを構築。
  4. **PASS 2**: 選択された指示書テンプレートに則り、LLM に本文解析をさせてMarkdown文書を生成。
  5. `head_content`（Frontmatterのみ）と `note_content`（Frontmatter ＋ 本文）を含む辞書を返す。

### `auto_sublimate_rag_answer(...) -> dict`
- **目的**: RAG で生成されたユーザーの質問と回答のペアから、タイトル、カテゴリ、概要、リレーションを自動抽出・推察し、ナレッジノートとしての二層コンテンツを構築して返す。
