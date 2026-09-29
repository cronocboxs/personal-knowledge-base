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

def clean_and_parse_json(json_str: str) -> dict:
    """LLMが生成したJSON文字列のエスケープ補正パース"""
    try:
        return json.loads(json_str, strict=False)
    except json.JSONDecodeError:
        pass
    cleaned_str = re.sub(r'\\(?!["\\/bfnrt]|u[0-9a-fA-F]{4})', r'\\\\', json_str)
    try:
        return json.loads(cleaned_str, strict=False)
    except json.JSONDecodeError:
        fixed_u = re.sub(r'\\u(?![0-9a-fA-F]{4})', r'\\\\u', cleaned_str)
        return json.loads(fixed_u, strict=False)

def generate_knowledge_files(
    title: str,
    content: str,
    today: str,
    category: str = "default",
    prompt_filename: str = "code-analysis.md",
    sources: list[str] = None,
    llm_provider: str = "Ollama (Local LLM)",
    gemini_model: str = "gemini-3.5-flash-lite",
    api_key: str = "",
    ollama_model: str = "gemma4:e2b",
    ollama_url: str = "http://localhost:11434"
) -> dict:
    if sources is None:
        sources = []

    """
    formatting.md の規約に基づき、処理を2段階（メタデータ抽出 / 本文解析生成）に分けて実行
    """
    rules_context = load_rule_docs()
    notes_context = get_existing_notes_context(category)
    
    # トークン溢れ対策（ローカルモデル用）
    max_len = 6000 if llm_provider == "Ollama (Local LLM)" else 20000
    truncated_content = content[:max_len]

    # ---------------------------------------------------------
    # PASS 1: メタデータ(YAML Frontmatter用項目) の抽出 (JSON出力)
    # ---------------------------------------------------------
    meta_prompt = f"""あなたは規約ドキュメントに厳格に従うAIエージェントです。
以下の【参照規約ドキュメント】にある「2. メタデータ (YAML Frontmatter)」の定義に厳格に従い、処理対象データからメタデータ属性（tags, summary, parent, children, related）を抽出してください。

【参照規約ドキュメント】
{rules_context}

---

【既存ナレッジ一覧 (リレーション参照用)】
{notes_context}

---

【処理対象データ】
- 本日日付: {today}
- カテゴリ: {category}
- タイトル: {title}
- 本文抜粋:
{truncated_content[:2000]}
【指示】:
formatting.md で定義されている Frontmatter 属性項目(tags, summary, parent, children, related)のみを含むJSONオブジェクトを出力してください。余計な解説文や思考プロセスは除外してください。
"""
    summary_val = f"{title}の解析ノート"
    tags_val = ["uncategorized"]
    parent_val, children_val, related_val = [], [], []

    try:
        raw_meta = call_llm(
            prompt=meta_prompt,
            llm_provider=llm_provider,
            gemini_model=gemini_model,
            api_key=api_key,
            ollama_model=ollama_model,
            ollama_url=ollama_url
        )
        json_match = re.search(r'\{.*\}', raw_meta, re.DOTALL)
        if json_match:
            data = clean_and_parse_json(json_match.group(0))
            summary_val = data.get("summary", summary_val)
            tags_val = data.get("tags", tags_val)
            parent_val = data.get("parent", parent_val)
            children_val = data.get("children", children_val)
            related_val = data.get("related", related_val)
    except Exception:
        pass

    # formatting.md に完全準拠した Frontmatter テキストを構築
    frontmatter_text = f"""---
created: {today}
updated: {today}
source: {json.dumps(sources, ensure_ascii=False)}
tags: {json.dumps(tags_val, ensure_ascii=False)}
status: draft
phase: 1
parent: {json.dumps(parent_val, ensure_ascii=False)}
children: {json.dumps(children_val, ensure_ascii=False)}
related: {json.dumps(related_val, ensure_ascii=False)}
task: []
summary: "{summary_val.replace('"', "'")}"
---"""

    # ---------------------------------------------------------
    # PASS 2: 選択された指示書テンプレートに基づく本文解析の生成 (Raw Markdown)
    # ---------------------------------------------------------
    template_path = os.path.join(PROMPTS_DIR, prompt_filename)
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            instruction_template = f.read()
    else:
        instruction_template = "入力されたコード/テキストを解析し、構造化された技術解説Markdownを出力してください。\n{content}"

    analysis_prompt = f"""【参照規約ドキュメント】
{rules_context}

---

【指示書テンプレート ({prompt_filename})】
{instruction_template.format(
    rules_context=rules_context,
    notes_context=notes_context,
    today=today,
    category=category,
    title=title,
    content=truncated_content
)}

---

【追加実行指示】:
JSON形式ではなく、Markdown文書本文（`# {title}` や見出しを含む本文）のみを直接出力してください。コードブロック記法(```markdown)による全体囲みは不要です。
"""

    try:
        raw_body = call_llm(
            prompt=analysis_prompt,
            llm_provider=llm_provider,
            gemini_model=gemini_model,
            api_key=api_key,
            ollama_model=ollama_model,
            ollama_url=ollama_url
        )
        
        # 不要な```markdown 囲みの除去
        body_text = raw_body.strip()
        if body_text.startswith("```markdown"):
            body_text = body_text.split("```markdown")[1].split("```")[0].strip()
        elif body_text.startswith("```"):
            body_text = body_text.split("```")[1].split("```")[0].strip()

        # Frontmatter と解析本文を結合して note_content を生成
        full_note_content = f"{frontmatter_text}\n\n{body_text}"

        return {
            "head_content": frontmatter_text,
            "note_content": full_note_content
        }

    except Exception as e:
        st.warning(f"解析本文の生成中にエラーが発生したため、標準フォーマットで保存します: {e}")
        return {
            "head_content": frontmatter_text,
            "note_content": f"{frontmatter_text}\n\n# {title}\n\n{content}"
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

    # Pass 1: タイトル・カテゴリ推察 & メタデータ抽出
    prompt_meta = f"""あなたは規約ドキュメントに準拠するエージェントです。
以下の質問と回答から、タイトル(kebab-case)、最適カテゴリ名、概要(summary)、リレーション(parent, children, related)をJSONで抽出してください。

【参照規約】
{rules_context}

【質問】: {user_query}
【回答】: {answer_text[:1000]}

【出力JSON】:
{{
  "inferred_title": "{title_val}",
  "inferred_category": "{selected_cat}",
  "summary": "...",
  "parent": [],
  "children": [],
  "related": []
}}
"""
    clean_title = custom_title if custom_title else f"rag-answer-{today}"
    cat_name = "default" if selected_cat == "🤖 AIに自動推察させる" else selected_cat
    summary_val = answer_text[:100].replace('\n', ' ')
    parent_val, children_val, related_val = [], [], []

    try:
        raw_meta = call_llm(
            prompt=prompt_meta,
            llm_provider=llm_provider,
            gemini_model=gemini_model,
            api_key=api_key,
            ollama_model=ollama_model,
            ollama_url=ollama_url
        )
        json_match = re.search(r'\{.*\}', raw_meta, re.DOTALL)
        if json_match:
            data = clean_and_parse_json(json_match.group(0))
            if data.get("inferred_title") and data.get("inferred_title") != "未指定":
                clean_title = data["inferred_title"]
            if data.get("inferred_category") and selected_cat == "🤖 AIに自動推察させる":
                cat_name = data["inferred_category"]
            summary_val = data.get("summary", summary_val)
            parent_val = data.get("parent", parent_val)
            children_val = data.get("children", children_val)
            related_val = data.get("related", related_val)
    except Exception:
        pass

    frontmatter_text = f"""---
created: {today}
updated: {today}
tags: ["rag-generated"]
status: draft
phase: 1
parent: {json.dumps(parent_val, ensure_ascii=False)}
children: {json.dumps(children_val, ensure_ascii=False)}
related: {json.dumps(related_val, ensure_ascii=False)}
task: []
summary: "{summary_val.replace('"', "'")}"
---"""

    return {
        "inferred_title": clean_title,
        "inferred_category": cat_name,
        "head_content": frontmatter_text,
        "note_content": f"{frontmatter_text}\n\n# {clean_title}\n\n{answer_text}"
    }