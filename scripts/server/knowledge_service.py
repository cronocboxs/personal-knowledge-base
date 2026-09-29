import os
import re
import json
import sqlite3
import streamlit as st
from config import PROJECT_ROOT, RULES_DIR, DB_PATH
from llm_client import call_llm

TEMPLATE_PATH = os.path.join(RULES_DIR, "prompts", "sublimation-prompt.md")

def load_rule_docs() -> str:
    rule_texts = []
    target_rules = [
        os.path.join(PROJECT_ROOT, "AGENTS.md"),
        os.path.join(RULES_DIR, "formatting.md"),
        os.path.join(RULES_DIR, "workflow.md"),
        os.path.join(RULES_DIR, "agent-behavior.md")
    ]
    for rule_path in target_rules:
        if os.path.exists(rule_path):
            try:
                rel_path = os.path.relpath(rule_path, PROJECT_ROOT)
                with open(rule_path, "r", encoding="utf-8") as f:
                    rule_texts.append(f"--- 【規約ファイル: {rel_path}】 ---\n" + f.read())
            except Exception:
                pass
    return "\n\n".join(rule_texts)

def get_existing_notes_context(category_filter: str = None) -> str:
    existing_notes_summary = []
    if os.path.exists(DB_PATH):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            if category_filter and category_filter != "すべて":
                cursor.execute("SELECT title, rel_path, summary FROM knowledge_index WHERE category = ?", (category_filter,))
            else:
                cursor.execute("SELECT title, rel_path, summary FROM knowledge_index")
            for t, rp, s in cursor.fetchall():
                existing_notes_summary.append(f"- タイトル: {t} (パス: {rp}) / 概要: {s}")
            conn.close()
        except Exception:
            pass
    return "\n".join(existing_notes_summary) if existing_notes_summary else "（既存ノートなし）"

def generate_knowledge_files(title: str, content: str, today: str, category: str = "default") -> dict:
    """指示書テンプレート(sublimation-prompt.md)を読み込んでAI解析・ナレッジ昇華を実行"""
    rules_context = load_rule_docs()
    notes_context = get_existing_notes_context(category)
    
    # 指示書テンプレートの読み込み
    if os.path.exists(TEMPLATE_PATH):
        with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
            prompt_template = f.read()
    else:
        st.error(f"指示書テンプレートが見つかりません: {TEMPLATE_PATH}")
        prompt_template = "入力データを解析してナレッジ化してください。\n{content}"

    # テンプレート変数埋め込み
    prompt = prompt_template.format(
        rules_context=rules_context,
        notes_context=notes_context,
        today=today,
        category=category,
        title=title,
        content=content
    )

    try:
        raw_text = call_llm(prompt)
        json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(0))
            if "head_content" in data and "note_content" in data:
                return data
    except Exception as e:
        st.warning(f"AIによる解析昇華処理でエラーが発生したため、標準フォーマットで作成します: {e}")
        
    short_summary = content[:100].replace('\n', ' ')
    default_fm = f"""---
created: {today}
updated: {today}
tags: ["uncategorized"]
status: draft
phase: 1
parent: []
children: []
related: []
task: []
summary: "{short_summary}"
---"""
    return {
        "head_content": default_fm,
        "note_content": f"{default_fm}\n\n# {title}\n\n{content}"
    }