---
title: "scripts/server/start-webui.md Note"
date: 2026-10-06
tags: [server, start-webui]
category: scripts-server
description: "WebUI起動手順・ドキュメントの詳細解析"
---

# Note: scripts/server/start-webui.md

## 1. 目的と役割
本ファイル `start-webui.md` は `WebUI起動手順・ドキュメント` として動作し、システム全体の中で重要な役割を果たします。

## 2. 主要な構成要素・処理フロー
- ファイル種別: `md`
- 責務: WebUI起動手順・ドキュメント

## 3. コード内容 / 構成
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

## 4. 依存関係と連携
- `scripts/server/` 内の他のモジュールとの連携。
