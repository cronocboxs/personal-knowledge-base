---
created: 2026-09-20
updated: 2026-09-20
tags: [KaMeToKo, spec, code-analysis]
phase: 3
status: active
unexplored_domains: []
---

# KaMeToKo 挙動・処理仕様ナレッジ

## 1. 識別された機能・インターフェース一覧 (Phase 1)
- [x] ルーティング定義 (`routes/web.php`, `routes/api.php`, `routes/console.php`, `routes/channels.php`)
- [x] Saas公開領域・認証前ルーティング (`routes/web/public/`, `routes/web/login.php`)
- [x] ユーザー・プロバイダー・サービス別業務アプリ領域 (`routes/web/user.php`, `routes/web/provier.php`, `routes/web/service.php`)
- [x] システム管理関連ルーティング (`routes/web/system.php`)
- [x] DockerインフラおよびConoHAデプロイCI/CD (`docker/`, `.github/workflows/`)

## 2. インターフェース・トリガー別詳細トレース (Phase 2)
### 機能1: ルーティングとリクエストディスパッチ
#### トリガー: 「HTTPリクエスト受信 (GET/POST)」
- **入力・要求（Input/Request）**:
  - URLパス、クエリパラメータ、HTTPヘッダー、セッションCookie。
- **内部処理流転（Execution Flow）**:
  1. `routes/web.php` が環境に応じたHTTPS強制 (`URL::forceScheme`) を適用。
  2. グループ化されたファイル群 (`public/`, `login.php`, `user.php`, `provier.php`, `service.php`, `system.php`) へルーティングを委譲。
  3. 各コントローラーおよびミドルウェアによる認証・認可・バリデーション処理。
- **出力・応答・状態変化（Output/Response/State Change）**:
  - **成功時**: 対応するBladeビューまたはJSONレスポンスを返却。
  - **失敗時**: 403/404エラーページへのリダイレクト、例外処理。

## 3. モジュール間連携・例外ハンドリング・設計パターン (Phase 3)
- **コンポーネント間・ドメイン間の相互作用**: Laravelベースのマルチテナント/マルチロール（User/Provider/Service/System）構造。モジュールごとに分割されたルーティングとサービス層が連携。
- **横断的関心事**: Sanctumによる認証、データベースマイグレーション、GitHub Actionsを通じたConoHAへのデプロイパイプライン。
