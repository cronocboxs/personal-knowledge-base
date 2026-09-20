---
title: "Docker-Laravel リポジトリ詳細実装仕様"
type: "specification"
repository: "Docker-Laravel"
created_at: "2026-09-20"
updated: 2026-09-20
phase: 2
---

# Docker-Laravel 詳細実装仕様

## 1. 概要
Docker-Laravelは、Docker環境下でLaravelアプリケーションを迅速に構築・運用するための開発用テンプレート・環境構成リポジトリです。

## 2. ディレクトリ構成と主要ファイル
- `docker/`: 各ミドルウェア（Nginx, PHP-FPM, MySQL等）のDockerfileや設定ファイルを配置。
- `app-src/`: Laravelアプリケーションのソースコード置き場。
- `docker-compose.base.yml`: Docker環境のベースとなるコンテナ構成定義。
- `ConoHa.md`: ConoHa VPS環境へのデプロイ・運用手順書。

## 3. インフラ・コンテナ構成
- Webサーバー: Nginx
- アプリケーションサーバー: PHP-FPM
- データベース: MySQL
- キャッシュ/キュー: Redis (`redis-volume/`)

## 4. 運用・デプロイに関する知見
`ConoHa.md` に記載がある通り、本環境はローカル開発だけでなく、ConoHaなどのVPS上での本番・ステージング運用も想定した設計になっています。
