---
created: 2026-09-21
updated: 2026-09-22
tags: [Docker-Laravel, spec, code-analysis, infrastructure, deep-logic]
phase: 5
status: active
unexplored_domains: []
---

# Docker-Laravel インフラ・構成詳細・最深部ロジック仕様ナレッジ

## 1. 識別された機能・インターフェース一覧 (Phase 1 完了)
- [x] Dockerコンテナ定義群 (`docker/`) -> nginx, php-fpm, mysql, reverb, ngrok
- [x] GitHub Actions デプロイワークフロー (`.github/workflows/deploy.yml`)
- [x] 環境変数設定テンプレート (`.env.example.doker`)
- [x] インフラ構築・運用ドキュメント (`ConoHa.md`, `README.md`)
- [x] Laravel Reverb リアルタイムWebSocket通信インフラ・プロキシ設定 (`docker/reverb-php/reverb.md`)

## 2. インターフェース・トリガー別詳細トレース (Phase 2 & Phase 4 必須)

### 機能1: コンテナオーケストレーションとビルド・起動処理
#### トリガー: 「`docker compose up -d --build` の実行」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: ルートの `docker-compose.yml` および `docker-compose.base.yml` によるサービス定義のロード。
  2. **サービス・ドメイン層**:
     - `app-php`: `docker/app-php/Dockerfile` から PHP 8.4-fpm ベースイメージをプル。`apt-get` を用いて `git`, `unzip`, `cron`, `vim`, `procps`, `npm`, `libzip-dev`, `libicu-dev`, `libonig-dev`, `libsqlite3-dev`, `default-mysql-client`, `libmemcached-dev`, `libpng-dev`, `imagemagick`, `libmagickwand-dev`, `ffmpeg` を一括インストール。
     - `docker-php-ext-install` により `intl`, `pdo_mysql`, `pdo_sqlite`, `zip`, `bcmath`, `sockets`, `mbstring`, `mysqli`, `gd` 拡張をビルド。
     - `pecl` コマンドで `igbinary`, `memcached`, `redis`, `imagick` 拡張をビルドおよび `docker-php-ext-enable` で有効化。
     - 公式 Composer イメージ (`composer:2.0`) から `/usr/bin/composer` をコピー。
     - サービス起動時に `/etc/init.d/cron start` を実行し、ワーキングディレクトリを `/app` に設定。
  3. **内部プライベート関数・ヘルパー (Nginx / Web層)**:
     - `docker/web-nginx/Dockerfile` から Alpine ベースの Nginx 1.29 コンテナをビルド。
     - `default.conf.template` を基に環境変数（`NGINX_SERVER_NAME`, `SSL_CERT_FILE`, `SSL_KEY_FILE`）を動的展開。
     - ポート 80 では Let's Encrypt 認証用パス (`/.well-known/acme-challenge/`) を `/var/www/html` に直結し、その他はすべて HTTPS (`301 Moved Permanently`) へリダイレクト。
     - ポート 443 では SSL 証明書・秘密鍵をロードし、WebSocket（Laravel Reverb）用パス `/app/` に対するプロキシパス (`http://reverb-php:8080/app/`) を構築。`Upgrade` および `Connection` ヘッダーを書き換えて WebSocket の双方向通信（タイムアウト 3600 秒）を維持。
     - PHP リクエスト (`~ \.php$`) は `app-php:9000` の FastCGI サーバーへ転送し、`SCRIPT_FILENAME` や `HTTPS on` などのパラメータを付与。
  4. **データ永続化・低層処理 (MySQL層)**:
     - `docker/db-mysql/` 内のバージョン別設定（`my57.cnf`, `my80.cnf`, `my84.cnf`, `my.cnf`）に基づき、MySQL コンテナ起動時にストレージエンジン設定、文字コード（`utf8mb4`）、バッファプールサイズを適用。
     - 永続ボリューム (`mysql-volume`, `mysql-test-volume`) を通じてデータベースファイルの状態をホスト側と隔離しつつ永続化。
  5. **副作用・非同期イベント**:
     - コンテナ間の依存関係 (`depends_on`) に従い、データベースや Redis、Reverb サーバーが準備完了した後にアプリケーションコンテナが稼働。

### 機能2: 自動デプロイ処理 (GitHub Actions)
#### トリガー: 「`main` ブランチへの `push`」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: `.github/workflows/deploy.yml` のトリガー発火。
  2. **サービス・ドメイン層**: `appleboy/ssh-action` を介してリモート VPS へ接続。
  3. **内部プライベート関数・ヘルパー**:
     - ワークディレクトリへの移動と `git reset --hard origin/main` によるコードの強制同期。
     - `docker compose down --remove-orphans` による既存コンテナの安全な破棄と解放。
     - `docker compose up -d --build app-php` によるアプリケーションコンテナの単独先行ビルドと起動。
  4. **データ永続化・低層処理**:
     - コンテナ内での `composer install --no-dev --optimize-autoloader`（依存関係の最適化インストール）および `npm install && npm run build`（フロントエンドアセットのコンパイル）。
     - 残りインフラコンテナ（Nginx, MySQL, Redis, Reverb）の起動。
     - `php artisan config:cache`, `php artisan route:cache` によるフレームワークの最適化。
  5. **副作用・非同期イベント**:
     - 本番環境におけるゼロダウンタイムに近い構成でのサービス再起動とエンドポイントの疎通状態への移行。

- **成功/失敗時の最深部挙動**:
  - 失敗時は SSH 接続断または Docker ビルドエラーにより GitHub Actions が停止し、VPS 側の古いコンテナが維持またはクリーンアップされる。

### 機能3: Laravel Reverb WebSocket リアルタイム通信基盤
#### トリガー: 「ブラウザからの `wss://` 接続および Laravel からのイベントブロードキャスト」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: ブラウザからの `wss://<host>/app/<key>` リクエストが Nginx (`docker/web-nginx/default.conf.template`) で受信される。
  2. **サービス・ドメイン層**: Nginx のプロキシ設定により、HTTP ヘッダー (`Upgrade`, `Connection`) が書き換えられ、`http://reverb-php:8080/app/` へ転送される。
  3. **内部プライベート関数・ヘルパー**:
     - `reverb-php` コンテナ (`docker/reverb-php/Dockerfile`) 内で実行される `php artisan reverb:start --host=0.0.0.0 --port=8080` がリクエストを処理。
     - 依存する `pcntl`, `sockets`, `redis` PHP 拡張を介して、高パフォーマンスな非同期イベント駆動ループを維持。
  4. **データ永続化・低層処理**:
     - Laravel アプリケーション層 (`app-php`) から `BROADCAST_CONNECTION=reverb` を通じて発火されたイベントが、Redis Pub/Sub バックエンドを経由して Reverb サーバーへと同期。
  5. **副作用・非同期イベント**:
     - 接続されたクライアント群へのリアルタイムメッセージプッシュと、接続維持のための Ping/Pong 制御。

## 3. 再走査・深層比較ログ (Phase 5)
- **最終再走査日**: 2026-09-22
- **発掘された未確認領域・補全履歴**:
  - 2026-09-21: Phase 1〜3 によるインフラ構成・デプロイフローの全体目録化および一巡トレース完了。
  - 2026-09-22: Phase 4 に基づく `docker/app-php/Dockerfile` のパッケージ群・拡張モジュール、`default.conf.template` の Nginx プロキシ・FastCGI パラメータの最深部ロジック追跡・加筆を実施。
  - 2026-09-22: Phase 5 の再走査・差分発掘により `docker/reverb-php/reverb.md` に記載されている Laravel Reverb の WebSocket プロキシ構成・Redis Pub/Sub 連携・Dockerfile 依存関係（`pcntl`, `sockets`, `redis`）の深層ロジックを発掘し、仕様ナレッジとして完全統合。新たな未確認領域は0件となり、完全網羅を達成。
