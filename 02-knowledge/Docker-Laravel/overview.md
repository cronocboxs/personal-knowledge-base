---
created: 2026-09-20
updated: 2026-09-20
tags: [Docker-Laravel, spec, code-analysis, overview]
phase: 3
status: active
unexplored_domains: []
---
# Docker-Laravel リポジトリ概要・機能目録 (Phase 1)

## 1. 技術スタック・アーキテクチャ判定
- **リポジトリ種別**: Docker Infrastructure & Template for Laravel Web/API Application
- **主要言語**: Dockerfile (Container), Bash, PHP (PHP 8.1 / 8.2 / 8.4 configurations)
- **インフラ・構成**:
  - **Web Server**: Nginx (`docker/web-nginx/`) with SSL/TLS support (`mkcert`)
  - **Application Server (PHP-FPM)**: Multi-version PHP support (`docker/app-php/` with php81, php82, php84.ini)
  - **Database**: MySQL (`docker/db-mysql/` with my57.cnf, my80.cnf, my84.cnf)
  - **WebSocket / Reverb**: Laravel Reverb container (`docker/reverb-php/`)
  - **Tunneling**: Ngrok (`docker/ngrok/`)
- **アプリケーションソース配置**: `app-src/` (外部Laravelプロジェクトを配置またはサブモジュールとして組み込む前提)

---

## 2. エントリーポイント・主要コンポーネント一覧
- **インフラ定義**:
  - `docker-compose.base.yml` / `docker-compose.yml` (ルートのsymlink)
  - `docker/web-nginx/Dockerfile`, `default.conf.template`
  - `docker/app-php/Dockerfile`
  - `docker/db-mysql/Dockerfile`
  - `docker/reverb-php/Dockerfile`
- **CI/CD**:
  - `.github/workflows/deploy.yml`
- **マニュアル・ガイド**:
  - `README.md` (利用方法、セットアップ、トラブルシューティング)
  - `ConoHa.md` (ConoHa VPSへのデプロイ・運用メモ)
  - `docker/reverb-php/reverb.md` (Reverb解説)

---

## 3. 未解析領域（`unexplored_domains`）
- `docker/` (各コンテナのDockerfileおよび設定ファイル詳細)
- `.github/workflows/deploy.yml` (CI/CDワークフロー詳細)
- `ConoHa.md` / `README.md` (運用手順・インフラ構成詳細)
