---
title: "scripts/server/start-webui.py Note"
date: 2026-10-06
tags: [server, start-webui]
category: scripts-server
description: "WebUI起動エントリポイントの詳細解析"
---

# Note: scripts/server/start-webui.py

## 1. 目的と役割
本ファイル `start-webui.py` は `WebUI起動エントリポイント` として動作し、システム全体の中で重要な役割を果たします。

## 2. 主要な構成要素・処理フロー
- ファイル種別: `py`
- 責務: WebUI起動エントリポイント

## 3. コード内容 / 構成
```
import os
import re
import datetime
import subprocess
import streamlit as st
from config import PROJECT_ROOT, KNOWLEDGE_DIR, RESOURCES_DIR, load_config, get_gemini_api_key
from rag_service import search_relevant_knowledge
from knowledge_service import generate_knowledge_files, auto_sublimate_rag_answer, get_available_prompts
from llm_client import call_llm

# python3 -m streamlit run scripts/server/start-webui.py

config = load_config()

# ---------------------------------------------------------
# ヘルパー関数: ツリー構築・ファイル取得
# ---------------------------------------------------------
def get_knowledge_categories() -> list[str]:
    categories = []
    if os.path.exists(KNOWLEDGE_DIR):
        for entry in os.listdir(KNOWLEDGE_DIR):
            full_path = os.path.join(KNOWLEDGE_DIR, entry)
            if os.path.isdir(full_path) and entry not in ["head", "note"]:
                categories.append(entry)
    if "default" not in categories:
        categories.insert(0, "default")
    return sorted(categories)

# ---------------------------------------------------------
# ヘルパー関数: Ollama モデル一覧取得
# ---------------------------------------------------------
def get_ollama_models() -> list[str]:
    default_ollama = config.get("ollama", {}).get("default_model", "qwen2.5:1.5b")
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True, check=True)
        lines = result.stdout.strip().split("\n")
        models = []
        if len(lines) > 1:
            for line in lines[1:]:
                parts = re.split(r'\s+', line.strip())
                if parts and parts[0]:
                    model_name = parts[0]
                    if "embed" not in model_name:
                        models.append(model_name)
        return models if models else [default_ollama]
    except Exception:
        return [default_ollama]


# 画面基本設定
st.set_page_config(page_title="Personal Knowledge Base", layout="wide")
st.title("🧠 Personal Knowledge Base WebUI")

# ---------------------------------------------------------
# Session State の初期化
# ---------------------------------------------------------
if "edit_mode" not in st.session_state:
    st.session_state["edit_mode"] = False
if "form_title" not in st.session_state:
    st.session_state["form_title"] = ""
if "form_content" not in st.session_state:
    st.session_state["form_content"] = ""
if "form_input_type_idx" not in st.session_state:
    st.session_state["form_input_type_idx"] = 0
if "form_category" not in st.session_state:
    st.session_state["form_category"] = "default"
if "form_subdir" not in st.session_state:
    st.session_state["form_subdir"] = ""
if "last_rag_answer" not in st.session_state:
    st.session_state["last_rag_answer"] = ""
if "last_rag_query" not in st.session_state:
    st.session_state["last_rag_query"] = ""

# ---------------------------------------------------------
# サイドバー: 1. AIモデル設定
# ---------------------------------------------------------
st.sidebar.header("⚙️ 
```

## 4. 依存関係と連携
- `scripts/server/` 内の他のモジュールとの連携。
