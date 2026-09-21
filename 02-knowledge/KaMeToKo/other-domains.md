---
created: 2026-09-20
updated: 2026-09-20
tags: [KaMeToKo, spec, code-analysis, user-system-db-api-service]
phase: 3
status: active
unexplored_domains: []

# ユーザー・システム・DB・API・サービス個別機能 挙動・処理仕様ナレッジ

## 1. 識別された機能一覧
- [x] ユーザー個人機能 (`app/Http/Controllers/User/`: Profile, EmailChange, Notify, Calendar, Attachment, List)
- [x] システム管理機能 (`app/Http/Controllers/System/`: User, Provider, App, Impersonation)
- [x] DB管理・データベース連携 (`app/Http/Controllers/Db/`: DbBase, Application, User, ActionLog, Service)
- [x] APIエンドポイント機能 (`app/Http/Controllers/Api/`: Markdown, Validate, Service)
- [x] サービス個別機能 (`app/Http/Controllers/Service/`: Attendance, Accounting, Reservation, Store, Contract)

## 2. インターフェース・トリガー別詳細トレース (Phase 2)

### 機能1: 勤怠管理 (`Service/Attendance/`)
#### トリガー: 「出退勤打刻 (Timestamp) / 勤怠申請 (Request) / 集計 (Result)」
- **入力・要求（Input/Request）**:
  - 打刻アクション（出勤、退勤、休憩開始、休憩終了）、日時、理由（申請時）
- **内部処理流転（Execution Flow）**:
  1. ユーザーの勤務体系に基づき打刻データを記録。
  2. マネージャー権限 (`ManagerController`) による勤怠承認フローの処理。
  3. 月次集計ロジックによる労働時間の計算 (`ResultController`)。
- **出力・応答・状態変化（Output/Response/State Change）**:
  - 打刻データの保存完了、勤怠ステータスの更新、集計結果のダッシュボード表示。

### 機能2: 予約管理 (`Service/Reservation/`)
#### トリガー: 「予約登録 (Reservation) / コース・スタッフ設定 (Course, Staff) / 公開予約 (Public)」
- **入力・要求（Input/Request）**:
  - 予約日時、コースID、スタッフID、顧客情報、繰り返しルール (`simshaun/recurr`)
- **内部処理流転（Execution Flow）**:
  1. スケジュールの重複チェック、スタッフの空き状況確認。
  2. 予約データの永続化。
  3. リマインダーや確認通知の発火。
- **出力・応答・状態変化（Output/Response/State Change）**:
  - 予約完了通知、カレンダーへの反映 (`CalendarController`)。

### 機能3: 会計・請求 (`Service/Accounting/`, `InvoiceController`)
#### トリガー: 「請求書発行 / 会計データ登録」
- **入力・要求（Input/Request）**:
  - 請求明細、金額、発行先情報、支払期限
- **内部処理流転（Execution Flow）**:
  1. 明細からの合計金額・税額計算。
  2. PDF / 帳票出力の準備 (`PhpSpreadsheet` 等を活用)。
- **出力・応答・状態変化（Output/Response/State Change）**:
  - 請求書データの保存とプレビュー・ダウンロード用ファイルの生成。
