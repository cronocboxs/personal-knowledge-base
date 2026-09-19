---
name: ingest-repo-knowledge
description: 04-resources/git-repository/ 配下のコードとログを解析し、02-knowledge/ 配下に構造化ノートとして蓄積・更新して git commit まで行う。APIレートリミットによる中断からのレジューム（途中再開）に対応。
---

# 役割

`04-resources/git-repository/<リポジトリ名>/` に配置されたソースコードや各種Gitメタデータをコードレベルまで詳細に解読し、AIが後から参照・活用しやすい概念ノート・仕様メモ（`overview.md`, `architecture.md` 等）として `02-knowledge/<リポジトリ名>/` 配下に整理・更新し、Git コミットまで完了させる。

## 前提条件（共通ルールの確認）

- 作業開始時に、リポジトリルート直下の `AGENTS.md` を必ず読み込み、そこに記載された「絶対遵守ルール」および「ディレクトリ編集ポリシー」に従うこと[cite: 4, 5]。

## 仕事

- **実行手順**:
  1. `04-resources/git-repository/<リポジトリ名>/history/` 配下の `file-tree.txt` や `stats.txt` を確認し、プロジェクト構造と変更頻度の高いコアモジュールを特定する。
  2. 主要な構成ファイル（`Dockerfile`, `docker-compose.yml`, `package.json`, `composer.json` 等）、エントリーポイント、ルーティング、および `stats.txt` 上位のソースコードを直接開いて実装ロジックを深掘り読解する。
  3. `02-knowledge/<リポジトリ名>/` を確認し、すでに作成済みのノート（`overview.md`, `architecture.md` 等）が存在するかチェックする。
  4. **レジューム処理**: すでに存在し内容が完成しているノートはスキップし、未作成または更新が必要な項目から解析・作成を再開する。
  5. 抽出した知見を Markdown ファイル群として1ファイルずつ作成・保存する（`00-rules/formatting.md` に従い YAML Frontmatter 等を付与する）[cite: 4, 5]。
  6. すべての解析・作成が完了したら、シェルツールを使用して変更ファイルをステージングし、以下の通りコミットを実行する:
     ```bash
     git add 02-knowledge/<リポジトリ名>/
     git commit -m "auto(doc): <リポジトリ名>のナレッジを追加・更新"
     ```

- **やらないこと**:
  - `04-resources/` 内の一次情報原本の改変・編集・直接削除（読み取り専用）[cite: 4, 5]。
  - ソースコード内に存在する暗号鍵やパスワード等の秘密情報をサニタイズ（マスキング）せずに `02-knowledge/` へ書き出すこと[cite: 4, 5]。
  - `01-private/` 配下へのアクセス[cite: 4, 5]。

- **レートリミット・エラーハンドリング**:
  - APIのレートリミット（`Rate limit exceeded` / `Quota exceeded`）が発生した場合は、それまでに作成できたファイルはそのままとし、どこまで完了して何が未完了かをログに出力して終了する（次回実行時にレジューム可能）。

- **入力**:
  - `04-resources/git-repository/<リポジトリ名>/clone/<ブランチ>/` 内のソースコード
  - `04-resources/git-repository/<リポジトリ名>/history/` 内の解析用メタデータ（`file-tree.txt`, `stats.txt`, `raw-git-log.txt`, `contributors.txt`, `active-branches.txt`）

- **出力先**:
  - `02-knowledge/<リポジトリ名>/`[cite: 4, 5]

- **終わりの条件**:
  - リポジトリの主要構成要素・ソースコードの実装仕様が `02-knowledge/<リポジトリ名>/` 内にすべて漏れなく構造化ノートとして書き出され、git commit が正常完了した時点。

- **止まる条件**:
  - `04-resources/git-repository/` 内に対象となるリポジトリ資料が存在しない場合。
  - APIのレートリミット等で処理が中断された場合（次回実行で続きから再開可能）[cite: 4]。
  - pre-commit フックでエラーが検知され、git commit に失敗した場合[cite: 4]。