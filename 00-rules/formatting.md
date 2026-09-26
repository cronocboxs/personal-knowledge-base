# ファイル命名・記述・メタデータ規約

AIエージェントがファイルを作成・更新する際は本規約に従うこと。

---

## 1. 命名規則

- 原則 `kebab-case.md`（例: `check-permission.md`）。

## 2. メタデータ (YAML Frontmatter)

新規・更新ファイル先頭には必ず以下のメタデータを付与すること。

```yaml
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [tag1, tag2]
status: draft # draft | active | archived
phase: 0 # 0:未着手 | 1:目録化 | 2:概要完了 | 3:一巡完了 | 4:最深部解読中 | 5:完全網羅
parent: [] # 上位ノート（親）
children: [] # 下位ノート（子）
related: [] # 連動・参照する関連ノート
task: [] # 解析対象・次タスク
---
```

### `task` プロパティの記述パターン

- コード閲覧指示: "app/Controller/Controller.php # 左のファイルについて調査"
- TODO参照指示: "05-todo/todo.md # 05-todoに配置された次タスクファイル"
- 関数深掘り指示: "UserModel::auth() # 次に調べる関数名"

## 3. ナレッジファイルの出力二層化ルール (head & note)

`02-knowledge/` 配下の保存時は、以下 2 箇所へ完全同期して出力すること。

1. `head/` ディレクトリ: YAML Frontmatter のみ出力（検索・grep高速化用）。
2. `note/` ディレクトリ: Frontmatter ＋ 本文を出力。

---

## 4. 先行宣言ルール (head-only Stub)

1. 解析時に新たな関連ドメインを発見した場合、`parent` / `children` / `related` にノート名を追加する。
2. 該当ノートが未存在（`note/` 配下にない）場合、`head/` 配下のみに `phase: 0` の YAML ファイルを作成する（`note/` 側には作成しない）。
3. 解析着手時に `phase` を 1 以上へ引き上げ、`note/` 配下に本文付きノートを出力する。
