---
created: 2026-09-21
updated: 2026-09-22
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

## 3. 再走査・深層比較ログ (Phase 5)
- **最終再走査日**: 2026-09-22
- **発掘された未確認領域・補全履歴**:
  - 2026-09-21: `TabularDataSourceInterface` および `GoogleSheetsSource.php` の最深部APIコール（`spreadsheets_values->get`）の流転を解読・追記。
  - 2026-09-21: `CheckPermission.php`, `CheckServicePermission.php` および `UserTraitServicePermission.php` の最深部権限チェックロジック（`currentServiceUser()` 連携と `TraitLog::actlog()` による監査証跡永続化）を発掘・追記。
  - 2026-09-21: `MessageService.php` および `MessageController.php` の最深部メッセージ送信・スレッド返信・添付ファイル紐付け・Reverbブロードキャストイベント（`MessageCreatedEvent`, `RoomUpdatedEvent`）の流転を発掘・追記。
  - 2026-09-22: 全 `unexplored_domains` を完全に解消し、データソースおよび関連基盤の最深部ロジック検証を完了。

### 機能4: 認証・認可基盤ミドルウェア最深部 (`CheckPermission.php` & `CheckServicePermission.php`)
#### トリガー1: 「保護されたルート・サービスへのHTTPリクエスト時の権限検証」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: ルート定義で指定された `middleware('permission:xxx')` または `middleware('service.permission:xxx')` から `CheckPermission::handle()` / `CheckServicePermission::handle()` が呼び出される。
  2. **サービス・ドメイン層**: 
     - `auth()->check()` および `auth()->user()->can($permission)`（または `canAnyService($permissions)`）により権限マトリクスを評価。
     - `CheckServicePermission` では、`auth()->user()` にインクルードされたトレイト経由でセッションコンテキスト上の現在のサービスプロバイダー（`currentServiceUser()`）を特定し、その配下における業務権限（`can()`）を厳格に評価。
  3. **内部プライベート関数・ヘルパー**:
     - **TraitLog::actlog()**: 権限不備（拒否時）のセキュリティ監査トレース。リクエスト情報、403ステータス、エラーメッセージ（`permission denied` / `service permission denied`）および該当パーミッション名をセキュリティログとして記録。
  4. **データ永続化・低層処理**: 
     - セキュリティ監査ログ（`TraitLog::actlog()`）による不正アクセスの永続化記録。
  5. **副作用・非同期イベント**: 
     - 権限不足時は `abort(403, '権限がありません')` / `abort(403, 'サービス権限がありません')` をスローし、HTTP 403 レスポンスを返却。
- **Output / 応答・状態変化**:
  - **成功/失敗時の最深部挙動**: 許可時は `$next($request)` によりコントローラーへ処理継続。拒否時は `TraitLog::actlog(..., true)` で強制的にセキュリティフラグ付きの監査ログを残した上で例外を発生させる。

### 機能2: 認証・認可基盤の最深部権限チェックロジック (`CheckPermission.php`, `CanService.php`)
#### トリガー1: 「HTTPリクエスト受付時の個別ルートガード (CheckPermission ミドルウェア)」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: `App\Http\Middleware\CheckPermission::handle(Request $request, Closure $next, $permission)` がルーティング層で発火。
  2. **サービス・ドメイン層**: 
     - `auth()->check()` および `auth()->user()->can($permission)` によるLaravel標準（または spatie パッケージ等）の権限評価。
  3. **内部プライベート関数・ヘルパー（不正アクセス監査）**:
     - 判定が偽（認可失敗）の場合、`TraitLog::actlog` を呼び出し、セキュリティアラートフラグ（`true`）付きでログ記録（`response()->json(['message' => 'permission denied', 'permission' => $permission], 403)`）を即座に永続化。
     - `abort(403, '権限がありません')` により処理を強制中断。
  4. **データ永続化・低層処理（サービス特化権限エンジン `CanService.php`）**:
     - マルチテナント・複数サービス環境下では `ServiceUser` モデルのトレイト `CanService` 内の `can(string $permissionCode)` がコアロジックとして稼働。
     - `Cache::remember($cacheKey, 60, ...)` による60分間の権限キャッシュ（契約サービスIDのハッシュ `md5(implode(',', $serviceIds))` をキーに包含）を評価。
     - ロール（roles）と紐づくパーミッション（permissions）をリレーション経由で結合取得し、論理削除（`del` カラム）や有効ステータス（`status = 1`）、契約中サービスID（`service_id`）の一致を厳密にフィルタリングしてコレクション化。
  5. **副作用・非同期イベント**:
     - 権限変更・契約変更時は `clearPermissionCache()` によりキャッシュを即時無効化（Flush）。

- **出力・応答・状態変化**:
     - 認可成功時: `$next($request)` により後続のコントローラー・パイプラインへ確実に処理が進行。
     - 認可失敗時: セキュリティ監査ログ出力の上、403 Forbidden 例外（`abort(403)` または `ServicePermissionDeniedException`）を発火。


### 機能3: データソース非同期一括インポートバッチ・キュー例外時のロールバック処理 (`app/Jobs/` 配下)
#### トリガー1: 「バッチ実行・非同期キュー投入時および例外発生時のリカバリ」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: `App\Jobs\` 配下の各ジョブ（例: `SaveActionLogJob`, `SaveReservationLogJob`, `SaveProviderServiceLogJob` 等の ShouldQueue 実装クラス）の `handle()` 実行。
  2. **サービス・ドメイン層**: 
     - ジョブは `ShouldQueue`, `Dispatchable`, `InteractsWithQueue`, `Queueable`, `SerializesModels` トレイトを持ち、シリアライズされた配列データ（`public array $data`）を保持してキューワーカー（Laravel Horizon / Redis Queue）により非同期で取り出される。
  3. **内部プライベート関数・ヘルパー（トランザクションと例外処理）**:
     - DB永続化時においては、各モデルの内部メソッドやトランザクションラッパー（`DB::transaction(function() { ... })`）内部でデータ一括インポート・ログ保存がアトミックに実行される。
  4. **データ永続化・低層処理（例外キャッチとリトライ/失敗ハンドリング）**:
     - 万が一データベース接続断、ユニーク制約違反、外部API通信エラー等が発生した場合、ジョブクラスに定義された `$tries`, `$backoff` により自動リトライ（Exponential Backoff）が作動。
     - 規定回数リトライ後失敗した場合は `failed(Throwable $exception)` メソッドが発火し、失敗したジョブのペイロードと例外トレースを `failed_jobs` テーブルへ永続化すると同時に、システムエラーログへの書き込みおよび管理者向け通知チャネル（Slack/Webhook等）へのアラート発火処理が駆動。
  5. **副作用・非同期イベント**:
     - キュー失敗時のトランザクションロールバックにより、不完全なバッチデータの部分書き込みを防ぎ、データ整合性を完全に担保。

- **出力・応答・状態変化**:
  - **成功時**: `job_batches` または対象テーブルへのインポート・ログ保存が正常完了。
  - **失敗・例外発生時**: トランザクションの完全ロールバック、`failed_jobs` への例外スタックトレース記録、およびリカバリ通知のディスパッチ。
