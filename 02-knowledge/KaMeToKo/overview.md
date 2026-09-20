---
created: 2026-09-20
updated: 2026-09-20
tags: [KaMeToKo, spec, code-analysis]
phase: 3
status: active
unexplored_domains: []
---

# KaMeToKo 挙動・処理仕様ナレッジ (Overview)

## 1. 識別された技術スタックとリポジトリ概要 (Phase 1)
- **技術スタック**: PHP 8.x / Laravel (Webアプリケーション / RESTful API / CLI)
- **データベース**: MySQL / MariaDB (Docker環境)
- **フロントエンド・UI**: Blade / Webpack / Vite / Vue.js 統合
- **主要モジュール**:
  - `routes/web/...` および `routes/api.php`: 認証、ユーザー管理、プロバイダー、システム管理、店舗・予約・勤怠サービス等のモジュール別ルーティング。
  - `app/Http/Controllers/`: コントローラー層（ログイン、テストなど）
  - `app/Models/`: ユーザー、プロバイダー、ログ、共通Traitベースのモデル群。
  - `app/Services/`: データソース処理、コンテキスト管理、impersonation、各種ユーティリティ、システム機能。
  - `app/Console/Commands/`: 権限同期、ユニットテスト実行などのCLIコマンド。

## 2. インターフェース・トリガー別詳細トレース (Phase 2)

### 機能1: 認証・ログインシステム (`routes/web/login.php`, `app/Http/Controllers/LoginController.php`)
- **トリガー**: `POST /login` (Webリクエスト)
- **入力・要求**: ユーザー名/メールアドレス、パスワード、CSRFトークン
- **内部処理流転**:
  1. `VerifyCsrfToken` ミドルウェアによるCSRF検証。
  2. `LoginController` による認証試行 (`Auth::attempt`)。
  3. 成功時、セッション再生成およびユーザーアクティブ状態 (`UserActive` ミドルウェア) の確認。
- **出力・応答**:
  - **成功時**: ダッシュボードまたは元のリクエストURLへリダイレクト。
  - **失敗時**: エラーメッセージと共にログイン画面へ戻る。

### 機能2: サービス予約システム (`routes/web/service/reservation.php`, `app/Observers/ReservationObserver.php`, `app/Jobs/SaveReservationLogJob.php`)
- **トリガー**: `POST /service/reservations` または画面操作による予約作成
- **入力・要求**: 予約日時、顧客ID、店舗ID、サービスID、オプションパラメータ
- **内部処理流転**:
  1. `CheckServicePermission` ミドルウェアによる権限チェック。
  2. 予約データのバリデーションとEloquentモデル作成。
  3. `ReservationObserver` が発火し、`SaveReservationLogJob`（非同期ジョブ）をキューに投入。
- **出力・応答**:
  - **成功時**: HTTP 201 / 302 リダイレクト、予約完了通知の送信 (`ReservationConfirmedNotification`)。
  - **失敗時**: 例外ハンドリングによるエラー返却とトランザクションロールバック。

### 機能3: CLIコマンド・メンテナンス (`app/Console/Commands/SyncPermissions.php`, `app/Console/Commands/RunUnitTest.php`)
- **トリガー**: ターミナル実行 (`php artisan permissions:sync`, `php artisan test:run`)
- **入力・要求**: CLI引数、オプション
- **内部処理流転**:
  1. `Console\Kernel` によるコマンド登録・起動。
  2. 権限定義ファイルの読み込みとDBパーミッションテーブルの同期、または `UnitTestRunnerService` を呼び出してテストスイートを実行。
- **出力・応答**:
  - 標準出力 (stdout) への処理ステータスおよび成功・失敗メッセージのログ記録。

## 3. モジュール間連携・例外ハンドリング・設計パターン (Phase 3)
- **コンポーネント間・ドメイン間の相互作用**:
  - `app/Providers/` に多くの独自プロバイダー（`DataBaseQueryServiceProvider`, `SystemLogServiceProvider`, `ViewServiceProvider` 等）が登録されており、クエリ監視やシステムログ、ビューへの共通データ注入 (`PropsComposer`) を一元管理している。
- **横断적関心事**:
  - `app/Exceptions/Handler.php` による階層化された例外ハンドリング (`Http40xException`, `PermissionDeniedException`)。
  - ミドルウェア (`Actionlog.php`, `RequestLogger.php`) による全リクエストの自動監査ログ・アクションログ記録。
