---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/start-webui.py"]
tags: [streamlit, webui, python, ui]
status: active
phase: 2
parent: []
children: []
related: ["scripts/server/rag_service.py", "scripts/server/knowledge_service.py", "scripts/server/llm_client.py", "scripts/server/config.py"]
task: ["scripts/server/start-webui.py # Python製Streamlit WebUIアプリケーションの構造とRAG機能の解読"]
summary: "StreamlitベースのPersonal Knowledge Base WebUIアプリケーションの構成、セッションステート管理、エクスプローラー描画、RAG質問・回答および自動昇華機能の静的解析。"
---

# start-webui.py の技術解析ノート

## 1. 概要
`scripts/server/start-webui.py` は、Streamlitフレームワークを用いたPersonal Knowledge Base（パーソナルナレッジベース）の統合Webインターフェースです。
ローカルLLM（Ollama）またはクラウドAPI（Gemini）を選択可能にし、ナレッジの新規登録・AI自動昇華、ファイルエクスプローラーによるツリー表示、および関連ナレッジを検索・参照しながら回答を生成するRAG（Retrieval-Augmented Generation）機能を提供します。

## 2. 主要コンポーネントと処理フロー

### 2.1 ヘルパー関数
- **`get_knowledge_categories() -> list[str]`**:
  - `KNOWLEDGE_DIR` 配下のディレクトリを走査し、システム予約フォルダ（`head`, `note` 等）を除外したナレッジカテゴリ一覧を取得。未作成時は `default` を挿入してソート済みで返す。
- **`get_ollama_models() -> list[str]`**:
  - `ollama list` コマンドをサブプロセスで実行し、システムにインストールされている利用可能なOllamaモデル一覧を動的取得する。埋め込みモデル（embed等）を除外し、取得失敗時は設定ファイルのデフォルトモデルフォールバックを返す。

### 2.2 UI構成とSession State
- `st.set_page_config(page_title="Personal Knowledge Base", layout="wide")` によりワイドレイアウトのダッシュボードを構築。
- セッションステート（`st.session_state`）で編集モードやフォーム入力内容、前回RAGクエリ・回答を永続管理し、ファイル選択や再読み込み時の状態保持を実現。

### 2.3 サイドバー設定とファイルエクスプローラー
- **AIモデル設定**:
  - プロバイダとして「Ollama (Local LLM)」と「Gemini (Cloud API)」を選択可能。
  - プロバイダに応じたモデル選択セレクトボックスやAPIキー読込状態のフィードバックを提供。
- **ファイルエクスプローラー**:
  - `render_explorer_tree()` により、`02-knowledge/` および `04-resources/` 配下のディレクトリ構造を再帰的に展開し、Markdownファイルをクリックすることでフォームに読み込んで編集・再昇華できるUIを提供。

### 2.4 メインタブ構成
1. **Tab 1: 状況・データ入力・編集（`📥`）**:
   - 一次素材の保存（`04-resources/`）モード、およびナレッジの新規登録・AI自動昇華（`04-resources`保存 ➔ `02-knowledge`昇華）モードを切り替え可能。
   - 選択されたテンプレートに基づきLLMが解析ノート（`head/` および `note/`）を自動生成し、SQLiteベクトル検索インデックスの更新スクリプトをサブプロセスで自動実行する。
2. **Tab 2: ナレッジ検索・質問（`💬`）**:
   - ユーザーの質問に対して指定カテゴリのナレッジDBからベクトル検索（`search_relevant_knowledge`）を実行。
   - 検索された関連ナレッジをコンテキストとしてLLMプロンプトを構築し、回答を生成。
   - 回答結果をさらにナレッジベースへ自動昇華・保存する機能（`auto_sublimate_rag_answer`）を備える。

## 3. 依存関係と関連モジュール
- **`config.py`**: `PROJECT_ROOT`, `KNOWLEDGE_DIR`, `RESOURCES_DIR`, `load_config`, `get_gemini_api_key`
- **`rag_service.py`**: `search_relevant_knowledge`
- **`knowledge_service.py`**: `generate_knowledge_files`, `auto_sublimate_rag_answer`, `get_available_prompts`
- **`llm_client.py`**: `call_llm`
