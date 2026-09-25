import urllib.request
import urllib.parse
import re

queries = [
    "東京都 中小企業 補助金 令和8年",
    "江戸川区 産業 助成金 補助金 企業",
    "茨城県 企業 補助金 支援 募集",
    "厚生労働省 雇用 助成金 一覧 2026",
    "経済産業省 中小企業 補助金 一覧",
    "東京都 中小企業振興公社 助成金 一覧",
    "江戸川区 店舗 改修 省エネ 補助金",
    "茨城県 ものづくり 補助金 制度"
]

existing_urls = set()
with open("04-resources/subsidies/extracted-urls.txt", "r") as f:
    for line in f:
        existing_urls.add(line.strip())

print(f"Loaded {len(existing_urls)} existing URLs.")

new_items = []

for q in queries:
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(q)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        with urllib.request.urlopen(req) as resp:
            html = resp.read().decode("utf-8")
            # find all hrefs in result snippets
            from html.parser import HTMLParser
            class DDGParser(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.urls = []
                def handle_starttag(self, tag, attrs):
                    if tag == "a":
                        d = dict(attrs)
                        href = d.get("href", "")
                        if "uddg=" in href:
                            m = re.search(r"uddg=([^&]+)", href)
                            if m:
                                self.urls.append(urllib.parse.unquote(m.group(1)))
            parser = DDGParser()
            parser.feed(html)
            print(f"Query '{q}': found {len(parser.urls)} URLs")
            for u in parser.urls:
                if u not in existing_urls:
                    new_items.append(u)
    except Exception as e:
        print(f"Error for query {q}: {e}")

print(f"Total new unique URLs found: {len(set(new_items))}")
