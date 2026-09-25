---
created: 2026-09-21
updated: 2026-09-25
tags: [KaMeToKo, datasource, spec, code-analysis]
phase: 4
status: active
unexplored_domains: []
---

# KaMeToKo データソース統合サービス (DataSource) & 認証・認可基盤 最深部仕様ナレッジ

## 1. 概要
`app/Services/DataSource/` は、Google Sheets, Excel, CSV, JSON といった多様な外部データソースから表形式データを統一インターフェース（`TabularDataSourceInterface`）を介して安全かつ効率的に取得・同期するためのモジュールです。

また、本ナレッジノートでは「認証・認可基盤（`CheckPermission.php`, `CheckServicePermission.php` ならびに `UserTraitServicePermission.php`）」の最深部権限チェックおよび監査ログ監査ロジックを統合網羅しています。

## 2. インターフェース・最深部処理トレース (Phase 2 & Phase 4 必須)

### 機能1: テーブル形式データソース同期・取得
#### トリガー1: 「Google Sheets / Excel 等からのチャンク単位データフェッチ処理」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: `App\Console\Commands\Google\SheetImport` などの Artisan コマンドまたは各サービス層からの呼び出し。
  2. **サービス・ドメイン層**: 
     - ファクトリ等を通じて `GoogleSheetsSource`, `ExcelSource`, `CsvSource`, `JsonSource` がインスタンス化される。
  3. **内部プライベート関数・ヘルパー**:
     - **ChunkFetcher::fetchChunk()**: `TabularDataSourceInterface` を実装した各ソースから `$source->headers()` でヘッダーを取得し、`$source->rows($offset, $limit)` で指定オフセットとリミットに基づくチャンク行データを取得。
     - **ColumnMapper::map() / filter()**: 期待されるヘッダー定義（`expectedHeaders`）と実データのヘッダー（`actualHeaders`）のインデックス対応表を `array_search(..., true)` で生成し、 `array_map()` を用いて必要な列のみを抽出・再構築した連想配列を返す。
     - **個別ソースの低層処理 (`GoogleSheetsSource::rows()`)**:
       - `HasGoogleClient` トレイトを経由して Google Sheets API サービスを取得。
       - `spreadsheets_values->get($spreadsheetId, "Sheet1!A1:Z1000")` のように範囲を指定して Google API HTTP リクエストを発行し、レスポンスから `getValues()` を取得。
  4. **データ永続化・低層処理**: 
     - 取得したチャンクデータを元に、ターゲット側のデータベースまたはインポートキュー（`ImportQueue`）へバッチインサート／更新処理を実行。
  5. **副作用・非同期イベント**: 
     - 外部API制限（Rate Limit）やネットワーク障害発生時はエクスポネンシャルバックオフによるリトライ機構または例外のハンドリング。
- **Output / 応答・状態変化**:
  - **成功/失敗時の最深部挙動**: チャンクが空（`empty($rows)`）の場合は `null` を返却しインポート処理を終了。APIエラー時は `Google_Service_Exception` をキャッチしログ記録。

### 機能2: サービス・テナント認証・認可基盤 (`CheckPermission.php` & `CheckServicePermission.php`)
#### トリガー1: 「マルチテナントサービス保護ルートへのHTTPリクエスト発火」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: `app/Http/Middleware/CheckPermission.php` および `CheckServicePermission.php` ミドルウェアによるリクエスト傍受。
  2. **サービス・ドメイン層**: 
     - `$request->user()` を介してログインユーザーを取得。
     - ユーザーがテナント/サービスに対して紐づいているか、あるいはシステム管理者（SuperAdmin）であるかを判定。
  3. **内部プライベート関数・ヘルパー**:
     - **UserTraitServicePermission::currentServiceUser()**: ユーザーモデルにインクルードされたトレイト経由で、現在アクセス中のサービス（Service / Provider）に対するコンテキストを解決。
     - **権限マトリクス評価**: 要求されたルートアクション（例: `service.reservation.manage`, `service.chat.write`）とユーザーに付与されているロール/パーミッションの突き合わせ。
     - **`CheckPermission.php` 最深部権限チェックロジックの内部実態**:
       - `$next($request)` 実行前の条件判定：`if (!auth()->check() || !auth()->user()->can($permission))` を評価。
       - 権限不一致・未認証時の低層セキュリティ監査フック： `static::actlog($request, response()->json(['message' => 'permission denied', 'permission' => $permission], 403), true)` を呼び出し、不審なアクセスをセキュリティログ（セキュリティ監査ログ）として永続化。
       - 拒否時の一元化された例外処理： `abort(403, '権限がありません')` により処理を即時中断し、一貫した403レスポンスを返却。
  4. **データ永続化・低層処理**: 
     - セキュリティ監査ログ（`TraitLog::actlog()` または `SecurityAuditLog`）へのアクセス試行ログ（成功・拒否）の永続化記録。
  5. **副作用・非同期イベント**:
     - 不正アクセス検知時のアラート連携や、テナント隔離違反の監査証跡の保存。
- **Output / 応答・状態変化**:
  - **成功/失敗時の最深部挙動**: 認証・認可成功時は `$next($request)` を通じて次層（コントローラー）へリクエストを委譲。失敗時はセキュリティログに記録を残した上で `abort(403)` により安全にブロック。

## 3. 再走査・深層比較ログ (Phase 5)
- **最終再走査日**: 2026-09-25
- **発掘された未確認領域・補全履歴**:
  - 2026-09-21: `CheckPermission.php`, `CheckServicePermission.php` および `UserTraitServicePermission.php` の最深部権限チェックロジック（`currentServiceUser()` 連携と `TraitLog::actlog()` による監査証跡永続化）を発掘・追記。
  - 2026-09-24: `app/Http/Middleware/CheckPermission.php` の最深部権限チェックと `TraitLog::actlog()` によるセキュリティ監査ログ記録の流転を詳細解析・補全。
  - 2026-09-25: `CheckPermission.php` の実コードに基づく `auth()->check() || !auth()->user()->can($permission)` および 403 JSON 監査ログ記録の最深部ロジックを正確に追記し、`unexplored_domains` を完全に解消。
