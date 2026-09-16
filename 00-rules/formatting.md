# ファイル命名・記述・メタデータ規約

AIエージェントがファイルを作成・更新する際は、本規約に従ってください。

---

## 1. ファイル命名規則

* 原則 `kebab-case.md`（例: `laravel-referer-check.md`）または日付プレフィックス `YYYY-MM-DD-title.md` を使用すること。

## 2. メタデータ (YAML Frontmatter)

* 新規Markdownファイルの先頭には、必ず以下のメタデータを付与すること。

```yaml
---
created: YYYY-MM-DD
tags: [tag1, tag2]
status: draft # draft | active | archived
---
```

* **非破壊原則**: ファイルの直接削除（`rm`）は禁止。不要ファイルは `99-trash/` へ移動
* **スクリプト活用**: 定型・バッチ処理は `scripts/` 内の既存コードを利用するか新規スクリプトを作成
