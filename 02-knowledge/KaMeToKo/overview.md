---
created: 2026-09-20
updated: 2026-09-20
tags: [kametoko, laravel, overview, architecture]
phase: 3
status: active
---

# かめトコ (KaMeToKo) 全体概要・アーキテクチャナレッジノート

## 1. 概要と役割 (Phase 1)
- **モジュールの目的と担当領域**:
  `KaMeToKo`（かめトコ / 亀処）は、店舗の経営を支えるためのLaravelベースの業務アプリケーション基盤です。
- **ディレクトリ役割と構成**:
  - `app/Http/Controllers/`: リクエストを受け付けるコントローラー群 (`Api/`, `Auth/`, `Db/`, `Service/`, `User/` 等に分離)
  - `routes/`: ルーティング定義 (`web.php`, `api.php` 等)
  - `resources/`: フロントエンドリソース (Blade / Vue / JS / CSS)
  - `database/`: マイグレーションファイル (`database/migrations/mysql/` 等)

## 2. コードレベルの処理・データフロー (Phase 2 必須)
- **参照ファイル**: 
  - `routes/web.php`, `app/Http/Controllers/Controller.php`
  - 各種サービスコントローラー (`app/Http/Controllers/Service/` 等)
- **リクエスト〜レスポンスの流れ**:
  1. Route (`web.php` / `api.php`) ➔ Middleware (認証・認可等) ➔ 各種コントローラー (例: `Service` や `User` のコントローラー)
  2. コントローラーからビジネスロジックを担うサービス層 (`app/Services/` またはコントローラー内のサービスクラス) に処理を移送
  3. Eloquent モデルを介して MySQL データベース (`minLaravel` DB等) と連携・永続化
  4. Blade ビュー、Inertia、または JSON レスポンスとしてクライアントへ返却される
- **主要ロジック・バリデーションルール**:
  - FormRequest やコントローラー内での厳格なバリデーション実施
  - 複数データベース接続（MySQL等）の適切なパス指定 (`--database=mysql --path=database/migrations/mysql/`)

## 3. アーキテクチャ・設計思想 (Phase 3 必須)
- **責務分離の方針**:
  - コントローラーはHTTPリクエストの受付とレスポンスの返却に特化させ、複雑なビジネスロジックやデータ操作はサービスクラスやアクションクラスへ分離。
- **状態管理とイベント**:
  - 認可（Policy / Gate）によるアクセス制御の徹底。
  - マイグレーションやマルチデータベース構成における柔軟な環境切り替え設計。
