---
name: ingest-repo-knowledge
description: 04-resources/git-repository/ 配下のコードを解析し、02-knowledge/ 配下のナレッジを段階的（Phase 1〜3）に深掘り・反復更新して git commit まで行う。
---

# 役割

`04-resources/git-repository/<リポジトリ名>/` 内のソースコードを読み込み、`02-knowledge/<リポジトリ名>/` 配下のノートを**「実行するたびに知識が深まる（反復進化）」**ルールに従って更新・作成し、Git コミットまで完結させる。

## 前提条件

- 作業開始時に `AGENTS.md` を必ず読み込み、「絶対遵守ルール」および「ディレクトリ編集ポリシー」に従うこと。

## 知識進化（Knowledge Evolution）アルゴリズム

`02-knowledge/<リポジトリ名>/` 内の既存ノートを読み込み、現在の達成フェーズを判定した上で**次のレベルへ深掘り・追記**してください。

| フェーズ | 判定基準 | 今回実行すべきアクション |
| :--- | :--- | :--- |
| **未作成** | ファイルが存在しない | **Phase 1 (概要作成)**: ディレクトリ構造、全体像、依存ライブラリの書き出し |
| **Phase 1** | 目録や一覧のみ記載されている | **Phase 2 (コード深掘り)**: 主要な Controller, Service, Model, Vueコンポーネントの具体的な処理・データフロー（リクエスト〜レスポンス）をコードレベルで解読して追記 |
| **Phase 2** | コード処理の解説はあるが設計思想がない | **Phase 3 (設計思想の抽出)**: 「なぜこの設計か」、責務分離（Service/Repository/Action）、状態管理（Pinia/Inertia）、認可（Policy）などの設計原則・パターンの抽出 |
| **Phase 3** | 設計思想・アーキテクチャまで完備 | **メンテナンス**: 新しい Git コミットによる差分・変更点がないか確認し、あれば差分のみ追記更新 |

---

## 解析ガイドライン（深掘り観点）

コードを解析する際、以下の **Laravel 12 + Vue 3 アーキテクチャ観点** を必ず意識して読み取ること。

### 1. ドメイン領域と設計パターンの特定
- **アーキテクチャ方針**: Action / Service / Repository / Trait 等の責務分離方針。ビジネスロジックは Controller に直書きされているか、Service層やActionクラスに閉じ込められているか？
- **DB & Model**: リレーション（Eloquent）、Scope、Accessor/Mutator、Cast、Domain Events / Observers の活用状況。
- **バリデーション & 認可**: FormRequest の設計、Policy / Gate による認可ロジック。

### 2. Vue 3 + フロントエンド設計思想
- **結合方式**: Inertia.js によるモノリス統合か、Blade + Vite によるコンポーネント埋め込みか、完全分離 API (Sanctum/JWT) か？
- **State Management**: Composition API (script setup) / Composables (useXxx) / Pinia / Stores の利用パターン。
- **UI & Event**: Props / Emits のデータフロー、共通コンポーネントの抽象化レベル。

### 3. モジュール間のデータ連携フロー
- ユーザーのリクエストが **Route ➔ Middleware ➔ Controller ➔ Service/Model ➔ Vue (Props/State)** へ到達し、レスポンスが返るまでの一連のシナリオをトレースする。

---

## 仕事

- **実行手順**:
  1. `02-knowledge/<リポジトリ名>/` 配下のノートを確認し、対象リポジトリのナレッジが現在どのフェーズ（Phase 1〜3）にあるか判定する。
  2. 未達フェーズの解読に必要なソースコード（`app/`, `resources/js/` 内の実装）および履歴メタデータ（`file-tree.txt`, `stats.txt`）を開く。
  3. 解読結果を `02-knowledge/<リポジトリ名>/` 配下のノート（`overview.md`, `architecture.md`, `components.md` 等）に追記・更新する（YAML Frontmatter も更新）。
  4. 完了後、変更ファイルをステージングし、コミットを実行する:
     ```bash
     git add 02-knowledge/<リポジトリ名>/
     git commit -m "auto(doc): <リポジトリ名> のナレッジを Phase X へ深掘り更新"
     ```

- **やらないこと**:
  - ディレクトリ構造やファイル名をただ箇条書きで羅列して終了すること（「どう動くか」「なぜその設計か」を必ず記述する）。
  - すでに Phase 3 まで到達している記述を削除したり、内容を後退させること。
  - `04-resources/` 内の一次情報の直接編集・削除。
  - 機密情報（APIキー、パスワード等）の書き出し。

- **レートリミット・エラーハンドリング**:
  - API制限（Quota / Rate limit）が発生した場合は、その時点で完了しているファイルのみを保存し、次回実行時にそのフェーズからレジュームできるようにログを残して終了する。

- **終わりの条件**:
  - 対象リポジトリのナレッジが Phase 3（設計思想・データフローの解読完了）まで昇華し、`git commit` が正常終了した時点。