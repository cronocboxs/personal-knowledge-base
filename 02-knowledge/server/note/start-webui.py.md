---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/start-webui.py"]
tags: [python, streamlit, server, webui, rag]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/rag_service.py", "scripts/server/knowledge_service.py", "scripts/server/llm_client.py"]
task: ["scripts/server/start-webui.py"]
summary: "Streamlitを用いたパーソナルナレッジベースのWebUIサーバー（エクスプローラー、データ保存、AI自動昇華、RAG質問検索機能を提供）"
---

# start-webui.py 技術解析ノート

## 1. 概要
`scripts/server/start-webui.py` は、Streamlitフレームワークを活用して構築された、パーソナルナレッジベース（Personal Knowledge Base）の統合型WebUIアプリケーションです。
一次素材の保存、AIによる自動ナレッジ昇華（構造化ドキュメント生成）、ローカル（Ollama）およびクラウド（Gemini）LLMの切り替え、ならびにベクトル検索（RAG）を活用した質問応答と自動ナレッジ化のインターフェースを提供します。

---

## 2. 依存関係・インポートモジュール
スクリプト内で利用されている外部モジュールおよび内部サービスモジュール：

- **標準ライブラリ**: `os`, `re`, `datetime`, `subprocess`
- **外部フレームワーク**: `streamlit as st`
- **内部サービス/モジュール**:
  - `config`: `PROJECT_ROOT`, `KNOWLEDGE_DIR`, `RESOURCES_DIR`, `load_config`, `get_gemini_api_key`
  - `rag_service`: `search_relevant_knowledge`
  - `knowledge_service`: `generate_knowledge_files`, `auto_sublimate_rag_answer`, `get_available_prompts`
  - `llm_client`: `call_llm`

---

## 3. 主要なヘルパー関数

### `get_knowledge_categories() -> list[str]`
- `KNOWLEDGE_DIR` 配下のディレクトリ走査を行い、`head`, `note` などの特殊フォルダを除外した既存ナレッジカテゴリの一覧を取得・返却する。
- カテゴリが存在しない場合、あるいは `"default"` が含まれない場合は先頭に `"default"` を挿入し、ソート済みリストを返す。

### `get_ollama_models() -> list[str]`
- `ollama list` コマンドをサブプロセス経由で実行し、現在利用可能なOllamaのローカルモデル一覧を動的に取得する。
- モデル名に `"embed"` が含まれる埋め込み専用モデルを除外し、取得失敗時は設定ファイルのデフォルトモデルにフォールバックする。

### `render_explorer_tree(dir_path: str, is_knowledge: bool = False, parent_container=st.sidebar)`
- 指定ディレクトリ（`02-knowledge/` または `04-resources/`）を再帰的に走査し、エクスプローラー風のサイドバー（`st.expander` とボタン）を描画する。
- ユーザーがファイルボタンをクリックした際、該当ファイルを読み込んでセッションステート（フォーム編集モード）にロードする。

### `load_file_to_form(rel_file_path: str, is_knowledge: bool)`
- 指定されたファイルパスのコンテンツを読み込み、Streamlitのセッションステート（`edit_mode`, `form_title`, `form_content`, `form_category` 等）にセットしてUIへ反映する。

---

## 4. UI 構成と主要機能フロー

アプリは2つのタブ（`st.tabs`）およびサイドバーで構成されています。

### サイドバー（Sidebar）
1. **AIモデル設定**:
   - プロバイダ選択（Ollama または Gemini）
   - モデル選択、APIキー確認、Ollamaエンドポイント設定
2. **ファイルエクスプローラー**:
   - 新規作成ボタン（フォームリセット）
   - `02-knowledge` ディレクトリのツリー表示とファイル読み込み
   - `04-resources` ディレクトリのツリー表示とファイル読み込み

### Tab 1: 状況・データ入力・編集 (`📥 状況・データ入力・編集`)
- **モード選択**:
  1. *一次素材の保存 (`04-resources/`)*: テキストデータを直接一次リソースとして保存。
  2. *ナレッジの新規登録・AI自動昇華*: 一次データを保存した上で、指定プロンプトテンプレートとLLMを用いて `02-knowledge/<category>/` 配下に `head/` と `note/` の二層ドキュメントを自動生成。
- **インデックス更新**: 生成・更新後、`scripts/index/update-index.py` を実行してSQLiteのベクトル検索インデックスを自動同期。

### Tab 2: ナレッジ検索・質問 (`💬 ナレッジ検索・質問`)
- **RAG パイプライン**:
  - ユーザーからの質問クエリを受け付け、選択カテゴリから類似度の高いナレッジを検索。
  - LLM（Ollama / Gemini）を用いて、参照ナレッジに基づいた高精度な回答を生成。
- **回答の自動ナレッジ化**:
  - 生成された回答を新たなナレッジとして自動昇華・構造化し、`02-knowledge/` に保存・インデックス化する機能を提供。
