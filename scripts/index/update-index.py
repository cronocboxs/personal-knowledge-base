#!/usr/bin/env python3
import os
import re
import json
import sqlite3
import urllib.request
import argparse

# ---------------------------------------------------------
# パス定義: プロジェクトルート基準の絶対パス
# ---------------------------------------------------------
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../"))

KNOWLEDGE_DIR = os.path.join(PROJECT_ROOT, "02-knowledge")
PRIVATE_DIR = os.path.join(PROJECT_ROOT, "01-private")
DB_PATH = os.path.join(PRIVATE_DIR, "knowledge_index.db")

OLLAMA_ENDPOINT = "http://localhost:11434"
EMBED_MODEL = "nomic-embed-text"

# ---------------------------------------------------------
# 1. DBの初期化
# ---------------------------------------------------------
def init_db():
    os.makedirs(PRIVATE_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # ノート情報・埋め込みベクトルのテーブル作成
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS knowledge_index (
        rel_path TEXT PRIMARY KEY,
        category TEXT,
        title TEXT,
        summary TEXT,
        tags TEXT,
        content TEXT,
        embedding TEXT,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()

# ---------------------------------------------------------
# 2. Ollama nomic-embed-text によるベクトル生成
# ---------------------------------------------------------
def get_embedding(text: str) -> list[float]:
    url = f"{OLLAMA_ENDPOINT.rstrip('/')}/api/embeddings"
    payload = json.dumps({
        "model": EMBED_MODEL,
        "prompt": text
    }).encode("utf-8")
    
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as res:
            res_data = json.loads(res.read().decode("utf-8"))
            return res_data.get("embedding", [])
    except Exception as e:
        print(f"⚠️ ベクトル化エラー ({text[:30]}...): {e}")
        return []

# ---------------------------------------------------------
# 3. Frontmatter & 本文の解析
# ---------------------------------------------------------
def parse_markdown(file_path: str):
    with open(file_path, "r", encoding="utf-8") as f:
        text = f.read()
        
    summary = ""
    tags = []
    content = text
    
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            raw_yaml = parts[1]
            content = parts[2].strip()
            
            # 簡易YAML解析 (summary & tags)
            summary_match = re.search(r'summary:\s*"(.*?)"', raw_yaml)
            if summary_match:
                summary = summary_match.group(1)
                
            tags_match = re.search(r'tags:\s*(\[.*?\])', raw_yaml)
            if tags_match:
                try:
                    tags = json.loads(tags_match.group(1))
                except Exception:
                    pass

    return summary, json.dumps(tags, ensure_ascii=False), content

# ---------------------------------------------------------
# 4. 単一ファイルまたは全体インデックスの更新
# ---------------------------------------------------------
def update_index(target_file: str = None):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    files_to_process = []
    
    if target_file:
        abs_target = os.path.abspath(target_file)
        if os.path.exists(abs_target):
            files_to_process.append(abs_target)
    else:
        # 全スキャン (note/ 配下のファイルのみ)
        for root, _, files in os.walk(KNOWLEDGE_DIR):
            for file in files:
                if file.endswith(".md") and "/note/" in os.path.join(root, file):
                    files_to_process.append(os.path.join(root, file))

    print(f"🔄 インデックス更新開始 ({len(files_to_process)} 件)...")
    
    for file_path in files_to_process:
        rel_path = os.path.relpath(file_path, PROJECT_ROOT)
        parts = rel_path.split(os.sep)
        category = parts[1] if len(parts) >= 3 else "default"
        title = os.path.basename(file_path).replace(".md", "")
        
        summary, tags, content = parse_markdown(file_path)
        
        # 検索インデックス生成用の埋め込み対象テキスト (summary + content)
        embed_target_text = f"{title}\n{summary}\n{content[:1000]}"
        embedding = get_embedding(embed_target_text)
        
        cursor.execute("""
        INSERT INTO knowledge_index (rel_path, category, title, summary, tags, content, embedding, updated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ON CONFLICT(rel_path) DO UPDATE SET
            category=excluded.category,
            title=excluded.title,
            summary=excluded.summary,
            tags=excluded.tags,
            content=excluded.content,
            embedding=excluded.embedding,
            updated_at=CURRENT_TIMESTAMP
        """, (rel_path, category, title, summary, tags, content, json.dumps(embedding)))
        
        print(f"  ✅ Indexed: {rel_path}")

    conn.commit()
    conn.close()
    print("✨ インデックス更新完了！")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ナレッジインデックス更新スクリプト")
    parser.add_argument("--file", type=str, help="指定したファイルのみインデックス更新")
    args = parser.parse_args()
    
    update_index(args.file)