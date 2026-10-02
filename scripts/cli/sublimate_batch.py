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

def is_text_file(filepath: str) -> bool:
    """バイナリファイルを除外してテキストファイルかどうかを判定"""
    try:
        with open(filepath, "tr", encoding="utf-8") as f:
            f.read(1024)
            return True
    except (UnicodeDecodeError, Exception):
        return False

def get_target_resources(target_input: str, force: bool = False) -> list[str]:
    """
    指定されたターゲット（ファイルまたはディレクトリ）から処理対象のファイル一覧を取得
    force=False の場合は未昇華チェックを行い、force=True の場合は全件を再昇華対象とする
    """
    abs_target = os.path.abspath(target_input)
    if not os.path.exists(abs_target):
        # 相対パスでの補完（PROJECT_ROOT 基準）
        abs_target = os.path.join(PROJECT_ROOT, target_input)
        if not os.path.exists(abs_target):
            print(f"⚠️ 指定されたパスが見つかりません: {target_input}")
            return []

    candidate_files = []
    if os.path.isfile(abs_target):
        candidate_files.append(abs_target)
    elif os.path.isdir(abs_target):
        for root, _, files in os.walk(abs_target):
            for file in files:
                # 隠しファイルやGit管理外キャッシュ・DBを除外
                if not file.startswith(".") and not file.endswith((".pyc", ".db")):
                    candidate_files.append(os.path.join(root, file))

    unprocessed = []
    for file_path in candidate_files:
        if not is_text_file(file_path):
            continue

        rel_path = os.path.relpath(file_path, PROJECT_ROOT)
        base_name = os.path.basename(file_path)
        
        # 強制再処理(--force)が指定されている場合は重複判定をスキップ
        if force:
            unprocessed.append(rel_path)
            continue

        # 保存時のMarkdownファイル名を想定 (例: script.py -> script.py.md)
        kb_base_name = base_name if base_name.endswith(".md") else f"{base_name}.md"
        
        # 02-knowledge 全域で同名ノートがあるか検索（未昇華判定）
        knowledge_matches = glob.glob(os.path.join(KNOWLEDGE_DIR, f"**/note/{kb_base_name}"), recursive=True)
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
    # CLI 引数の設定 (argparse & 日本語ヘルプ)
    # ---------------------------------------------------------
    parser = argparse.ArgumentParser(
        description="🧠 自律型ナレッジ昇華 CLI ツール\n一次素材（コード/テキスト/ログ等）を解析し、02-knowledge/ に二層（head/note）で昇華保存・Gitコミットまで自動実行します。",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""実行例:
  # 1. 04-resources/ 全体を対象に自動昇華（デフォルト）
  python3 scripts/cli/sublimate_batch.py

  # 2. 既存ノートが存在していても強制的に再解析・上書き更新 (--force)
  python3 scripts/cli/sublimate_batch.py -t scripts/server/ -f

  # 3. 単一のファイルを Gemini で再昇華
  python3 scripts/cli/sublimate_batch.py -t scripts/server/start-webui.py -p "Gemini (Cloud API)" -f
"""
    )
    
    parser.add_argument(
        "-t", "--target",
        default=RESOURCES_DIR,
        metavar="PATH",
        help="解析対象のファイルパスまたはディレクトリパス (デフォルト: 04-resources/)"
    )
    parser.add_argument(
        "-f", "--force",
        action="store_true",
        help="昇華済みノートが存在する場合でも強制的に再昇華（上書き）します"
    )
    parser.add_argument(
        "-i", "--instruction",
        default="code-analysis.md",
        metavar="NAME_OR_PATH",
        help="使用する指示書ファイル名、フルパス、またはスキル名 (例: code-analysis.md, sublimation-agent / デフォルト: code-analysis.md)"
    )
    parser.add_argument(
        "-p", "--provider",
        default=config.get("default_provider", "Ollama (Local LLM)"),
        metavar="PROVIDER",
        help="使用するLLMプロバイダ ('Ollama (Local LLM)' または 'Gemini (Cloud API)' / デフォルト: settings.json の設定)"
    )
    parser.add_argument(
        "-m", "--model",
        default="",
        metavar="MODEL_NAME",
        help="使用するLLMモデル名 (空欄の場合は settings.json のデフォルトモデルを使用)"
    )
    parser.add_argument(
        "-c", "--category",
        default="auto",
        metavar="CATEGORY",
        help="保存先カテゴリ名 ('auto' の場合はAIが自動判別 / デフォルト: auto)"
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

    unprocessed = get_target_resources(args.target, force=args.force)
    if not unprocessed:
        print(f"✨ 指定対象 [{args.target}] 内に未処理の一次素材はありません。")
        return

    print(f"🚀 {len(unprocessed)} 件の一次素材を検出しました。昇華処理を開始します...")
    print(f"  ・対象パス  : {args.target}")
    print(f"  ・強制再昇華: {'有効 (-f)' if args.force else '無効'}")
    print(f"  ・指示書    : {args.instruction}")
    print(f"  ・プロバイダ: {args.provider}")
    print(f"  ・モデル    : {args.model}")
    print(f"  ・カテゴリ  : {args.category}\n" + "-" * 50)

    for idx, rel_res_path in enumerate(unprocessed, 1):
        abs_res_path = os.path.join(PROJECT_ROOT, rel_res_path)
        orig_filename = os.path.basename(rel_res_path)
        
        # 02-knowledge 用の出力Markdownファイル名決定
        kb_filename = orig_filename if orig_filename.endswith(".md") else f"{orig_filename}.md"
        title = orig_filename.replace(".", "-") if not orig_filename.endswith(".md") else orig_filename[:-3]
        today = datetime.date.today().strftime("%Y-%m-%d")

        print(f"[{idx}/{len(unprocessed)}] 昇華中: {rel_res_path}")

        try:
            with open(abs_res_path, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            print(f"  ⚠️ ファイル読み込みエラーのためスキップ: {e}")
            continue

        # 昇華処理 (Pass 1 メタデータ抽出 & カテゴリ自動判定 + Pass 2 本文解析)
        res = generate_knowledge_files(
            title=title,
            content=content,
            today=today,
            category=args.category,
            prompt_filename=args.instruction,
            sources=[rel_res_path],
            llm_provider=args.provider,
            gemini_model=args.model if args.provider == "Gemini (Cloud API)" else "",
            api_key=api_key,
            ollama_model=args.model if args.provider != "Gemini (Cloud API)" else "",
            ollama_url=ollama_url
        )

        final_cat = res.get("inferred_category", "default")
        print(f"  └ 判別カテゴリ: {final_cat}")

        # 出力先パスの設定
        target_repo_dir = os.path.join(KNOWLEDGE_DIR, final_cat)
        head_dir = os.path.join(target_repo_dir, "head")
        note_dir = os.path.join(target_repo_dir, "note")
        os.makedirs(head_dir, exist_ok=True)
        os.makedirs(note_dir, exist_ok=True)

        head_path = os.path.join(head_dir, kb_filename)
        note_path = os.path.join(note_dir, kb_filename)

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