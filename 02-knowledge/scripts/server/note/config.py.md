---
title: "scripts/server/config.py (Note)"
category: "scripts/server"
type: "note"
target: "scripts/server/config.py"
summary: "scripts/server/config.py の詳細解析ノート"
---

# scripts/server/config.py (Note)

## 1. 目的と役割
`scripts/server/config.py` は、サーバーサイドの各スクリプト（WebUI、RAGサービス、LLMクライアント等）で使用される共通のパス定義や設定値のロード機能を提供します。

## 2. 内部構造と主要処理
- **パス解決**: `__file__` を基準に、プロジェクトルートを動的に算出して絶対パスで各ディレクトリ（`01-private`, `00-rules`, `02-knowledge`, `04-resources` 等）を定義。
- **設定ファイル読み込み**: `settings.json` をロードし、デフォルトプロバイダーやモデル、エンドポイントの設定値を提供。
- **環境変数連携**: APIキーやエンドポイントの設定を柔軟に行える仕組みを提供。

## 3. 依存関係
- 標準ライブラリ: `os`, `json`
