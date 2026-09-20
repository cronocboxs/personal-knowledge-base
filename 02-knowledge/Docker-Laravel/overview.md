---
created: 2026-09-20
updated: 2026-09-20
tags: [Docker-Laravel, spec, code-analysis]
phase: 3
status: active
unexplored_domains: []
---

# Docker-Laravel 挙動・処理仕様ナレッジ

## 1. 識別された機能・インターフェース一覧 (Phase 1)
- [x] Dockerインフラストラクチャ定義 (`docker/` & `docker-compose.base.yml`)
- [x] Nginx Webサーバー設定 (`docker/web-nginx/`)
- [x] MySQLデータベース設定 (`docker/db-mysql/`)
- [x] PHP/Reverb ランタイム環境 (`docker/app-php/`, `docker/reverb-php/`)
- [x] デプロイメント自動化ワークフロー (`.github/workflows/deploy.yml`)

## 2. インターフェース・トリガー別詳細トレース (Phase 2)

### 機能1: Dockerコンテナ群の構築・起動
#### トリガー: 「`docker-compose` コマンド実行 / デプロイメントスクリプトの実行」
- **入力・要求（Input/Request）**:
  - 環境変数設定ファイル (`.env.example.doker`)、ベースコンポーズ設定 (`docker-compose.base.yml`)。
- **内部処理流転（Execution Flow）**:
  1. Nginx, MySQL, PHP-FPM, Reverb 等の各コンテナイメージ構築 (`Dockerfile`)。
  2. ボリューム・ネットワークの割り当てとコンテナ間リンクの確立。
- **出力・応答・状態変化（Output/Response/State Change）**:
  - **成功時**: 各サービスが指定ポートで起動し、Webリクエストを処理可能な状態になる。
  - **失敗時**: ポート競合やボリューム権限エラーの発生。

## 3. モジュール間連携・例外ハンドリング・設計パターン (Phase 3)
- **コンポーネント間・ドメイン間の相互作用**: Nginxがリバースプロキシとしてリクエストを受け付け、PHP-FPMへFastCGI経由で転送、DB（MySQL）およびReverb（WebSocket）と連携する構成。
- **横断的関心事**: コンテナ化された環境におけるログ管理、環境変数の分離、GitHub ActionsによるCI/CDデプロイ。
