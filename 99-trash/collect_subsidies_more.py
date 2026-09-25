import os

urls_file = '04-resources/subsidies/extracted-urls.txt'
existing_urls = set()
if os.path.exists(urls_file):
    with open(urls_file, 'r', encoding='utf-8') as f:
        for line in f:
            u = line.strip()
            if u:
                existing_urls.add(u)

more_subsidies = [
    # --- 東京都 追加 ---
    {
        "name": "東京都女性・若者・シニア創業サポート事業",
        "url": "https://www.tokyo-kosha.or.jp/support/josei/sogyo/josei.html",
        "region": "東京都",
        "subject": "個人",
        "overview": "女性、若者、シニア層の起業家を対象とした無担保・低利の融資と、創業支援を一体的に提供。",
        "requirements": "都内で創業予定または創業後5年未満の個人・中小企業。"
    },
    {
        "name": "東京都商店街デジタル化推進事業",
        "url": "https://www.sangyo-rodo.metro.tokyo.lg.jp/chushou/shoko/shotengai/digital.html",
        "region": "東京都",
        "subject": "中小企業",
        "overview": "商店街のキャッシュレス導入や共通ポイントカード導入、SNS活用などのデジタル化を支援。",
        "requirements": "都内の商店街振興組合等。"
    },
    {
        "name": "東京都エコハウス・中小ビル省エネ改修促進事業",
        "url": "https://www.tokyo-kankyo.jp/building/index.html",
        "region": "東京都",
        "subject": "中小企業",
        "overview": "中小規模事業所やテナントビルの省エネルギー改修工事費用を助成。",
        "requirements": "都内のビルオーナー・テナント企業。"
    },
    {
        "name": "東京都農商工連携ファンド事業",
        "url": "https://www.tokyo-kosha.or.jp/support/shien/noshoko/index.html",
        "region": "東京都",
        "subject": "中小企業",
        "overview": "都内農業者等と中小企業者による新商品開発や地域特産品ブランド化を支援。",
        "requirements": "都内の農林漁業者と中小企業の連携体。"
    },
    {
        "name": "東京都事業承継・引継ぎ支援事業",
        "url": "https://www.tokyo-kosha.or.jp/support/shien/shoukei/index.html",
        "region": "東京都",
        "subject": "中小企業",
        "overview": "後継者問題に悩む中小企業に対し、専門家による相談対応やM&Aマッチングを支援。",
        "requirements": "都内中小企業者。"
    },
    {
        "name": "東京都デザイン活用促進事業（Tokyo Design Station）",
        "url": "https://www.tokyo-kosha.or.jp/support/shien/design/index.html",
        "region": "東京都",
        "subject": "中小企業",
        "overview": "中小企業のデザイン経営導入や製品パッケージデザインの刷新を支援。",
        "requirements": "都内の中小製造業・デザイン関連企業。"
    },
    {
        "name": "東京都中小企業特許出願等支援事業",
        "url": "https://www.tokyo-kosha.or.jp/support/shien/chizai/kokunai.html",
        "region": "東京都",
        "subject": "中小企業",
        "overview": "国内外への特許・実用新案・意匠・商標の出願にかかる経費の一部を補助。",
        "requirements": "都内中小企業者。"
    },
    {
        "name": "東京都外国人材受入環境整備助成金",
        "url": "https://www.shigotozaidan.or.jp/gaikokujin/boshu/index.html",
        "region": "東京都",
        "subject": "中小企業",
        "overview": "外国人材が働きやすい職場環境を整備するための多言語対応や生活支援の取り組みを助成。",
        "requirements": "都内中小企業。"
    },
    {
        "name": "東京都中小企業障害者雇用促進助成金",
        "url": "https://www.shigotozaidan.or.jp/shougaisha/boshu/index.html",
        "region": "東京都",
        "subject": "中小企業",
        "overview": "障害者の雇用促進と職場定着を図るための設備改修や作業環境整備費を助成。",
        "requirements": "都内中小企業。"
    },
    {
        "name": "東京都中小企業シニア活用促進助成金",
        "url": "https://www.shigotozaidan.or.jp/senior/boshu/index.html",
        "region": "東京都",
        "subject": "中小企業",
        "overview": "高年齢者の雇用継続や新たなシニア人材の雇用・定着に向けた取り組みを支援。",
        "requirements": "都内中小企業。"
    },

    # --- 江戸川区 追加 ---
    {
        "name": "江戸川区小規模事業者応援資金利子補給",
        "url": "https://www.city.edogawa.tokyo.jp/e093/shigotosangyo/jigyosha_oen/yushi/rishi.html",
        "region": "江戸川区",
        "subject": "小規模事業者",
        "overview": "小規模事業者の経営安定を図るための融資に対する利子補給。",
        "requirements": "区内小規模事業者。"
    },
    {
        "name": "江戸川区商店街イベント支援事業補助金",
        "url": "https://www.city.edogawa.tokyo.jp/e093/shigotosangyo/jigyosha_oen/sangyo_jigyosya/event.html",
        "region": "江戸川区",
        "subject": "中小企業",
        "overview": "商店街が実施する地域活性化イベントやプレミアム付商品券発行を支援。",
        "requirements": "区内商店街振興組合。"
    },
    {
        "name": "江戸川区ものづくり中小企業技術交流補助金",
        "url": "https://www.city.edogawa.tokyo.jp/e093/shigotosangyo/jigyosha_oen/sangyo_jigyosya/gijutsu.html",
        "region": "江戸川区",
        "subject": "中小企業",
        "overview": "区内製造業の技術交流や展示会出展にかかる費用を補助。",
        "requirements": "区内製造業の中小企業。"
    },
    {
        "name": "江戸川区事業承継支援補助金",
        "url": "https://www.city.edogawa.tokyo.jp/e093/shigotosangyo/jigyosha_oen/sogyo/shoukei.html",
        "region": "江戸川区",
        "subject": "中小企業",
        "overview": "親族内承継や第三者承継（M&A）に伴う専門家費用や登記費用等を補助。",
        "requirements": "区内中小事業者。"
    },
    {
        "name": "江戸川区エコ事業所表彰・奨励金制度",
        "url": "https://www.city.edogawa.tokyo.jp/e093/kankyo/kankyo/jigyosho/hyosho.html",
        "region": "江戸川区",
        "subject": "中小企業",
        "overview": "優れた環境配慮や省エネ実績を上げた事業所を表彰および奨励金を交付。",
        "requirements": "区内事業所。"
    },
    {
        "name": "江戸川区中小企業従業員福利厚生充実支援事業",
        "url": "https://www.city.edogawa.tokyo.jp/e093/shigotosangyo/jigyosha_oen/sangyo_jigyosya/fukuri.html",
        "region": "江戸川区",
        "subject": "中小企業",
        "overview": "中小企業の従業員向け福利厚生サービス加入費用や健康管理の取り組みを補助。",
        "requirements": "区内中小企業。"
    },
    {
        "name": "江戸川区テレワーク・WEB面談導入支援補助金",
        "url": "https://www.city.edogawa.tokyo.jp/e093/shigotosangyo/jigyosha_oen/digital/telework.html",
        "region": "江戸川区",
        "subject": "中小企業",
        "overview": "区内企業のテレワーク環境整備やWEB面談システムの導入を支援。",
        "requirements": "区内中小事業者。"
    },
    {
        "name": "江戸川区空き店舗活用出店支援事業",
        "url": "https://www.city.edogawa.tokyo.jp/e093/shigotosangyo/jigyosha_oen/sogyo/akitempo.html",
        "region": "江戸川区",
        "subject": "個人事業主",
        "overview": "商店街等の空き店舗を活用して新規出店する際の家賃の一部を助成。",
        "requirements": "区内で新規出店する個人・中小企業。"
    },
    {
        "name": "江戸川区中小企業知的財産相談窓口",
        "url": "https://www.city.edogawa.tokyo.jp/e093/shigotosangyo/jigyosha_oen/sangyo_jigyosya/chizai.html",
        "region": "江戸川区",
        "subject": "中小企業",
        "overview": "商標や特許等の知的財産に関する専門家相談を実施。",
        "requirements": "区内中小事業者。"
    },
    {
        "name": "江戸川区中小企業合同企業説明会支援",
        "url": "https://www.city.edogawa.tokyo.jp/e093/shigotosangyo/jigyosha_oen/jinzai/gousetsu.html",
        "region": "江戸川区",
        "subject": "中小企業",
        "overview": "地元就職を希望する求職者と区内企業のマッチングを支援。",
        "requirements": "区内企業。"
    },

    # --- 茨城県 追加 ---
    {
        "name": "茨城県地域経済牽引事業促進補助金",
        "url": "https://www.pref.ibaraki.jp/shoko/shosei/chiiki/kenin.html",
        "region": "茨城県",
        "subject": "中小企業",
        "overview": "地域の特性を活かして高い経済波及効果をもたらす事業の設備投資を支援。",
        "requirements": "県内事業者。"
    },
    {
        "name": "茨城県IT・ソフトウェア産業振興補助金",
        "url": "https://www.pref.ibaraki.jp/shoko/shosei/it/index.html",
        "region": "茨城県",
        "subject": "中小企業",
        "overview": "IT企業やソフトウェア開発企業による県内立地や事業拡大を支援。",
        "requirements": "IT関連企業。"
    },
    {
        "name": "茨城県小規模企業者経営改善資金（マル経融資）利子補給",
        "url": "https://www.pref.ibaraki.jp/shoko/shosei/kinyu/marukei.html",
        "region": "茨城県",
        "subject": "小規模事業者",
        "overview": "商工会等の経営指導を受けた小規模事業者が無担保・無保証人で借りられる融資に対する利子補給。",
        "requirements": "県内小規模事業者。"
    },
    {
        "name": "茨城県農商工連携・6次産業化推進事業",
        "url": "https://www.pref.ibaraki.jp/nosan/shinko/6jika/index.html",
        "region": "茨城県",
        "subject": "中小企業",
        "overview": "農林漁業者が自ら生産した農水産物を原材料とした加工・販売を行う6次産業化の取組みを支援。",
        "requirements": "県内農林漁業者・中小企業。"
    },
    {
        "name": "茨城県観光地魅力度向上・受入環境整備事業",
        "url": "https://www.pref.ibaraki.jp/shoko/kanko/seibi/index.html",
        "region": "茨城県",
        "subject": "中小企業",
        "overview": "観光施設のバリアフリー化や多言語化、Wi-Fi環境整備等の受入環境向上を支援。",
        "requirements": "県内観光事業者。"
    },
    {
        "name": "茨城県いばらき働き方改革推進補助金",
        "url": "https://www.pref.ibaraki.jp/shoko/rodo/hatarakikata/josei.html",
        "region": "茨城県",
        "subject": "中小企業",
        "overview": "長時間労働の是正や年次有給休暇の取得促進、賃金引き上げに向けた設備投資等を支援。",
        "requirements": "県内中小企業。"
    },
    {
        "name": "茨城県女性活躍推進企業認定制度・奨励事業",
        "url": "https://www.pref.ibaraki.jp/shoko/rodo/josei/nintei.html",
        "region": "茨城県",
        "subject": "中小企業",
        "overview": "女性の活躍推進や仕事と家庭の両立支援に積極的に取り組む企業を認定・支援。",
        "requirements": "県内企業。"
    },
    {
        "name": "茨城県次世代産業研究開発推進補助金",
        "url": "https://www.pref.ibaraki.jp/shoko/shosei/jisedai/index.html",
        "region": "茨城県",
        "subject": "中小企業",
        "overview": "宇宙、航空、次世代モビリティ、ライフサイエンス分野等における研究開発を支援。",
        "requirements": "県内中小企業。"
    },
    {
        "name": "茨城県商店街リニューアル支援事業",
        "url": "https://www.pref.ibaraki.jp/shoko/shosei/shinko/shotengai/index.html",
        "region": "茨城県",
        "subject": "中小企業",
        "overview": "商店街のアーケード改修や街路灯LED化、コミュニティスペース整備等を補助。",
        "requirements": "県内商店街組織。"
    },
    {
        "name": "茨城県中小企業人材育成研修支援事業",
        "url": "https://www.pref.ibaraki.jp/shoko/rodo/jinzai/kenshu.html",
        "region": "茨城県",
        "subject": "中小企業",
        "overview": "従業員のスキルアップや専門資格取得のための研修費用を助成。",
        "requirements": "県内中小企業。"
    },

    # --- 日本国（全国対象）追加 ---
    {
        "name": "事業承継・引継ぎ補助金（中小企業庁）",
        "url": "https://jigyou-shoukei.go.jp/",
        "region": "日本全国",
        "subject": "中小企業",
        "overview": "事業承継を契機とした経営革新や、M&Aによる経営資源の引き継ぎにかかる費用を補助。",
        "requirements": "中小企業・小規模事業者。"
    },
    {
        "name": "受給資格者創業支援事業（雇用保険・ハローワーク）",
        "url": "https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/koyou_roudou/koyou/shokugyoushoukai/index.html",
        "region": "日本全国",
        "subject": "個人",
        "overview": "雇用保険の受給資格者が自ら創業する場合の支援や給付金。",
        "requirements": "受給資格者。"
    },
    {
        "name": "ものづくりベンチャー育成支援事業（経済産業省）",
        "url": "https://www.meti.go.jp/policy/sangi/venture/index.html",
        "region": "日本全国",
        "subject": "中小企業",
        "overview": "ハードウェア系ベンチャーの試作品開発や事業化を支援。",
        "requirements": "中小企業・スタートアップ。"
    },
    {
        "name": "知財活用ベンチャー支援事業（INPIT）",
        "url": "https://www.inpit.go.jp/katsuyo/venture/index.html",
        "region": "日本全国",
        "subject": "中小企業",
        "overview": "スタートアップの知財戦略構築や特許調査、海外出願を支援。",
        "requirements": "スタートアップ・中小企業。"
    },
    {
        "name": "省エネルギー投資促進支援事業費補助金（環境共創イニシアチブ・SII）",
        "url": "https://sii.or.jp/shouene05/",
        "region": "日本全国",
        "subject": "中小企業",
        "overview": "工場や事業場における設備更新（高効率空調、ボイラー、LED等）による省エネ化を支援。",
        "requirements": "工場・事業場を有する法人・個人事業者。"
    },
    {
        "name": "商業・サービス競争力強化連携事業（中小機構）",
        "url": "https://www.smrj.go.jp/sme/funding/index.html",
        "region": "日本全国",
        "subject": "中小企業",
        "overview": "商店街や商業者が連携して行う消費喚起や新サービス開発を支援。",
        "requirements": "商業・サービス業の事業者グループ。"
    },
    {
        "name": "戦略的パートナーシップ構築推進事業（内閣府・経産省）",
        "url": "https://www.meti.go.jp/policy/s_kigyo/partner/index.html",
        "region": "日本全国",
        "subject": "中小企業",
        "overview": "大企業と中小企業の共存共栄を目指すパートナーシップ構築宣言の推進と、サプライチェーン全体の生産性向上を支援。",
        "requirements": "全事業者。"
    },
    {
        "name": "中小企業活性化協議会事業（中小機構）",
        "url": "https://www.smrj.go.jp/kasseika/index.html",
        "region": "日本全国",
        "subject": "中小企業",
        "overview": "収益力改善や事業再生、過剰債務の解消等に悩む中小企業の総合的な経営相談・支援。",
        "requirements": "中小企業者。"
    },
    {
        "name": "厚生労働省：両立支援等助成金（育児休業等支援コース）",
        "url": "https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/koyou_roudou/koyou/kyufukin/ryouritsu.html",
        "region": "日本全国",
        "subject": "中小企業",
        "overview": "労働者の育児休業取得や職場復帰を円滑に行うための取り組みを実施した事業主を助成。",
        "requirements": "雇用保険適用事業所の事業主。"
    },
    {
        "name": "独立行政法人中小企業基盤整備機構：J-GoodTech（ジェグテック）",
        "url": "https://jgoodtech.smrj.go.jp/",
        "region": "日本全国",
        "subject": "中小企業",
        "overview": "国内の優れた中小企業と大手企業・海外企業をつなぐビジネスマッチングサイトの運営と支援。",
        "requirements": "中小企業。"
    }
]

added_count = 0
new_list = []
for item in more_subsidies:
    if item["url"] not in existing_urls:
        existing_urls.add(item["url"])
        new_list.append(item)
        added_count += 1

print(f"Added {added_count} more subsidies.")

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

print(f"Total extracted URLs now: {len(existing_urls)}")
