---
created: 2026-09-20
updated: 2026-09-20
phase: 3
tags: [docker-laravel, architecture, php, nginx, mysql, reverb, multi-version]
status: active
---

# Docker-Laravel アーキテクチャ・設計思想仕様 (Phase 3)

本ドキュメントでは、`Docker-Laravel` リポジトリにおけるマルチPHP環境・コンテナ設計、および開発・本番運用を見据えたインフラストラクチャ設計思想を詳細に解説します。

---

## 1. インフラアーキテクチャ方針

`Docker-Laravel` は、ローカル開発環境から本番ステージング環境までシームレスに再現可能なDocker Compose構成を提供します。各ミドルウェア（PHP, Nginx, MySQL, Redis, Reverb）を独立したコンテナとして分割し、Dockerネットワーク経由で結合する **マイクロサービス指向のローカル開発インフラ** を採用しています。

### コンテナ責務と構成
- **PHP Application (`docker/app-php/`)**:
  - マルチPHPバージョン（PHP 8.1, 8.2, 8.4）をそれぞれの Dockerfile (`Dockerfile`, `Dockerfile.81-base`, etc.) で管理。
  - Composer, Xdebug, GD, PDO, BCMathなどの必要なPHP拡張モジュールをあらかじめビルドに組み込み。
- **Web Server (`docker/web-nginx/`)**:
  - Nginxをリバースプロキシ兼Webサーバーとして配置。ホストからのリクエストを受け付け、FastCGI（Port 9000等）を介してPHPコンテナへ転送。
- **Database (`docker/db-mysql/`)**:
  - MySQL 5.7 / 8.0 / 8.4 の各バージョン別設定 (`my.cnf`, `my57.cnf` 等) を提供し、レガシーから最新バージョンまでの互換性テストをサポート。
- **Realtime / Queue (`docker/reverb-php/`)**:
  - Laravel 11以降で標準となった Laravel Reverb（WebSocketサーバー）の常駐コンテナ構成。

---

## 2. コンテナ間連携フローとデータ永続化

```
[Host Browser / HTTP Request (Port 80/443)]
       │
       ▼
[Nginx Container (`docker/web-nginx`)]
       │
       ├─► Static Assets (`public/` volume mount)
       │
       └─► FastCGI Proxy (TCP `app-php:9000`)
             │
             ▼
      [PHP Application Container (`docker/app-php`)]
             │
             ├─► Database Query (TCP `db-mysql:3306`)
             ├─► Cache / Session (TCP `redis:6379`)
             └─► WebSocket Broadcast (TCP `reverb-php:8080`)
```

### ボリュームマウント戦略
- ソースコードディレクトリはホストからコンテナへバインドマウントされ、リアルタイムなコード変更の反映（Hot-reload / Laravel Octane / Vite連携）を実現。
- データベースの実データ (`mysql_data`) やログは Docker Volume によりコンテナライフサイクルから独立して永続化。

---

## 3. 設計思想と運用メリット
- **環境差異の排除 (Environment Parity)**: 開発チーム全員が同一のPHP拡張バージョンやMySQLバージョンをコンテナで強制することで、「動かないバグ」を防止。
- **マルチバージョン・柔軟性**: 複数PHPバージョンを切り替えることで、Laravelのバージョンアップ時における互換性検証を容易化。
