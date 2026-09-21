---
created: 2026-09-20
updated: 2026-09-20
tags: [KaMeToKo, spec, code-analysis, auth]
phase: 3
status: active
unexplored_domains: []
  # - "プロバイダ管理・機能 (`app/Http/Controllers/Provider/`)"
  - "ユーザー個人機能 (`app/Http/Controllers/User/`)"
  - "システム管理機能 (`app/Http/Controllers/System/`)"
  - "DB管理・データベース連携 (`app/Http/Controllers/Db/`)"
  - "APIエンドポイント機能 (`app/Http/Controllers/Api/`)"
  - "サービス個別機能（勤怠・会計・予約・ストア） (`app/Http/Controllers/Service/`)"
---

# 認証機能 (Auth) 挙動・処理仕様ナレッジ

## 1. 識別された機能・インターフェース一覧
- [x] ログイン機能 (`LoginController.php`)
- [x] パスワード忘れ・再設定機能 (`Auth/ForgotPasswordController.php`, `Auth/ResetPasswordController.php`)
- [x] 会員登録機能 (`Auth/RegisterController.php`)
- [x] パスキー認証 (`Auth/PasskeyController.php`)
- [x] Googleソーシャルログイン (`Auth/GoogleAuthController.php`)

## 2. インターフェース・トリガー別詳細トレース (Phase 2)

### 機能1: 通常ログイン (`LoginController`)
#### トリガー: 「POST /login」
- **入力・要求（Input/Request）**:
  - `email`: ユーザーメールアドレス（文字列、必須、メール形式）
  - `password`: パスワード（文字列、必須）
  - `remember`: ログイン保持フラグ（任意）
- **内部処理流転（Execution Flow）**:
  1. `Auth::attempt()` を用いた資格情報の検証。
  2. 認証成功時: セッション固定化攻撃防止のためのセッション再生成 (`$request->session()->regenerate()`)。
  3. 認証失敗時: バリデーションエラー (`ValidationException`) をスローし、エラーメッセージと共にログイン画面へリダイレクト。
- **出力・応答・状態変化（Output/Response/State Change）**:
  - **成功時**: ダッシュボードまたは直前のリクエスト元へリダイレクト。
  - **失敗時**: `email` フィールドに「認証情報が記録と一致しません。」等のエラーを付与して応答。

### 機能2: Googleソーシャルログイン (`GoogleAuthController`)
#### トリガー: 「GET /auth/google」および「GET /auth/google/callback」
- **入力・要求（Input/Request）**:
  - Laravel Socialite を経由した Google OAuth 2.0 認可コード。
- **内部処理流転（Execution Flow）**:
  1. `/auth/google`: `Socialite::driver('google')->redirect()` により Google 認証画面へリダイレクト。
  2. `/auth/google/callback`: Google から返却されたユーザー情報（メールアドレス、名前、Google ID）を取得。
  3. 該当メールアドレスを持つユーザーを DB から検索 (`User::where('email', ...)`)。
  4. 存在しない場合は新規登録またはエラー処理、存在する場合はログイン処理を実行。
- **出力・応答・状態変化（Output/Response/State Change）**:
  - セッション確立後、ホーム画面・ダッシュボードへリダイレクト。

### 機能3: パスキー認証 (`PasskeyController`)
#### トリガー: 「WebAuthn / Passkey API endpoints」
- **入力・要求（Input/Request）**:
  - WebAuthn 登録・認証用の JSON ペイロード（チャレンジ、署名データ等）。
- **内部処理流転（Execution Flow）**:
  1. `laravel/passkeys` パッケージを活用し、FIDO2 / WebAuthn 規格に基づく公開鍵暗号認証を実行。
  2. 登録時: ユーザーのデバイス（Touch ID, Face ID, Windows Hello 等）から公開鍵を登録。
  3. 認証時: チャレンジに対する署名を検証し、ユーザーを特定してセッションを発行。
- **出力・応答・状態変化（Output/Response/State Change）**:
  - 成功時は JSON レスポンスまたは画面遷移による認証完了。
