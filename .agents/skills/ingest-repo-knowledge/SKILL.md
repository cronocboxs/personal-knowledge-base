---
name: ingest-repo-knowledge
description: 04-resources/git-repository/ 配下のコードを解析し、02-knowledge/ 配下のナレッジを段階的（Phase 1〜3）に深掘り・反復更新して git commit まで行う。
---

# 役割

`04-resources/git-repository/<リポジトリ名>/` 内のソースコードを読み込み、`00-rules/workflow.md` で定義された **Knowledge Evolution（Phase 1〜3）** に従って `02-knowledge/<リポジトリ名>/` 配下のナレッジノートを実体コードレベルまで深掘り作成・更新し、Git コミットまで完結させる。

---

## 前提条件（共通ルールの確認）

- 作業開始時に、リポジトリルート直下の `AGENTS.md` および `00-rules/workflow.md` を必ず読み込み、そこに記載された「絶対遵守ルール」「ディレクトリ編集ポリシー」「ナレッジ育成ルール」に従うこと。

---

## 知識進化（Knowledge Evolution）判定規則

`02-knowledge/<リポジトリ名>/` 内の各ノートの Frontmatter 内にある `phase` タグを確認し、以下の基準で深掘り処理を行ってください。

| 現在の Phase | 昇進（進級）の必須条件 | 今回実行すべき深掘りタスク |
| :--- | :--- | :--- |
| **未作成** | なし | **Phase 1 (概要・構造把握)**: 全体像、ディレクトリ役割、依存ライブラリ、基本ルーティングの整理 |
| **Phase 1** | 単なるディレクトリ/ファイル一覧しか存在しない | **Phase 2 (詳細・データフロー解読)**: コントローラー、サービス、モデル、Vueコンポーネントの実装コードを直接閲覧し、具体的処理とデータ連携（リクエスト〜レスポンス）を追記 |
| **Phase 2** | コード処理の解説はあるが「設計意図・責務分離」がない | **Phase 3 (背景・設計思想抽出)**: 責務分離（Service/Action/Repository）、状態管理（Pinia/Inertia）、認可（Policy/Gate）、共通化パターンの抽象化 |
| **Phase 3** | コード・設計思想ともに完備 | **メンテナンス**: 直近の Git コミット差分を確認し、変更箇所のナレッジのみ追記・最新化 |

---

## 仕事

- **実行手順**:
  1. `02-knowledge/<リポジトリ名>/` 内の既存ノート（`overview.md`, `architecture.md`, `domain-logic.md` 等）の Frontmatter (`phase`) を読み取り、今回着手すべきターゲットノートと目標 Phase を決定する。
  2. `04-resources/git-repository/<リポジトリ名>/` 配下のソースコード（`routes/`, `app/`, `resources/js/` 等）を直接参照（`read`/`view`）する。
  3. 各ノートに以下の **【必須記述フォーマット】** を満たす形で深掘り成果を書き込む（更新時は `phase` の値を引き上げる）。
  4. 更新完了後、サニタイズ処理（機密情報のマスキング）を確認の上、以下の通りコミットを実行する:
     ```bash
     git add 02-knowledge/<リポジトリ名>/
     git commit -m "auto(doc): <リポジトリ名> のナレッジを Phase X へ昇華更新"
     ```

- **必須記述フォーマット（02-knowledge 配下の各ファイル構造）**:
  ノート作成・更新時は、単なる箇条書きを禁止し、必ず以下の構文を含めて記述すること。
  ```markdown
  ---
  created: YYYY-MM-DD
  updated: YYYY-MM-DD
  tags: [repository-name, laravel, vue, domain]
  phase: 2 # 1 | 2 | 3
  status: active
  ---

  # [モジュール/機能名] ナレッジノート

  ## 1. 概要と役割 (Phase 1)
  - モジュールの目的と担当領域

  ## 2. コードレベルの処理・データフロー (Phase 2 必須)
  - **参照ファイル**: `app/Http/Controllers/XxxController.php`, `resources/js/Pages/Xxx.vue`
  - **リクエスト〜レスポンスの流れ**:
    1. Route `POST /xxx` ➔ Middleware ➔ `XxxController@store`
    2. `XxxService::create()` に処理を移送し、`XxxModel::create()` で永続化
    3. Inertia / JSON レスポンスとして Vue コンポーネントへ渡される Props 構造
  - **主要ロジック・バリデーションルール**: FormRequest や Service 内のビジネスルール詳細

  ## 3. アーキテクチャ・設計思想 (Phase 3 必須)
  - **責務分離の方針**: なぜこのロジックが Service / Action に切り出されているか
  - **状態管理とイベント**: Piniaストアの利用範囲、Domain Event / Observer の発火条件

- **やらないこと**:
  - 実際のソースコードファイルを開かずに、ディレクトリ名やファイル名からの推測のみで記述すること。
  - ファイル構成やパスの単なる箇条書き羅列（「〜〜があります」で終わる記述の禁止）。
  - `04-resources/` 内の一次情報の直接編集・削除。
  - 機密情報（APIキー、パスワード等）の書き出し。

- **入力**:
  - 04-resources/git-repository/<リポジトリ名>/clone/<ブランチ>/ 配下のソースコード
  - 04-resources/git-repository/<リポジトリ名>/history/ 配下のログ・ファイルツリー

- **出力先**:
  - 02-knowledge/<リポジトリ名>/ 配下の Markdown ファイル群

- **終わりの条件**:
  - 対象ノートの Frontmatter が phase: 3 まで更新され、コードレベルのデータフローおよび設計思想の解読が記録された状態で git commit が正常完了した時点。

- **止まる条件**:
  - 04-resources/git-repository/<リポジトリ名>/ に対象のコードが存在しない場合。
  - API のレートリミット（Rate limit exceeded）が発生した場合（作成途中のファイルを保存して進捗をログに出力し終了）。
  - pre-commit フックでエラーが発生し、自動修復が不可能な場合。

- **レートリミット・エラーハンドリング**:
  - API制限（Quota / Rate limit）が発生した場合は、その時点で完了しているファイルのみを保存し、次回実行時にそのフェーズからレジュームできるようにログを残して終了する。
