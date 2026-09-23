#!/usr/bin/env python3
# scripts/extract-markdown-graph.py
# 指定された Git リポジトリ内の Markdown 内部リンクを抽出し、doc-graph として保存する。

import os
import re
import sys
import json
import glob
from pathlib import Path

PKM_ROOT = Path.cwd()

if len(sys.argv) < 2:
    print("❌ エラー: 対象のリポジトリ名またはパスを指定してください。")
    sys.exit(1)

input_target = sys.argv[1]
branch_name = sys.argv[2] if len(sys.argv) > 2 else "main"

target_dir = Path(input_target)
if target_dir.exists() and target_dir.is_dir():
    target_dir = target_dir.resolve()
    branch_name = target_dir.name
    repo_name = target_dir.parent.parent.name
    if repo_name in [".", "git-repository"]:
        repo_name = target_dir.name
else:
    repo_name = input_target
    target_dir = PKM_ROOT / "04-resources" / "git-repository" / repo_name / "clone" / branch_name

if not target_dir.exists():
    print(f"❌ エラー: 解析対象のディレクトリが存在しません: {target_dir}")
    sys.exit(1)

output_graph_dir = PKM_ROOT / "04-resources" / "git-repository" / repo_name / "graph" / branch_name
output_json_file = output_graph_dir / "doc-graph.json"
output_mermaid_file = output_graph_dir / "doc-graph-report.md"

def parse_markdown_links(content):
    links = []
    md_links = re.findall(r'\[.*?\]\((.*?\.md)\)', content)
    for target in md_links:
        links.append(Path(target).stem)
    wiki_links = re.findall(r'\[\[(.*?)\]\]', content)
    for target in wiki_links:
        target_name = target.split('|')[0].split('#')[0].strip()
        links.append(Path(target_name).stem)
    return list(set(links))

def parse_frontmatter_tags(content):
    tags = []
    fm_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL)
    if fm_match:
        tag_match = re.search(r'tags:\s*\[(.*?)\]', fm_match.group(1))
        if tag_match:
            tags = [t.strip().strip("'\"") for t in tag_match.group(1).split(',')]
    return tags

def generate_graph():
    print(f"🔍 [{repo_name}] ({branch_name}) Markdown 内部リンク解析中...")

    md_files = glob.glob(str(target_dir / "**" / "*.md"), recursive=True)
    nodes = {}
    edges = []
    
    for filepath in md_files:
        path_obj = Path(filepath)
        node_id = path_obj.stem
        try:
            rel_path = str(path_obj.relative_to(target_dir))
        except ValueError:
            rel_path = str(path_obj)
        
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            
        tags = parse_frontmatter_tags(content)
        links = parse_markdown_links(content)
        
        nodes[node_id] = {"id": node_id, "path": rel_path, "tags": tags, "links": links}

    for source_id, data in nodes.items():
        for target_id in data["links"]:
            if target_id in nodes and source_id != target_id:
                edges.append((source_id, target_id))

    output_graph_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. doc-graph-report.md (Mermaid)
    with open(output_mermaid_file, 'w', encoding='utf-8') as f:
        f.write(f"# {repo_name} ({branch_name}) ドキュメント依存関係グラフ\n\n")
        f.write(f"- 解析対象ファイル数: {len(nodes)}\n")
        f.write(f"- 検出リンク数: {len(edges)}\n\n")
        f.write("```mermaid\ngraph TD;\n")
        f.write("    classDef default fill:#1f2937,stroke:#4b5563,color:#fff;\n")
        for n_id in nodes.keys():
            f.write(f'    {n_id}["{n_id}"]\n')
        for src, tgt in edges:
            f.write(f'    {src} --> {tgt}\n')
        f.write("```\n")

    # 2. doc-graph.json
    json_data = {
        "nodes": [{"id": k, "type": "doc", "path": v["path"], "tags": v["tags"]} for k, v in nodes.items()],
        "edges": [{"source": src, "target": tgt, "relation": "references"} for src, tgt in edges]
    }
    with open(output_json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=2, ensure_ascii=False)

    print(f"✅ ドキュメント解析完了: {output_json_file}")

if __name__ == "__main__":
    generate_graph()