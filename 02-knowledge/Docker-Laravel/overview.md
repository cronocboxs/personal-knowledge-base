---
created: 2026-09-20
updated: 2026-09-20
tags: [Docker-Laravel, spec, code-analysis]
phase: 3
status: active
unexplored_domains: []
---

# Docker-Laravel リポジトリ 挙動・処理仕様ナレッジ

## 1. 識別された機能・インターフェース一覧 (Phase 1)
- [x] Docker開発環境構築定義 (`docker-compose.base.yml`)
- [x] Nginx Webサーバー設定 (`docker/web-nginx/`)
- [x] MySQL データベースコンテナ設定 (`docker/db-mysql/`)
- [x] PHP-FPM アプリケーションコンテナ設定 (`docker/app-php/`)
- [x] Reverb (Laravel WebSocket) サービス定義 (`docker/reverb-php/`)
- [x] 動作確認用静的エントリーポイント (`app-src/public/phpinfo.php`)

## 2. インターフェース・トリガー別詳細トレース (Phase 2)

### 機能1: Nginx & PHP-FPM Webリクエスト処理
#### トリガー: 「HTTPリクエスト (Port 80/443)」
- **入力・要求（Input/Request）**:
  - クライアントからのHTTP/HTTPSリクエスト。
- **内部処理流転（Execution Flow）**:
  1. Nginx (`docker/web-nginx/default.conf.template`) がリクエストを受信。
  2. 静的ファイルの場合は直接返却、PHPスクリプトの場合は FastCGI 経由で `app-php` コンテナ（Port 9000等）へ転送。
  3. `app-php` (`app-src/public/phpinfo.php` 等) が実行され処理結果を返す。
- **出力・応答・状態変化（Output/Response/State Change）**:
  - **成功時**: HTTP 200 OK およびPHP情報やレスポンスの返却。
  - **失敗時**: 502 Bad Gateway (PHP-FPM未起動時など) や 404 Not Found。

### 機能2: データベース初期化・接続
#### トリガー: 「MySQLコンテナ起動 / DB接続要求」
- **入力・要求（Input/Request）**:
  - 環境変数で指定されたDBユーザー、パスワード、データベース名。
- **内部処理流転（Execution Flow）**:
  1. `docker/db-mysql/Dockerfile` および設定ファイル (`my.cnf`, `my80.cnf`等) に基づき MySQL デーモン起動。
  2. 初期化スクリプト実行、ネットワーク経由で `app-php` からの接続を受け付け。
- **出力・応答・状態変化（Output/Response/State Change）**:
  - **成功時**: MySQL接続確立、クエリ実行可能状態。

## 3. モジュール間連携・例外ハンドリング・設計パターン (Phase 3)
- **コンポーネント間・ドメイン間の相互作用**:
  - Docker Compose ベースで Nginx, PHP-FPM, MySQL, Reverb, Redis が連携するマルチコンテナ構成。
- **横断的関心事**:
  - 環境変数による一元的なコンフィグ管理、ログ・ボリューム永続化 (`redis-volume`)。
