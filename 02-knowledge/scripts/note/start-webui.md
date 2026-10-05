---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/start-webui.py"]
tags: [streamlit, webui, python, server, rag, llm]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/rag_service.py", "scripts/server/knowledge_service.py", "scripts/server/llm_client.py"]
task: ["scripts/server/start-webui.py # Streamlit WebUIスクリプトの全般解析"]
summary: "Personal Knowledge BaseのStreamlitによるWebUIアプリケーション（スクリプト、エクスプローラー、RAG検索・質問応答、自動ナレッジ昇華機能）の実装解説。"
---

# start-webui.py 技術解析ノート

## 1. 概要
`scripts/server/start-webui.py` は、Streamlitを用いたPersonal Knowledge BaseのインタラクティブなWebUIアプリケーションです。
ローカルLLM（Ollama）またはクラウドAPI（Gemini）を選択・切り替えながら、一次データの保存、ナレッジの自動昇華、ファイルエクスプローラーによる閲覧・編集、およびRAG（Retrieval-Augmented Generation）に基づく質問応答を行います。

## 2. 依存関係とモジュール連携
本スクリプトは以下のモジュールおよび外部パッケージと連携しています：
- **標準ライブラリ**: `os`, `re`, `datetime`, `subprocess`
- **外部フレームワーク**: `streamlit`
- **内部モジュール (`scripts/server/`)**:
  - `config.py`: パス定義 (`PROJECT_ROOT`, `KNOWLEDGE_DIR`, `RESOURCES_DIR`)、設定読込、Gemini APIキー取得
  - `rag_service.py`: SQLite / ベクトル検索を用いた関連ナレッジ検索 (`search_relevant_knowledge`)
  - `knowledge_service.py`: ナレッジファイル生成・自動昇華・プロンプト一覧取得
  - `llm_client.py`: 統一LLM呼び出し (`call_llm`)

## 3. 主要機能と処理フロー

### A. サイドバー設定・エクスプローラー
1. **AIモデル設定**:
   - プロバイダ（Ollama または Gemini）の選択。
   - モデルの動的切替（Ollamaの場合は `ollama list` コマンド結果のパースにより利用可能モデルを動的取得）。
   - Gemini APIキーの検証状態表示。
2. **ファイルエクスプローラー**:
   - `02-knowledge/` および `04-resources/` 配下のディレクトリ構造を再帰的に走査し、折りたたみ式エクスプローラーとしてサイドバーに描画。
   - 任意のMarkdownファイルを選択すると、対応するフォーム領域へ内容が自動ロードされ編集モードへ切り替わる。

### B. Tab 1: 状況・データ入力・編集
- **一次素材の保存**: 入力内容を `04-resources/` 配下にMarkdownとして保存。
- **ナレッジの新規登録・AI自動昇華**:
  1. `04-resources/` へ一次データを保存。
  2. 選択された指示書テンプレートとLLMプロバイダに基づき、`knowledge_service.py` を通じて二層ドキュメント（`head/` と `note/`）を生成。
  3. `scripts/index/update-index.py` をサブプロセスとして実行し、SQLiteベクトル検索インデックスを自動更新。

### C. Tab 2: ナレッジ検索・質問 (RAG)
1. **関連ナレッジ検索**: ユーザーの質問に対し、指定カテゴリから関連度の高いナレッジをベクトル検索 (`search_relevant_knowledge`) で抽出。
2. **回答生成**: 抽出されたナレッジをコンテキストとしてプロンプトに組み込み、LLM (`call_llm`) で回答を生成。
3. **回答のナレッジ昇華**: 生成された回答を指定カテゴリまたはAI自動推察カテゴリへ新規ナレッジとしてワンクリックで保存・インデックス化 (`auto_sublimate_rag_answer`)。

## 4. セッションステート管理
Streamlitの `st.session_state` を利用して、以下の状態を保持・管理しています：
- 編集モードフラグ (`edit_mode`)
- フォーム入力値 (`form_title`, `form_content`, `form_input_type_idx`, `form_category`, `form_subdir`)
- 直近のRAG質問と回答 (`last_rag_answer`, `last_rag_query`)
