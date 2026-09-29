import json
import time
import urllib.request
import urllib.error

# ---------------------------------------------------------
# 汎用LLM呼び出し関数
# ---------------------------------------------------------
def call_llm(
    prompt: str,
    llm_provider: str = "Ollama (Local LLM)",
    gemini_model: str = "gemini-2.5-flash",
    api_key: str = "",
    ollama_model: str = "qwen2.5:1.5b",
    ollama_url: str = "http://localhost:11434"
) -> str:
    max_retries = 3
    retry_delay = 2  # 初回待機時間（秒）
    
    for attempt in range(max_retries):
        try:
            if llm_provider == "Gemini (Cloud API)":
                if not api_key:
                    raise ValueError("Gemini API キーが取得できませんでした。`01-private/gemini_api_key.txt` を配置してください。")
                
                url = f"https://generativelanguage.googleapis.com/v1beta/models/{gemini_model}:generateContent?key={api_key}"
                payload = json.dumps({"contents": [{"parts": [{"text": prompt}]}]}).encode("utf-8")
                req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
                
                with urllib.request.urlopen(req) as res:
                    res_data = json.loads(res.read().decode("utf-8"))
                    return res_data["candidates"][0]["content"]["parts"][0]["text"]

            else:
                url = f"{ollama_url.rstrip('/')}/api/generate"
                payload = json.dumps({
                    "model": ollama_model,
                    "prompt": prompt,
                    "stream": False,
                    "options": {"keep_alive": "5m"}
                }).encode("utf-8")
                req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})
                
                with urllib.request.urlopen(req) as res:
                    res_data = json.loads(res.read().decode("utf-8"))
                    return res_data["response"]
                    
        except urllib.error.HTTPError as e:
            if e.code == 503 and attempt < max_retries - 1:
                time.sleep(retry_delay)
                retry_delay *= 2  # 2秒 ➔ 4秒 と待機時間を倍増
                continue
            raise e
        except Exception as e:
            raise e
