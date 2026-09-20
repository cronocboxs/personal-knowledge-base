---
created: 2026-09-20
updated: 2026-09-20
tags: [KaMeToKo, screen-spec, user-action, auth]
phase: 3
status: active
unexplored_domains: []
---

# 認証・ログイン画面 操作・挙動仕様ナレッジ

## 1. 画面概要・要素一覧 (Phase 1)
- **対象画面**: ログイン画面 (`resources/views/auth/login.blade.php`)
- **構成要素**:
  - メール or ユーザーID入力欄 (`name="login"`)
  - パスワード入力欄 (`name="password"`)
  - 「パスワードをお忘れですか？」リンク (`route('password.forgot')`)
  - Passkeyログインコンポーネント (`<passkey-login-component>`)
  - ログイン状態保持チェックボックス (`name="remember"`, `id="remember"`)
  - 「ログイン」ボタン (`type="submit"`)
  - 「新規登録」リンク (`route('register.pre')`)

## 2. 操作トリガー別・詳細挙動トレース (Phase 2 必須)

### 操作A: 「ログイン」ボタン押下時
- **画面上の動作**:
  1. フォームが `POST` メソッドで送信される。
  2. バリデーションエラーや認証失敗時は該当の入力欄に `is-invalid` クラスが付与され、赤字でエラーメッセージがフィードバックされる。
- **裏での処理（コード連携）**:
  1. Route: `POST /login` ➔ `LoginController@login`
  2. `Request` バリデーション: `login` (必須/文字列), `password` (必須/文字列)。
  3. `filter_var(..., FILTER_VALIDATE_EMAIL)` により、入力された `login` 文字列がメールアドレス形式の場合は `email` カラム、それ以外の場合は `userid` カラムを照合フィールドとして判定。
  4. `Auth::attempt($credentials, $remember)` による認証処理の実行。
- **処理結果と画面変化**:
  - **成功時**: セッションが再生成 (`$request->session()->regenerate()`) され、「ログインに成功しました。」のサクセスアラートがフラッシュされた上で、`/dashboard` (`route('user.dashboard')`) へリダイレクト。
  - **失敗時（認証情報不一致）**: 画面は遷移せずエラー(`back()`)となり、`login` フィールドに「ログイン情報が一致しません。」のバリデーションエラーが設定され、入力された `login` 値が `old()` で保持される。

### 操作B: 「パスワードをお忘れですか？」リンク押下時
- **画面上の動作**:
  - パスワードリセット申請画面 (`route('password.forgot')`) へ遷移する。

### 操作C: 「新規登録」リンク押下時
- **画面上の動作**:
  - プレ登録画面 (`route('register.pre')`) へ遷移する。

## 3. 例外・エラーハンドリング・表示制御 (Phase 3 必須)
- **認証済みの場合の制御**:
  - すでに `Auth::check()` が真（ログイン済み）の状態でログイン画面URLにアクセスした場合、`LoginController@showLoginForm` により自動的に `/dashboard` (`route('user.dashboard')`) へリダイレクトされる。
- **例外系（入力不備・認証失敗）**:
  - 必須項目が未入力または認証情報がDBと一致しない場合、ページ上（またはアラート）にエラーメッセージが表示され、ユーザーは再入力を求められる。
