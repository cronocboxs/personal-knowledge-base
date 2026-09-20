---
created: 2026-09-20
tags: [docker, laravel, environment, php, nginx, mysql]
status: active
---

# Docker-Laravel 概要

本リポジトリ (`Docker-Laravel`) は、Laravelアプリケーション開発のための高度にカスタマイズ可能なDocker開発環境（および簡易本番運用環境）を提供します。マルチPHPバージョン（PHP 8.1, 8.2, 8.4）やMySQL、Nginx、Redis、Laravel Reverbを組み合わせた柔軟な構成を特徴としています。

## 主な構成要素

- **PHP Application (`docker/app-php/`)**:
  - PHP 8.1 / 8.2 / 8.4 に対応したカスタムDockerfile (`Dockerfile`, `Dockerfile.81-base`, etc.) および専用の `php.ini` 設定群。
- **Web Server (`docker/web-nginx/`)**:
  - NginxコンテナとSSL証明書（Let's Encrypt / 自己署名証明書用テンプレート）を含み、リバースプロキシおよびLaravelのフロントコントローラー (`public/index.php`) へのルーティングを担当。
- **Database (`docker/db-mysql/`)**:
  - MySQL 5.7 / 8.0 / 8.4 の各バージョンに対応した設定 (`my.cnf`, `my57.cnf`, `my80.cnf`, `my84.cnf`)。
- **Realtime / Queue (`docker/reverb-php/`)**:
  - Laravel Reverb（WebSocketサーバー）用のDocker設定およびドキュメント。
- **Tunnel (`docker/ngrok/`)**:
  - 外部公開・Webhook検証用の `ngrok.yml`。

## デプロイメント・CI/CD

- `.github/workflows/deploy.yml` により、ConoHa等のVPS環境への自動デプロイやSSH経由でのリモートビルドをサポート。
- `ConoHa.md` にVPS構築手順が詳細にまとめられている。
