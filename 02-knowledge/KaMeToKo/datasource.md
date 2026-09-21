---
created: 2026-09-21
updated: 2026-09-21
tags: [KaMeToKo, datasource, spec, code-analysis]
phase: 4
status: active
unexplored_domains:
    - "予約・店舗管理ドメイン `app/Http/Controllers/Service/Reservation/` と `ManageReservationService.php` のトランザクション・通知処理"
    - "チャット・リアルタイム通信ドメイン `app/Http/Controllers/Provider/Room/` と `MessageService.php`, Reverb連携イベント"
---

# KaMeToKo データソース統合サービス (DataSource) 最深部仕様ナレッジ

## 1. 概要
`app/Services/DataSource/` は、Google Sheets, Excel, CSV, JSON といった多様な外部データソースから表形式データを統一インターフェース（`TabularDataSourceInterface`）を介して安全かつ効率的に取得・同期するためのモジュールです。

## 2. インターフェース・最深部処理トレース (Phase 2 & Phase 4 必須)

### 機能1: テーブル形式データソース同期・取得
#### トリガー1: 「Google Sheets / Excel 等からのチャンク単位データフェッチ処理」
- **最深部までの処理流転（Deep Logic Execution Flow）**:
  1. **エントリーポイント**: `App\Console\Commands\Google\SheetImport` などの Artisan コマンドまたは各サービス層からの呼び出し。
  2. **サービス・ドメイン層**: 
     - ファクトリ等を通じて `GoogleSheetsSource`, `ExcelSource`, `CsvSource`, `JsonSource` がインスタンス化される。
     - 各ソースは `TabularDataSourceInterface` を実装しており、`headers()` および `rows(int $offset, int $limit)` を提供。
  3. **内部プライベート関数・ヘルパー**:
     - **GoogleSheetsSource**: `HasGoogleClient` トレイトを経由して Google API Client を初期化。`$service->spreadsheets_values->get()` を用いてスプレッドシートの指定範囲（例: `Sheet1!1:1` や `Sheet1!A2:Z101`）にアクセス。APIのページネーションやチャンク範囲（`ChunkFetcher.php`）を制御。
     - **ColumnMapper**: 取得した未加工の配列データを、データベースカラム構造へマッピング・バリデーション。
  4. **データ永続化・低層処理**: 
     - 取得したチャンクをトランザクション内でDBにバルクインサートまたは更新（Upsert）。
  5. **副作用・非同期イベント**: 
     - インポート失敗時の例外スローとログ出力 (`SystemLogServiceProvider`).
- **Output / 応答・状態変化**:
  - **成功/失敗時の最深部挙動**: APIクォータ制限や不正なスプレッドシート構造による `Google_Service_Exception` 発生時はキャッチされ、上位サービスへログ付き例外を伝播。

## 3. 再走査・深層比較ログ (Phase 5)
- **最終再走査日**: 2026-09-21
- **発掘された未確認領域・補全履歴**:
  - 2026-09-21: `TabularDataSourceInterface` および `GoogleSheetsSource.php` の最深部APIコール（`spreadsheets_values->get`）の流転を解読・追記。 `unexplored_domains` から DataSource 領域を除外。
