---
created: 2026-09-20
updated: 2026-09-20
tags: [KaMeToKo, spec, code-analysis]
phase: 3
status: active
unexplored_domains: []
---

# KaMeToKo 挙動・処理仕様ナレッジ

## 1. 識別された機能・インターフェース一覧 (Phase 1)
- [x] Webルーティング基盤 (`app/routes/web/`, `app/routes/web.php`)
- [x] APIルーティング基盤 (`app/routes/api.php`, `app/routes/web/api.php`)
- [x] ユーザー・プロバイダー・システム管理モジュール (`app/app/Http/Controllers/`, `app/app/Services/`)
- [x] 予約・勤怠・ストア管理機能 (`app/routes/web/service/`)
- [x] データベースモデル・マイグレーション・シーダー (`app/database/`)
- [x] 非同期ジョブ・イベント・オブザーバー (`app/app/Jobs/`, `app/app/Events/`, `app/app/Observers/`)

## 2. インターフェース・トリガー別詳細トレース (Phase 2 必須)

### 機能1: 予約・サービス管理システム
#### トリガー1: 「HTTPリクエスト (Web/API) およびコンソールコマンド」
- **入力・要求（Input/Request）**:
  - ユーザーおよびプロバイダーからのHTTPリクエスト（GET/POST）、CLIコマンド（`app/app/Console/`）。
- **内部処理流転（Execution Flow）**:
  1. ミドルウェア層による認証・認可・パスキー/権限チェック (`app/app/Http/Middleware/`).
  2. ルーター (`app/routes/`) から対応するコントローラーおよびサービス (`app/app/Services/`) へディスパッチ。
  3. Eloquentモデルを通じたMySQLデータベース操作およびバリデーション (`app/app/Rules/`).
  4. 必要に応じた非同期ジョブ (`app/app/Jobs/SaveReservationLogJob.php` 等) のキュー投入。
- **出力・応答・状態変化（Output/Response/State Change）**:
  - **成功時**: レスポンス返却（Bladeビュー、JSON、Resource）、DB状態更新、ログ記録、通知送信 (`app/app/Notifications/`).
  - **失敗時**: 例外ハンドリング (`app/app/Exceptions/Handler.php`)、バリデーションエラー応答、ロールバック。

## 3. モジュール間連携・例外ハンドリング・設計パターン (Phase 3)
- **コンポーネント間・ドメイン間の相互作用**: 予約変更やプロバイダーアクションに伴うオブザーバー (`ReservationObserver.php`) からのログジョブ非同期発火。
- **横断的関心事**: 独自のユーティリティ (`app/app/Utils/`)、マルチテナント/プロバイダー分離、ConoHaデプロイメントワークフロー (`.github/workflows/conoha-deploy.yml`).
