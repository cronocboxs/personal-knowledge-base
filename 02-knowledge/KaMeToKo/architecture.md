---
created: 2026-09-20
tags: [kametoko, architecture, laravel, vue, database, routing]
status: active
---

# KaMeToKo アーキテクチャ仕様

本リポジトリは、Laravel (Backend) と Vue.js (Frontend) のハイブリッド・モノリス構造を採用しています。

## ディレクトリ・モジュール構造

- **ルーティング (`app/routes/`)**:
  - `web.php` を起点に、サービス別 (`web/service/reservation.php`) やシステムプロバイダー別 (`web/system/provider.php`) にルーティングを分割管理。
- **データベース設計 (`app/database/migrations/`)**:
  - 予約関連テーブル (`2026_06_29_00_create_reservations_tables.php`) をはじめとする、リレーショナルデータベーススキーマ。
- **フロントエンド (`app/resources/js/vue/`)**:
  - Vue.js (`vue.js`, `roomsg.js`) と Bladeテンプレート (`resources/views/`) の融合。
  - コンポーネント指向でカレンダー (`CalendarViewComponent.vue`) やモーダル (`DataModalComponent.vue`)、チャットUIを構築。
- **サービス・ログ設計 (`app/app/Services/`, `app/app/Log/`)**:
  - ビジネスロジックをサービス層に分離 (`MessageService.php`)。
  - 共通ロギングTrait (`TraitLog.php`) によるトレーサビリティの確保。
