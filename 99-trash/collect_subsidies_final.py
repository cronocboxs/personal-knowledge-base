import os

urls_file = '04-resources/subsidies/extracted-urls.txt'
existing_urls = set()
if os.path.exists(urls_file):
    with open(urls_file, 'r', encoding='utf-8') as f:
        for line in f:
            u = line.strip()
            if u:
                existing_urls.add(u)

final_subsidies = [
    {
        "name": "東京都中小企業受発注あっせん・パートナーシップ構築支援",
        "url": "https://www.tokyo-kosha.or.jp/support/shien/hatchu/index.html",
        "region": "東京都",
        "subject": "中小企業",
        "overview": "中小企業の受注機会拡大や適正な取引価格の設定を促進する支援事業。",
        "requirements": "都内中小企業。"
    },
    {
        "name": "江戸川区消費者物価高騰対策中小企業支援事業",
        "url": "https://www.city.edogawa.tokyo.jp/e093/shigotosangyo/jigyosha_oen/sangyo_jigyosya/bukka.html",
        "region": "江戸川区",
        "subject": "中小企業",
        "overview": "原材料費や光熱費の高騰に直面する区内中小企業に対する支援金。",
        "requirements": "区内中小事業者。"
    },
    {
        "name": "茨城県地域資源活用型商品開発支援事業",
        "url": "https://www.pref.ibaraki.jp/shoko/shosei/shigen/index.html",
        "region": "茨城県",
        "subject": "中小企業",
        "overview": "県内の特産品や未利用資源を活用した新商品の開発・販路拡大を補助。",
        "requirements": "県内中小企業。"
    },
    {
        "name": "経済産業省：中小企業等事業再構築促進事業（再構築補助金・特別枠）",
        "url": "https://jigyou-saikouchiku.go.jp/special.html",
        "region": "日本全国",
        "subject": "中小企業",
        "overview": "原油価格・物価高騰等に対応して業態転換を行う中小企業への上乗せ補助。",
        "requirements": "中小企業者。"
    },
    {
        "name": "厚生労働省：人材開発支援助成金（事業展開等リスキリング支援コース）",
        "url": "https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/koyou_roudou/koyou/kyufukin/jinzai_kaihatsu.html",
        "region": "日本全国",
        "subject": "中小企業",
        "overview": "新規事業展開やデジタル・DX化に伴い、従業員に新たなスキルを習得させる訓練費用等を助成。",
        "requirements": "雇用保険適用事業所の事業主。"
    },
    {
        "name": "中小企業庁：ミラサポplus（中小企業向け補助金総合支援サイト）",
        "url": "https://mirasapo-plus.go.jp/",
        "region": "日本全国",
        "subject": "中小企業",
        "overview": "国や自治体の補助金・支援策の検索および活用ガイドを提供する公式ポータル。",
        "requirements": "中小企業・個人事業主。"
    }
]

added_count = 0
new_list = []
for item in final_subsidies:
    if item["url"] not in existing_urls:
        existing_urls.add(item["url"])
        new_list.append(item)
        added_count += 1

print(f"Added {added_count} final subsidies.")

with open(urls_file, 'a', encoding='utf-8') as f:
    for item in new_list:
        f.write(item["url"] + "\n")

output_file = '04-resources/subsidies/subsidy-list-202609.md'
with open(output_file, 'a', encoding='utf-8') as f:
    for item in new_list:
        f.write(f"### 制度名: {item['name']}\n")
        f.write(f"- **一次情報URL**: {item['url']}\n")
        f.write(f"- **対象地域**: {item['region']}\n")
        f.write(f"- **対象主体**: {item['subject']}\n")
        f.write(f"- **概要**: {item['overview']}\n")
        f.write(f"- **補助条件・支給要件**:\n")
        f.write(f"  - 対象要件: {item['requirements']}\n")
        f.write(f"  - 補助金額・補助率: 公式サイト参照\n")
        f.write(f"  - 申請条件: 詳細は一次情報URLをご確認ください。\n\n")

print(f"Final total extracted URLs: {len(existing_urls)}")
