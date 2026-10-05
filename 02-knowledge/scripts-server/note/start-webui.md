---
title: "start-webui.py"
category: "scripts-server"
summary: "FastAPIおよびUvicornを使用したWebUIサーバーの起動スクリプト。設定読込、ロギング設定、サーバー起動およびプロセス管理を行う。"
tags: ["python", "fastapi", "uvicorn", "server", "webui"]
created_at: "2026-10-06"
updated_at: "2026-10-06"
---

# start-webui.py Note

## 1. 概要
`scripts/server/start-webui.py` は、本パーソナルナレッジベースシステムのWebUIおよびAPIバックエンドを提供するFastAPIアプリケーションを起動するためのエントリポイントスクリプトである。Uvicorn ASGIサーバーを背後に使用し、ローカルホスト上での開発・運用サーバー起動を担う。

## 2. 主要コンポーネントと処理フロー

### 2.1. 設定と引数解析 (Argument Parsing)
スクリプトは標準の `argparse` ライブラリを使用して以下のコマンドライン引数を受け付ける：
- `--host`: バインドするホストアドレス（デフォルト: `127.0.0.1` または設定ファイル依存）
- `--port`: リッスンポート番号（デフォルト: `8000` 等）
- `--reload`: 開発用のコード変更自動リロード機能の有効化

### 2.2. FastAPI アプリケーションの初期化
Uvicornを起動する際、同一ディレクトリ内の FastAPIインスタンス（通常は `knowledge_service.py` またはルーター群を統合したモジュール）をインポートし、ASGIアプリケーションとして渡す構成になっている。

### 2.3. ロギングとエラーハンドリング
サーバー起動前後に標準出力・ファイル出力へのログ設定を初期化し、ポート競合や依存関係の欠落、DB接続エラーなどの例外をキャッチして適切なエラーメッセージを出力する。

## 3. 依存関係
- `uvicorn`: ASGIサーバー
- `fastapi`: Webフレームワーク
- `scripts/server/config.py`: サーバー環境設定・定数管理
- `scripts/server/knowledge_service.py`: ナレッジ検索・管理APIロジック
- `scripts/server/rag_service.py`: RAG（Retrieval-Augmented Generation）処理ロジック

## 4. 拡張・運用の注意点
- 本スクリプトを直接実行することでローカル WebUIサーバーが起動する。
- 本番運用時はプロセス管理ツール（systemd, supervisor等）やDockerコンテナ内からのエントリポイントとして利用されることを想定している。
