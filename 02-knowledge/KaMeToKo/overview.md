---
created: 2026-09-21
updated: 2026-09-21
tags: [KaMeToKo, spec, code-analysis]
phase: 2
status: active
unexplored_domains:
    - "認証・認可基盤 `app/Http/Middleware/CheckPermission.php`, `CheckServicePermission.php` の最深部権限チェックロジック"
    - "データソースサービス群 `app/Services/DataSource/` の抽象インターフェースと各Source(Json, GoogleSheets, Csv, Excel)の実装"
    - "予約・店舗管理ドメイン `app/Http/Controllers/Service/Reservation/` と `ManageReservationService.php` のトランザクション・通知処理"
    - "チャット・リアルタイム通信ドメイン `app/Http/Controllers/Provider/Room/` と `MessageService.php`, Reverb連携イベント"
---

# KaMeToKo 挙動・最深部仕様ナレッジ (Overview)

## 1. 識別された機能・インターフェース一覧 (Phase 1)
KaMeToKo は Laravel製の大規模マルチテナント型サービス・システムプラットフォーム（予約、チャット、勤怠管理、データソースインポート等を含む）です。主なモジュール群は以下の通りです：

- [x] **認証・認可 (Auth / Passkey / GoogleAuth)**: `app/Http/Controllers/Auth/`, `app/Http/Controllers/LoginController.php`
- [x] **プロバイダー/テナント管理 (Provider)**: `app/Http/Controllers/Provider/`, `app/Models/Service/Provider/`
- [x] **予約管理システム (Reservation)**: `app/Http/Controllers/Service/Reservation/`, `app/Services/Service/Reservation/`
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
  5. **副作用・非同期イベント**: インポート完了ログの出力、例外時のハンドリング (`app/Exceptions/`)。
- **出力・応答・状態変化**:
  - **成功/失敗時の最深部挙動**: 例外発生時はロールバックおよび `SystemLogServiceProvider` を介したログ記録。

## 3. 再走査・深層比較ログ (Phase 5)
- **最終再走査日**: 2026-09-21
- **発掘された未確認領域・補全履歴**:
  - 2026-09-21: Phase 1 目録化完了、`overview.md` を作成し主要な未確認ドメインを `unexplored_domains` に登録。
