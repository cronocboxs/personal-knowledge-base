---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/start-webui.py"]
tags: [server, streamlit, webui, ui, python]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/rag_service.py", "scripts/server/knowledge_service.py", "scripts/server/llm_client.py"]
task: ["scripts/server/start-webui.py # scripts/server/start-webui.pyの静的解析完了"]
summary: "Streamlitを用いたPersonal Knowledge Base用のWebUIアプリケーション。ファイルエクスプローラー、ナレッジ新規登録、AI自動昇華、RAG検索・質問応答機能を提供する。"
---

# start-webui.py 解析ノート

## 1. 概要
`start-webui.py` は、Streamlit を用いたパーソナルナレッジベース（Personal Knowledge Base）向けの WebUI アプリケーションのエントリポイントです。AIモデルの設定、エクスプローラー風ディレクトリツリーからのファイル読み込み・編集、一次素材の保存とAIによるナレッジ自動昇華、RAGを活用した検索・質問応答機能を提供します。

## 2. 依存関係
- **インポートモジュール**: `os`, `re`, `datetime`, `subprocess`, `streamlit as st`
- **内部設定・サービス依存**: 
  - `config.py` (`PROJECT_ROOT`, `KNOWLEDGE_DIR`, `RESOURCES_DIR`, `load_config`, `get_gemini_api_key`)
  - `rag_service.py` (`search_relevant_knowledge`)
  - `knowledge_service.py` (`generate_knowledge_files`, `auto_sublimate_rag_answer`, `get_available_prompts`)
  - `llm_client.py` (`call_llm`)

## 3. 主要な関数・機能構成

### ヘルパー関数
- `get_knowledge_categories() -> list[str]`: `02-knowledge/` 配下のカテゴリディレクトリ一覧を取得する。
- `get_ollama_models() -> list[str]`: `ollama list` コマンドを実行して利用可能なローカルモデルの一覧を動的取得する。
- `render_explorer_tree(...)`: サイドバーにエクスプローラー風のツリー構造（ディレクトリ展開とファイルボタン）を描画し、選択時にフォームへ読み込む。
- `load_file_to_form(rel_file_path: str, is_knowledge: bool)`: 選択されたファイルをセッションステートを経由して編集フォームに読み込む。

### WebUI レイアウト・画面構成
- **ページ設定**: `st.set_page_config(page_title="Personal Knowledge Base", layout="wide")`
- **サイドバー**:
  - **AIモデル設定**: Ollama (Local LLM) と Gemini (Cloud API) の切り替え、モデル選択、APIキー確認。
  - **ファイルエクスプローラー**: 新規作成ボタン、`02-knowledge` と `04-resources` のツリー表示。
- **タブ構成**:
  - **Tab 1: 状況・データ入力・編集**:
    - 一次素材の保存 (`04-resources/`) と、ナレッジ新規登録・AI自動昇華 (`04-resources/` 保存 ➔ `02-knowledge/` への二層出力 ＋ `update-index.py` によるSQLiteインデックス更新) を切り替えて実行。
  - **Tab 2: ナレッジ検索・質問 (RAG)**:
    - ユーザーからの質問を受け付け、`search_relevant_knowledge` で関連ナレッジを検索。
    - 参照ナレッジをコンテキストとして LLM（`call_llm`）に渡し、回答を生成。
    - 生成された回答を `auto_sublimate_rag_answer` を用いて新たなナレッジとして自動昇華・保存する機能を提供。
