---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/knowledge_service.py"]
tags: [knowledge, sublimation, python, llm, rag]
status: active
phase: 2
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/llm_client.py"]
task: ["scripts/server/knowledge_service.py # Python製ナレッジ昇華・プロンプト解決・メタデータ抽出サービス機能の静的解析"]
summary: "プロンプトテンプレートのパス解決、規約・既存ノートコンテキストの読み込み、およびLLMを用いた2パス方式（メタデータ抽出と本文生成）によるナレッジ自動昇華機能の静的解析。"
---

# knowledge_service.py の技術解析ノート

## 1. 概要
`scripts/server/knowledge_service.py` は、パーソナルナレッジベースにおける「ナレッジの自動昇華・構造化」を担うコアサービスモジュールです。
LLMを用いた2パス方式（PASS 1: メタデータ/カテゴリ/リレーション抽出、PASS 2: 指示書に基づく本文解析生成）により、入力データやRAG回答をリポジトリ規約（`00-rules/`）に完全準拠したMarkdownノートへ昇華します。

## 2. 主要関数と処理フロー

### 2.1 プロンプト解決・設定読み込み
- **`resolve_prompt_path(prompt_input: str) -> str`**:
  - 指定されたプロンプト名やファイルパスを、`00-rules/prompts/` や `.agents/skills/` 配下から探索して絶対パスへ解決する。
- **`get_available_prompts() -> list[str]`**:
  - `00-rules/prompts/` 配下の利用可能なプロンプトテンプレートファイル（`.md`）の一覧を返す。
- **`load_rule_docs() -> str`**:
  - `AGENTS.md` や `formatting.md`, `workflow.md`, `agent-behavior.md` などの規約ファイルを結合してLLMにインジェクトするためのコンテキスト文字列を生成。
- **`get_existing_notes_context(category_filter) -> str`**:
  - SQLiteデータベース（`DB_PATH`）から既存のナレッジインデックスを読み込み、親・子・関連ノート（リレーション）の抽出精度を高めるためのコンテキストを構築。

### 2.2 JSONパース補正
- **`clean_and_parse_json(json_str: str) -> dict`**:
  - LLMが生成した不完全またはエスケープの乱れたJSON文字列を正規表現などで安全にパース・修復する。

### 2.3 ナレッジ自動昇華パイプライン
- **`generate_knowledge_files(...) -> dict`**:
  - **PASS 1**: 規約・既存ノートを参照しつつ、LLMにメタデータ（カテゴリ、タグ、概要、親・子・関連ノート）をJSON出力させる。カテゴリが `auto` の場合は自動推察。
  - YAML Frontmatter（`formatting.md` 準拠）を構築。
  - **PASS 2**: 選択されたプロンプトテンプレートを適用し、規約に従った詳細な技術解説・構造化Markdown本文を生成。
  - ヘッド用とノート用のコンテンツを辞書として返す。
- **`auto_sublimate_rag_answer(...) -> dict`**:
  - Tab 2のRAGによるQ&A結果を、同様にLLMを用いてメタデータ付与された高品位なナレッジノートへと自動昇華する。

## 3. 依存関係と連携モジュール
- **`config.py`**: パス定義や環境設定の参照
- **`llm_client.py`**: LLM呼び出し関数 (`call_llm`) の利用
