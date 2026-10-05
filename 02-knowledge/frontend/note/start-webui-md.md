---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/start-webui.md"]
tags: ["scripts", "server", "frontend"]
status: active
phase: 5
parent: []
children: []
related: []
task: ["scripts/server/start-webui.md # 解析対象ファイル"]
summary: "WebUIの起動手順や操作方法を記述したドキュメントファイル"
---

# start-webui-md

## 概要
WebUIの起動手順や操作方法を記述したドキュメントファイル

## ソースコード内容
```
# 入力用webUI `scripts/server/start-webui.py`

`Streamlit` を使用し、解析対象データの保存（`04-resources/` または `02-knowledge/` への振り分け）と、質問回答（RAG）インターフェースを備えた最小コード。

```bash
# 必要なライブラリのインストール（未導入の場合）
python3 -m pip install streamlit

# WebUI サーバーの起動
python3 -m streamlit run scripts/server/start-webui.py
```

## 仕様

### 04-resources

 1. **保存時のサブディレクトリ指定:** 
   任意のサブディレクトリ名を入力可能にし、存在しない場合は自動生成します（例: `04-resources/system-logs/`）。
 2. **02-knowledge 保存時の一次データ保存 ＋ AI自動昇華パイプライン:**
    1. 入力データは必ず 一次データとして `04-resources/` に配置 されます。
    2. その後、AI（LLM API）へテキストを送信し、`formatting.md` の規約に沿って YAML メタデータを抽出・生成 します。
    3. AIから返却されたメタデータと本文から `head/*.md` (Frontmatterのみ) と `note/*.md` (Frontmatter + 本文) の二層構造を同時に自動生成して配置します。

export GEMINI_API_KEY="your-api-key" をターミナルで実行しておくと、Gemini が自動で summary や tags を抽出して formatting.md 規約通りのナレッジを二層（head/ & note/）に自動出力します。
```
