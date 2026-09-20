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
- [x] Docker Compose基盤構成 (`docker-compose.base.yml`)
- [x] Nginx Webサーバーコンテナ (`docker/web-nginx/`)
- [x] MySQLデータベースコンテナ (`docker/db-mysql/`)
- [x] PHP-FPM アプリケーションコンテナ (`docker/app-php/`)
- [x] Laravel Reverb リアルタイム通信コンテナ (`docker/reverb-php/`)
- [x] Ngrok トンネリング設定 (`docker/ngrok/`)

## 2. インターフェース・トリガー別詳細トレース (Phase 2 必須)

### 機能1: コンテナ起動・デプロイメント環境
#### トリガー1: 「Docker Compose による環境構築・起動 (`docker compose up`)」
- **入力・要求（Input/Request）**:
  - `docker-compose.base.yml`, `.env.example.doker`, 各Dockerfileおよび設定ファイル。
- **内部処理流転（Execution Flow）**:
  1. `web-nginx`: Nginxがポート80/443で起動し、`app-src` または `app` 内のPHP-FPMへFastCGIプロキシ接続を構成。
  2. `app-php`: 指定されたPHPバージョン（8.1/8.2/8.4）のini設定をロードし、PHP-FPMとして起動。
  3. `db-mysql`: MySQL（5.7 / 8.0 / 8.4）設定 (`my.cnf`) に従いデータディレクトリをマウントして起動。
  4. `reverb`: Laravel ReverbによるWebSocket/リアルタイム通信サーバーの起動。
- **出力・応答・状態変化（Output/Response/State Change）**:
  - **成功時**: 各コンテナがネットワーク上で協調動作し、WEBアクセスおよびDB接続が可能になる。
  - **失敗時**: ポート競合やボリュームマウントエラーによるコンテナ停止・ログ出力。

## 3. モジュール間連携・例外ハンドリング・設計パターン (Phase 3)
- **コンポーネント間・ドメイン間の相互作用**: Nginx ➔ PHP-FPM (FastCGI) ➔ MySQL / Redis のマルチコンテナ連携。
- **横断的関心事**: SSL/TLS証明書配置 (`docker/web-nginx/certs/`) によるセキュア通信、ConoHa等のVPS環境へのデプロイメント自動化 (`.github/workflows/deploy.yml`)。
