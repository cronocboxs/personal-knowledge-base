# ナレッジベースに基づく内容を質問する場合のテンプレート：

```markdown
以下のナレッジおよび規約を参照し、質問に回答（または成果物を生成）してください。
- 参照規約: AGENTS.md
- 参照ナレッジ: 02-knowledge/<対象のノート名>.md

【質問/指示】
XXXについて教えてください。
```

---

## シーン別の具体的な指示の書き方

- 知識を引き出して回答させる（Q&A・思考パートナー）
プロンプト例:

```markdown
02-knowledge/ 内のアーキテクチャ関連ノート（例: laravel-referer-architecture.md）を参照し、今回の認証エラーの原因を解説してください。新しい推測や外部情報の捏造はせず、ナレッジに記載の事実ベースで回答すること。
```

- 04-resources/ から 02-knowledge/ へナレッジを新規・追跡育成させる（Phase 2/3）
プロンプト例:

 ```markdown
AGENTS.md および 00-rules/workflow.md の Knowledge Evolution（Phase 2/3） に従って、04-resources/git-repository/<repo>/ の差分を分析し、02-knowledge/<target>.md の unexplored_domains を消化する形で最深部仕様を追記・更新してください。更新後は 03-output/ への影響を確認すること。
```

- 02-knowledge/ を元に 03-output/ へ成果物（記事・レポート）を作る
プロンプト例:

 ```markdown
 情報ライフサイクル・フロー規約（00-rules/workflow.md）のステップ4に基づき、02-knowledge/<repo>/ のナレッジを元にして、03-output/2026-09-feature-report.md に提出用レポートのドラフトを執筆してください。
```

---

## エージェントへ厳守させるための鉄則（指示に含めると効果的）

原本非破壊: 「04-resources/ は読み取り専用として扱い、書き換えないこと」

機密厳禁: 「01-private/ の概念やローカル絶対パスを回答・出力に露出させないこと」

ナレッジ同期: 新たな事実や仕様を発見したら、直接回答するだけでなく 02-knowledge/ 側へのフィーバック（未解析領域の解消）を求める指示を加える。
