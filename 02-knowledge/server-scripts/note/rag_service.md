---
created: 2026-10-06
updated: 2026-10-06
source: ["scripts/server/rag_service.py"]
tags: ["uncategorized"]
status: draft
phase: 1
parent: []
children: []
related: []
task: []
summary: "rag_serviceの解析ノート"
---

# rag_service

import os
import sqlite3
import math
import json
import urllib.request
from config import DB_PATH, OLLAMA_ENDPOINT, EMBED_MODEL

# ---------------------------------------------------------
# RAG ヘルパー関数: ベクトル計算 & SQLite 類似度検索
# ---------------------------------------------------------
def get_query_embedding(text: str) -> list[float]:
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
        st.error(f"⚠️ 質問文のベクトル変換エラー (Ollamaが稼働しているか確認してください): {e}")
        return []

def cosine_similarity(v1: list[float], v2: list[float]) -> float:
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    dot_product = sum(a * b for a, b in zip(v1, v2))
    norm_v1 = math.sqrt(sum(a * a for a in v1))
    norm_v2 = math.sqrt(sum(b * b for b in v2))
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
    return dot_product / (norm_v1 * norm_v2)

def search_relevant_knowledge(query: str, top_k: int = 3, target_categories: list[str] = None) -> list[dict]:
    if not os.path.exists(DB_PATH):
        return []

    query_vec = get_query_embedding(query)
    if not query_vec:
        return []

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if target_categories and "すべて" not in target_categories:
        placeholders = ','.join(['?'] * len(target_categories))
        sql = f"SELECT rel_path, category, title, summary, content, embedding FROM knowledge_index WHERE category IN ({placeholders})"
        cursor.execute(sql, target_categories)
    else:
        cursor.execute("SELECT rel_path, category, title, summary, content, embedding FROM knowledge_index")
        
    rows = cursor.fetchall()
    conn.close()

    results = []
    for rel_path, category, title, summary, content, emb_str in rows:
        if not emb_str:
            continue
        try:
            doc_vec = json.loads(emb_str)
            score = cosine_similarity(query_vec, doc_vec)
            results.append({
                "rel_path": rel_path,
                "category": category,
                "title": title,
                "summary": summary,
                "content": content,
                "score": score
            })
        except Exception:
            pass

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]
