---
created: 2026-09-19
updated: 2026-09-19
tags: [knowledge, overview, personal-knowledge-base, architecture]
---

# personal-knowledge-base 概要・動作環境 (`overview.md`)

## 1. プロジェクトの目的・全体像
`personal-knowledge-base` は、AIエージェント（Claude, Cursor, Copilot, Goose等）および自動化スクリプトとの協調運用を前提とした構造化ナレッジベースです。
人間の手動メンテナンス負担を減らし、AIエージェントが自律的に一次情報を取得・整理し、ナレッジの生成やドキュメント作成を行うためのフレームワークを提供します。

## 2. 技術スタック
- **言語 / ランタイム**: Shell Script (`bash`), Markdown
- **依存ツール / フック**: Git, Gitleeks (シークレット検出), Git Hooks (`pre-commit`)
- **AIエージェント基盤**: Goose (Agentic AI Foundation) および各種エージェントスキル (`.agents/skills/`)

## 3. 環境構築・実行手順
リポジトリのセットアップやスクリプトの実行に関する手順は以下の通りです。

### リポジトリのクローン・初期化
```bash
git clone <repository-url> personal-knowledge-base
cd personal-knowledge-base
```

### Git Hooks（pre-commit / Gitleeks）の設定
コミット時のセキュリティチェックおよび構造チェックを有効化するため、Git hooksを設定します。
```bash
git config core.hooksPath .githooks
```

### メンテナンススクリプトの実行
リポジトリ内の構造チェックやGit履歴の取得は `scripts/` 配下のスクリプトで行います。
- **構造チェック**:
  ```bash
  bash scripts/check-structure.sh
  ```
- **Git履歴の取得**:
  ```bash
  bash scripts/fetch-git-log.sh <リポジトリ名>
  ```
