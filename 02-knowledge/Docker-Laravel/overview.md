---
title: "Docker-Laravel リポジトリ解析・最深部ロジックナレッジ"
repo: "Docker-Laravel"
phase: 3
unexplored_domains: []
created_at: "2026-09-25"
updated_at: "2026-09-25"
---

# Docker-Laravel リポジトリ概要

## 1. 目的とスコープ
Docker-Laravel は、Docker環境上でのLaravelアプリケーションの構築・運用を効率化するためのボイラープレート・インフラ構成リポジトリです。本ナレッジでは、Dockerコンテナ構成、Nginx/PHP-FPM/データベースの連携、および Laravel アプリケーションのエントリーポイントから最深部までの動作をトレースします。

## 2. インターフェース・最深部処理トレース

### 2.1 コンテナオーケストレーション（`docker-compose.base.yml`）
- **app-php**: PHP 8.4 ベースのアプリケーションコンテナ。ビルドコンテキストをベースディレクトリに設定し、ソースコードや php.ini、SSL証明書をボリュームマウント。Vite開発サーバー用のポート（5173）も公開。
- **reverb-php**: Laravel Reverb によるWebSocketサーバーコンテナ。`php artisan reverb:start` を常時実行し、Redisと連携。
- **web-nginx**: Nginx Webサーバーコンテナ。HTTP（80）およびHTTPS（443）ポートをホストに公開し、`default.conf.template` をテンプレートとして使用、SSL証明書をマウント。
- **db-mysql / db-mysql-test**: MySQL データベースコンテナ（本番/開発用およびテスト用）。`innodb-buffer-pool-size=512M` 設定、およびテスト用コンテナにはヘルスチェックを完備。
- **補助コンテナ**: MailHog（メールキャプチャ）、Memcached、Redis、ngrok（トンネリング）を完備した統合開発環境。

### 2.2 Dockerfile 構成とビルド最深部
- **app-php (`docker/app-php/Dockerfile`)**: Composerのインストール、必要なPHP拡張モジュールのビルド、システム依存関係のセットアップ。
- **web-nginx (`docker/web-nginx/Dockerfile`)**: Nginxのベースイメージを元に、設定ファイルやSSL証明書の配置ディレクトリを構築。
- **db-mysql (`docker/db-mysql/Dockerfile`)**: MySQLの初期設定、`my.cnf` の最適化チューニングを適用。
