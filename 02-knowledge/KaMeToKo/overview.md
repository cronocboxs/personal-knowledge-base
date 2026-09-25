---
title: "KaMeToKo リポジトリ解析・最深部ロジックナレッジ"
repo: "KaMeToKo"
phase: 2
unexplored_domains:
  - "app/app/Http/Controllers/Auth"
  - "app/app/Services/ReservationService.php"
  - "app/app/Services/AttendanceService.php"
  - "app/database/migrations"
created_at: "2026-09-25"
updated_at: "2026-09-25"
---

# KaMeToKo リポジトリ概要

## 1. 目的とスコープ
KaMeToKo はLaravelベースの予約・勤怠・ストア管理システムです。本ナレッジでは、エントリーポイント（Web/API Routes）からコントローラー、サービス層、Eloquentモデル、データベーストランザクション、さらに非同期処理・外部連携の最深部までをトレースします。

## 2. インターフェース・最深部処理トレース

### 2.1 ルーティングとエントリーポイント
- **Web Routes**: `app/routes/web/user.php`, `app/routes/web/system.php`, `app/routes/web/api.php` 等に分割・定義されており、ユーザー向け、管理者（システム）向け、API向けの各ルートグループにディスパッチされます。
- **Public Routes**: `app/routes/public/` 配下にて認証不要の予約受付やヘルプページが公開されています。

### 2.2 予約・勤怠管理サービス層のトレース
- **ReservationService**: 予約作成・変更・キャンセル時における空き枠バリデーション、排他制御（データベーストランザクション、ロック）、通知メール送信の最深部ロジックを保有します。
- **AttendanceService**: ストアスタッフの勤怠打刻（出退勤、休憩）、月次集計ロジックを処理します。
