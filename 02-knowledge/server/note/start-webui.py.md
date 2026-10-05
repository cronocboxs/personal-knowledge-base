---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/start-webui.py"]
tags: [server, streamlit, webui, python]
status: active
phase: 3
parent: []
children: []
related: ["scripts/server/config.py", "scripts/server/rag_service.py", "scripts/server/knowledge_service.py", "scripts/server/llm_client.py"]
task: ["scripts/server/start-webui.py # scripts/server/start-webui.pyの静的解析・ナレッジ生成"]
summary: "scripts/server/start-webui.py は Streamlit を用いたパーソナルナレッジベースの統合 WebUI アプリケーションであり、エクスプローラー、一次データ保存、AI自動昇華、RAG検索・質問応答機能を提供します。"
---

# start-webui.py - Streamlit 統合 WebUI アプリケーション

## 1. 概要
`scripts/server/start-webui.py` は、Streamlit をベースに構築されたパーソナルナレッジベースのグラフィカルインターフェースです。サイドバーによるファイルツリーエクスプローラー、LLMプロバイダ/モデル切り替え設定、一次データの保存とAIによる自動二層昇華、RAGに基づく質問応答（対話）および回答のナレッジ化機能を統合しています。

## 2. 主要な関数・コンポーネント
- **`get_knowledge_categories() -> list[str]`**: `02-knowledge/` 配下のディレクトリからカテゴリ一覧を取得する。
- **`get_ollama_models() -> list[str]`**: `ollama list` コマンドを実行して利用可能なローカル LLM モデル一覧を動的に取得する。
- **`render_explorer_tree(dir_path, ...)`**: サイドバーにエクスプローラー風のディレクトリツリーを描画し、ファイルクリック時にフォームへ内容をロードする。
- **`load_file_to_form(rel_file_path, ...)`**: 指定されたマークダウンやテキストファイルを読み込み、Streamlit のセッションステート（編集モード、タイトル、本文）に反映する。

## 3. WebUI タブ構成
1. **📥 状況・データ入力・編集 (Tab 1)**:
   - 一次素材（`04-resources/`）の直接保存。
   - ナレッジの新規登録・指示書（プロンプトテンプレート）選択に基づく AI 自動二層昇華。
   - 既存ファイルの読み込み・更新・再昇華。
2. **💬 ナレッジ検索・質問 (Tab 2)**:
   - 自然言語クエリによる高精度 RAG 検索（対象カテゴリ・参照件数の選択可能）。
   - 参照された関連ナレッジの展開表示とコサイン類似度確認。
   - LLM による回答生成。
   - 生成された回答をAIに自動推察させてナレッジ（`02-knowledge/`）として昇華・保存する機能。

## 4. 依存関係
- 設定: `config.py`
- RAG検索: `rag_service.py`
- ナレッジ生成: `knowledge_service.py`
- LLMクライアント: `llm_client.py`
- フレームワーク: `streamlit`
- 標準ライブラリ: `os`, `re`, `datetime`, `subprocess`
