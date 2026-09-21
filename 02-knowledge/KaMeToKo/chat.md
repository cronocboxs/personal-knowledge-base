---
created: 2026-09-21
updated: 2026-09-21
tags: [KaMeToKo, chat, room, message, reverb, spec, code-analysis]
phase: 5
status: active
unexplored_domains: []
---

# リアルタイムチャット・メッセージング (`MessageController` / `MessageService` / Reverb連携) 最深部仕様ナレッジ

## 1. 概要
`app/Http/Controllers/Provider/Room/MessageController.php` および `app/Services/Service/Provider/Message/MessageService.php` は、KaMeToKo におけるリアルタイムチャット（ルーム、メッセージ投稿、スレッド返信、ファイル添付、メンション、ピン留め、Laravel Reverbを用いたWebSocketブロードキャスト通知）の最深部ロジックを担うモジュールです。

## 2. インターフェース・最深部処理トレース (Phase 2 & Phase 4 必須)

### 機能1: メッセージ送信・更新・スレッド処理 (`MessageService::send`)
#### トリガー1: 「チャットルームにおけるメッセージ新規投稿・スレッド返信または編集」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: `MessageController::post()` または `update()` からの入力受取。
  2. **サービス・ドメイン層**: 
     - `MessageService::send()` が呼び出され、まず `trim($body) === '' && empty($attachmentIds)` による入力バリデーション（例外: `InvalidArgumentException`）。
     - `DB::transaction()` 内で処理を実行。
  3. **内部プライベート関数・ヘルパー（最深部ロジック）**:
     - **書き込みロック & 権限チェック**: `RoomAccessService::writeLock($room->id, $user)` により、テナントコンテキストおよびルームアクセス権を厳密に検証しつつ悲観的ロックを確保。
     - **新規作成 vs 更新分岐**:
       - **新規 ($id == null)**: `ServiceProviderMessage::create()` によりメッセージを永続化。親IDがある場合（スレッド返信）、親メッセージの `thread_reply_count` をインクリメントし `last_reply_at` を更新。ルームの `last_message_id` と `last_message_ins` を更新。投稿者を自動既読にする (`$roomUser->update()`)。
       - **更新 ($id != null)**: 該当メッセージ（自作メッセージに限る）を取得し、`body` を更新。添付ファイル (`$attachmentIds`) の差分比較を行い、不要になったアセットのストレージ紐付け解除（`detach`）および実体削除 (`$attachment->delete()`) を実行。
     - **添付ファイルパス管理**: `MessageService::makeAttachmentPath($room->provider_id, $room->id, $message->id)` により物理ストレージパスを構造化し、`TagParser` を用いてタグを自動生成。
     - **メンション抽出・通知**: `MessageService::extractMentionIds()` が `@[ID:名前]` の正規表現パターンから対象ユーザーIDを抽出し、`notifyMentions()` を介して `UserNotification::notify()` を非同期/同期発行。
  4. **データ永続化・低層処理**: 
     - データベーストランザクション内でのモデル保存と関連リレーションの同期 (`syncWithoutDetaching`)。
  5. **副作用・非同期イベント**: 
     - `MessageService::broadcastCreatedMessage()` / `broadcastUpdatedMessage()` を通じて、Laravel Reverb (`broadcast(new MessageCreatedEvent($message))`) を発火し、WebSocket経由でクライアントへリアルタイム同期。
- **出力・応答・状態変化**:
  - **成功/失敗時の最深部挙動**: 正常時は成功JSONレスポンス (`successToJson`)、アクセス権違反時は `RuntimeException` をキャッチして 403 エラーレスポンス、その他の例外は 500 エラーレスポンス。

---

### 機能2: メッセージアーカイブ処理 (`ArchiveMessageJob` / `MessageArchiveService`)
#### トリガー1: 「大量メッセージの定期または手動アーカイブ処理」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: `MessageController::archive()` からの `ArchiveMessageJob::dispatch()` 呼び出し。
  2. **サービス・ドメイン層**: キューワーカーワーカーによって非同期バックグラウンド実行される `ArchiveMessageJob`。
  3. **内部プライベート関数・ヘルパー（最深部ロジック）**:
     - 期間やID範囲指定（`start_id`, `end_id`, `start_date`, `end_date`）に基づいて、該当メッセージおよび添付ファイルをアーカイブテーブル（`ServiceProviderMessageArchive`, `ServiceMessageAttachmentArchive`）へ一括退避・構造化移管。
  4. **データ永続化・低層処理**: トランザクションによる安全なデータ移動と元テーブルからの削除。

## 3. 再走査・深層比較ログ (Phase 5)
- **最終再走査日**: 2026-09-21
- **発掘された未確認領域・補全履歴**:
  - 2026-09-21: `MessageController.php` および `MessageService.php` のスレッド返信、添付ファイルの動的差分削除・紐付け、正規表現メンション抽出（`extractMentionIds`）、および Reverb ブロードキャスト（`MessageCreatedEvent` 等）の最深部処理流転を完全解読・追記。
  - 2026-09-21: `overview.md` の `unexplored_domains` をすべて消化し、完全網羅状態（Phase 5）に到達。