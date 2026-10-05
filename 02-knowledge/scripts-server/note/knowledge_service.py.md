---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/knowledge_service.py"]
tags: ["scripts", "server", "knowledge", "sublimation"]
status: active
phase: 2
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/llm_client.py"]
task: []
summary: "scripts/server/knowledge_service.py の静的解析ノート"
---

# `scripts/server/knowledge_service.py` 解析ノート

## 概要
`scripts/server/knowledge_service.py` は、パーソナルナレッジベースにおける「知識の昇華（Sublimation）」プロセスを担当するモジュールです。
LLM を用いて規約に準拠した YAML メタデータ（Frontmatter）の生成や、テンプレートに基づく二層ノート（`head/` および `note/`）の構造化データ生成を行います。

## 主な関数
### 1. `resolve_prompt_path(prompt_input: str) -> str`
- 指定されたプロンプト名やパスを `00-rules/prompts/` やスキルディレクトリ等から解決します。

### 2. `get_available_prompts() -> list[str]`
- `00-rules/prompts/` 内にある利用可能なプロンプトファイル一覧を取得します。

### 3. `generate_knowledge_files(...) -> dict`
- **PASS 1**: 規約とコンテンツを基に LLM でメタデータ（カテゴリ、要約、タグ、リレーション等）を JSON 抽出します。
- **PASS 2**: 選択されたプロンプトテンプレートと規約に沿って、構造化された解説本文を生成します。
- `head` 用の Frontmatter テキストと、本文付きの `note` 用テキストを辞書型で返します。

### 4. `auto_sublimate_rag_answer(...) -> dict`
- RAG で生成されたユーザーへの回答や質問内容を基に、自動でナレッジ化用のタイトルやカテゴリ、メタデータを推察して二層コンテンツを構築します。
