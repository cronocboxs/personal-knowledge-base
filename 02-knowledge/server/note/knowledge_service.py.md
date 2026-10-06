---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/knowledge_service.py"]
tags: [server, knowledge-service, python]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/llm_client.py", "scripts/server/rag_service.py", "scripts/server/start-webui.py"]
task: ["scripts/server/knowledge_service.py # knowledge_service.pyの静的解析"]
summary: "プロンプトパス解決、規約・既存ノート読み込み、LLMを用いたメタデータ抽出と本文解析による二層ノート生成サービスモジュール。"
---

# knowledge_service.py 解析ノート

## 概要
`scripts/server/knowledge_service.py` は、パーソナルナレッジベースにおいて、LLMを用いたコード解析やRAGの回答内容から構造化されたナレッジファイル（`head/` および `note/`）を自動生成するためのコアサービスモジュールです。

## 主要な関数と責務

### 1. プロンプトパス解決 (`resolve_prompt_path`)
- 指定されたプロンプト名やパス（ファイル名、相対パス、スキル名）を探索し、存在する場合は対応する絶対パスへ解決して返します。
- 探索順序:
  1. 絶対・相対ファイルの直接存在確認
  2. `00-rules/prompts/` 配下
  3. `.agents/skills/<prompt_input>/SKILL.md`
  4. `00-rules/skills/<prompt_input>/SKILL.md`

### 2. 規約・コンテキスト読み込み
- `load_rule_docs()`: `AGENTS.md` および `00-rules/` 配下の主要規約（`formatting.md`, `workflow.md`, `agent-behavior.md`）を結合してロードします。
- `get_existing_notes_context()`: SQLite データベース (`DB_PATH`) から既存のナレッジ一覧（タイトル、パス、概要）を取得し、LLMへのコンテキストとして提供します。

### 3. JSONパース補助 (`clean_and_parse_json`)
- LLMが生成した不完全またはエスケープ不備のあるJSON文字列を、正規表現を用いて安全にパース可能な形にクリーニング・補正して `json.loads` を実行します。

### 4. 二層ノート生成 (`generate_knowledge_files`)
- **PASS 1 (メタデータ抽出)**: 規約と既存ノートをコンテキストとしてLLMに渡し、カテゴリ、タグ、サマリー、リレーション（parent, children, related）をJSON形式で自動判定させます。
- **PASS 2 (本文解析生成)**: 指定されたプロンプトテンプレートと対象データに基づき、LLMに技術解説Markdown本文を生成させます。
- 最終的に `head_content`（Frontmatterのみ）と `note_content`（Frontmatter ＋ 本文）を辞書として返却します。

### 5. RAG回答自動昇華 (`auto_sublimate_rag_answer`)
- RAGの質疑応答結果を入力として、同様にLLMを用いて適切なタイトル、カテゴリ、メタデータを抽出・生成し、ナレッジノート化します。

## 依存関係
- 標準ライブラリ: `os`, `re`, `json`, `sqlite3`, `pathlib`
- 外部ライブラリ: `streamlit`
- 内部モジュール: `config`, `llm_client`
- 被依存モジュール: `rag_service.py`, `start-webui.py`
