---
title: "scripts/server/knowledge_service.py Note"
date: 2026-10-06
tags: [server, knowledge_service]
category: scripts-server
description: "ナレッジベース操作サービスの詳細解析"
---

# Note: scripts/server/knowledge_service.py

## 1. 目的と役割
本ファイル `knowledge_service.py` は `ナレッジベース操作サービス` として動作し、システム全体の中で重要な役割を果たします。

## 2. 主要な構成要素・処理フロー
- ファイル種別: `py`
- 責務: ナレッジベース操作サービス

## 3. コード内容 / 構成
```
import os
import re
import json
import sqlite3
from pathlib import Path
import streamlit as st
from config import PROJECT_ROOT, RULES_DIR, KNOWLEDGE_DIR, DB_PATH
from llm_client import call_llm

PROMPTS_DIR = os.path.join(RULES_DIR, "prompts")

def resolve_prompt_path(prompt_input: str) -> str:
    """
    指示書指定（ファイル名, パス, ディレクトリ名）を適切な絶対パスへ解決する
    - "code-analysis.md" -> 00-rules/prompts/code-analysis.md
    - "sublimation-agent" -> .agents/skills/sublimation-agent/SKILL.md や 00-rules/skills/
    - "/path/to/my-prompt.md" -> そのまま
    """
    path_obj = Path(prompt_input)
    if path_obj.is_file():
        return str(path_obj)

    # 1. 00-rules/prompts/ 配下の検索
    rules_path = Path(PROMPTS_DIR) / prompt_input
    if rules_path.is_file():
        return str(rules_path)
    if not prompt_input.endswith(".md"):
        rules_path_md = Path(PROMPTS_DIR) / f"{prompt_input}.md"
        if rules_path_md.is_file():
            return str(rules_path_md)

    # 2. .agents/skills/<dir>/SKILL.md や 00-rules/skills/<dir>/SKILL.md の検索
    skill_candidate1 = Path(PROJECT_ROOT) / ".agents" / "skills" / prompt_input / "SKILL.md"
    if skill_candidate1.is_file():
        return str(skill_candidate1)

    skill_candidate2 = Path(RULES_DIR) / "skills" / prompt_input / "SKILL.md"
    if skill_candidate2.is_file():
        return str(skill_candidate2)

    return prompt_input

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
            if category_filter and category_filter not in ["すべて", "auto", "🤖 AIに自動推察させる"]:
                cursor.execute("SELECT title, rel_path, summary FROM knowledge_index WHERE category = ?", (category_filter,))
            else:
                cursor.execute("SELECT title, rel_path, summary FROM knowledge_index")
            for t, rp, s in cursor.fetchall():
                existing_notes_summary.append(f
```

## 4. 依存関係と連携
- `scripts/server/` 内の他のモジュールとの連携。
