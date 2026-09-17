# ファイル分類・配置判定規約 (Classification & Routing Rules)

AIエージェントが新たな情報・ファイル・テキストを入力された際、配置先のディレクトリを迷わず判定するための分類ルールです。

---

## 1. 自動判定フローチャート (Decision Tree)

情報を取得・入力されたら、上から順番に条件を判定し、最初に合致したディレクトリへ配置してください。

1. **機密・個人情報か？**
   * YES ➔ `01-private/`（※ただしAIは直接書き込まず、ユーザーに手動配置を促すか報告のみ行う）
2. **動画・PDF・音声・大容量バイナリか？**
   * YES ➔ `06-storage/`
3. **外部からのWebクリップ・他人の記事・未加工の一次資料・ログ・コード原本か？**
   * YES ➔ `04-resources/`（原本保護のため読み取り専用）
4. **自身に関する事実、または `04-resources/` から抽出・概念化した自分の知見ノートか？**
   * YES ➔ `02-knowledge/`
5. **ブログ記事・提出用レポート・コード成果物など、公開・出力用の完成品/推敲中ドラフトか？**
   * YES ➔ `03-output/`（`02-knowledge/` を元に作成）
6. **タスク・TODO・プロジェクト計画・進行中のロードマップか？**
   * YES ➔ `05-todo/`
7. **エージェント定義・プロンプト・コンテキスト構造か？**
   * **手順書・作業フロー指示** ➔ `.agents/skills/`
   * **ペルソナ・システムプロンプト** ➔ `.agents/prompts/`
   * **出力用フォーマット雛形** ➔ `.agents/templates/`
   * **長期記憶・会話フィードバック** ➔ `.agents/memories/`
8. **PythonやBashなど、機械・プログラムが直接実行する自動化スクリプトか？**
   * YES ➔ `scripts/`

---

## 2. ディレクトリ別 判定基準マトリクス

| ディレクトリ | 判定キーワード・特徴 | 含まれるファイル例 | 編集権限 |
| :--- | :--- | :--- | :--- |
| `01-private/` | パスワード、APIキー、個人識別情報、日記、非公開メモ | `passwords.md`, `private-log.md` | **AIアクセス厳禁** |
| `02-knowledge/` | 「〜とは何か」「〜の概念」「自分のスキル/経験の整理」 | `laravel-referer-architecture.md`, `my-profile.md` | 追記・新規作成 |
| `03-output/` | 「〜向け記事」「提出用ドキュメント」「公開コード」 | `2026-09-blog-post.md`, `app-script.js` | 追記・新規作成 |
| `04-resources/` | 他人・外部が作成した一次情報、Webスクレイピング結果、RAWデータ | `article-clip.md`, `raw-api-response.json` | **読み取り専用** |
| `05-todo/` | 「〜をやる」「ロードマップ」「進捗管理」「タスク」 | `todo-list.md`, `project-x-roadmap.md` | 更新・追記 |
| `06-storage/` | 動画(`.mp4`), 大量画像(`.zip`), 大容量PDF | `presentation-video.mp4`, `dataset.zip` | 移動・配置 |
| `scripts/` | **機械実行用プログラム**: 定型処理、データ変換、バッチスクリプト | `backup.sh`, `fetch-rss.py` | 実行・作成・保守 |
| `.agents/skills/` | **AI手順書**: エージェント用指示書、タスクプロンプト、拡張定義 | `summarize-article.md`, `search-web/` | 参照・機能追加 |
| `.agents/prompts/` | **AIペルソナ**: 振る舞い・思考スタンス・基本システムプロンプト | `persona-editor.md`, `code-reviewer.md` | 参照・必要時更新 |
| `.agents/templates/` | **出力雛形**: 記事やナレッジの標準フォーマット | `knowledge-template.md`, `report-format.md` | 参照・更新 |
| `.agents/memories/` | **長期記憶**: 過去のセッション文脈、ユーザーの好み、修正履歴 | `user-preferences.md`, `feedback-log.md` | 追記・自動更新 |

---

## 3. 判断が曖昧な場合のフォールバック

* **情報源が外部か内部か迷った場合**:
  * 外部の情報をそのまま保存する場合はまず `04-resources/` に配置する。
  * 自分の言葉で要約・整理し直した時点で `02-knowledge/` に新規作成する。
* **エージェント定義で迷った場合**:
  * 実行手順であれば `.agents/skills/` に寄せ、概念が増えた段階で上記のサブディレクトリへ整理する。
* **削除するか迷った場合**:
  * 物理削除は行わず、必ず `99-trash/` へ移動する。