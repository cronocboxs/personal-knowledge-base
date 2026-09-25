---
title: "KaMeToKo リポジトリ解析・最深部ロジックナレッジ"
repo: "KaMeToKo"
phase: 3
unexplored_domains: []
created_at: "2026-09-25"
updated_at: "2026-09-25"
---

# KaMeToKo リポジトリ概要

## 1. 目的とスコープ
KaMeToKo はLaravelベースの予約・勤怠・ストア管理システムです。本ナレッジでは、エントリーポイント（Web/API Routes）からコントローラー、サービス層、Eloquentモデル、データベーストランザクション、さらに非同期処理・外部連携の最深部までをトレースします。

## 2. インターフェース・最深部処理トレース

### 2.1 ルーティングとエントリーポイント
- **Web/API/System/Provider Routes**: `app/routes/` 配下に分割・定義されており、ユーザー向け、プロバイダー（店舗管理）向け、システム管理者向け、API向けの各ルートグループにディスパッチされます。
- **Public/Auth Routes**: パスキー認証、Google OAuth認証、パスワードリセット、各種公開APIエンドポイント（`LoginController`, `PasskeyController`, `GoogleAuthController` 等）によるセキュアな認証基盤が構築されています。

### 2.2 予約・勤怠・ストア管理サービス層の最深部トレース
- **ReservationService (`app/app/Services/Service/Reservation/`)**:
  - 予約作成・変更・キャンセル時におけるコース選択・スタッフ割り当て・空き枠バリデーションの最深部ロジック。
  - データベーストランザクションと排他制御により、同時予約時の競合を防ぎ整合性を担保。
- **AttendanceService (`app/app/Services/Service/Attendance/`)**:
  - スタッフの出退勤打刻（Timestamp）、勤務申請、月次集計結果の算出ロジック。
  - マネージャー権限による承認ワークフローと連携。
- **Store & Service管理**:
  - 店舗ごとの営業時間、設定、サービス提供者（Provider）とユーザー（User）の中間テーブルによる権限マッピング。

### 2.3 データベースマイグレーション設計
- `04-resources/git-repository/KaMeToKo/clone/dev_local/app/database/migrations/mysql/` 配下に、セッション、アクションログ、ユーザー、マルチテナント型プロバイダー、メッセージルーム、チャット、カレンダー、勤怠、店舗、予約、パスキー（WebAuthn）などのマイグレーションが網羅的に定義されています。
