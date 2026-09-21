---
created: 2026-09-21
updated: 2026-09-21
tags: [KaMeToKo, spec, code-analysis, deep-logic]
phase: 4
status: active
unexplored_domains: []
---

# KaMeToKo 最深部ロジック・処理トレースナレッジ (Phase 4 / Phase 5)

本ドキュメントでは、KaMeToKo リポジトリ（Laravel 12.0）におけるサービス層、カスタムCasts、モデルTraits、DBトランザクション、非同期イベント、例外ハンドリングなどの最深部ロジックを体系的に記録する。

## 1. カスタムCastsとデータ変換ロジック
### `RruleCast` (`app/Casts/RruleCast.php`)
- **役割**: カレンダーや予約機能で使用される繰り返しルール（RRULE）をデータベース保存形式とオブジェクト間で双方向変換するカスタムEloquent Cast。
- **最深部ロジック**:
  - `get()` 呼び出し時: DB上の文字列（iCalendar形式等のRRULE文字列）を受け取り、`simshaun/recurr` ライブラriを用いてパース、操作可能な `RRule` オブジェクトまたはラップ構造に変換する。
  - `set()` 呼び出し時: アプリケーション側のオブジェクトや配列から、標準的なRRULE構文の文字列にシリアライズしてデータベースへ永続化する。

## 2. モデル・Traitsによる権限・サービス連携ロジック
### ユーザーモデル群 (`app/Models/User/Trait/`)
- **役割**: 巨大化しがちな `User` モデルの責任を責務ごとに分離するための Traits 群。
  - `UserTraitRole.php` / `UserTraitServiceRole.php`: スパティ権限パッケージ（`spatie/laravel-permission`）と連携し、グローバルおよび特定サービス単位でのロール・権限判定 (`hasRole`, `hasPermissionTo` 等) を抽象化・ラップする。
  - `UserTraitAuth.php` / `UserTraitBan.php`: 認証状態の判定、パスキー連携、BAN（凍結）状態の厳格なチェック。
  - `UserTraitRelation.php` / `UserTraitServiceRelation.php`: マルチテナント的なプロバイダ（Provider）や各サービス（勤怠、予約、会計など）との多対多・一対多のリレーション定義と動的クエリ構築。

## 3. データベース・クエリログ監視・監査ログ最深部挙動
### `DataBaseQueryServiceProvider` / `SystemLogServiceProvider` (`app/Providers/`)
- **役割**: アプリケーション全体で実行される生クエリの監視、スロークエリ検知、およびユーザのアクション履歴（ActionLog）の自動記録。
- **最深部ロジック**:
  - `DB::listen()` を活用し、すべてのクエリ発行時にバインドパラメータを置換してロギングまたは監査証跡（ActionLog）テーブルへの非同期書き込みを行う。

## 4. 再走査・深層比較ログ (Phase 5)
- **最終再走査日**: 2026-09-21
- **発掘された未確認領域・補全履歴**:
  - 2026-09-21: `RruleCast` による繰り返しルールのシリアライズ・パース処理、および `User` モデルの Traits 分割構造（権限・サービス連携）を最深部レベルで解読・追記完了。
