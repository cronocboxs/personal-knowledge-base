---
created: 2026-09-21
updated: 2026-09-21
tags: [KaMeToKo, attendance, spec, code-analysis]
phase: 5
status: active
unexplored_domains: []
---

# KaMeToKo 勤怠管理システム (Attendance) 最深部仕様ナレッジ

## 1. 概要
`app/Http/Controllers/Service/Attendance/TimestampController.php` および関連モデル（`ServiceAttendanceTime`, `ServiceAttendanceRequest`, `ServiceAttendanceUser`）は、KaMeToKo プラットフォームにおけるスタッフの勤怠打刻（出勤・退勤）、夜勤を考慮した日付判定、二重出勤ガード、および予約管理システム（Reservation）のスタッフ出勤判定との連携ロジックを担う中核モジュールです。

## 2. インターフェース・最深部処理トレース (Phase 2 & Phase 4 必須)

### 機能1: 打刻処理 (`TimestampController::punch` / `punchUser`)
#### トリガー1: 「スタッフによる出勤 (`type=1`) または退勤 (`type=0`) の打刻実行」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: `TimestampController::punch()` または `punchUser()`。
  2. **サービス・ドメイン層**: 
     - プロバイダーコンテキストおよび勤務者（`attendanceUser`）を特定。
     - 打刻タイプ（`type`）を取得し、現在時刻 (`now()`)、今日の日付 (`$todayStr`)、および夜勤対応用の昨日日付 (`$yesterdayStr`) を算出。
  3. **内部プライベート関数・ヘルパー（最深部ロジック）**:
     - **出勤打刻時の二重出勤防止ガード**:
       - `ServiceAttendanceTime::lastAttendance($provider->id, $attendanceUser->id)->first()` により、未完了（退勤時刻が空）の出勤データが既に存在するかをチェック。存在する場合は 400 エラー。
       - 本日分の実績レコードが既に存在し、かつ `clock_out_time` が埋まっている場合は「本日分打刻済み」エラー。
     - **予定（`ServiceAttendanceRequest`）の自動紐付け**:
       - 本日の日付に対応する `ServiceAttendanceRequest`（シフト・勤務予定）が存在するか検索。存在する場合はその `type`（勤務区分）や `clock_rest_time`（休憩時間）をデフォルト値として取得。
     - **実績レコードの作成または上書き**:
       - 既存レコード（下書き状態等）がある場合は実打刻時刻（`clock_in_time`, `input_clock_in_time`）および未設定時の `type` を上書き保存。
       - レコードがない場合は新規作成（`ServiceAttendanceTime::create`）。
     - **退勤打刻時のピンポイント対象行特定**:
       - 未来のゴミ行や誤ったレコードを掴まないよう、`whereNull('clock_out_time')` かつ `whereIn('work_date', [$todayStr, $yesterdayStr])` に厳密に絞り込み、今日の日付のレコードを優先して取得。見つからない場合は「対応する出勤データが見つからないか、出勤から24時間が経過している」として 400 エラー。
       - 該当レコードの `clock_out_time` に現在時刻を反映し、ステータスを下書き（`draft`）に更新。
  4. **データ永続化・低層処理**: 
     - データベース操作と JSON レスポンス（成功時トーストメッセージ・新ステータス返却）。
  5. **副作用・非同期イベント**: 
     - 予約管理システムの `ServiceReservation::isStaffWorking()` において、勤怠管理システムと連携し、出勤フラグが有効なスタッフの打刻実績・シフトから勤務時間をリアルタイム検証。

## 3. Re-scan & Deep Comparison Log (Phase 5)
- **Last Re-scan Date**: 2026-09-21
- **Discovered Undocumented Domains & Completion History**:
  - 2026-09-21: `TimestampController.php` の出勤二重ガード、シフト予定自動紐付け、および退勤打刻時の今日/昨日限定ピンポイント行特定ロジックを完全解読・追記。
  - 2026-09-21: `overview.md` の全 `unexplored_domains` が空 (`[]`) となり、全機能の最深部トレースが完了。Phase 5（完全網羅状態）に到達。
