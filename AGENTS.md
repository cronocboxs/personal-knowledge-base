# AGENTS.md - Root Guidelines

当リポジトリ（personal-knowledge-base）は、AIエージェントおよび自動化スクリプトとの協調運用を前提とした構造化ナレッジベースです。
すべてのAIエージェント（Claude, Cursor, Copilot, 独自スクリプト等）は、本ファイルの絶対ルールおよび `00-rules/` 内の各規約の遵守を最優先とします。

---

## 1. 最優先行動原則（即時適用）

1. **`ls` コマンドの実行は完全禁止**:
   - ファイルの存在確認や一覧取得のために `ls`, `ls -la`, `find` を実行してはならない。
   - ファイルの存在・パス確認は、**必ず `02-knowledge/global-index.json` または各階層の `index.json`（例: `02-knowledge/subsidies/index.json`）を 1 回 `read` して特定すること**。

2. **重複チェックの標準フロー**:
   - 未解析の制度（またはファイル）を特定する際は、`ls` ではなく `02-knowledge/subsidies/index.json` を `read` し、`nodes` の中に該当する `id`（slug）が存在するかどうかで判定すること。

3. **完了時の同期義務**:
   - ファイルの新規作成・更新が完了したら、最後に以下を実行してインデックスを更新すること。
     `./scripts/run-markdown-index.sh <更新したディレクトリパス>`

4. **最高機密・原本保護**:
   - `01-private/` へのアクセス禁止。
   - `04-resources/` は読み取り専用（原本変更禁止）。
   - 直接削除（`rm`）禁止。不要物は `99-trash/` へ移動。

---

## 2. ディレクトリ構造と編集ポリシー（Directory Index）

| ディレクトリ | 役割 | エージェントの編集権限・ルール |
| :--- | :--- | :--- |
| `00-rules/` | システム規約・フォーマット | **参照および運用性向上のための自律改変許可**（要 `04-resources/logs/` 変更ログ記録） |
| `01-private/` | 個人情報・秘密情報 | **最高機密**: `.gitignore` 対象。外部送信・要約出力厳禁 |
| `02-knowledge/` | 自分に関する事実、体系化された知見・概念メモ | 新規作成・追記（構造化されたMarkdown）。最深部ロジックの解読・蓄積 |
| `03-output/` | 作った成果物・記事・コード | 生成物・ドラフトの配置。`02-knowledge/` の内容から作成する |
| `04-resources/` | 参照資料・Web素材・一次情報の原本 | 入力データの保管・参照・要約元の配置。書き換え不可（`logs/` の新規出力のみ例外許可） |
| `05-todo/` | タスク・プロジェクト | ステータス更新・タスク追加・ロードマップ |
| `06-storage/` | 動画・PDF等の大容量ファイル・バイナリ | `.gitignore` 対象。Git管理不能な大容量データ置き場 |
| `99-trash/` | 一時廃棄 | 不要ファイルの退避場所（直接削除禁止） |
| `scripts/` | 自動化・メンテナンス | 整理・更新・検証・コード全件比較スクリプトの配置・実行 |
| `.agents/skills/` | エージェント手順書・スキル定義 | エージェント用タスク定義ファイルの参照・機能追加・メンテナンス |

---

## 3. 詳細規約インデックス（Detailed Rules）

具体的な運用手順やフォーマット規定については、作業内容に応じて以下の規約を参照してください。

* **情報ライフサイクル・フロー規約**: [00-rules/workflow.md](./00-rules/workflow.md)
* **ファイル分類・配置判定規約**: [00-rules/classification.md](./00-rules/classification.md)
* **ファイル命名・記述・メタデータ規約**: [00-rules/formatting.md](./00-rules/formatting.md)
* **エージェント行動規範・連携規約**: [00-rules/agent-behavior.md](./00-rules/agent-behavior.md)
* **プライバシー・セキュリティ規約**: [00-rules/privacy-security.md](./00-rules/privacy-security.md)
