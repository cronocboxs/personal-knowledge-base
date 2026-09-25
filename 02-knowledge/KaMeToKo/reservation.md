---
created: 2026-09-21
updated: 2026-09-21
tags: [KaMeToKo, reservation, spec, code-analysis]
phase: 4
status: active
unexplored_domains: []
---

# KaMeToKo 予約・店舗管理ドメイン 最深部仕様ナレッジ

## 1. 概要
`app/Services/Service/Reservation/ManageReservationService.php` および関連コントローラーは、店舗のマルチテナント環境下における予約・カレンダーデータ取得、空き席自動割り当て、重複チェック、および予約作成・更新のトランザクションを包括的に管理します。

## 2. インターフェース・最深部処理トレース (Phase 2 & Phase 4 必須)

### 機能1: 予約登録・更新および空き状況トランザクション
#### トリガー1: 「ストアスタッフまたは管理画面からの予約作成・更新リクエスト」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: `App\Http\Controllers\Service\Reservation\ManageController::save()` などのコントローラーアクション。
  2. **サービス・ドメイン層**: 
     - `ManageReservationService::saveReservation()` が呼び出され、入力されたバリデーション済みリクエストデータを検証。
     - コース情報やスタッフ情報、店舗アセット（席・設備）の紐づきを取得・検証。
  3. **内部プライベート関数・ヘルパー**:
     - **席の自動割り当て (`ServiceReservation::findAvailableAsset`)**: 予約時にアセットIDが指定されていない場合、指定された日時、時間帯、ゲスト人数に収容可能な空き席を自動検索・割り当て。
     - **重複・可否チェック (`ServiceReservation::checkAvailability`)**: 同一店舗内でのスタッフのスケジュール重複、アセットの重複予約、店舗の営業時間内判定を低層クエリで厳密にチェック。
  4. **データ永続化・低層処理**: 
     - データベーストランザクション（LaravelのDBファサード等）内で `ServiceReservation` モデルへの `fill()` および `save()` を実行し、価格（コース価格の適用または既存保持）を確定・永続化。
  5. **副作用・非同期イベント**: 
     - 予約確定・変更時に連動する通知イベントやステータス更新のディスパッチ。
- **Output / 応答・状態変化**:
  - **成功時の最深部挙動**: 新規作成または更新された `ServiceReservation` モデルインスタンスを返却。
  - **失敗時の最深部挙動**: 空き枠なしや条件不整合がある場合、バリデーションエラーまたはエラーメッセージ配列（`['error' => "..."]`）を返却し、トランザクションをロールバック。

## 3. 再走査・深層比較ログ (Phase 5)
- **最終再走査日**: 2026-09-21
- **発掘された未確認領域・補全履歴**:
  - 2026-09-21: `ManageReservationService.php` の空き席自動割り当て（`findAvailableAsset`）および重複チェック（`checkAvailability`）の最深部処理流転を解読・追記。 `unexplored_domains` から予約ドメインを除外。
