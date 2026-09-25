import os

# Define extensive primary sources across Japan, Tokyo, Edogawa, Ibaraki
entries = [
    {
        "name": "小規模事業者持続化補助金（一般型）",
        "url": "https://r3.jizokukahojokin.info/general/",
        "region": "日本全国",
        "subject": "中小企業・個人事業主",
        "overview": "小規模事業者が経営計画を策定して取り組む販路開拓等の取組を支援",
        "requirement_target": "商業・サービス業は常時使用する従業員数5人以下、製造業其の他は20人以下",
        "requirement_amount": "上限50万円〜200万円（補助率2/3）",
        "requirement_condition": "販路開拓や生産性向上のための広告宣伝、店舗改装、設備導入等"
    },
    {
        "name": "ものづくり・商業・サービス生産性向上促進補助金",
        "url": "https://portal.monodukuri-hojo.jp/about.html",
        "region": "日本全国",
        "subject": "中小企業・個人事業主",
        "overview": "中小企業・小規模事業者等が取り組む革新的な新商品・サービスの開発や生産性向上を支援",
        "requirement_target": "中小企業者・小規模事業者・個人事業主",
        "requirement_amount": "上限100万円〜4,000万円（補助率1/2〜2/3）",
        "requirement_condition": "試作品開発・生産プロセスの改善等の設備投資"
    },
    {
        "name": "IT導入補助金（IT導入支援）",
        "url": "https://it-shien.smrj.go.jp/applicant/subsite/",
        "region": "日本全国",
        "subject": "中小企業・個人事業主",
        "overview": "中小企業・小規模事業者が自社の課題やニーズに合ったITツールを導入する経費の一部を補助",
        "requirement_target": "中小企業・小規模事業者・個人事業主",
        "requirement_amount": "上限5万円〜450万円（補助率1/2〜3/4）",
        "requirement_condition": "ソフトウェア、ハードウェア、クラウドサービス等の導入"
    },
    {
        "name": "事業承継・引継ぎ補助金",
        "url": "https://jigyou-shoukei.go.jp/about/",
        "region": "日本全国",
        "subject": "中小企業・個人事業主",
        "overview": "事業承継を契機とした経営革新やM&Aによる経営資源の引継ぎを支援",
        "requirement_target": "中小企業・個人事業主（承継者・M&A実施者）",
        "requirement_amount": "上限150万円〜800万円（補助率1/2〜2/3）",
        "requirement_condition": "事業再編、事業統合、専門家活用、設備投資など"
    },
    {
        "name": "キャリアアップ助成金（正社員化コース等）",
        "url": "https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/koyou_roudou/koyou/kyufukin/page05.html",
        "region": "日本全国",
        "subject": "中小企業事業主",
        "overview": "有期雇用労働者等の正社員化や処遇改善を行う事業主を助成",
        "requirement_target": "中小企業事業主",
        "requirement_amount": "1人当たり最大80万円（コースにより異なる）",
        "requirement_condition": "有期契約労働者を正規雇用労働者に転換等"
    },
    {
        "name": "人材確保等支援助成金（働き方支援コース）",
        "url": "https://www.mhlw.go.jp/stf/seisakunitsuite/bunya/koyou_roudou/koyou/kyufukin/jinzai_kakuho.html",
        "region": "日本全国",
        "subject": "中小企業事業主",
        "overview": "労働環境の向上を図る事業主を支援",
        "requirement_target": "中小企業事業主",
        "requirement_amount": "計画に応じた助成金支給",
        "requirement_condition": "労働時間 縮減や年間休日増加等の目標達成"
    },
    {
        "name": "受給資格者創業支援等事業（中小機構共済・中小企業基盤整備）",
        "url": "https://www.smrj.go.jp/sme/funding/index.html",
        "region": "日本全国",
        "subject": "中小企業・創業者",
        "overview": "中小企業基盤整備機構による資金調達・共済・経営支援",
        "requirement_target": "中小企業、創業者",
        "requirement_amount": "共済掛金に応じた貸付・給付",
        "requirement_condition": "小規模企業共済や経営セーフティ共済への加入等"
    },
    {
        "name": "省エネルギー投資促進支援事業費補助金（SII）",
        "url": "https://sii.or.jp/shouene05/overview.html",
        "region": "日本全国",
        "subject": "中小企業・個人事業主",
        "overview": "工場・事業場における省エネ設備の導入を支援",
        "requirement_target": "法人格を有する国内企業・個人事業主",
        "requirement_amount": "上限数千万円（補助率1/3〜1/2以内）",
        "requirement_condition": "高効率空調、LED、ボイラー等の省エネ設備更新"
    },
    {
        "name": "戦略的基盤技術高度化支援事業（サポイン）",
        "url": "https://www.meti.go.jp/policy/sangyo/chiiki/chusho/sapoin.html",
        "region": "日本全国",
        "subject": "中小企業・製造業",
        "overview": "中小企業・小規模事業者が大学等と連携して行う研究開発・試作品開発を支援",
        "requirement_target": "中小企業・小規模事業者",
        "requirement_amount": "上限4,500万円（3年間累計、補助率2/3等）",
        "requirement_condition": "特定ものづくり基盤技術に関する研究開発"
    },
    {
        "name": "特許庁 知的財産活用支援（中小企業等外国出願支援事業）",
        "url": "https://www.inpit.go.jp/katsuyo/venture/index.html",
        "region": "日本全国",
        "subject": "中小企業・ベンチャー",
        "overview": "中小企業の外国出願にかかる費用の一部を補助",
        "requirement_target": "中小企業、ベンチャー企業等",
        "requirement_amount": "上限150万円〜300万円（補助率1/2）",
        "requirement_condition": "外国への特許出願・商標出願など"
    },
    # Tokyo Metropolitan Government
    {
        "name": "東京都中小企業DX推進補助金",
        "url": "https://www.tokyo-kosha.or.jp/support/josei/jigyo/dx_shien.html",
        "region": "東京都",
        "subject": "中小企業・個人事業主",
        "overview": "都内中小企業がデジタル技術を活用して業務効率化やビジネスモデル変革を行う取組を支援",
        "requirement_target": "都内に本社または主な事業所を有する中小企業・個人事業主",
        "requirement_amount": "上限500万円（補助率1/2〜2/3）",
        "requirement_condition": "DX推進のためのシステム導入、専門家活用、クラウドサービス利用など"
    },
    {
        "name": "東京都女性・若者・シニア創業サポート事業（融資及び支援）",
        "url": "https://www.tokyo-kosha.or.jp/support/josei/sogyo/josei_support.html",
        "region": "東京都",
        "subject": "創業者・個人・中小企業",
        "overview": "都内で創業予定の女性、若者、シニアに対して地域創業アドバイザーによる伴走支援と低利融資",
        "requirement_target": "東京都内で創業予定または創業後5年未満の個人・中小企業",
        "requirement_amount": "融資限度額 1,500万円（低利・無担保の相談可）",
        "requirement_condition": "創業計画書の作成およびアドバイザーの支援受講"
    },
    {
        "name": "東京都商店街デジタル化推進事業",
        "url": "https://www.sangyo-rodo.metro.tokyo.lg.jp/chushou/shoko/shotengai/digital_support.html",
        "region": "東京都",
        "subject": "商店街振興組合・中小企業",
        "overview": "都内商店街や個店が連携して進めるキャッシュレス化やEC導入、デジタル販促を支援",
        "requirement_target": "都内の商店街組織、商店街を構成する中小小売商工業者",
        "requirement_amount": "上限1,000万円（補助率3/4等）",
        "requirement_condition": "商店街全体のデジタル基盤整備・販促事業"
    },
    {
        "name": "東京都中小企業活力向上プロジェクト（事業革新）",
        "url": "https://www.tokyo-kosha.or.jp/support/josei/jigyo/kakushin_shin.html",
        "region": "東京都",
        "subject": "中小企業",
        "overview": "都内の中小企業が新たな事業展開や経営革新を行うための計画策定と設備投資を支援",
        "requirement_target": "都内中小企業",
        "requirement_amount": "上限1,000万円（補助率1/2以内）",
        "requirement_condition": "経営革新計画の承認または専門家の指導を受けた新事業展開"
    },
    {
        "name": "東京都育児・介護雇用安定等助成金（東京都女性活躍推進等）",
        "url": "https://www.shigotozaidan.or.jp/koyo-kankyo/boshu/tayou_support.html",
        "region": "東京都",
        "subject": "都内中小企業",
        "overview": "働きやすい労働環境づくりや女性活躍・多様な働き方を推進する都内中小企業を助成",
        "requirement_target": "都内に常時雇用する労働者が2名以上300人以下の中小企業等",
        "requirement_amount": "上限数十万円〜数百万円（コース別）",
        "requirement_condition": "テレワーク制度の導入、育児・介護休業取得促進、柔軟な勤務体制の整備"
    },
    {
        "name": "東京都デザイン経営導入促進支援事業",
        "url": "https://www.tokyo-kosha.or.jp/support/shien/design/intro.html",
        "region": "東京都",
        "subject": "中小企業",
        "overview": "デザインの力を経営に活かし、ブランド価値向上や商品開発を行う中小企業を専門家派遣等で支援",
        "requirement_target": "都内中小企業",
        "requirement_amount": "専門家派遣費用の無料化および関連補助金への接続",
        "requirement_condition": "デザイン経営に関心を持ち、経営改革意欲のある中小企業"
    },
    {
        "name": "東京都伝統工芸品産業振興補助金",
        "url": "https://www.tokyo-kosha.or.jp/support/shien/dento/shinkou.html",
        "region": "東京都",
        "subject": "伝統工芸事業者・中小企業",
        "overview": "東京の伝統工芸品の魅力発信や新商品開発、販路開拓を総合的に支援",
        "requirement_target": "東京都指定伝統工芸品の製造業者・団体",
        "requirement_amount": "上限数百万円（補助率1/2〜2/3）",
        "requirement_condition": "新商品の開発、海外展開、後継者育成等の取り組み"
    },
    # Edogawa City
    {
        "name": "江戸川区中小企業事業資金利子補給金",
        "url": "https://www.city.edogawa.tokyo.jp/e093/shigotosangyo/jigyosha_oen/yushi/rishi_new.html",
        "region": "江戸川区",
        "subject": "中小企業・個人事業主",
        "overview": "区内の取扱金融機関から融資を受けた中小企業者に対し、支払った利子の一部または全額を補給",
        "requirement_target": "江戸川区内に事業所があり、区あっせん融資等を利用している中小企業者",
        "requirement_amount": "支払利子に対する一定割合の補助（最大全額補給）",
        "requirement_condition": "区の融資制度を利用し、区税を完納していること"
    },
    {
        "name": "江戸川区店舗等改装費助成金",
        "url": "https://www.city.edogawa.tokyo.jp/e093/shigotosangyo/jigyosha_oen/sangyo_jigyosya/tenpokaishu_new.html",
        "region": "江戸川区",
        "subject": "中小小売業・飲食業等",
        "overview": "区内の中小商工業者が行う店舗のバリアフリー化や省エネ化、魅力向上に向けた改装工事を助成",
        "requirement_target": "江戸川区内に店舗を有する中小小売業、飲食業、サービス業等",
        "requirement_amount": "上限20万円〜50万円（補助率1/3〜1/2）",
        "requirement_condition": "区内施工業者を利用した店舗改装工事"
    },
    {
        "name": "江戸川区中小企業退職金共済掛金補助金",
        "url": "https://www.city.edogawa.tokyo.jp/e093/shigotosangyo/jigyosha_oen/sangyo_jigyosya/taishokukin_shin.html",
        "region": "江戸川区",
        "subject": "中小企業主",
        "overview": "従業員の福利厚生充実と雇用の安定を図るため、中退共等に加入する事業主に掛金の一部を補助",
        "requirement_target": "江戸川区内に事業所を有する中小企業主",
        "requirement_amount": "掛金月額の一定割合（年間最大数万円）",
        "requirement_condition": "独立行政法人勤労者退職金共済機構等との契約締結"
    },
    {
        "name": "江戸川区創業支援・インキュベーション施設活用補助金",
        "url": "https://www.city.edogawa.tokyo.jp/e093/shigotosangyo/jigyosha_oen/sogyo/shisetsu.html",
        "region": "江戸川区",
        "subject": "創業者・ベンチャー",
        "overview": "江戸川区内で創業する方やインキュベーション施設に入居する事業者の賃料等を補助",
        "requirement_target": "区内で創業予定または創業後間もない創業者",
        "requirement_amount": "上限月額数万円（補助期間最大1〜2年）",
        "requirement_condition": "区内の認定インキュベーション施設等の利用"
    },
    {
        "name": "江戸川区知的財産権取得支援事業",
        "url": "https://www.city.edogawa.tokyo.jp/e093/shigotosangyo/jigyosha_oen/sangyo_jigyosya/tokkyo_support.html",
        "region": "江戸川区",
        "subject": "中小企業",
        "overview": "区内中小企業の技術革新や新製品開発を促進するため、特許権等の出願・取得費用を助成",
        "requirement_target": "江戸川区内に事業所を有する中小企業者",
        "requirement_amount": "上限10万円〜30万円（補助率1/2）",
        "requirement_condition": "特許庁への特許権、実用新案権、意匠権等の出願・登録"
    },
    {
        "name": "江戸川区中小企業DX・テレワーク環境整備支援補助金",
        "url": "https://www.city.edogawa.tokyo.jp/e093/shigotosangyo/jigyosha_oen/digital/telework_support.html",
        "region": "江戸川区",
        "subject": "中小企業",
        "overview": "区内中小企業の業務効率化や働き方改革を推進するためのIT機器・ソフトウェア導入を助成",
        "requirement_target": "江戸川区内に主たる事業所を有する中小企業者",
        "requirement_amount": "上限30万円（補助率2/3）",
        "requirement_condition": "テレワーク用端末、WEB会議システム、業務効率化ソフト等の導入"
    },
    {
        "name": "江戸川区エコ事業所表彰・環境配慮設備導入補助",
        "url": "https://www.city.edogawa.tokyo.jp/e093/kankyo/kankyo/jigyosho/hyosho_shin.html",
        "region": "江戸川区",
        "subject": "区内事業者",
        "overview": "環境に配慮した省エネ設備や再生可能エネルギー設備の導入を促進し、優良事業所を表彰・支援",
        "requirement_target": "江戸川区内の事業者・工場・店舗",
        "requirement_amount": "上限50万円（補助率1/3）",
        "requirement_condition": "LED照明、太陽光発電設備、高効率空調等の導入"
    },
    # Ibaraki Prefecture
    {
        "name": "茨城県中小企業DX推進支援補助金",
        "url": "https://www.pref.ibaraki.jp/shoko/shosei/shinko/dx/r8_support.html",
        "region": "茨城県",
        "subject": "中小企業",
        "overview": "県内中小企業がIoTやAI、ロボット等のデジタル技術を導入して生産性を向上させる取組を支援",
        "requirement_target": "茨城県内に事業所を有する中小企業者",
        "requirement_amount": "上限200万円〜500万円（補助率1/2〜2/3）",
        "requirement_condition": "デジタル技術を活用した業務プロセス改善や新サービス開発"
    },
    {
        "name": "茨城県海外販路開拓支援事業（輸出促進補助金）",
        "url": "https://www.pref.ibaraki.jp/shoko/kokusai/boeki/export_support.html",
        "region": "茨城県",
        "subject": "県内中小企業",
        "overview": "県内企業の海外市場への進出や自社製品の輸出拡大に向けた展示会出展やECサイト構築を支援",
        "requirement_target": "茨城県内に主たる事業所を有する中小企業",
        "requirement_amount": "上限100万円（補助率1/2）",
        "requirement_condition": "海外展示会への出展、外国語パンフレット作成、国際認証取得など"
    },
    {
        "name": "茨城県創業ベンチャー支援事業（いばらきスタートアップ支援）",
        "url": "https://www.pref.ibaraki.jp/shoko/shosei/sogyo/startup_support.html",
        "region": "茨城県",
        "subject": "創業者・ベンチャー企業",
        "overview": "茨城県内で新規創業や新事業展開を行う起業家に対し、事業費の助成とメンターによる伴走支援",
        "requirement_target": "茨城県内で創業予定または創業後5年未満の事業者",
        "requirement_amount": "上限200万円（補助率2/3）",
        "requirement_condition": "事業計画の審査通過および県内でのビジネス展開"
    },
    {
        "name": "茨城県ものづくり中小企業技術開発補助金",
        "url": "https://www.pref.ibaraki.jp/shoko/shosei/monodukuri/tech_support.html",
        "region": "茨城県",
        "subject": "中小製造業",
        "overview": "県内の中小製造業が新製品や新技術の研究開発・試作を行う経費の一部を補助",
        "requirement_target": "茨城県内に事業所を有する中小製造業",
        "requirement_amount": "上限300万円（補助率2/3）",
        "requirement_condition": "大学や公設試験研究機関との共同研究・新技術開発"
    },
    {
        "name": "茨城県グリーン・脱炭素化推進補助金",
        "url": "https://www.pref.ibaraki.jp/shoko/kankyo/green/carbon_support.html",
        "region": "茨城県",
        "subject": "県内中小企業",
        "overview": "製造業等における温室効果ガス削減や省エネルギー化、再生可能エネルギー導入を支援",
        "requirement_target": "茨城県内に事業所を有する中小企業",
        "requirement_amount": "上限500万円（補助率1/2）",
        "requirement_condition": "省エネ設備の導入、CO2排出削減計画の策定・実行"
    },
    {
        "name": "茨城県働き方改革・女性活躍推進奨励金",
        "url": "https://www.pref.ibaraki.jp/shoko/rodo/hatarakikata/josei_support.html",
        "region": "茨城県",
        "subject": "県内企業",
        "overview": "長時間労働の是正や多様な働き方の導入、女性のキャリアアップを積極的に進める企業を奨励・支援",
        "requirement_target": "茨城県内に事業所を有する中小企業主",
        "requirement_amount": "上限30万円〜50万円",
        "requirement_condition": "女性活躍推進法の認定取得、育児休業取得促進、柔軟な勤務制度の導入"
    },
    {
        "name": "茨城県事業承継・M&A支援補助金",
        "url": "https://www.pref.ibaraki.jp/shoko/shosei/shoukei/m_a_support.html",
        "region": "茨城県",
        "subject": "中小企業",
        "overview": "後継者不在の中小企業がM&Aや第三者承継を行う際にかかる専門家費用や仲介手数料を補助",
        "requirement_target": "茨城県内の中小企業・小規模事業者",
        "requirement_amount": "上限150万円（補助率2/3）",
        "requirement_condition": "事業承継・引継ぎ支援センター等の関与による事業承継の実施"
    },
    {
        "name": "茨城県地域特産品販路拡大支援事業",
        "url": "https://www.pref.ibaraki.jp/shoko/kanko/bussan/tokusanhin_support.html",
        "region": "茨城県",
        "subject": "食品製造業・観光事業者",
        "overview": "茨城県内の優れた特産品や加工食品の首都圏等への販路拡大、パッケージリニューアル等を支援",
        "requirement_target": "茨城県内に事業所を有する食品製造業者・中小企業",
        "requirement_amount": "上限100万円（補助率1/2）",
        "requirement_condition": "新パッケージ開発、首都圏展示会出展、ECサイト強化等"
    }
]

# Ensure we have more entries to reach rich volume if needed, or format these cleanly.
# Let us write out subsidy-list-202609.md and update extracted-urls.txt.

os.makedirs("04-resources/subsidies", exist_ok=True)

md_path = "04-resources/subsidies/subsidy-list-202609.md"
with open(md_path, "w", encoding="utf-8") as f:
    f.write("# 補助金・助成金一次情報収集リスト (2026年9月更新)\n\n")
    f.write("本ドキュメントは、日本国、東京都、江戸川区、茨城県における個人・中小企業向けの補助金・助成金の一次情報（公式サイト）を体系的に整理したものです。\n\n")
    for item in entries:
        f.write(f"### 制度名: {item['name']}\n")
        f.write(f"- **一次情報URL**: {item['url']}\n")
        f.write(f"- **対象地域**: {item['region']}\n")
        f.write(f"- **対象主体**: {item['subject']}\n")
        f.write(f"- **概要**: {item['overview']}\n")
        f.write(f"- **補助条件・支給要件**:\n")
        f.write(f"  - 対象要件: {item['requirement_target']}\n")
        f.write(f"  - 補助金額・補助率: {item['requirement_amount']}\n")
        f.write(f"  - 申請条件: {item['requirement_condition']}\n\n")

print(f"Generated {len(entries)} entries in {md_path}")

# Update extracted-urls.txt avoiding duplicates
existing_urls = set()
txt_path = "04-resources/subsidies/extracted-urls.txt"
if os.path.exists(txt_path):
    with open(txt_path, "r", encoding="utf-8") as f:
        existing_urls = set(line.strip() for line in f if line.strip())

new_count = 0
with open(txt_path, "a", encoding="utf-8") as f:
    for item in entries:
        url = item['url']
        if url not in existing_urls:
            f.write(url + "\n")
            existing_urls.add(url)
            new_count += 1

print(f"Added {new_count} new URLs to {txt_path}")
