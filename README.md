# パーソナルナレッジベース　＆　AIエージェント

```markdown
[1. 収集フェーズ (Script)]
  └─ scripts/fetch-*.sh や Pythonスクリプトを実行
  └─ 外部情報・ローカルデータを 04-resources/ に格納（一次資料・原本保護）

[2. 実行フェーズ (AI Agent)]
  └─ .agents/skills/ 内の手順書（Skill）および 00-rules/ を読み込み
  └─ 04-resources/ の情報を元に 02-knowledge/ や 03-output/ に成果物を生成
  └─ ルール変更が必要な場合は 04-resources/logs/ に理由を出力して 00-rules/ を更新

[3. 確認・検証フェーズ (Human & Hook)]
  └─ 人間が生成物（03-output/ 等）を確認・推敲
  └─ git commit 実行時に .githooks/pre-commit が自動割り込み
  └─ scripts/check-structure.sh ＋ gitleeks によるサニタイズ・漏洩最終検証
```