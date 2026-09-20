---
created: 2026-09-20
tags: [docker, architecture, composer, nginx, mysql]
status: active
---

# Docker-Laravel アーキテクチャ仕様

本環境は、コンテナ化されたマイクロサービス指向のローカル開発・テスト環境です。`docker-compose.yml` および `docker-compose.base.yml` を基盤に構築されています。

## コンテナ構成図と連携

1. **Web (Nginx)**:
   - ポート `80` / `443` を公開し、外部からのリクエストを受信。
   - `docker/web-nginx/default.conf.template` を用いて、FastCGI経由でPHPコンテナにリクエストを転送。
2. **App (PHP-FPM)**:
   - `app-src/` ディレクトリをボリュームマウントし、Laravelアプリケーションのソースコードをリアルタイムで反映。
   -Composer, Node.js, 必要なPHP拡張（PDO, Mbstring, BCMath等）を内包。
3. **Database (MySQL)**:
   - 永続ボリューム (`mysql-volume/`) を使用し、データの喪失を防止。
4. **Cache / Queue (Redis)**:
   - セッション管理、キャッシュ、キューワーカー用。

## 環境変数と拡張性

- `.env.example.doker` をベースに環境変数 (`.env`) を設定。
- 各種PHPバージョン（`php81.ini`, `php82.ini`, `php84.ini`）およびMySQLバージョンを必要に応じて切り替え可能。
