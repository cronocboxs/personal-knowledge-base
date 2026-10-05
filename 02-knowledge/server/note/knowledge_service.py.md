---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/knowledge_service.py"]
tags: [server, knowledge, service, sublimation, llm]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/llm_client.py", "scripts/server/rag_service.py"]
task: ["scripts/server/knowledge_service.py # ナレッジ生成・自動昇華サービスモジュールの静的解析"]
summary: "scripts/server/knowledge_service.py は、LLMを活用して一次リソースから二層構造のナレッジ（head/note）を自動生成・昇華させるサービスモジュールです。"
---

# `scripts/server/knowledge_service.py` 解析ノート

## 1. 概要
`scripts/server/knowledge_service.py` は、ユーザーが入力したテキストやリソースに対して、指定されたプロンプトや規約（`00-rules/`）を適用し、LLM経由でYAML Frontmatter付きの二層ナレッジファイル（`head/` および `note/`）を自動生成（昇華）する機能を提供するサービスモジュールです。

## 2. 主要関数
- **`resolve_prompt_path(prompt_input: str) -> str`**:
  - 指示書指定（ファイル名、パス、スキル名など）を適切な絶対パスに解決する。
- **`get_available_prompts() -> list[str]`**:
  - `00-rules/prompts/` 内の `.md` ファイル一覧を取得する。
- **`load_rule_docs() -> str`**:
  - リポジトリ内の主要規約ファイル（`AGENTS.md`, `formatting.md`, `workflow.md`, `agent-behavior.md`）のテキストを結合してロードする。
- **`generate_knowledge_files(...)` / `auto_sublimate_rag_answer(...)`**:
  - LLMを呼び出してナレッジの構造化・ノートファイル書き出しを行う。
