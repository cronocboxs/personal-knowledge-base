---
title: "scripts/server/config.py (Head)"
category: "scripts/server"
type: "head"
target: "scripts/server/config.py"
summary: "サーバー関連スクリプト用の共通設定・パス定義モジュール"
---

# scripts/server/config.py (Head)

## 概要
プロジェクトルートや各種ディレクトリ（`01-private`, `00-rules`, `02-knowledge`, `04-resources`）、データベースパス、LLMエンドポイントの設定と環境変数読み込みを行うモジュールです。

## 主要な定義・変数
- `PROJECT_ROOT`: プロジェクトルートディレクトリの絶対パス
- `CONFIG_PATH`: 設定ファイル (`settings.json`) のパス
- `DB_PATH`: SQLiteデータベースファイルのパス
- `OLLAMA_ENDPOINT`: OllamaのAPIエンドポイント
- `load_config()`: `settings.json` の読み込み・設定管理関数
