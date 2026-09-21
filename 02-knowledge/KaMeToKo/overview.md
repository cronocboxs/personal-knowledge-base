---
created: 2026-09-20
updated: 2026-09-21
tags: [KaMeToKo, spec, code-analysis, overview]
phase: 3
status: active
unexplored_domains: []
---

# KaMeToKo リポジトリ概要・機能目録 (Phase 3 完了)

## 1. 技術スタック・アーキテクチャ判定
- **言語**: PHP 8.4
- **フレームワーク**: Laravel 12.0
- **フロントエンド / UI**: Inertia.js (Inertia-Laravel), Vite, Laravel UI, Vue / Blade
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

## 3. 主要モジュール・コントローラー群 (全解読完了)
1. **認証モジュール (`app/Http/Controllers/Auth/`)** - 完了
2. **プロバイダモジュール (`app/Http/Controllers/Provider/`)** - 完了
3. **ユーザーモジュール (`app/Http/Controllers/User/`)** - 完了
4. **システム管理モジュール (`app/Http/Controllers/System/`)** - 完了
5. **DB管理モジュール (`app/Http/Controllers/Db/`)** - 完了
6. **APIエンドポイントモジュール (`app/Http/Controllers/Api/`)** - 完了
7. **サービス個別モジュール (`app/Http/Controllers/Service/`)** - 完了 (勤怠、会計、予約、ストア、契約管理等)
