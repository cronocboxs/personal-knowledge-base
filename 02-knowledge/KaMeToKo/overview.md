---
created: 2026-09-21
updated: 2026-09-21
tags: [KaMeToKo, spec, code-analysis]
phase: 4
status: active
unexplored_domains:
    - "チャット・リアルタイム通信ドメイン `app/Http/Controllers/Provider/Room/` と `MessageService.php`, Reverb連携イベント"
---

# KaMeToKo 挙動・最深部仕様ナレッジ (Overview)

## 1. 識別された機能・インターフェース一覧 (Phase 1)
KaMeToKo は Laravel製の大規模マルチテナント型サービス・システムプラットフォーム（予約、チャット、勤怠管理、データソースインポート等を含む）です。主なモジュール群は以下の通りです：

- [x] **認証・認可 (Auth / Passkey / GoogleAuth / Middleware CheckPermission)**: `app/Http/Controllers/Auth/`, `app/Http/Middleware/CheckPermission.php`, `app/Http/Middleware/CheckServicePermission.php`
- [x] **プロバイダー/テナント管理 (Provider)**: `app/Http/Controllers/Provider/`, `app/Models/Service/Provider/`
- [x] **予約管理システム (Reservation)**: `app/Http/Controllers/Service/Reservation/`, `app/Services/Service/Reservation/ManageReservationService.php`
- [x] **リアルタイムチャット (Chat / Room)**: `app/Http/Controllers/Provider/Room/`, `app/Events/Provider/Room/`, `app/Jobs/ArchiveMessageJob.php`
- [x] **勤怠管理 (Attendance)**: `app/Http/Controllers/Service/Attendance/`
- [x] **データソースインポート機能 (DataSource)**: `app/Services/DataSource/` (Google Sheets, Excel, CSV, Json)
- [x] **システム・管理コンソール (System)**: `app/Http/Controllers/System/`

## 2. インターフェース・最深部処理トレース (Phase 2 & Phase 4 必須)

### 機能1: データソース連携サービス (`app/Services/DataSource/`)
#### トリガー1: 「外部スプレッドシートやExcel/CSVファイルの同期取り込み処理」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: `Google/SheetImport.php` コマンドや各コントローラーからの呼び出し。
  2. **サービス・ドメイン層**: `DataSource` ファクトリパターンまたは直接各 Source クラス (`GoogleSheetsSource.php`, `ExcelSource.php`, `CsvSource.php`, `JsonSource.php`) のインスタンス化。
  3. **内部プライベート関数・ヘルパー**: `TabularDataSourceInterface` を実装した各クラスによるチャンク単位（`ChunkFetcher.php`）でのストリーミング/フェッチ処理。カラムマッパー（`ColumnMapper.php`）を経由したスキーマ変換。
  4. **データ永続化・低層処理**: 該当モデルへのバッチインサートまたはアップサート処理。
  5. **副作用・非同期イベント**: インポート完了ログの出力、例外時のハンドリング (`app/Exceptions/`).
- **出力・応答・状態変化**:
  - **成功/失敗時の最深部挙動**: 例外発生時はロールバックおよび `SystemLogServiceProvider` を介したログ記録。

### 機能2: 認証・認可基盤ミドルウェア (`app/Http/Middleware/`)
#### トリガー1: 「テナントおよび標準権限チェック (`CheckPermission` / `CheckServicePermission`)」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: HTTP リクエスト受信時のミドルウェアハンドラ。
  2. **サービス・ドメイン層**: `auth()->user()->can()` またはテナント固有の `currentServiceUser()->can()` による権限評価。
  3. **内部プライベート関数・ヘルパー**: 権限不許可時に `TraitLog::actlog()` をを通じて不正アクセスを監査ログに永続化。
  4. **データ永続化・低層処理**: 監査ログストレージへのインシデント記録。
  5. **副作用・非同期イベント**: `abort(403)` によるセキュアなリクエスト遮断。
- **出力・応答・状態変化**:
  - **成功/失敗時の最深部挙動**: 許可時は後続処理へ、拒否時は 403 レスポンスと監査ログ記録。

### 機能3: 予約管理システム (`app/Services/Service/Reservation/ManageReservationService.php`)
#### トリガー1: 「予約作成・更新時の自動席割り当ておよび重複チェック処理」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: `ManageController::save()` 等からの予約保存リクエスト。
  2. **サービス・ドメイン層**: `ManageReservationService::saveReservation()` によるバリデーション済みデータの検証とコース・スタッフ・アセットの関連付け。
  3. **内部プライベート関数・ヘルパー**: 
     - `ServiceReservation::findAvailableAsset()` による空きアセットの自動検索・割り当て。
     - `ServiceReservation::checkAvailability()` によるスタッフスケジュール・アセット重複・営業時間制約の低層チェック。
  4. **データ永続化・低層処理**: トランザクション内での `ServiceReservation` の永続化（`fill()` / `save()`）。
  5. **副作用・非同期イベント**: エラー時のロールバックおよびメッセージ返却。
- **出力・応答・状態変化**:
  - **成功/失敗時の最深部挙動**: 成功時は保存された予約オブジェクト返却、失敗時（空きなし・重複）はエラーメッセージ配列返却。

## 3. 再走査・深層比較ログ (Phase 5)
- **最終再走査日**: 2026-09-21
- **発掘された未確認領域・補全履歴**:
  - 2026-09-21: Phase 1 目録化完了、`overview.md` を作成し主要な未確認ドメインを `unexplored_domains` に登録。
  - 2026-09-21: `CheckPermission.php`, `CheckServicePermission.php` の最深部権限チェックロジックおよび監査ログ記録流転を発掘・追記。
  - 2026-09-21: `ManageReservationService.php` の空き席自動割り当ておよび重複チェックロジックの最深部処理流転を発掘・追記。
