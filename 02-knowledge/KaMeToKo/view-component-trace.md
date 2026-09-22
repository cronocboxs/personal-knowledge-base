---
created: 2026-09-22
updated: 2026-09-23
tags: [KaMeToKo, views, vue, components, spec, code-analysis]
phase: 4
status: active
unexplored_domains:
  - "組み込み package と使用箇所の抜き出し、使用している場所の仕様"
---

# KaMeToKo View / Vue コンポーネントおよび画面階層構造 挙動・最深部仕様ナレッジ

## 1. 識別された機能・インターフェース一覧 (Phase 1)
- [x] Blade View 階層 (`resources/views/`) と Controller からのビュー呼び出しフロー
- [x] Vue.js コンポーネント群 (`resources/js/vue/`) と専用エントリポイント
- [x] 独自ライブラリ (`library/My/`) とカスタムヘルパー

## 2. インターフェース・最深部処理トレース (Phase 2 & Phase 4 必須)

### 機能1: コントローラーから Blade ビューへのデータ流転とレンダリング最深部
#### トリガー1: 「ユーザーによる画面アクセス（例: `DashboardController` や `ReservationController`）」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: `routes/web.php` から各コントローラーのアクションメソッドへルーティング。
  2. **サービス・ドメイン層**: コントローラー内で認証チェック (`CheckPermission` 等) を経由後、ビジネスロジック・サービスからデータを取得。
  3. **内部プライベート関数・ヘルパー**: 
     - コントローラー内での `view('view.path', compact('data'))` の実行。
     - Blade エンジンによるコンパイルと、`resources/views/layouts/app.blade.php` 等のマスターレイアウトへのテンプレート継承 (`@section`, `@yield`, `@include`)。
  4. **データ永続化・低層処理**: ビュー内でのコンポーネント呼出 (`@include`, `<x-component>`) および Blade ディレクティブによる権限・ロール別の表示制御。
  5. **副作用・非同期イベント**: なし（レンダリング時）。
- **出力・応答・状態変化**:
  - HTML レスポンスの返却。フロントエンド側での Vue.js (`resources/js/vue/`) マウント。

### 機能2: Vue.js フロントエンド・コンポーネント統合
#### トリガー1: 「フロントエンドSPA/パーツの初期化 (`app.js`, `provider.js`, `reservation.js` 等)」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: Blade テンプレート内で `@vite('resources/js/app.js')` または個別 Vue エントリ (`resources/js/vue/reservation.js`) を読み込み。
  2. **サービス・ドメイン層**: 
     - Vue アプリの初期化、Pinia/Vuex ストア（`resources/js/vue/store/`）のロード、Ziggy (`ziggy.js`) による Laravel ルートのフロントエンド利用。
  3. **内部プライベート関数・ヘルパー / コンポーネント群**:
     - `resources/js/vue/components/` 配下の共通パーツ（カレンダー、通知、ファイル管理、モーダル等）およびドメイン別コンポーネントのインスタンス化。
     - `axios` インターセプターを介した非同期 API リクエスト。

### 機能3: 独自ライブラリ `Library\My\` (`library/My/`) の最深部処理トレース
#### トリガー1: 「サービス層やコントローラーからのファイル操作・文字列処理・排他制御の呼び出し」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: `composer.json` の PSR-4 オートロード（`"Library\\": "library/"`）により自動読み込みされ、各種サービスやコントローラーから静的メソッド（例: `FuncFile::base64ToFile()` や `FuncLock` 等）として呼び出し。
  2. **サービス・ドメイン層**:
     - **`Library\My\Funcs\FuncFile` (`library/My/Funcs/FuncFile.php`)**:
       - `base64ToFile(string $base64, $fileName = null)`: 先頭50文字のプレフィックス検証 (`preg_match('/data\:.*\;base64\,/', ...)`) を行い、カンマで分解して `base64_decode()` を実行。一時ファイルディレクトリへ書き出し、ファイル情報を返す。
     - **`Library\My\Funcs\FuncLock` (`library/My/Funcs/FuncLock.php`)**:
       - 排他制御（ファイルロックやプロセスロック等）の最深部実装。
     - **`Library\My\Funcs\FuncString` / `FuncDate` / `Funcs`**:
       - 文字列操作・日付パース・汎用ユーティリティ群。基底クラス `Library\My\baseClass` を継承。
  3. **データ永続化・低層処理 / 副作用**:
     - OS一時ディレクトリへのファイル出力、ファイルポインタ操作、メモリ上でのストリーム処理。

## 3. 再走査・深層比較ログ (Phase 5)
- **最終再走査日**: 2026-09-22
- **発掘された未確認領域・補全履歴**:
  - 2026-09-22: コントローラーからの Blade ビュー呼出、`resources/views/` の階層構造、および `resources/js/vue/` の Vue コンポーネント群の最深部アーキテクチャを新規発掘・追記。
  - 2026-09-23: `library/My/` 配下の独自ライブラリ（`Library\My\Funcs\FuncFile`, `FuncLock`, `baseClass` 等）の最深部処理ロジックを解析・追記。
