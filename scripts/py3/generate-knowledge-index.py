#!/usr/bin/env python3
# scripts/generate-global-index.py
# PKMの対象ディレクトリ（00, 02, 03, 04, 05, 06）を第2階層まで自動分割してインデックス化する。
# 02-knowledge/ に全体の親インデックス (global-index.json / global-index-report.md) を配置。
#
# 使い方:
#   python3 scripts/generate-global-index.py               # 全体を一括作成・更新
#   python3 scripts/generate-global-index.py 02-knowledge/subsidies # 指定階層のみピンポイント更新

# 02-knowledge/
# ├── global-index.json         <-- PKM全体の親目次（各第2階層 index.json へのポインタ）
# ├── global-index-report.md    <-- AIエージェントが最初に参照する全インデックスツリー
# ├── index.json                <-- 02-knowledge 直下のドキュメント用インデックス
# │
# ├── subsidies/
# │   └── index.json            <-- 02-knowledge/subsidies 用インデックス
# │
# ├── (その他の第2階層)/
# │   └── index.json            <-- 各サブディレクトリ用インデックス

import os
import re
import sys
import json
import glob
from pathlib import Path

PKM_ROOT = Path.cwd()

# インデックス対象の第1階層（01-private, 99-trash, tmp は除外）
TARGET_TOP_DIRS = [
    "00-rules",
    "02-knowledge",
    "03-output",
    "04-resources",
    "05-todo",
    "06-storage"
]

# 除外対象（リポジトリクローン等は専用graphスクリプトがあるため除外）
EXCLUDE_PATTERNS = [
    "04-resources/git-repository",
    "node_modules",
    ".git",
    "__pycache__"
]

GLOBAL_INDEX_FILE = PKM_ROOT / "02-knowledge" / "global-index.json"
GLOBAL_REPORT_FILE = PKM_ROOT / "02-knowledge" / "global-index-report.md"

def is_excluded(rel_path_str):
    for pattern in EXCLUDE_PATTERNS:
        if rel_path_str.startswith(pattern):
            return True
    return False

def parse_md_meta(filepath):
    """Frontmatter と H1 タイトルを抽出"""
    meta = {"tags": [], "title": None}
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        fm_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
        if fm_match:
            tag_match = re.search(r'tags:\s*\[(.*?)\]', fm_match.group(1))
            if tag_match:
                meta["tags"] = [t.strip().strip("'\"") for t in tag_match.group(1).split(',')]

        title_match = re.search(r'^#\s+(.+)', content, re.MULTILINE)
        if title_match:
            meta["title"] = title_match.group(1).strip()
    except Exception:
        pass
    return meta

def scan_target_domains():
    """対象となる第1階層および第2階層のパス一覧を動的に収集"""
    domains = {}
    
    for top_dir_name in TARGET_TOP_DIRS:
        top_dir = PKM_ROOT / top_dir_name
        if not top_dir.exists():
            continue
            
        rel_top = top_dir_name
        if not is_excluded(rel_top):
            domains[rel_top] = top_dir
            
        # 第2階層のサブディレクトリを検索
        for entry in top_dir.iterdir():
            if entry.is_dir():
                rel_sub = f"{top_dir_name}/{entry.name}"
                if not is_excluded(rel_sub):
                    domains[rel_sub] = entry
                    
    return domains

def build_single_domain_index(domain_rel_path, domain_dir):
    """単一ディレクトリ（第1または第2階層）内のインデックスを生成"""
    md_files = glob.glob(str(domain_dir / "*.md"))  # 直下の Markdown のみ対象（ネストは第2階層側で消化）
    nodes = []

    for filepath in md_files:
        path_obj = Path(filepath)
        if "index" in path_obj.name.lower():
            continue

        rel_path = str(path_obj.relative_to(PKM_ROOT))
        meta = parse_md_meta(filepath)

        nodes.append({
            "id": path_obj.stem,
            "title": meta["title"] or path_obj.stem,
            "path": rel_path,
            "tags": meta["tags"]
        })

    domain_data = {
        "domain": domain_rel_path,
        "total_count": len(nodes),
        "nodes": nodes
    }

    # 各階層の直下に index.json を保存
    index_json_path = domain_dir / "index.json"
    with open(index_json_path, 'w', encoding='utf-8') as f:
        json.dump(domain_data, f, indent=2, ensure_ascii=False)

    return domain_data

def generate_global_indexes(target_filter=None):
    all_domains = scan_target_domains()
    
    global_manifest = {"domains": {}}
    if GLOBAL_INDEX_FILE.exists():
        try:
            with open(GLOBAL_INDEX_FILE, 'r', encoding='utf-8') as f:
                global_manifest = json.load(f)
        except Exception:
            pass

    print("🔍 [Global Index] インデックス生成・更新を開始します...")

    for domain_rel_path, domain_dir in all_domains.items():
        # 特定引数指定時はその階層のみ更新
        if target_filter and target_filter.rstrip('/') != domain_rel_path.rstrip('/'):
            continue

        res = build_single_domain_index(domain_rel_path, domain_dir)
        index_json_rel = f"{domain_rel_path}/index.json"
        
        global_manifest["domains"][domain_rel_path] = {
            "total_count": res["total_count"],
            "index_json": index_json_rel
        }
        print(f"  ✅ [{domain_rel_path}] -> `{index_json_rel}` ({res['total_count']} 件)")

    # 02-knowledge/ に全親インデックスを書き出し
    GLOBAL_INDEX_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(GLOBAL_INDEX_FILE, 'w', encoding='utf-8') as f:
        json.dump(global_manifest, f, indent=2, ensure_ascii=False)

    # 02-knowledge/global-index-report.md の作成
    with open(GLOBAL_REPORT_FILE, 'w', encoding='utf-8') as f:
        f.write("# PKM 全体構造・第2階層インデックスマップ\n\n")
        f.write("AIエージェントは `ls` コマンドを使用せず、本レポートおよび各階層の `index.json` を直接参照して目的のファイルパスを特定すること。\n\n")
        
        for d_path, info in global_manifest["domains"].items():
            f.write(f"### 📁 `{d_path}/` (件数: **{info['total_count']}**)\n")
            f.write(f"- 階層インデックス: `{info['index_json']}`\n\n")

    print(f"\n🎉 全親インデックス更新完了: `{GLOBAL_INDEX_FILE.relative_to(PKM_ROOT)}`")
    print(f"🎉 全レポート更新完了: `{GLOBAL_REPORT_FILE.relative_to(PKM_ROOT)}`")

if __name__ == "__main__":
    target_arg = sys.argv[1] if len(sys.argv) > 1 else None
    generate_global_indexes(target_arg)
