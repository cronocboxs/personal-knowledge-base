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
st.sidebar.header("⚙️ AIモデル設定")

providers = ["Ollama (Local LLM)", "Gemini (Cloud API)"]
default_provider_setting = config.get("default_provider", "Ollama (Local LLM)")
default_provider_idx = 0 if default_provider_setting == "Ollama (Local LLM)" else 1

llm_provider = st.sidebar.radio(
    "使用するLLMプロバイダ",
    providers,
    index=default_provider_idx
)

if llm_provider == "Gemini (Cloud API)":
    gemini_models = config.get("gemini", {}).get("available_models", ["gemini-3.5-flash-lite"])
    default_gemini = config.get("gemini", {}).get("default_model", "gemini-3.5-flash-lite")
    gemini_idx = gemini_models.index(default_gemini) if default_gemini in gemini_models else 0
    
    gemini_model = st.sidebar.selectbox(
        "Gemini モデル選択",
        gemini_models,
        index=gemini_idx
    )
    api_key = get_gemini_api_key()
    
    if api_key:
        st.sidebar.success("🔑 Gemini APIキーを読み込みました")
    else:
        st.sidebar.error("⚠️ Gemini APIキーが見つかりません。`01-private/gemini_api_key.txt` を確認してください。")

else:
    available_ollama_models = get_ollama_models()
    default_ollama = config.get("ollama", {}).get("default_model", "gemma4:e2b")
    ollama_idx = available_ollama_models.index(default_ollama) if default_ollama in available_ollama_models else 0
    
    ollama_model = st.sidebar.selectbox(
        "Ollama モデル選択 (動的取得)",
        available_ollama_models,
        index=ollama_idx
    )
    ollama_url = st.sidebar.text_input(
        "Ollama Endpoint",
        value=config.get("ollama", {}).get("endpoint", "http://localhost:11434")
    )

st.sidebar.markdown("---")

# ---------------------------------------------------------
# サイドバー: 2. エクスプローラー風ディレクトリツリー描画
# ---------------------------------------------------------
def render_explorer_tree(dir_path: str, is_knowledge: bool = False, parent_container=st.sidebar):
    if not os.path.exists(dir_path):
        parent_container.caption("（ディレクトリ未作成）")
        return

    try:
        entries = sorted(os.listdir(dir_path))
    except Exception:
        return

    dirs = []
    files = []
    for entry in entries:
        if entry.startswith(".") or entry in ["head", "node_modules", "__pycache__"]:
            continue
        full_path = os.path.join(dir_path, entry)
        if os.path.isdir(full_path):
            dirs.append(entry)
        elif entry.endswith(".md"):
            files.append(entry)

    for d in dirs:
        full_dir_path = os.path.join(dir_path, d)
        with parent_container.expander(f"📁 {d}", expanded=False):
            sub_container = st.container()
            render_explorer_tree(full_dir_path, is_knowledge, parent_container=sub_container)

    for f in files:
        full_file_path = os.path.join(dir_path, f)
        rel_path = os.path.relpath(full_file_path, PROJECT_ROOT)
        
        if parent_container.button(f"📄 {f}", key=f"btn_{rel_path}", use_container_width=True):
            load_file_to_form(rel_path, is_knowledge)
            st.rerun()

def load_file_to_form(rel_file_path: str, is_knowledge: bool):
    abs_path = os.path.join(PROJECT_ROOT, rel_file_path)
    if os.path.exists(abs_path):
        with open(abs_path, "r", encoding="utf-8") as f:
            file_text = f.read()
            
        st.session_state["edit_mode"] = True
        base_name = os.path.basename(rel_file_path).replace(".md", "")
        title_clean = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', base_name)
        st.session_state["form_title"] = title_clean
        
        if is_knowledge or "02-knowledge" in rel_file_path:
            st.session_state["form_input_type_idx"] = 1
            parts = rel_file_path.split(os.sep)
            if len(parts) >= 3:
                st.session_state["form_category"] = parts[1]
                
            if file_text.startswith("---"):
                body_parts = file_text.split("---", 2)
                if len(body_parts) >= 3:
                    raw_body = body_parts[2].strip()
                    raw_body = re.sub(r'^#\s+.*?\n\n', '', raw_body)
                    st.session_state["form_content"] = raw_body
                else:
                    st.session_state["form_content"] = file_text
            else:
                st.session_state["form_content"] = file_text
        else:
            st.session_state["form_input_type_idx"] = 0
            st.session_state["form_content"] = file_text
            rel_res = os.path.relpath(abs_path, RESOURCES_DIR)
            res_dir = os.path.dirname(rel_res)
            st.session_state["form_subdir"] = "" if res_dir == "." else res_dir
            
        st.sidebar.success(f"読み込みました: `{rel_file_path}`")

st.sidebar.header("📂 ファイルエクスプローラー")

if st.sidebar.button("➕ 新規作成 (フォームリセット)", use_container_width=True):
    st.session_state["edit_mode"] = False
    st.session_state["form_title"] = ""
    st.session_state["form_content"] = ""
    st.session_state["form_input_type_idx"] = 0
    st.session_state["form_category"] = "default"
    st.session_state["form_subdir"] = ""
    st.rerun()

st.sidebar.markdown("---")

st.sidebar.subheader("🧠 02-knowledge")
render_explorer_tree(KNOWLEDGE_DIR, is_knowledge=True)

st.sidebar.markdown("---")

st.sidebar.subheader("📥 04-resources")
render_explorer_tree(RESOURCES_DIR, is_knowledge=False)

# ---------------------------------------------------------
# WebUIメイン表示
# ---------------------------------------------------------
tab1, tab2 = st.tabs(["📥 状況・データ入力・編集", "💬 ナレッジ検索・質問"])

# ---------------------------------------------------------
# Tab 1: 解析対象データの配置 & ナレッジ昇華・編集
# ---------------------------------------------------------
with tab1:
    if st.session_state["edit_mode"]:
        st.header("✏️ データ・ナレッジの編集・再昇華")
        st.info("※ 左メニューから既存ファイルが選択・読み込みされています。")
    else:
        st.header("解析対象データ / 状況の入力 (新規保存)")
    
    input_type = st.radio(
        "処理モードを選択してください",
        [
            "1. 一次素材の保存 (04-resources/)",
            "2. ナレッジの新規登録・AI自動昇華 (04-resources/ 保存 ➔ 02-knowledge/ 昇華)"
        ],
        index=st.session_state["form_input_type_idx"]
    )
    
    title = st.text_input("タイトル / 識別名", value=st.session_state["form_title"], placeholder="例: system-error-log")
    
    if "1." in input_type:
        subdir = st.text_input("保存先サブディレクトリ（任意）", value=st.session_state["form_subdir"], placeholder="例: server-logs や web-scraps (空欄で直下)")
    else:
        # カテゴリ選択
        existing_categories = get_knowledge_categories()
        category_options = existing_categories + ["＋ 新規カテゴリ作成..."]
        default_cat = st.session_state["form_category"]
        cat_idx = existing_categories.index(default_cat) if default_cat in existing_categories else 0
        
        selected_cat = st.selectbox("ナレッジ保存先カテゴリ (02-knowledge/<カテゴリ>/)", category_options, index=cat_idx, key="tab1_knowledge_category_select")
        repo_name = st.text_input("新規カテゴリ名（フォルダ名）", placeholder="例: system-architecture").strip() if selected_cat == "＋ 新規カテゴリ作成..." else selected_cat

        # 指示書テンプレートの選択ボックス（ユニークキー設定）
        available_prompts = get_available_prompts()
        selected_prompt = st.selectbox("使用する指示書（プロンプトテンプレート）", available_prompts, key="tab1_sublimation_prompt_select")

    content = st.text_area("本文・状況の詳細", value=st.session_state["form_content"], height=250)
    
    btn_label = "変更を更新・再昇華" if st.session_state["edit_mode"] else "実行（保存・昇華）"
    
    if st.button(btn_label):
        if title and content:
            today = datetime.date.today().strftime("%Y-%m-%d")
            base_filename = f"{today}-{title.strip().lower().replace(' ', '-')}.md"
            
            if "1." in input_type:
                target_dir = os.path.join(RESOURCES_DIR, subdir.strip()) if subdir.strip() else RESOURCES_DIR
                os.makedirs(target_dir, exist_ok=True)
                resource_path = os.path.join(target_dir, base_filename)
                
                with open(resource_path, "w", encoding="utf-8") as f:
                    f.write(content)
                st.success(f"✅ 一次素材を保存・更新しました: `{resource_path}`")
                
            else:
                if not repo_name:
                    st.error("カテゴリ名を入力してください。")
                else:
                    with st.spinner("1. 04-resources/ に一次データを保存中..."):
                        os.makedirs(RESOURCES_DIR, exist_ok=True)
                        resource_path = os.path.join(RESOURCES_DIR, base_filename)
                        with open(resource_path, "w", encoding="utf-8") as f:
                            f.write(content)
                        st.info(f"📁 一次保存完了: `{resource_path}`")
                    
                    target_repo_dir = os.path.join(KNOWLEDGE_DIR, repo_name)
                    head_dir = os.path.join(target_repo_dir, "head")
                    note_dir = os.path.join(target_repo_dir, "note")
                    os.makedirs(head_dir, exist_ok=True)
                    os.makedirs(note_dir, exist_ok=True)
                    
                    head_path = os.path.join(head_dir, base_filename)
                    note_path = os.path.join(note_dir, base_filename)
                    
                    selected_model_name = gemini_model if llm_provider == "Gemini (Cloud API)" else ollama_model
                    with st.spinner(f"2. [{selected_model_name}] が 指示書 ({selected_prompt}) に従って解析昇華中..."):
                        generated_data = generate_knowledge_files(
                            title=title,
                            content=content,
                            today=today,
                            category=repo_name,
                            prompt_filename=selected_prompt,
                            llm_provider=llm_provider,
                            gemini_model=gemini_model if llm_provider == "Gemini (Cloud API)" else "",
                            api_key=get_gemini_api_key(),
                            ollama_model=ollama_model if llm_provider != "Gemini (Cloud API)" else "",
                            ollama_url=ollama_url if llm_provider != "Gemini (Cloud API)" else ""
                        )
                        
                        with open(head_path, "w", encoding="utf-8") as f:
                            f.write(generated_data["head_content"].strip() + "\n")
                            
                        with open(note_path, "w", encoding="utf-8") as f:
                            f.write(generated_data["note_content"].strip() + "\n")

                    with st.spinner("3. SQLite ベクトル検索インデックスを更新中..."):
                        try:
                            indexer_script = os.path.join(PROJECT_ROOT, "scripts/index/update-index.py")
                            subprocess.run(
                                ["python3", indexer_script, "--file", note_path],
                                check=True,
                                capture_output=True,
                                text=True
                            )
                            st.info("🔍 インデックス同期完了")
                        except Exception as e:
                            st.warning(f"⚠️ インデックスの更新に失敗しました: {e}")
                        
                    st.success(f"✨ ナレッジ昇華完了！ (`02-knowledge/{repo_name}/`)\n- `head`: `{head_path}`\n- `note`: `{note_path}`")
        else:
            st.warning("タイトルと本文を入力してください。")

# ---------------------------------------------------------
# Tab 2: ナレッジに基づく質問回答 (RAG パイプライン & 回答ナレッジ化)
# ---------------------------------------------------------
with tab2:
    st.header("💬 ナレッジベースへ質問 (RAG)")
    
    user_query = st.text_input("質問を入力してください", placeholder="例: 今月の収支の傾向や、gitのブランチ切り替え手順は？")
    
    col1, col2 = st.columns([2, 1])
    with col1:
        all_categories = ["すべて"] + get_knowledge_categories()
        selected_categories = st.multiselect(
            "検索対象カテゴリ (複数選択可)",
            options=all_categories,
            default=["すべて"]
        )
    with col2:
        top_k = st.number_input("参照するナレッジ件数", min_value=1, max_value=10, value=3, key="rag_top_k_input")

    if st.button("回答を生成", type="primary"):
        if user_query:
            selected_model_name = gemini_model if llm_provider == "Gemini (Cloud API)" else ollama_model
            
            with st.spinner("🔍 指定カテゴリのナレッジDBから関連情報を検索中..."):
                relevant_docs = search_relevant_knowledge(
                    user_query, 
                    top_k=top_k, 
                    target_categories=selected_categories
                )

            if relevant_docs:
                st.subheader("📚 参照した関連ナレッジ")
                context_str = ""
                for idx, doc in enumerate(relevant_docs, 1):
                    similarity_pct = round(doc['score'] * 100, 1)
                    with st.expander(f"【参照 {idx}】[{doc['category']}] {doc['title']} (類似度: {similarity_pct}%) - `{doc['rel_path']}`"):
                        st.markdown(f"**カテゴリ**: `{doc['category']}` | **概要**: {doc['summary']}")
                        st.text_area(f"本文抜粋 ({doc['rel_path']})", value=doc['content'], height=150, disabled=True, key=f"rag_ctx_{idx}")
                    
                    context_str += f"\n--- 【ナレッジ {idx} (カテゴリ: {doc['category']}): {doc['title']}】 ---\n{doc['content']}\n"
            else:
                st.warning("⚠️ 指定されたカテゴリに関連するナレッジが見つかりませんでした。一般的な知識で回答します。")
                context_str = "（参照可能なローカルナレッジはありません）"

            rag_prompt = f"""あなたは登録されたパーソナルナレッジベースに基づいて回答するAIアシスタントです。
以下の【参照ナレッジ】の情報を最優先の根拠として使用し、ユーザーの【質問】に対して分かりやすく回答してください。

【参照ナレッジ】:
{context_str}

【質問】:
{user_query}

【回答指示】:
- 参照ナレッジに含まれる事実に基づいて正確に答えてください。
- 該当する情報がある場合は、参照したナレッジタイトルやファイル名を適宜引用してください。
"""
            with st.spinner(f"🤖 [{selected_model_name}] が回答を生成中..."):
                try:
                    answer = call_llm(
                        prompt=rag_prompt,
                        llm_provider=llm_provider,
                        gemini_model=gemini_model if llm_provider == "Gemini (Cloud API)" else "",
                        api_key=get_gemini_api_key(),
                        ollama_model=ollama_model if llm_provider != "Gemini (Cloud API)" else "",
                        ollama_url=ollama_url if llm_provider != "Gemini (Cloud API)" else ""
                    )
                    st.session_state["last_rag_answer"] = answer
                    st.session_state["last_rag_query"] = user_query
                except Exception as e:
                    st.error(f"回答生成中にエラーが発生しました: {e}")
        else:
            st.warning("質問を入力してください。")

    # --- 回答結果とナレッジ昇華フォーム ---
    if st.session_state["last_rag_answer"]:
        st.markdown("---")
        st.markdown("### 💡 AIからの回答")
        st.markdown(st.session_state["last_rag_answer"])

        st.markdown("---")
        with st.expander("💡 この回答をナレッジとして昇華・保存する", expanded=False):
            save_title = st.text_input("保存用タイトル (任意 / 空欄でAI自動生成)", placeholder="例: macbook-llm-setup-guide")
            
            sublimate_categories = ["🤖 AIに自動推察させる"] + get_knowledge_categories() + ["＋ 新規カテゴリ作成..."]
            save_cat_choice = st.selectbox("保存先カテゴリ", sublimate_categories, key="rag_save_category_select")
            
            if save_cat_choice == "＋ 新規カテゴリ作成...":
                target_cat_name = st.text_input("新規作成するカテゴリ名", placeholder="例: mac-settings").strip()
            else:
                target_cat_name = save_cat_choice

            if st.button("✨ ナレッジへ自動昇華＆インデックス再作成"):
                today = datetime.date.today().strftime("%Y-%m-%d")
                
                with st.spinner("AIがタイトル・カテゴリ・関連ノート(parent/children/related)を判定し昇華中..."):
                    res = auto_sublimate_rag_answer(
                        user_query=st.session_state["last_rag_query"],
                        answer_text=st.session_state["last_rag_answer"],
                        custom_title=save_title.strip(),
                        selected_cat=target_cat_name,
                        today=today,
                        llm_provider=llm_provider,
                        gemini_model=gemini_model if llm_provider == "Gemini (Cloud API)" else "",
                        api_key=get_gemini_api_key(),
                        ollama_model=ollama_model if llm_provider != "Gemini (Cloud API)" else "",
                        ollama_url=ollama_url if llm_provider != "Gemini (Cloud API)" else ""
                    )
                    
                    final_title = res.get("inferred_title", f"rag-answer-{today}").replace(".md", "").strip().lower().replace(" ", "-")
                    final_cat = res.get("inferred_category", "default").strip()
                    
                    filename = f"{today}-{final_title}.md"
                    target_repo_dir = os.path.join(KNOWLEDGE_DIR, final_cat)
                    head_dir = os.path.join(target_repo_dir, "head")
                    note_dir = os.path.join(target_repo_dir, "note")
                    
                    os.makedirs(head_dir, exist_ok=True)
                    os.makedirs(note_dir, exist_ok=True)
                    
                    head_path = os.path.join(head_dir, filename)
                    note_path = os.path.join(note_dir, filename)
                    
                    with open(head_path, "w", encoding="utf-8") as f:
                        f.write(res["head_content"].strip() + "\n")
                        
                    with open(note_path, "w", encoding="utf-8") as f:
                        f.write(res["note_content"].strip() + "\n")

                with st.spinner("SQLite ベクトル検索インデックスを再構築中..."):
                    try:
                        indexer_script = os.path.join(PROJECT_ROOT, "scripts/index/update-index.py")
                        subprocess.run(
                            ["python3", indexer_script, "--file", note_path],
                            check=True,
                            capture_output=True,
                            text=True
                        )
                        st.info("🔍 インデックス同期完了")
                    except Exception as e:
                        st.warning(f"⚠️ インデックス更新エラー: {e}")

                st.success(f"✨ 回答をナレッジとして保存しました！\n- **カテゴリ**: `{final_cat}`\n- **ファイル名**: `{filename}`")
                st.rerun()