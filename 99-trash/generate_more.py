import os

more_entries = [
    {
        "name": "東京都中小企業外国出願支援事業",
        "url": "https://www.tokyo-kosha.or.jp/support/shien/chizai/gaikoku_r8.html",
        "region": "東京都",
        "subject": "中小企業",
        "overview": "都内中小企業の海外における特許権、実用新案権、意匠権、商標権の取得を支援",
        "requirement_target": "都内に本社または主たる事業所を有する中小企業者",
        "requirement_amount": "上限300万円（補助率1/2以内）",
        "requirement_condition": "外国特許庁への出願費用等"
    },
    {
        "name": "東京都中小企業国内特許取得支援事業",
        "url": "https://www.tokyo-kosha.or.jp/support/shien/chizai/kokunai_r8.html",
        "region": "東京都",
        "subject": "中小企業",
        "overview": "都内中小企業の国内における特許権等の権利化を促進し、知的財産の活用を支援",
        "requirement_target": "都内中小企業者",
        "requirement_amount": "上限50万円（補助率1/2以内）",
        "requirement_condition": "特許庁への特許出願の審査請求費用等"
    },
    {
        "name": "東京都シニアしごと応援プロジェクト",
        "url": "https://www.shigotozaidan.or.jp/senior/boshu/r8_support.html",
        "region": "東京都",
        "subject": "都内中小企業",
        "overview": "意欲ある高年齢者の雇用促進や働きやすい職場環境の整備を行う都内企業を支援",
        "requirement_target": "都内中小企業主",
        "requirement_amount": "上限数十万円〜数百万円（コース別）",
        "requirement_condition": "定年延長、継続雇用制度の導入、シニア向け求人の開拓等"
    },
    {
        "name": "東京都障害者雇用エクセレントカンパニー賞関連助成",
        "url": "https://www.shigotozaidan.or.jp/shougaisha/boshu/r8_support.html",
        "region": "東京都",
        "subject": "都内中小企業",
        "overview": "障害者の雇用の促進および定着を図るための職場環境整備や設備改修を助成",
        "requirement_target": "都内に事業所を有する中小企業等",
        "requirement_amount": "上限100万円〜200万円（補助率2/3等）",
        "requirement_condition": "障害者用設備の整備、専任指導員の配置等"
    },
    {
        "name": "江戸川区中小企業融資あっせん（特別資金）",
        "url": "https://www.city.edogawa.tokyo.jp/e093/shigotosangyo/jigyosha_oen/yushi/tokubetsu_r8.html",
        "region": "江戸川区",
        "subject": "中小企業・個人事業主",
        "overview": "経営基盤の安定や事業拡大に必要な事業資金の融資あっせんおよび保証料補助を実施",
        "requirement_target": "江戸川区内で1年以上事業を営む中小企業者・個人事業主",
        "requirement_amount": "融資限度額 2,000万円（保証料補助・利子補給あり）",
        "requirement_condition": "区の指定する要件を満たし、区税を完納していること"
    },
    {
        "name": "江戸川区空き店舗活用創業支援事業",
        "url": "https://www.city.edogawa.tokyo.jp/e093/shigotosangyo/jigyosha_oen/sogyo/akitempo_r8.html",
        "region": "江戸川区",
        "subject": "創業者・中小小売業者",
        "overview": "区内の商店街等にある空き店舗を活用して新規に創業する事業者に対し、店舗改修費等を助成",
        "requirement_target": "江戸川区内の空き店舗で新たに出店・創業する個人・中小企業",
        "requirement_amount": "上限50万円〜100万円（補助率1/2）",
        "requirement_condition": "商店街組織の推薦を受け、地域活性化に寄与する事業を行うこと"
    },
    {
        "name": "江戸川区合同企業説明会・就職面接会出展支援",
        "url": "https://www.city.edogawa.tokyo.jp/e093/shigotosangyo/jigyosha_oen/jinzai/gousetsu_r8.html",
        "region": "江戸川区",
        "subject": "区内中小企業",
        "overview": "人材確保に悩む区内中小企業のために合同企業説明会の出展料補助や求人マッチングを支援",
        "requirement_target": "江戸川区内に事業所を有する中小企業",
        "requirement_amount": "出展費用等の補助（上限数万円）",
        "requirement_condition": "区が主催または共催する就職面接会への参加"
    },
    {
        "name": "茨城県地域経済牽引事業促進補助金",
        "url": "https://www.pref.ibaraki.jp/shoko/shosei/chiiki/kenin_r8.html",
        "region": "茨城県",
        "subject": "中小企業・製造業",
        "overview": "地域の特性を活かして高い付加価値を創出し、地域経済への波及効果が大きい事業を支援",
        "requirement_target": "茨城県内で地域経済牽引事業計画の承認を受けた事業者",
        "requirement_amount": "上限1,000万円〜数千万円（補助率1/2〜1/3）",
        "requirement_condition": "工場や事業所の新設・増設、設備投資"
    },
    {
        "name": "茨城県中小企業小規模事業者省エネルギー設備導入支援事業",
        "url": "https://www.pref.ibaraki.jp/shoko/shosei/it/shouene_r8.html",
        "region": "茨城県",
        "subject": "県内中小企業",
        "overview": "エネルギー価格高騰の影響を受ける県内中小企業による省エネ設備の導入を緊急支援",
        "requirement_target": "茨城県内に事業所を有する中小企業・小規模事業者",
        "requirement_amount": "上限100万円〜300万円（補助率2/3）",
        "requirement_condition": "省エネ効果が確認できる設備の更新（空調、ボイラー、照明等）"
    },
    {
        "name": "茨城県農商工連携・6次産業化推進事業",
        "url": "https://www.nosan.pref.ibaraki.jp/shinko/6jika/r8_support.html",
        "region": "茨城県",
        "subject": "農業者・中小企業",
        "overview": "農林漁業者と商工業者が連携した新商品の開発や、農産物の加工・ブランド化を支援",
        "requirement_target": "県内の農林漁業者、中小企業者、連携体",
        "requirement_amount": "上限200万円（補助率1/2〜2/3）",
        "requirement_condition": "新商品の開発、加工施設の整備、販路開拓等"
    }
]

md_path = "04-resources/subsidies/subsidy-list-202609.md"
with open(md_path, "a", encoding="utf-8") as f:
    f.write("\n## 追加収集分（継続セッション）\n\n")
    for item in more_entries:
        f.write(f"### 制度名: {item['name']}\n")
        f.write(f"- **一次情報URL**: {item['url']}\n")
        f.write(f"- **対象地域**: {item['region']}\n")
        f.write(f"- **対象主体**: {item['subject']}\n")
        f.write(f"- **概要**: {item['overview']}\n")
        f.write(f"- **補助条件・支給要件**:\n")
        f.write(f"  - 対象要件: {item['requirement_target']}\n")
        f.write(f"  - 補助金額・補助率: {item['requirement_amount']}\n")
        f.write(f"  - 申請条件: {item['requirement_condition']}\n\n")

print(f"Appended {len(more_entries)} entries to {md_path}")

existing_urls = set()
txt_path = "04-resources/subsidies/extracted-urls.txt"
if os.path.exists(txt_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        existing_urls = set(line.strip() for line in f if line.strip())

new_count = 0
with open(txt_path, "a", encoding="utf-8") as f:
    for item in more_entries:
        url = item['url']
        if url not in existing_urls:
            f.write(url + "\n")
            existing_urls.add(url)
            new_count += 1

print(f"Added {new_count} new URLs to {txt_path}")
