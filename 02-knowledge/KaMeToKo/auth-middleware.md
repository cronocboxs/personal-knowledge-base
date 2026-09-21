---
created: 2026-09-21
updated: 2026-09-21
tags: [KaMeToKo, auth, middleware, permission, spec, code-analysis]
phase: 4
status: active
unexplored_domains:
    - "予約・店舗管理ドメイン `app/Http/Controllers/Service/Reservation/` と `ManageReservationService.php` のトランザクション・通知処理"
    - "チャット・リアルタイム通信ドメイン `app/Http/Controllers/Provider/Room/` と `MessageService.php`, Reverb連携イベント"
    - "勤怠管理 (Attendance)**: `app/Http/Controllers/Service/Attendance/` と 予約管理システム (Reservation),Reverb連携イベント"
---

# 認証・認可基盤 (`CheckPermission` / `CheckServicePermission`) 最深部仕様ナレッジ

## 1. 概要
`app/Http/Middleware/CheckPermission.php` および `CheckServicePermission.php` は、KaMeToKo におけるマルチテナント環境およびテナント横断的な業務権限（Service Permission）を厳密に制御するためのカスタムミドルウェアです。Laravel標準のロール・パーミッション機能（Spatie Laravel-Permission等）に依存せず、不審なアクセスの監査ログ（`actlog`）記録や、テナントごとのアクティブなセッション情報（`currentServiceUser()`）を唯一の真実として評価する独自の認可エンジンを構築しています。

## 2. インターフェース・最深部処理トレース (Phase 2 & Phase 4 必須)

### 機能1: 標準権限チェック (`CheckPermission`)
#### トリガー1: 「ルーティング定義におけるミドルウェア指定 (例: `middleware('permission:user.manage')`)」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: `CheckPermission::handle(Request $request, Closure $next, $permission)`。
  2. **サービス・ドメイン層**:
     - `auth()->check()` によりユーザーのログイン状態を検証。
     - `auth()->user()->can($permission)` を呼び出し、ユーザーに紐づくロール・パーミッションを評価。
  3. **内部プライベート関数・ヘルパー**:
     - 権限不許可（`!auth()->check() || !auth()->user()->can($permission)`）の場合、`TraitLog::actlog()` を呼び出して不正アクセス試行をセキュリティログとして強制記録。
  4. **データ永続化・低層処理**:
     - `actlog` により監査ログストレージ/DBへインシデントログを保存。
  5. **副作用・非同期イベント**:
     - `abort(403, '権限がありません')` をスローし、セキュアにリクエストを中断。
- **出力・応答・状態変化**:
  - **成功時**: `$next($request)` を通じて後続のコントローラー・処理へ進行。
  - **失敗時**: HTTP 403 レスポンスおよびログ記録。

---

### 機能2: サービス・マルチテナント権限チェック (`CheckServicePermission`)
#### トリガー1: 「サービス内ルーティングにおける権限チェック (例: `middleware('service.permission:invoice.create')` または複数指定)」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: `CheckServicePermission::handle($request, Closure $next, ...$permissions)`。
  2. **サービス・ドメイン層**:
     - `$user = auth()->user()` を取得。
     - `$user->canAnyService($permissions)`（内部的には `UserTraitServicePermission`）を呼び出し。
  3. **内部プライベート関数・ヘルパー（最深部ロジック）**:
     - **`currentServiceUser()`**: セッション情報を唯一の真実として、現在のテナント・サービスコンテキストに紐づく `ServiceUser` インスタンスを解決。
     - **`ServiceUser::can($permissionCode)` / `canAny()` / `canAll()`**: テナント内のロール（`ServiceRole`）とパーミッション（`ServiceMasterPermission` / `ServiceRolePermission`）の中間テーブルを辿る業務権限エンジン。
  4. **データ永続化・低層処理**:
     - 権限不足時は `TraitLog::actlog()` によりセキュリティ違反としてリクエストボディやパーミッション情報を監査ログに記録。
  5. **副作用・非同期イベント**:
     - `abort(403, 'サービス権限がありません')` による拒否レスポンス。
- **出力・応答・状態変化**:
  - **成功/失敗時の最深部挙動**: 例外的にコントローラー層から呼び出す場合は `UserTraitServicePermission::requireServicePermission()` が `ServicePermissionDeniedException` をスロー。

## 3. 再走査・深層比較ログ (Phase 5)
- **最終再走査日**: 2026-09-21
- **発掘された未確認領域・補全履歴**:
  - 2026-09-21: `CheckPermission.php` および `CheckServicePermission.php` の監査ログ出力（`actlog`）と `currentServiceUser()` を基軸とする最深部権限エンジン（`UserTraitServicePermission`）の流転を完全解読・追記。`overview.md` および `datasource.md` の `unexplored_domains` から該当項目を除外。
