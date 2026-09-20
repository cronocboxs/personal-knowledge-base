---
created: 2026-09-20
updated: 2026-09-20
phase: 3
tags: [kametoko, architecture, laravel, vue, database, routing, design-patterns]
status: active
---

# KaMeToKo アーキテクチャ・設計思想仕様 (Phase 3)

本ドキュメントでは、`KaMeToKo` リポジトリにおけるLaravelバックエンドおよびVue.jsフロントエンドのアーキテクチャ、モジュール間のデータフロー、および設計思想を詳細に解説します。

---

## 1. 全体アーキテクチャ方針と設計原則

`KaMeToKo` は、Laravel 11/12系をバックエンドAPIおよびサーバーサイドレンダリング・Bladeホスティング基盤として使用し、フロントエンドに Vue.js (Viteバンドル) を組み合わせたモノリシック構成（一部SPA的コンポーネント埋め込み）を採用しています。

### 責務分離 (Separation of Concerns)
- **Controller層 (`app/Http/Controllers/`)**:
  - リクエストの受け付け、FormRequestによるバリデーション、サービス層（Service Layer）の呼び出し、レスポンス（JSON or Inertia/View）の返却に特化し、ビジネスロジックは保持しない。
- **Service層 (`app/Services/`)**:
  - 複雑なトランザクション管理、複数モデルを跨ぐビジネスロジック（例: 予約作成＋通知＋チャットルーム初期化など）を集約。
- **Model / Eloquent (`app/Models/`)**:
  - データベーステーブルとのマッピング、リレーション定義、スコープ、アクセサ/ミューテーター、および `TraitLog` 等による横断的関心事（ロギング）の適用。
- **Frontendコンポーネント (`resources/js/vue/`)**:
  - Composition API や再利用可能な単一ファイルコンポーネント (SFC)、個別エントリーポイント (`vue.js`, `roomsg.js`) による画面・ウィジェットの駆動。

---

## 2. モジュール間データ連携フロー（リクエスト 〜 レスポンス）

代表例として、**予約作成/更新フロー** および **リアルタイムチャットメッセージングフロー** のデータ連携をトレースします。

```
[User Browser / Vue.js Component]
       │
       ▼ HTTP Request (POST / GET / WebSocket)
[Route (`routes/web/service/reservation.php` etc.)]
       │
       ▼ Middleware (Auth, Verified, Custom Role Checks)
[Controller (`app/Http/Controllers/...`)]
       │
       ▼ FormRequest (Validation & Authorization)
[Service Layer (`app/Services/...`)]
       │
       ▼ Eloquent ORM / Transactions
[Database (`MySQL` Tables: users, reservations, rooms, messages)]
       │
       ▼ Response / Broadcast (JSON / Blade View + Vue Props)
[User Browser Render]
```

---

## 3. ドメイン領域別詳細設計

### ① 予約管理ドメイン (`app/Http/Controllers/Service/Reservation/`)
- **パブリック予約 (`PublicController`)**: 認証なし、またはゲスト向けのエントリーポイント。空き状況の確認 (`CalendarViewComponent.vue`) と予約仮押さえを行う。
- **管理・スタッフ操作 (`StaffController`, `ManageController`)**: プロバイダー（店舗・施術者）側からの予約確定、キャンセル、シフト管理。

### ② リアルタイムチャットドメイン (`app/Http/Controllers/Provider/Room/`, `MessageService.php`, `roomsg.js`)
- **チャットルーム管理 (`RoomController`)**: 顧客とプロバイダー間で1対1またはグループのチャットルームを構築。
- **メッセージング (`MessageService.php`)**: メッセージの永続化、添付ファイル処理、WebSocket (Laravel Reverb / Pusher等) を介したリアルタイムブロードキャストのトリガー。
- **フロントエンドチャット (`roomsg.js`, Vueコンポーネント)**: ポーリングまたはWebSocketによる非同期メッセージの送受信とUI自動スクロール。

### ③ インフラストラクチャ・デプロイ設計
- **GitHub Actions (`.github/workflows/conoha-deploy.yml`)**:
  - コードプッシュまたは手動トリガーにより、ConoHa VPS環境へSSH経由でデプロイを実行。
  - Composer依存関係のインストール (`composer install --no-dev`)、npmビルド (`npm run build`)、マイグレーション (`php artisan migrate --force`) の自動化。

---

## 4. 拡張性・メンテナンスの指針
- **ログ設計**: `TraitLog.php` を各主要クラスにインクルードすることで、エラーハンドリングや処理トレースの統一性を確保。
- **セキュリティ**: 厳格なミドルウェアグループ分け (`routes/web/system/provider.php`, `routes/web/service/reservation.php`) により、プロバイダーと一般ユーザーの認可境界を明確化。
