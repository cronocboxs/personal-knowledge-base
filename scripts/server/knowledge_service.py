import os
import re
import json
import sqlite3
import streamlit as st
from config import PROJECT_ROOT, RULES_DIR, DB_PATH
from llm_client import call_llm

PROMPTS_DIR = os.path.join(RULES_DIR, "prompts")

def get_available_prompts() -> list[str]:
    """00-rules/prompts/ 内の .md ファイル一覧を取得"""
    if not os.path.exists(PROMPTS_DIR):
        os.makedirs(PROMPTS_DIR, exist_ok=True)
    files = [f for f in os.listdir(PROMPTS_DIR) if f.endswith(".md")]
    return sorted(files) if files else ["sublimation-prompt.md"]

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

def generate_knowledge_files(
    title: str,
    content: str,
    today: str,
    category: str = "default",
    prompt_filename: str = "code-analysis.md",
    llm_provider: str = "Ollama (Local LLM)",
    gemini_model: str = "gemini-3.5-flash-lite",
    api_key: str = "",
    ollama_model: str = "gemma4:e2b",
    ollama_url: str = "http://localhost:11434"
) -> dict:
    """指定された指示書テンプレートを読み込んでAI解析・昇華を実行"""
    rules_context = load_rule_docs()
    notes_context = get_existing_notes_context(category)
    
    template_path = os.path.join(PROMPTS_DIR, prompt_filename)
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            prompt_template = f.read()
    else:
        st.warning(f"指示書 {prompt_filename} が見つかりません。標準テンプレートを使用します。")
        prompt_template = "入力データを解析して構造化ナレッジを作成してください。\n{content}"

    prompt = prompt_template.format(
        rules_context=rules_context,
        notes_context=notes_context,
        today=today,
        category=category,
        title=title,
        content=content
    )

    try:
        raw_text = call_llm(
            prompt=prompt,
            llm_provider=llm_provider,
            gemini_model=gemini_model,
            api_key=api_key,
            ollama_model=ollama_model,
            ollama_url=ollama_url
        )
        json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)

            try:
                data = json.loads(json_str, strict=False)
            except json.JSONDecodeError:
                # \uXXXX などの不正エスケープ補正処理
                cleaned_json = re.sub(r'\\(?![/"bfnrtu])', r'\\\\', json_str)
                data = json.loads(cleaned_json, strict=False)

            if "head_content" in data and "note_content" in data:
                return data
    except Exception as e:
        st.warning(f"昇華処理でエラーが発生したため標準フォーマットで作成します: {e}")
        
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

def auto_sublimate_rag_answer(
    user_query: str,
    answer_text: str,
    custom_title: str,
    selected_cat: str,
    today: str,
    llm_provider: str = "Ollama (Local LLM)",
    gemini_model: str = "gemini-3.5-flash-lite",
    api_key: str = "",
    ollama_model: str = "gemma4:e2b",
    ollama_url: str = "http://localhost:11434"
) -> dict:
    notes_context = get_existing_notes_context()
    rules_context = load_rule_docs()
    title_val = custom_title if custom_title else "未指定"

    prompt = f"""あなたはパーソナルナレッジベースのナレッジ昇華エージェントです。
以下の【関連規約ドキュメント】を遵守し、ユーザーの質問とAIの回答からナレッジ（head/note）を生成してください。

【関連規約ドキュメント】
{rules_context}

---

【既存ナレッジ一覧 (リレーション参照用)】
{notes_context}

---

【本日日付】: {today}
【指定タイトル】: {title_val}
【指定カテゴリ】: {selected_cat}
【ユーザーの質問】: {user_query}
【AIの回答内容】:
{answer_text}

【指示】:
1. `custom_title` が空欄の場合、回答内容から適切な kebab-case.md のタイトルを生成してください。
2. `selected_cat` が "🤖 AIに自動推察させる" または空欄の場合、最適カテゴリを推察してください。
3. リレーション(parent/children/related)を設定してください。
4. formatting.md に完全準拠した JSON フォーマットのみで出力してください。

{{
  "inferred_title": "推察されたタイトル",
  "inferred_category": "推察されたカテゴリ名",
  "head_content": "--- YAML Frontmatter ---",
  "note_content": "--- YAML Frontmatter ---\n\n# タイトル\n\n本文"
}}
"""
    try:
        raw_text = call_llm(
            prompt=prompt,
            llm_provider=llm_provider,
            gemini_model=gemini_model,
            api_key=api_key,
            ollama_model=ollama_model,
            ollama_url=ollama_url
        )
        json_match = re.search(r'\{.*\}', raw_text, re.DOTALL)
        if json_match:
            data = json.loads(json_match.group(0))
            return data
    except Exception as e:
        st.error(f"ナレッジ昇華処理でエラーが発生しました: {e}")
        
    clean_title = custom_title if custom_title else f"rag-answer-{today}"
    cat_name = "default" if selected_cat == "🤖 AIに自動推察させる" else selected_cat
    short_summary = answer_text[:100].replace('\n', ' ')
    default_fm = f"""---
created: {today}
updated: {today}
tags: ["rag-generated"]
status: draft
phase: 1
parent: []
children: []
related: []
task: []
summary: "{short_summary}"
---"""
    return {
        "inferred_title": clean_title,
        "inferred_category": cat_name,
        "head_content": default_fm,
        "note_content": f"{default_fm}\n\n# {clean_title}\n\n{answer_text}"
    }