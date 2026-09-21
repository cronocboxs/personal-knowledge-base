---
created: 2026-09-20
updated: 2026-09-20
tags: [KaMeToKo, spec, code-analysis, provider]
phase: 3
status: active
unexplored_domains: []

# プロバイダ管理・機能 (Provider) 挙動・処理仕様ナレッジ

## 1. 識別された機能・インターフェース一覧
- [x] プロバイダダッシュボード (`Provider/DashboardController.php`)
- [x] ルーム・チャット・リアルタイム通信 (`Provider/Room/`, `Provider/Chat/ChatMessageController.php`)
- [x] 参加・申請管理 (`Provider/Join/`, `Provider/Apply/`)
- [x] 招待管理 (`Provider/Invite/`)
- [x] ユーザー・ロール・権限管理 (`Provider/UserController.php`, `Provider/RoleController.php`)
- [x] プロバイダ切り替え・プロフィール (`Provider/SwitchController.php`, `Provider/ProfileController.php`)
- [x] 添付ファイル管理 (`Provider/AttachmentController.php`)

## 2. インターフェース・トリガー別詳細トレース (Phase 2)

### 機能1: ルーム・チャット機能 (`Provider/Room/RoomController`, `MessageController`)
#### トリガー: 「チャットメッセージ送信・閲覧操作」
- **入力・要求（Input/Request）**:
  - `room_id`: ルーム識別子
  - `message`: 送信メッセージ本文（テキスト、添付ファイル等）
- **内部処理流転（Execution Flow）**:
  1. ユーザーが当該ルームへのアクセス権限（Spatie Permission 等）を持っているかを検証。
  2. メッセージをデータベースに保存。
  3. `Laravel Reverb` を用いて、該当チャットチャンネルへリアルタイムイベント (`MessageCreated` 等) をブロードキャスト。
- **出力・応答・状態変化（Output/Response/State Change）**:
  - **成功時**: JSON レスポンスおよび WebSocket 経由で接続中のクライアントへメッセージが即時配信され、UIが更新される。

### 機能2: 招待・参加管理 (`Provider/Invite/`, `Provider/Join/`)
#### トリガー: 「メンバー招待リンク発行 / 参加申請承認」
- **入力・要求（Input/Request）**:
  - 招待先メールアドレス、付与ロール情報
- **内部処理流転（Execution Flow）**:
  1. 招待トークンの生成と有効期限の設定。
  2. メールの送信（または招待リンクの生成）。
  3. ユーザーがリンクにアクセスして承認または登録を行うことでプロバイダに紐づけ。
- **出力・応答・状態変化（Output/Response/State Change）**:
  - プロバイダのユーザーリストへ新規メンバーが追加される。
