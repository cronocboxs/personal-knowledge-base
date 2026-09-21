---
created: 2026-09-21
updated: 2026-09-21
tags: [Docker-Laravel, spec, code-analysis, infrastructure]
phase: 3
status: active
unexplored_domains: []
---

# Docker-Laravel インフラ・構成詳細・処理仕様ナレッジ

## 1. 識別された機能・インターフェース一覧 (Phase 1 完了)
- [x] Dockerコンテナ定義群 (`docker/`) -> nginx, php-fpm, mysql, reverb, ngrok
- [x] GitHub Actions デプロイワークフロー (`.github/workflows/deploy.yml`)
- [x] 環境変数設定テンプレート (`.env.example.doker`)
- [x] インフラ構築・運用ドキュメント (`ConoHa.md`, `README.md`)

## 2. インターフェース・トリガー別詳細トレース (Phase 2 完了)

### 機能1: コンテナオーケストレーションとビルド・起動処理
#### トリガー: 「`docker compose up -d --build` の実行」
- **入力・要求（Input/Request）**:
  - ルートの `docker-compose.yml` (シンボリックリンクまたは実体) および `docker-compose.base.yml`
  - 環境変数設定ファイル (`.env`)
- **内部処理流転（Execution Flow）**:
  1. `docker-compose.base.yml` に定義された各サービス（`app-php`, `web-nginx`, `db-mysql`, `db-mysql-test`, `reverb-php`, `redis`, `memcached`, `mail-mailhog`, `ngrok`）のビルドコンテキストとイメージを読み込み。
  2. `app-php`: 指定された Dockerfile (`docker/app-php/Dockerfile`) から PHP-FPM コンテナをビルドし、ソースコード (`app/`) および PHP 設定 (`php84.ini`)、SSL 証明書をマウント。
  3. `web-nginx`: Nginx コンテナをビルドし、テンプレート (`default.conf.template`) および SSL 証明書をマウント。
  4. `db-mysql` / `db-mysql-test`: MySQL コンテナをビルドし、my.cnf 設定と永続ボリューム (`mysql-volume`, `mysql-test-volume`) を割り当て、Innodb バッファプールサイズなどの起動オプションを適用。
  5. `reverb-php`: WebSocket サーバー（Laravel Reverb）を起動し、Redis コンテナとの依存関係を解決。
- **出力・応答・状態変化（Output/Response/State Change）**:
  - **成功時**: 各コンテナが正常にバックグラウンド起動し、指定されたポート（Web: 80/443, DB: 3306/3307, Reverb: 8080 等）でリクエスト受付状態になる。
  - **失敗時**: ポート競合やビルドコンテキストのパス不整合によるエラー終了。

### 機能2: 自動デプロイ処理 (GitHub Actions)
#### トリガー: 「`main` ブランチへの `push`」
- **入力・要求（Input/Request）**:
  - GitHub Actions のトリガー (`push` to `main`)
  - GitHub Secrets に登録された接続情報 (`CONOHA_DOCKER_20250809_SSH_HOST`, `SSH_PORT`, `SSH_PRIVATE_KEY`, `SSH_USERNAME`)
- **内部処理流転（Execution Flow）**:
  1. `appleboy/ssh-action` を利用して ConoHa VPS サーバーに SSH 接続。
  2. 作業ディレクトリ (`~/Work/Docker-Laravel`) に移動し、最新のコードを `git fetch` および `git reset --hard origin/main` で強制同期。
  3. 既存のコンテナ群を安全に停止・削除 (`docker compose ... down --remove-orphans`)。
  4. アプリケーション用コンテナ (`app-php`) のみを先行ビルド・起動 (`up -d --build app-php`)。
  5. コンテナ起動待機後、`composer install --no-dev --optimize-autoloader` および `npm install && npm run build` をコンテナ内で実行。
  6. 残りのインフラサービス（`web-nginx`, `db-mysql`, `redis`, `reverb-php` 等）を起動。
  7. Laravel 最適化コマンド (`artisan config:cache`, `route:cache`) を実行。
- **出力・応答・状態変化（Output/Response/State Change）**:
  - **成功時**: 本番サーバー上のコンテナ群が最新コードおよびビルド済みアセットで稼働状態になり、GitHub Actions がグリーン（成功）で終了。
  - **失敗時**: SSH 接続エラー、メモリ不足によるビルド失敗、マイグレーション/キャッシュエラーによる中断。

## 3. モジュール間連携・例外ハンドリング・設計パターン (Phase 3 完了)
- **コンポーネント間・ドメイン間の相互作用**:
  - `Docker-Laravel` はインフラストラクチャ層（Docker, Nginx, MySQL, Redis, Reverb）を完全にカプセル化し、実アプリケーション（`app-src/`）とはシンボリックリンクおよびボリュームマウントによって疎結合に連携する。
- **横断的関心事**:
  - **環境分離**: 開発環境ではローカル証明書（`mkcert`）を用いた HTTPS 通信、本番環境では GitHub Actions と Secrets によるセキュアな自動デプロイメントを実現。
  - **リソース管理**: メモリ制限（`--max-old-space-size=1024`）やコンテナの依存関係管理（`depends_on`）により、安定したコンテナライフサイクルを維持。
