---
created: 2026-09-20
updated: 2026-09-20
tags: [KaMeToKo, spec, code-analysis, laravel]
phase: 1
status: active
unexplored_domains:
  - "認証機能・アカウント管理 (Login, Google, Passkey, Register, Password Reset) (`app/Http/Controllers/Auth/`, `routes/web/login.php`)"
  - "プロバイダー・テナント管理機能 (`app/Http/Controllers/Provider/`, `routes/web/provier.php`)"
  - "ユーザー機能・マイページ・カレンダー (`app/Http/Controllers/User/`, `routes/web/user.php`)"
  - "システム管理機能 (`app/Http/Controllers/System/`, `routes/web/system.php`)"
  - "サービス個別機能（勤怠管理、会計・請求、予約管理、チャット、ストア） (`app/Http/Controllers/Service/`, `routes/web/service.php`)"
  - "DB基盤・CRUDコントローラー (`app/Http/Controllers/Db/`)"
  - "APIおよび非同期処理・イベント (`app/Http/Controllers/Api/`, `app/Events/`, `app/Jobs/`, `routes/api.php`)"
---

# KaMeToKo リポジトリ 挙動・処理仕様ナレッジ (Overview)

## 1. 技術スタック・アーキテクチャ概要 (Phase 1)
- **フレームワーク**: Laravel 12 (PHP ^8.4)
- **フロントエンド / 通信**: Inertia.js (`inertiajs/inertia-laravel`), Blade, Tailwind/Vite
- **主要パッケージ**: 
  - 認証・認可: Laravel Sanctum, Laravel Socialite (Google Auth), Laravel Passkeys, Spatie Laravel Permission
  - リアルタイム・チャット: Laravel Reverb (`laravel/reverb`)
  - ファイル・データ処理: Alexusmai Laravel File Manager, PhpSpreadsheet
- **リポジトリ構造**: マルチテナント型Webアプリケーション（システム管理者、プロバイダー/テナント管理者、一般ユーザー、各種サービスモジュール（勤怠・会計・予約・チャット・ストア等）を包括する統合プラットフォーム）。

## 2. ルーティングおよびエントリーポイント一覧
- `routes/web.php`: メインWebルート（プレフィクス・ミドルウェア設定）
- `routes/web/login.php`: 認証系ルート
- `routes/web/provier.php`: プロバイダー管理ルート
- `routes/web/user.php`: ユーザー向けルート
- `routes/web/system.php`: システム管理者ルート
- `routes/web/service.php`: 各種サービス（勤怠・予約等）ルート
- `routes/api.php`: APIルート
- `routes/channels.php`: リアルタイムブロードキャストチャンネル
- `routes/console.php`: Artisanコマンド定義

## 3. 未解析領域 (unexplored_domains)
現在、全モジュールの個別トリガー・内部処理フロー詳細が未着手のため、以下のドメインを `unexplored_domains` に登録し順次解読・トレースを行う。
