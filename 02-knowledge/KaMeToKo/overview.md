---
created: 2026-09-20
tags: [kametoko, laravel, vue, reservation, chat, system]
status: active
updated: 2026-09-20
phase: 2
unexplored_domains: []
---

# KaMeToKo 概要

`KaMeToKo` は、LaravelとVue.jsを組み合わせた総合的な予約管理およびメッセージングプラットフォーム（Webアプリケーション）です。ユーザー、プロバイダー（店舗・施術者）、システムの3者間における複雑な予約管理、スタッフシフト、リアルタイムチャット機能を提供します。

## 1. 識別された全ドメイン領域 (Phase 1 / Phase 3 完了)
- [x] 予約管理ドメイン (`app/Http/Controllers/Service/Reservation/`)
- [x] 勤怠・シフト管理ドメイン (`app/Http/Controllers/Service/Attendance/`, `app/Http/Controllers/Service/Working/`)
- [x] チャット・メッセージングドメイン (`app/Http/Controllers/Provider/Room/`)
- [x] プロバイダー・ユーザー管理ドメイン (`app/Http/Controllers/Provider/`, `app/Http/Controllers/User/`)
- [x] システム管理ドメイン (`app/Http/Controllers/System/`)

## 2. 主な特徴・モジュール (Phase 2)
- **予約管理システム**: 公開予約 (`PublicController`, `PublicReservation.vue`)、スタッフ管理 (`StaffController`)、コース管理 (`CourseController`)、マネジメント (`ManageController`)。
- **勤怠・シフト管理**: スタッフの勤務シフト、打刻、カレンダー連携イベント (`user_calendars`, `user_calendar_events`)。予約可能枠への動的影響。
- **メッセージング / リアルタイムチャット**: プロバイダーとユーザー間のルーム管理、メッセージ送受信、Vue.jsベースのリアルタイムUIコンポーネント (`roomsg.js`, Laravel Reverb チャネル)。
- **プロバイダー・システム管理**: 権限管理 (`permission.php`)、プロファイル、契約管理、各種マスターデータ。

## 3. 全体アーキテクチャ・設計思想 (Phase 3)
- モノリシック構成にサービス層・オブザーバーパターン（`ReservationObserver`, `ProviderServiceObserver`）、非同期ジョブ（`SaveReservationLogJob`, `ArchiveMessageJob`）を導入し、関心の分離とロギングの徹底を実現。
