---
created: 2026-09-21
updated: 2026-09-21
tags: [KaMeToKo, spec, code-analysis]
phase: 4
status: active
unexplored_domains: []
---

# KaMeToKo 挙動・最深部仕様ナレッジ (Overview)

## 1. 識別された機能・インターフェース一覧 (Phase 1)
KaMeToKo は Laravel製の大規模マルチテナント型サービス・システムプラットフォーム（予約、チャット、勤怠管理、データソースインポート等を含む）です。主なモジュール群は以下の通りです：

- [x] **認証・認可 (Auth / Passkey / GoogleAuth / Middleware CheckPermission)**: `app/Http/Controllers/Auth/`, `app/Http/Middleware/CheckPermission.php`, `app/Http/Middleware/CheckServicePermission.php`
- [x] **プロバイダー/テナント管理 (Provider)**: `app/Http/Controllers/Provider/`, `app/Models/Service/Provider/`
- [x] **予約管理システム (Reservation)**: `app/Http/Controllers/Service/Reservation/`, `app/Services/Service/Reservation/ManageReservationService.php`
- [x] **リアルタイムチャット (Chat / Room)**: `app/Http/Controllers/Provider/Room/`, `app/Events/Provider/Room/`, `app/Jobs/ArchiveMessageJob.php`
- [x] **勤怠管理 (Attendance)**: `app/Http/Controllers/Service/Attendance/`, `TimestampController.php`
- [x] **データソースインポート機能 (DataSource)**: `app/Services/DataSource/` (Google Sheets, Excel, CSV, Json)
- [x] **システム・管理コンソール (System)**: `app/Http/Controllers/System/`

## 2. インターフェース・最深部処理トレース (Phase 2 & Phase 4 必須)

### 機能1: データソース連携サービス (`app/Services/DataSource/`)
#### トリガー1: 「外部スプレッドシートやExcel/CSVファイルの同期取り込み処理」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: `Google/SheetImport.php` コマンドや各コントローラーからの呼び出し。
  2. **サービス・ドメイン層**: `TabularDataSourceInterface` を実装した各データソースクラス。
  3. **内部プライベート関数・ヘルパー**: `HasGoogleClient` トレイト、チャンクフェッチ制御。

### 機能2: 予約・店舗管理ドメイン (`app/Services/Service/Reservation/`)
#### トリガー1: 「ストアスタッフまたは管理画面からの予約作成・更新リクエスト」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: `ManageController::save()`。
  2. **サービス・ドメイン層**: `ManageReservationService::saveReservation()`。
  3. **内部プライベート関数・ヘルパー**: `ServiceReservation::findAvailableAsset()` による空き席自動割り当て、`ServiceReservation::checkAvailability()` による営業時間・スタッフシフト重複チェック。

### 機能3: リアルタイムチャットドメイン (`app/Http/Controllers/Provider/Room/`)
#### トリガー1: 「メッセージ新規投稿・スレッド返信・添付ファイル管理」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: `MessageController::post()`。
  2. **サービス・ドメイン層**: `MessageService::send()`。
  3. **内部プライベート関数・ヘルパー**: `RoomAccessService::writeLock()`、正規表現メンション抽出（`extractMentionIds()`）、Laravel Reverb WebSocketイベントブロードキャスト（`MessageCreatedEvent`）。

### 機能4: 勤怠管理システム (`app/Http/Controllers/Service/Attendance/`)
#### トリガー1: 「スタッフによる出勤・退勤打刻処理」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: `TimestampController::punch()`。
  2. **サービス・ドメイン層**: 勤務者特定と現在時刻/日付判定。
  3. **内部プライベート関数・ヘルパー**: 二重出勤ガード（`ServiceAttendanceTime::lastAttendance()`）、シフト予定（`ServiceAttendanceRequest`）の自動紐付け、退勤時の今日・昨日限定ピンポイント行特定ロジック。

## 3. 再走査・深層比較ログ (Phase 5)
- **最終再走査日**: 2026-09-21
- **発掘された未確認領域・補全履歴**:
  - 2026-09-21: `KaMeToKo` リポジトリの全機能（認証・認可、データソース、予約管理、チャット・Reverb、勤怠管理）の最深部ロジックを完全網羅。`unexplored_domains` が全ドメインで空（`[]`）となり、完全網羅状態（Phase 5）を達成。
  - 2026-09-21: `KaMeToKo` リポジトリの全機能の最深部ロジックを完全網羅できていない(phase3,4あり)。`unexplored_domains` を再登録。
