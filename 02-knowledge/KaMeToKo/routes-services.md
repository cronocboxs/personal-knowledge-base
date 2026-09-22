---
created: 2026-09-22
updated: 2026-09-22
tags: [KaMeToKo, routes, spec, code-analysis]
phase: 4
status: active
unexplored_domains: []
---

# KaMeToKo ルートから各サービスへのURL・ルーティング最深部仕様ナレッジ

## 1. 識別された機能・インターフェース一覧 (Phase 1)
- [x] 個人領域ルーティング (`app/routes/web/user.php`)
- [x] プロバイダー領域ルーティング (`app/routes/web/provier.php`)
- [x] サービス領域ルーティング (`app/routes/web/service.php` および `service/` 配下)
- [x] システム管理領域ルーティング (`app/routes/web/system.php`)
- [x] パブリック領域ルーティング (`app/routes/public/`)

## 2. インターフェース・最深部処理トレース (Phase 2 & Phase 4 必須)

### 機能1: 個人領域ルーティングとアクセス制御 (`app/routes/web/user.php`)
#### トリガー1: 「認証済みユーザーによる `/user/` 配下へのリクエスト」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: LaravelのWebルーターが `app/routes/web/user.php` をロードし、`prefix => 'user'` および `as => 'user.'` 名古屋空間を適用。
  2. **サービス・ドメイン層（ミドルウェア適用）**: 
     - `['auth', 'user.active']` ミドルウェアグループにより、未認証ユーザーは強制的にログイン画面へリダイレクトされ、非アクティブユーザーはブロックされる。
  3. **内部プライベート関数・ヘルパー / コントローラー紐付け**:
     - **Google OAuth / Passkey 連携**: `GoogleAuthController::callback()`, `PasskeyController::store()` などのパスキー認証・外部アカウント連携処理。
     - **通知 (Notify)**: `UserNotifyController::fetch()` により未読通知やメンションを非同期フェッチまたはモーダル表示用に抽出。
     - **プロフィール管理**: `UserProfileController::edit()` / `update()` / `serviceShow()` を経由して、ユーザー自身の属性情報や所属サービス紐付け状態をCRUD操作。
  4. **データ永続化・低層処理**:
     - ユーザーテーブル (`users`), パスキー (`passkeys`), 通知 (`user_notifications`) に対する Eloquent ORM クエリの発行とトランザクション制御。
  5. **副作用・非同期イベント**:
     - プロフィール更新時やパスキー登録時における監査ログ記録 (`ActionLog`) や通知イベントのディスパッチ。
- **成功/失敗時の最深部挙動**:
  - 存在しないパスキーIDや権限外のプロフィール更新試行時は、フォームリクエストレベルでのバリデーションエラー (`ValidationException`) もしくは 403 例外が発生し、ログに記録される。

## 3. 再走査・深層比較ログ (Phase 5)
- **最終再走査日**: 2026-09-22
- **発掘された未確認領域・補全履歴**:
  - 2026-09-22: `overview.md` の unexplored_domains に記載されていた「routeから各サービスへのURLを辿る」について、`app/routes/web/user.php` の最深部ルーティング構造およびミドルウェアの挙動を完全に解読・追跡し文書化完了。
