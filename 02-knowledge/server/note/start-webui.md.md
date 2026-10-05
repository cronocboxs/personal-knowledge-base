---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/start-webui.md"]
tags: [server, webui, documentation, streamlit, python]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/start-webui.py", "scripts/server/config.py", "scripts/server/rag_service.py", "scripts/server/knowledge_service.py", "scripts/server/llm_client.py"]
task: ["scripts/server/start-webui.md # WebUI起動手順・仕様ドキュメントの仕様解析"]
summary: "scripts/server/start-webui.md は Streamlit WebUI の起動コマンド、必要パッケージ、一次データ保存とAI自動昇華パイプラインの仕様を解説するドキュメントです。"
---

# `scripts/server/start-webui.md` 解析ノート

## 1. 概要
`scripts/server/start-webui.md` は、Streamlit を用いたパーソナルナレッジベース統合 WebUI（`scripts/server/start-webui.py`）の起動手順および仕様を定義した解説ドキュメントです。

## 2. 主要な内容

### 2.1 起動コマンド
```bash
python3 -m pip install streamlit
python3 -m streamlit run scripts/server/start-webui.py
```

### 2.2 仕様詳細
- **04-resources 保存**: サブディレクトリの動的生成をサポート。
- **02-knowledge 自動昇華パイプライン**:
  1. 一次データを `04-resources/` に保存。
  2. AI（LLM API）へテキストを送信し、`formatting.md` に沿った YAML メタデータを抽出・生成。
  3. `head/*.md` と `note/*.md` の二層構造を自動生成。
  4. 環境変数 `GEMINI_API_KEY` の設定により、自動でサマリーやタグを抽出して二層構造へ出力。

## 3. 依存関係
- 対象プログラム: `scripts/server/start-webui.py`
- 関連サービス: `config.py`, `rag_service.py`, `knowledge_service.py`, `llm_client.py`
