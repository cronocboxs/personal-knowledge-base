#!/usr/bin/env python3
"""05-todo 配下のタスクリスト初期化・レジューム制御スクリプト"""

import os
import sys

def main():
    todo_path = os.environ.get("PY_TODO_FILE")
    target_path = os.environ.get("PY_TARGET_PATH")
    force_flg = os.environ.get("PY_FORCE_FLG") == "true"
    agent_name = os.environ.get("PY_AGENT_NAME")
    today = os.environ.get("PY_TODAY")

    if not todo_path or not target_path:
        print("❌ エラー: 環境変数が不足しています", file=sys.stderr)
        sys.exit(1)

    # 既にTODOファイルが存在し、forceフラグもない場合はスキップ (レジューム)
    if os.path.exists(todo_path) and not force_flg:
        print(f"🔄 既存のタスクリストを読み込みます (レジューム): {todo_path}")
        return

    files = []
    if os.path.isfile(target_path):
        files = [target_path]
    elif os.path.isdir(target_path):
        for root, _, filenames in os.walk(target_path):
            for f in filenames:
                if f.endswith(('.py', '.md', '.json', '.sh', '.js', '.ts', '.yml', '.yaml', '.php')):
                    rel_p = os.path.relpath(os.path.join(root, f))
                    files.append(rel_p)

    files.sort()

    content = "---\n"
    content += f"created: {today}\n"
    content += f"updated: {today}\n"
    content += f"tags: [todo, {agent_name}]\n"
    content += "status: active\n"
    content += "task:\n"
    content += f'  - "{todo_path} # 本タスクリスト"\n'
    content += "---\n\n"
    content += f"# {agent_name} Tasks: {target_path}\n\n"
    content += "## Target Directory\n\n"
    content += f"`{target_path}`\n\n"
    content += "## Tasks\n\n"
    for f in files:
        content += f"- [ ] {f}\n"

    os.makedirs(os.path.dirname(todo_path), exist_ok=True)
    with open(todo_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    print(f"📋 タスクリストを作成しました: {todo_path}")

if __name__ == "__main__":
    main()