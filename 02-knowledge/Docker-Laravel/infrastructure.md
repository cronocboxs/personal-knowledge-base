---
created: 2026-09-20
updated: 2026-09-20
tags: [Docker-Laravel, spec, code-analysis, infrastructure]
phase: 3
status: active
unexplored_domains: []
---

# Docker-Laravel インフラ構造・コンテナ仕様ナレッジ (Phase 3 完了)

## 1. 識別されたコンテナ・インフラサービス一覧 (Phase 1)
- [x] `app-php`: PHP-FPM（PHP 8.1 / 8.2 / 8.4）コンテナ
- [x] `web-nginx`: Nginx Webサーバー（SSL/TLS, HTTP/HTTPS, テンプレート対応）
- [x] `db-mysql`: MySQL メインデータベースコンテナ
- [x] `db-mysql-test`: MySQL テスト用データベースコンテナ（Healthcheck対応）
- [x] `reverb-php`: Laravel Reverb WebSocketサーバーコンテナ
- [x] `mail-mailhog`: MailHog メールキャプチャコンテナ
- [x] `memcached`: Memcached キャッシュサーバー
- [x] `redis`: Redis キャッシュ/キューサーバー
- [x] `ngrok`: Ngrok トンネリングコンテナ

---

## 2. インターフェース・トリガー別詳細トレース (Phase 2)

### サービス起動・構築トリガー (`docker compose up -d --build`)
- **入力・要求（Input/Request）**:
  - ルートの `docker-compose.yml`（`docker-compose.base.yml` へのシンボリックリンク）および `.env` で定義された環境変数（`BASEDIR`, `APP_ENV`, ポート番号等）。
- **内部処理流転（Execution Flow）**:
  1. `docker-compose.base.yml` の定義に従い、各サービスの `build.context`（通常は `./app-src/<app-name>` またはローカル）から各 Dockerfile を読み込んでイメージをビルド。
  2. ボリュームマウントの設定に基づき、ホスト側のアプリケーションソース（`app/`）や設定ファイルをコンテナ内にバインド。
  3. ネットワークおよび依存関係（`depends_on`）の順序に従ってコンテナ群を起動。
- **出力・応答・状態変化（Output/Response/State Change）**:
  - **成功時**: `app-php`, `web-nginx`, `db-mysql` 等のコンテナがバックグラウンドで起動し、ホスト側の指定ポート（HTTP: 80/443, MySQL: 3307, MailHog: 8025等）でアクセス可能になる。
  - **失敗時**: ポート競合や `.env` のパス不整合によるビルドエラー・起動失敗。

### CI/CD デプロイメント機能 (`.github/workflows/deploy.yml`)
- **トリガー**: `main` ブランチへの Push。
- **内部処理流転（Execution Flow）**:
  1. `appleboy/ssh-action` を利用して ConoHa VPS に SSH 接続（秘密鍵・ポート番号を GitHub Secrets から取得）。
  2. サーバー上の `~/Work/Docker-Laravel` に移動し、`git fetch origin main && git reset --hard origin/main` でコードを最新化。
  3. `docker compose down --remove-orphans` で既存コンテナをクリーンアップ。
  4. まず `app-php` コンテナをビルド・起動し、コンテナ内で `composer install` および `npm install && npm run build` を実行。
  5. 残りのインフラサービス（`web-nginx`, `db-mysql`, `redis`, `reverb-php` 等）を起動。
  6. `php artisan config:cache` および `php artisan route:cache` を実行して Laravel を最適化。
- **出力・応答・状態変化**:
  - 本番サーバー上でのコンテナ群の自動更新・ビルド完了。

---

## 3. モジュール間連携・例外ハンドリング・設計パターン (Phase 3 完了)
- **コンテナ間ネットワークと連携**:
  - `web-nginx` はリバースプロキシとして動作し、PHPのリクエストを `app-php`（PHP-FPM）へ転送。
  - アプリケーションは `db-mysql` (MySQL) や `redis`, `memcached` に内部ネットワーク経由で接続。
- **外部ストレージ・ボリューム永続化**:
  - MySQLのデータは Docker Volume (`mysql-volume`, `mysql-test-volume`) に永続化され、コンテナの再作成時もデータが保持される。
  - MailHogのメールデータもバインドマウント（`mail-volume`）により保持。
- **設計パターン**:
  - **インフラとアプリの分離**: インフラ設定（Docker-Laravel）とアプリケーションロジック（minLaravel等）を別リポジトリにし、シンボリックリンクおよび環境変数（`BASEDIR`）で柔軟に結合するマルチテナント/マルチプロジェクト対応設計。
