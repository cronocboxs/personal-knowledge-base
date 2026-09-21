---
created: 2026-09-21
updated: 2026-09-21
tags: [kametoko, spec, code-analysis, attendance]
phase: 4
status: active
unexplored_domains: []
---

# KaMeToKo 勤怠管理システム (Attendance) 最深部仕様ナレッジ

## 1. 識別された機能・インターフェース一覧 (Phase 1)
- [x] 勤怠管理・タイムスタンプ制御 (`app/Http/Controllers/Service/Attendance/TimestampController.php`)
- [x] 勤務者・リクエスト・実績モデル (`app/Models/Service/Attendance/ServiceAttendanceTime.php`, `ServiceAttendanceRequest.php`, `ServiceAttendanceUser.php`)
- [x] マネージャー・結果・申請管理 (`app/Http/Controllers/Service/Attendance/ManagerController.php`, `RequestController.php`, `ResultController.php`)

## 2. インターフェース・最深部処理トレース (Phase 2 & Phase 4 必須)

### 機能1: 勤怠打刻・タイムスタンプ処理 (`TimestampController::punch`)
#### トリガー1: 「出勤ボタン押下 (`type = 1`)」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: `TimestampController::punch()` または `punchUser()` にリクエストが入る。プロバイダー情報 (`$provider`) と職員情報 (`$attendanceUser`) を特定する。
  2. **サービス・ドメイン層**: 
     - 24時間以内の未完了レコード（退勤が空のレコード）を `ServiceAttendanceTime::lastAttendance()` により検索し、存在する場合は二重出勤エラー（400）を返却する。
     - 当日の日付 (`work_date = todayStr`) に対応する既存の実績レコードを取得し、すでに `clock_out_time` が埋まっている場合は「本日分は既に打刻済みです」エラーとする。
  3. **内部プライベート関数・ヘルパー & プラン連動**:
     - 当日の日付に対応する予定 (`ServiceAttendanceRequest`) を検索し、存在する場合は予定データからデフォルト区分 (`type`) や休憩時間 (`clock_rest_time`) を取得。
  4. **データ永続化・低層処理**:
     - 既存実績レコードが存在する場合は、実出勤時刻 (`clock_in_time`)、初回入力実出勤時刻 (`input_clock_in_time`)、ステータス（`config('service.attendance.status.draft.value')`）を上書き保存。
     - レコードが存在しない場合は、予定値を反映して `ServiceAttendanceTime::create()` により新規作成。
  5. **副作用・非同期イベント**:
     - 打刻成功時はJSONレスポンスとともに新しいステータス（`working`）およびトーストメッセージを返却。

#### トリガー2: 「退勤ボタン押下 (`type = 0`)」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: ユーザーおよび職員コードの特定後、`type = 0` で処理分岐。
  2. **データ探索（未来行ガード）**:
     - 未来のゴミ行や別日を誤って掴まないよう、対象を「今日 (`$todayStr`)」または「昨日（夜勤の場合: `$yesterdayStr`）」の未完了行（`clockNull('clock_out_time')`）に限定してピンポイントで `ServiceAttendanceTime::where(...)` により検索。
  3. **データ永続化・低層処理**:
     - 該当レコードが存在しない場合は「対応する出勤データが見つからないか、出勤から24時間が経過しているため退勤打刻できません。」エラー（400）を返す。
     - 該当レコードが存在する場合は `update()` を実行し、退勤時刻 (`clock_out_time`) とステータスを更新。
  4. **出力・応答**:
     - ステータス `offline` と完了メッセージをJSONで返却。

## 3. 再走査・深層比較ログ (Phase 5)
- **最終再走査日**: 2026-09-21
- **発掘された未確認領域・補全履歴**:
  - 2026-09-21: `TimestampController` の出勤・退勤時の二重打刻防止ロジック、夜勤を考慮した昨日判定、予定データ（`ServiceAttendanceRequest`）からのデフォルト値フォールバック処理の最深部ロジックを完全解読・記録。
