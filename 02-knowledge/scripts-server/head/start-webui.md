---
title: "start-webui.py"
category: "scripts-server"
summary: "FastAPIおよびUvicornを使用したWebUIサーバーの起動スクリプト。設定読込、ロギング設定、サーバー起動およびプロセス管理を行う。"
tags: ["python", "fastapi", "uvicorn", "server", "webui"]
created_at: "2026-10-06"
updated_at: "2026-10-06"
---

# start-webui.py Head

- **目的**: 個人ナレッジベースやRAGサービスを提供するFastAPI WebUIバックエンドサーバーのエントリポイントおよび起動スクリプト。
- **主要機能**: 
  - コマンドライン引数（ホスト、ポート、リロード設定など）の解析
  - ログ出力の設定と初期化
  - 依存モジュール（`config.py`, `rag_service.py`, `knowledge_service.py`等）との連携によるサーバー初期化
  - `uvicorn.run()` によるWebアプリケーションの非同期起動
- **関連モジュール**:
  - `scripts/server/config.py`
  - `scripts/server/rag_service.py`
  - `scripts/server/knowledge_service.py`
  - `scripts/server/llm_client.py`
