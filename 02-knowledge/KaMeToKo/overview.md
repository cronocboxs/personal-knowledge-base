---
created: 2026-09-20
tags: [kametoko, laravel, vue, reservation, chat, system]
status: active
updated: 2026-09-20
phase: 3
---

# KaMeToKo 概要

`KaMeToKo` は、LaravelとVue.jsを組み合わせた総合的な予約管理およびメッセージングプラットフォーム（Webアプリケーション）です。ユーザー、プロバイダー（店舗・施術者）、システムの3者間における複雑な予約管理、スタッフシフト、リアルタイムチャット機能を提供します。

## 主な特徴・モジュール

- **予約管理システム (`app/app/Http/Controllers/Service/Reservation/`)**:
  - 公開予約 (`PublicController`, `PublicReservation.vue`)、スタッフ管理 (`StaffController`)、コース管理 (`CourseController`)、マネジメント (`ManageController`)。
- **メッセージング / リアルタイムチャット (`app/app/Http/Controllers/Provider/Room/`, `MessageService.php`, `roomsg.js`)**:
  - プロバイダーとユーザー間のルーム管理、メッセージ送受信、Vue.jsベースのリアルタイムUIコンポーネント。
- **プロバイダー・システム管理 (`app/app/Http/Controllers/Provider/`, `app/app/Models/Service/Provider/`)**:
  - 権限管理 (`permission.php`)、プロファイル、契約管理、各種マスターデータ。
- **インフラ・デプロイ**:
  - GitHub Actions (`.github/workflows/conoha-deploy.yml`) によるConoHa VPSへの自動デプロイメント。
  - Dockerコンテナ環境 (`docker/docker-compose.yml`)。
