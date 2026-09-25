---
title: "Docker-Laravel リポジトリ解析・最深部ロジックナレッジ"
repo: "Docker-Laravel"
phase: 2
unexplored_domains:
  - "docker/app-php/Dockerfile"
  - "docker/web-nginx/default.conf.template"
  - ".github/workflows/deploy.yml"
created_at: "2026-09-25"
updated_at: "2026-09-25"
---

# Docker-Laravel リポジトリ概要

## 1. 目的とスコープ
Docker-Laravel は、PHP (8.1/8.2/8.4)、Nginx、MySQL、Laravel Reverb (WebSocket) を含むマルチコンテナ環境のLaravel開発・本番デプロイ基盤テンプレートです。

## 2. インターフェース・最深部処理トレース

### 2.1 コンテナ構成とエントリーポイント
- **Docker Compose (`docker-compose.base.yml`)**: アプリケーションPHPコンテナ、Nginx Webサーバー、MySQLデータベース、Reverbコンテナのオーケストレーションを定義。
- **PHP Container (`docker/app-php/Dockerfile`)**: PHP extensions (GD, Zip, BCMath, PDO MySQL等) のビルドとComposerのセットアップを担う最深部ビルドレイヤー。
- **Nginx Config (`docker/web-nginx/default.conf.template`)**: リバースプロキシ設定、SSL/TLS終端、Laravelの `public/index.php` へのルーティングディスパッチ。

### 2.2 CI/CD パイプライン
- **GitHub Actions (`.github/workflows/deploy.yml`)**: ConoHa VPS等への自動デプロイメント、SSH接続、コンテナビルド・マイグレーション実行の自動化フロー。
