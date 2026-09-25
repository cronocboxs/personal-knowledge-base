---
created: 2026-09-21
updated: 2026-09-21
tags: [KaMeToKo, chat, room, reverb, websocket, spec, code-analysis]
phase: 4
status: active
unexplored_domains: []
---

# KaMeToKo リアルタイムチャット・ルーム管理ドメイン 最深部仕様ナレッジ

## 1. 概要
`app/Services/Service/Provider/Message/MessageService.php` および関連コントローラー・イベントは、マルチテナント環境におけるリアルタイムチャットシステムの中核を担います。Laravel Reverb（WebSocket）を用いたメッセージ配信、ルーム作成・更新・メンバー同期、添付ファイルの動的ストレージパス生成、メンション抽出および `UserNotification` による通知連動を完全に統合制御しています。

## 2. インターフェース・最深部処理トレース (Phase 2 & Phase 4 必須)

### 機能1: チャットメッセージ送受信・スレッド返信・既読管理
#### トリガー1: 「ストアスタッフまたはユーザーからのチャットメッセージ送信 (`MessageService::send()`)」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: `App\Http\Controllers\Provider\Room\MessageController::store()` などのコントローラー経由。
  2. **サービス・ドメイン層**: 
     - `MessageService::send()` が呼び出され、`body` または `attachmentIds` の存在を検証 (`InvalidArgumentException`)。
  3. **内部プライベート関数・ヘルパー（最深部ロジック）**:
     - **書き込みロックと権限チェック (`RoomAccessService::writeLock`)**: ルームへのアクセス権・書き込み権限を排他制御付きで検証。
     - **新規作成 vs 更新分岐 (`$id` の有無)**:
       - 新規作成時は `ServiceProviderMessage::create()` を実行。親メッセージ（`parent_id`）が存在する場合はスレッド返信として `parent->increment('thread_reply_count')` および `last_reply_at` を更新。ルームの `last_message_id` および `last_message_ins` を更新。投稿者を自動既読にする (`roomUser->update`)。
       - 更新時は指定された `$attachmentIds` 以外の添付ファイルをデータベースから切り離し（`detach()`）、物理削除を実行。
     - **添付ファイルパス生成 (`MessageService::makeAttachmentPath`)**: `provider_{id}/room_{id}/message_{id}` の構造でストレージパスおよびタグを動的生成・更新。
     - **メンション抽出 (`MessageService::extractMentionIds`)**: `@[ID:名前]` の正規表現パターンから対象ユーザーIDを抽出。
  4. **データ永続化・低層処理**: 
     - データベーストランザクション（`DB::transaction`）により、メッセージ、添付ファイルリレーション（`syncWithoutDetaching`）、既読状態の整合性を保証。
  5. **副作用・非同期イベント**: 
     - メンション対象ユーザーへの `UserNotification::notify()` による通知発行。
- **出力・応答・状態変化**:
  - **成功時**: 永続化された `ServiceProviderMessage` モデルインスタンスを返却。

---

### 機能2: ルーム作成・メンバー同期・ブロードキャスト通知
#### トリガー1: 「チャットルーム作成またはメンバーの追加・除外」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: `MessageService::create()` / `update()`。
  2. **サービス・ドメイン層**: 
     - 指定された `serviceUserIds` をユニーク化・整数化し、`ServiceProviderMessageRoom::create()` または `update()` を実行。
  3. **内部プライベート関数・ヘルパー（最深部ロジック）**:
     - **メンバー同期 (`syncWithoutDetaching` / `sync`)**: `last_read_message_id => 0` 初期値付きで中間テーブルを同期。
     - **ブロードキャスト配信 (`broadcastCreatedMessage` / `broadcastUpdateRoom`)**: Laravel Reverb を用いて `RoomCreatedEvent`, `RoomUpdatedEvent`, `RoomRemovedEvent`, `MessageCreatedEvent`, `MemberUpdatedEvent` をイベントブロードキャスト。
  4. **データ永続化・低層処理**: 
     - メンバー追加・除外時に自動システムメッセージ（例: 「〇〇さんを追加しました」）を内部的に送信。
  5. **副作用・非同期イベント**: 
     - WebSocket経由のリアルタイム画面更新および対象ユーザーへの非同期プッシュ/DB通知（`UserNotification`）。
- **出力・応答・状態変化**:
  - **成功時**: `ServiceProviderMessageRoom` モデルを返却。

## 3. 再走査・深層比較ログ (Phase 5)
- **最終再走査日**: 2026-09-21
- **発掘された未確認領域・補全履歴**:
  - 2026-09-21: `MessageService.php` のメッセージ送受信トランザクション、添付ファイル動的パス生成（`makeAttachmentPath`）、正規表現メンション抽出（`extractMentionIds`）、および Reverb ブロードキャスト連動処理の最深部仕様を解読・追記。
