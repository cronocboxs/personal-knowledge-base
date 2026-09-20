---
created: 2026-09-20
updated: 2026-09-20
tags: [KaMeToKo, spec, code-analysis, overview]
phase: 2
status: active
unexplored_domains:
  - "認証機能 (Auth / Login / Register / Passkey / GoogleAuth) (`app/Http/Controllers/Auth/`)"
  - "プロバイダ管理・機能 (`app/Http/Controllers/Provider/`)"
  - "ユーザー個人機能 (`app/Http/Controllers/User/`)"
  - "システム管理機能 (`app/Http/Controllers/System/`)"
  - "DB管理・データベース連携 (`app/Http/Controllers/Db/`)"
  - "APIエンドポイント機能 (`app/Http/Controllers/Api/`)"
  - "サービス個別機能（勤怠・会計・予約・ストア） (`app/Http/Controllers/Service/`)"
---

# KaMeToKo リポジトリ概要・機能目録 (Phase 1)

## 1. 技術スタック・アーキテクチャ判定
- **言語**: PHP 8.4
- **フレームワーク**: Laravel 12.0
- **フロントエンド / UI**: Inertia.js (Inertia-Laravel), Vite, Laravel UI, Vue / Blade (推測)
- **主要ライブラリ**:
  - `alexusmai/laravel-file-manager`: ファイルマネージャー
  - `google/apiclient`: Google API連携
  - `inertiajs/inertia-laravel`: SPA構築 (Inertia.js)
  - `laravel/passkeys`: パスキー認証
  - `laravel/reverb`: リアルタイムWebSocket通信 (Laravel Reverb)
  - `laravel/sanctum`: API認証
  - `laravel/socialite`: SNSログイン (Google等)
  - `spatie/laravel-data`: DTO / データオブジェクトマッピング
  - `spatie/laravel-permission`: ロール・権限管理
  - `phpoffice/phpspreadsheet`: Excel/Spreadsheet操作
  - `simshaun/recurr`: 予約・カレンダー等の繰り返しルール処理

## 2. エントリーポイント・ルーティング一覧
- **Webルーティング (`routes/web.php`)**: アプリケーションのメイン画面、認証、ユーザーポータル、プロバイダ管理機能のルーティング。
- **APIルーティング (`routes/api.php`)**: 外部・内部APIエンドポイント。
- **コンソール・CLI (`routes/console.php`, `artisan`)**: バックグラウンド処理・メンテナンスコマンド。
- **チャンネル (`routes/channels.php`)**: Reverb等によるリアルタイム通信用ブロードキャストチャンネル。

## 3. 主要モジュール・コントローラー群 (Phase 1 目録)
1. **認証モジュール (`app/Http/Controllers/Auth/`)**
   - Login, Register, Forgot/Reset Password, Passkey, GoogleAuth
2. **プロバイダモジュール (`app/Http/Controllers/Provider/`)**
   - Dashboard, Room (チャット), Join/Apply, Invite, ChatMessage, Role, Switch, Profile, Attachment
3. **ユーザーモジュール (`app/Http/Controllers/User/`)**
   - Profile, EmailChange, Notify, Calendar, Attachment, List
4. **システムモジュール (`app/Http/Controllers/System/`)**
   - User, Provider (Service/Apply/Provider), App, Impersonation, Help/Public
5. **DBモジュール (`app/Http/Controllers/Db/`)**
   - DbBase, Application, User, ActionLog, Service (Permission/User/Service/Role/Provider)
6. **APIモジュール (`app/Http/Controllers/Api/`)**
   - Markdown, Validate, Service (RolePermission, UserRole)
7. **サービス個別モジュール (`app/Http/Controllers/Service/`)**
   - Attendance (勤怠管理: Result, Request, Timestamp, Manager)
   - Accounting (会計・請求: Accounting, Invoice)
   - Reservation (予約管理: Reservation, Course, Staff, Manage, Public)
   - Store (ストア管理: Store, Manage)
   - Contract, Select, Attachment
