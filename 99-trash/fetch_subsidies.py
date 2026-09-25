import urllib.request
import urllib.parse
import re
import time

def search_duckduckgo(query, max_results=10):
    url = "https://html.duckduckgo.com/html/"
    data = urllib.parse.urlencode({"q": query}).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Referer": "https://html.duckduckgo.com/"
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            html = response.read().decode('utf-8', errors='ignore')
            urls = []
            pattern = re.compile(r'class="result__url"[^>]*href="([^"]+)"')
            matches = pattern.findall(html)
            for m in matches:
                if 'uddg=' in m:
                    parsed = urllib.parse.urlparse(m)
                    qs = urllib.parse.parse_qs(parsed.query)
                    if 'uddg' in qs:
                        real_url = qs['uddg'][0]
                        urls.append(real_url)
            return urls[:max_results]
    except Exception as e:
        print(f"Error searching for {query}: {e}")
        return []

if __name__ == "__main__":
    queries = [
        "茨城県 中小企業 補助金 制度 公式 site:pref.ibaraki.jp",
        "茨城県 産業振興財団 補助金 公式",
        "経済産業省 小規模事業者持続化補助金 公式",
        "IT導入補助金 公式",
        "東京都中小企業振興公社 助成金 一覧",
        "江戸川区 中小企業 融資 助成金 公式 site:city.edogawa.tokyo.jp",
        "東京都 創業 助成金 公式 site:metro.tokyo.lg.jp",
        "茨城県 取手市 つくば市 補助金 中小企業 公式"
    ]
    all_urls = []
    for q in queries:
        print(f"Query: {q}")
        urls = search_duckduckgo(q, 10)
        for u in urls:
            print(f"  - {u}")
            all_urls.append(u)
        time.sleep(3)
    print(f"Total found: {len(all_urls)}")
