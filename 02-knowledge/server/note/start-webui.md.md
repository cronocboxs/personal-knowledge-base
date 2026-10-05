---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/start-webui.md"]
tags: [server, webui, streamlit, documentation]
status: active
phase: 5
parent: []
children: []
related: ["scripts/server/start-webui.py"]
task: ["scripts/server/start-webui.md # WebUI使用ガイドドキュメントの静的解析"]
summary: "scripts/server/start-webui.md は、Streamlit WebUIの起動方法や04-resourcesから02-knowledgeへの自動昇華パイプラインの仕様を解説したドキュメントです。"
---

# `scripts/server/start-webui.md` 解析ノート

## 1. 概要
`scripts/server/start-webui.md` は、`scripts/server/start-webui.py` で提供されるStreamlit WebUIの起動手順、インストールコマンド、および一次データ保存からAI自動昇華パイプラインに至るまでの仕様をまとめた解説ドキュメントです。

## 2. 主要仕様
- **起動コマンド**: `python3 -m streamlit run scripts/server/start-webui.py`
- **パイプライン仕様**:
  1. 入力データはまず `04-resources/` に一次データとして配置される。
  2. LLM APIへテキストが送信され、`formatting.md` に沿ったYAMLメタデータと本文が生成される。
  3. `head/*.md` と `note/*.md` の二層構造として自動書き出しされる。
