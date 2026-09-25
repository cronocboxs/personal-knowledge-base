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
  4. **データ永続化・低層処理**: 
     - セキュリティ監査ログ（`TraitLog::actlog()` または `SecurityAuditLog`）へのアクセス試行ログ（成功・拒否）の永続化記録。
  5. **副作用・非同期イベント**: 
     - 権限不備の場合は `abort(403, '権限がありません')` または `ServicePermissionDeniedException` を送出。
- **Output / 応答・状態変化**:
  - **成功/失敗時の最深部挙動**: 許可時は `$next($request)` でコントローラーへ処理継続、拒否時は 403 JSON レスポンス＋HTML例外ページの返却。

### 機能3: チャット・リアルタイム通信ドメイン (`MessageService.php` & `ChatMessageController.php`)
#### トリガー1: 「ルーム内メッセージ送信・スレッド返信およびReverb連携イベント発火」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: `App\Http\Controllers\Provider\Chat\MessageController::send()` または `MessageService::send()` の呼び出し。
  2. **サービス・ドメイン層**: 
     - リクエストのバリデーション（`message: required|string|max:2000`）。
     - `RoomAccessService::writeLock($room->id, $user)` を呼び出し、ルームに対する書き込みロックとメンバー権限の厳格な検証。
  3. **内部プライベート関数・ヘルパー**:
     - **新規作成・更新分岐**: `$id` の有無により `ServiceProviderMessage::create()` または既存メッセージの `update()` を実行。親メッセージ（`$parent`）が存在する場合は `thread_reply_count` のインクリメントと `last_reply_at` の更新。
     - **添付ファイル処理**: `$attachmentIds` が指定されている場合、`ServiceProviderAttachment::whereIn()` で取得し、`makeAttachmentPath()` を用いてストレージパスとタグを再構築。`syncWithoutDetaching()` で中間テーブルに紐付け。
     - **メンション抽出**: `extractMentionIds()` により `@[ID:名前]` の形式から正規表現（`/@\[(\d+):.+?\]/`）でメンション対象ユーザーIDを抽出。
  4. **データ永続化・低層処理**: 
     - すべての処理は `DB::transaction()` 内でアトミックに実行され、ルームの `last_message_id` や `last_message_ins`、送信者の `last_read_message_id` が同時に更新される。
  5. **副作用・非同期イベント**: 
     - **Laravel Reverb (WebSocket) ブロードキャスト**: `broadcast(new ChatMessageSent($msg))->toOthers()` または `MessageService::broadcastCreatedMessage()` 経由で `MessageCreatedEvent`、`RoomUpdatedEvent` を発火し、各クライアントのリアルタイムUIを更新。
     - **通知送信**: メンションされたユーザーに対して `UserNotification::notify()` を実行し、データベース・通知キューへレコードを永続化。
- **Output / 応答・状態変化**:
  - **成功/失敗時の最深部挙動**: 本文も添付ファイルも空の場合は `InvalidArgumentException` をスロー。トランザクションエラー時はロールバックし例外を伝播。

### 機能4: 認証・認可基盤ミドルウェア最深部権限チェック (`app/Http/Middleware/CheckPermission.php`)
#### トリガー1: 「個別ルートガード（CheckPermission ミドルウェア）によるHTTPリクエスト受付時の権限検証」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: ルート定義で指定された `middleware('permission:xxx')` から `App\Http\Middleware\CheckPermission::handle(Request $request, Closure $next, $permission)` が発火。
  2. **サービス・ドメイン層**: 
     - `auth()->check()` により認証状態を検証。未認証または `$auth->user()->can($permission)` が偽（権限不足）の場合に保護ロジックへ移行。
  3. **内部プライベート関数・ヘルパー（不正アクセス監査と例外処理）**:
     - 認可失敗時に `static::actlog($request, response()->json(['message' => 'permission denied', 'permission' => $permission], 403), true)` を呼び出し、セキュリティ監査ログ（`TraitLog`）に拒否イベントおよびリクエスト詳細を即座に永続化。
     - `abort(403, '権限がありません')` によりHTTP 403例外をスローして処理を強制中断。
  4. **データ永続化・低層処理**:
     - `TraitLog::actlog()` 内でのセキュリティ監査ログの永続化書き込み。
  5. **副作用・非同期イベント**:
     - 不正アクセス試行の即時監査ログ記録および403例外応答。
- **Output / 応答・状態変化**:
  - **許可時**: `$next($request)` により後続のコントローラーへ処理が正常に継続。
  - **拒否時**: セキュリティフラグ付き監査ログの保存と、403 Forbidden（メッセージ: 「権限がありません」）の返却。

## 3. 再走査・深層比較ログ (Phase 5)
- **最終再走査日**: 2026-09-24
- **発掘された未確認領域・補全履歴**:
  - 2026-09-21: `TabularDataSourceInterface` および `GoogleSheetsSource.php` の最深部APIコール（`spreadsheets_values->get`）の流転を解読・追記。
  - 2026-09-21: `CheckPermission.php`, `CheckServicePermission.php` および `UserTraitServicePermission.php` の最深部権限チェックロジック（`currentServiceUser()` 連携と `TraitLog::actlog()` による監査証跡永続化）を発掘・追記。
  - 2026-09-21: `MessageService.php` および `MessageController.php` の最深部メッセージ送信・スレッド返信・添付ファイル紐付け・Reverbブロードキャストイベント（`MessageCreatedEvent`, `RoomUpdatedEvent`）の流転を発掘・追記。
  - 2026-09-22: 全 `unexplored_domains` を完全に解消し、データソースおよび関連基盤の最深部ロジック検証を完了。
  - 2026-09-24: `app/Http/Middleware/CheckPermission.php` の最深部権限チェックと `TraitLog::actlog()` によるセキュリティ監査ログ記録の流転を詳細解析・補全し、`unexplored_domains` リストを完全に整理。
