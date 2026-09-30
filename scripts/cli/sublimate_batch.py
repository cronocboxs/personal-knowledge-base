import argparse
import os
import sys
import glob
import datetime
import subprocess

# ---------------------------------------------------------
# パス設定: scripts/server/ を Python モジュール検索パスに追加
# ---------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../"))
sys.path.append(os.path.join(PROJECT_ROOT, "scripts/server"))

from config import RESOURCES_DIR, KNOWLEDGE_DIR, get_gemini_api_key, load_config
from knowledge_service import generate_knowledge_files

def get_unsublimated_resources() -> list[str]:
    """04-resources/ 内でまだ 02-knowledge/ に昇華されていないファイルを取得"""
    resource_files = glob.glob(os.path.join(RESOURCES_DIR, "**/*.md"), recursive=True)
    unprocessed = []
    
    for res_path in resource_files:
        rel_path = os.path.relpath(res_path, PROJECT_ROOT)
        base_name = os.path.basename(res_path)
        
        # 02-knowledge 全域で同名ファイルがあるか検索
        knowledge_matches = glob.glob(os.path.join(KNOWLEDGE_DIR, f"**/note/{base_name}"), recursive=True)
        if not knowledge_matches:
            unprocessed.append(rel_path)
            
    return sorted(unprocessed)

def git_commit_knowledge(note_path: str, category: str, title: str):
    """変更ファイルを git add & commit"""
    try:
        rel_note = os.path.relpath(note_path, PROJECT_ROOT)
        rel_head = rel_note.replace("/note/", "/head/")
        db_path = "01-private/knowledge_index.db"
        
        subprocess.run(["git", "add", rel_note, rel_head, db_path], cwd=PROJECT_ROOT, check=True)
        commit_msg = f"feat(knowledge): sublimate {title} into {category}"
        subprocess.run(["git", "commit", "-m", commit_msg], cwd=PROJECT_ROOT, check=True)
        print(f"  ✅ Git committed: {commit_msg}")
    except Exception as e:
        print(f"  ⚠️ Git commit failed: {e}")

def main():
    config = load_config()
    
    # ---------------------------------------------------------
    # CLI 引数の設定 (argparse)
    # ---------------------------------------------------------
    parser = argparse.ArgumentParser(description="自律型ナレッジ昇華 CLI ツール")
    parser.add_argument(
        "-i", "--instruction",
        default="code-analysis.md",
        help="指示書ファイル名、パス、またはスキル名 (例: code-analysis.md, sublimation-agent)"
    )
    parser.add_argument(
        "-p", "--provider",
        default=config.get("default_provider", "Ollama (Local LLM)"),
        help="LLMプロバイダ ('Ollama (Local LLM)' または 'Gemini (Cloud API)')"
    )
    parser.add_argument(
        "-m", "--model",
        default="",
        help="使用モデル名 (空欄の場合は settings.json のデフォルトを使用)"
    )
    parser.add_argument(
        "-c", "--category",
        default="auto",
        help="保存カテゴリ (デフォルト: 'auto' でAI自動判定)"
    )

    args = parser.parse_args()

    # モデル名が未指定の場合、settings.json のデフォルトを設定
    if not args.model:
        if args.provider == "Gemini (Cloud API)":
            args.model = config.get("gemini", {}).get("default_model", "gemini-3.5-flash-lite")
        else:
            args.model = config.get("ollama", {}).get("default_model", "gemma4:e2b")

    api_key = get_gemini_api_key()
    ollama_url = config.get("ollama", {}).get("endpoint", "http://localhost:11434")

    unprocessed = get_unsublimated_resources()
    if not unprocessed:
        print("✨ 未処理の一次素材はありません（すべて昇華完了済み）。")
        return

    print(f"🚀 {len(unprocessed)} 件の未昇華一次素材を検出しました。昇華処理を開始します...")
    print(f"  ・指示書  : {args.instruction}")
    print(f"  ・プロバイダ: {args.provider}")
    print(f"  ・モデル  : {args.model}")
    print(f"  ・カテゴリ: {args.category}\n" + "-" * 50)

    for idx, rel_res_path in enumerate(unprocessed, 1):
        abs_res_path = os.path.join(PROJECT_ROOT, rel_res_path)
        base_filename = os.path.basename(rel_res_path)
        title = base_filename.replace(".md", "")
        today = datetime.date.today().strftime("%Y-%m-%d")

        print(f"[{idx}/{len(unprocessed)}] 昇華中: {rel_res_path}")

        with open(abs_res_path, "r", encoding="utf-8") as f:
            content = f.read()

        # 昇華処理 (Pass 1 メタデータ抽出 & カテゴリ自動判定 + Pass 2 本文解析)
        res = generate_knowledge_files(
            title=title,
            content=content,
            today=today,
            category=args.category,  # 'auto' で AI 自動判別
            prompt_filename=args.instruction,  # ファイル名 / ディレクトリ名 / パス
            sources=[rel_res_path],
            llm_provider=args.provider,
            gemini_model=args.model if args.provider == "Gemini (Cloud API)" else "",
            api_key=api_key,
            ollama_model=args.model if args.provider != "Gemini (Cloud API)" else "",
            ollama_url=ollama_url
        )

        final_cat = res.get("inferred_category", "default")
        print(f"  └ 判別カテゴリ: {final_cat}")

        # ファイル出力先決定
        target_repo_dir = os.path.join(KNOWLEDGE_DIR, final_cat)
        head_dir = os.path.join(target_repo_dir, "head")
        note_dir = os.path.join(target_repo_dir, "note")
        os.makedirs(head_dir, exist_ok=True)
        os.makedirs(note_dir, exist_ok=True)

        head_path = os.path.join(head_dir, base_filename)
        note_path = os.path.join(note_dir, base_filename)

        with open(head_path, "w", encoding="utf-8") as f:
            f.write(res["head_content"].strip() + "\n")

        with open(note_path, "w", encoding="utf-8") as f:
            f.write(res["note_content"].strip() + "\n")

        # ベクトルインデックス更新
        try:
            indexer_script = os.path.join(PROJECT_ROOT, "scripts/index/update-index.py")
            subprocess.run(["python3", indexer_script, "--file", note_path], check=True, capture_output=True)
            print("  🔍 ベクトルインデックス更新完了")
        except Exception as e:
            print(f"  ⚠️ インデックス更新失敗: {e}")

        # Git Commit
        git_commit_knowledge(note_path, final_cat, title)
        print("--------------------------------------------------")

if __name__ == "__main__":
    main()
