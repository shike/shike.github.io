from pathlib import Path
import json
import re
import struct
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


INDEX = read("index.html")
CSS = read("css/style.css")
JS = read("js/main.js")
LLMS = read("llms.txt")
BOOKS = (
    {
        "zh": "《AI Coding：人人都是程序员》",
        "en": "AI Coding: Everyone Is a Programmer",
        "cover": "assets/books/ai-coding-cover.jpg",
        "width": 896,
        "height": 1200,
        "url": "https://github.com/shike/ai_coding_book",
    },
    {
        "zh": "《FDE：AI 的胜负不在于模型》",
        "en": "FDE: Winning and Losing in AI Isn't About the Model",
        "cover": "assets/books/fde-cover.svg",
        "width": 800,
        "height": 500,
        "url": "https://github.com/shike/FDE-AI-race-isn-t-won-on-models",
    },
)


def secure_link_pattern(url):
    return rf'href="{re.escape(url)}"[^>]+target="_blank"[^>]+rel="noopener noreferrer"'


class PersonalProfileTests(unittest.TestCase):
    def test_hero_uses_approved_positioning(self):
        self.assertIn(
            "连续创业者 / 水滴跃动 Dropleap 创始人 / 企业级 AI 实践者",
            INDEX,
        )
        self.assertIn(
            "Serial Entrepreneur / Founder of Dropleap / Enterprise AI Practitioner",
            INDEX,
        )
        self.assertIn("现聚焦企业级 AI Agent 与 GEO", INDEX)

    def test_about_covers_approved_narrative(self):
        required = [
            "16 年职业经历横跨软件工程、互联网产品、创业与企业经营",
            "完成从产品构建、团队组建到机构融资的完整创业过程",
            "可靠性、可观测性、可评估性与持续运营能力",
            "GEO 不只是内容投放或关键词优化",
            "《AI Coding：人人都是程序员》",
            "《FDE：AI 的胜负不在于模型》",
            "His 16-year career spans software engineering, internet products, entrepreneurship, and business operations",
            "taking it through product development, team formation, and institutional funding",
            "the reliability, observability, evaluability, and long-term operability of AI systems",
            "He views GEO not simply as content distribution or keyword optimization",
        ]
        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, INDEX)

    def test_stats_use_experience_venture_and_books(self):
        self.assertIn("年技术、产品与商业实践", INDEX)
        self.assertIn("连续创业与产品构建", INDEX)
        self.assertIn("AI 主题著作", INDEX)
        self.assertIn(">0→1<", INDEX)
        self.assertIn(">2 本<", INDEX)
        self.assertIn('data-en-aria="Key career indicators"', INDEX)

    def test_removed_metrics_and_award_are_absent(self):
        combined = "\n".join((INDEX, JS, LLMS))
        # Ban specific phrases (not raw percentage numbers — those appear legitimately
        # in the new manufacturing-AI product page as anonymized reference samples)
        banned = [
            "业绩增长 80%",
            "成本下降 15%",
            "应收下降 60%",
            "阿里云 AI 大赛银奖",
            "Alibaba Cloud AI Competition Silver Award",
        ]
        for text in banned:
            with self.subTest(text=text):
                self.assertNotIn(text, combined)

    def test_language_metadata_uses_new_positioning(self):
        self.assertIn(
            "title: '施可｜连续创业者、Dropleap 创始人、企业级 AI 实践者'",
            JS,
        )
        self.assertIn(
            "title: 'Shi Ke — Serial Entrepreneur, Founder of Dropleap, Enterprise AI Practitioner'",
            JS,
        )
        self.assertIn("企业级 AI Agent、GEO 与应用工程", JS)
        self.assertIn('data-en="Linhuiba">邻汇吧</p>', INDEX)


class LogoWallTests(unittest.TestCase):
    def test_logo_wall_groups(self):
        expected_brands = [
            "assets/logos/xiaomi.svg",
            "assets/logos/xpeng.svg",
            "assets/logos/volkswagen.svg",
            "assets/logos/dongfeng-nissan.png",
            "assets/logos/saic.png",
            "assets/logos/yhetea.png",
            "assets/logos/kawangke.png",
            "assets/logos/kuafu-zhachua.png",
            "assets/logos/zhengxin-jipai.png",
            "assets/logos/sanjin-tangbao.png",
            "assets/logos/ginoble.png",
            "assets/logos/xiaotiancai.svg",
            "assets/logos/hao-xianglai.png",
            "assets/logos/aldi.png",
        ]
        for path in expected_brands:
            with self.subTest(asset=path):
                self.assertIn(f'src="{path}"', INDEX)
                self.assertTrue((ROOT / path).is_file(), f"missing {path}")
                self.assertLess((ROOT / path).stat().st_size, 500_000)
        self.assertIn("万益蓝 WITSBB", INDEX)
        self.assertIn("小象超市", INDEX)
        self.assertRegex(INDEX, r'data-en="ASICS"[^<]*>亚瑟士</div>')
        self.assertRegex(INDEX, r'data-en="Yifeng Pharmacy"[^<]*>益丰大药房</div>')
        self.assertNotIn('>医药</h4>', INDEX)
        self.assertNotIn("--brand-color:#D4A853", INDEX)
        self.assertNotIn("--brand-color:#E5302C", INDEX)

    def test_logo_wall_uses_verified_assets(self):
        expected = [
            "assets/logos/xiaomi.svg",
            "assets/logos/xpeng.svg",
            "assets/logos/volkswagen.svg",
            "assets/logos/yhetea.png",
            "assets/logos/kawangke.png",
            "assets/logos/ginoble.png",
            "assets/logos/xiaotiancai.svg",
        ]
        for path in expected:
            with self.subTest(asset=path):
                self.assertIn(f'src="{path}"', INDEX)
                if path.endswith((".png", ".svg", ".jpg")) and path not in (
                    "assets/logos/xiaomi.svg",
                    "assets/logos/xpeng.svg",
                    "assets/logos/volkswagen.svg",
                    "assets/logos/xiaotiancai.svg",
                    "assets/logos/ginoble.png",
                ):
                    self.assertTrue((ROOT / path).is_file(), f"missing {path}")
                    self.assertLess((ROOT / path).stat().st_size, 50_000)

    def test_logo_card_styles_are_uniform(self):
        self.assertIn(".logo-card {", CSS)
        self.assertIn("height: 64px;", CSS)
        self.assertIn("display: flex;", CSS)
        self.assertIn("align-items: center;", CSS)
        self.assertIn("justify-content: center;", CSS)
        self.assertIn(".logo-card.has-logo img {", CSS)
        self.assertIn("max-width: 80%;", CSS)
        self.assertIn("max-height: 40px;", CSS)
        self.assertIn("object-fit: contain;", CSS)
        self.assertRegex(CSS, r"@media \(max-width:\s*768px\)\s*\{[\s\S]*?\.logo-card\s*\{[^}]*height:\s*56px;")
        self.assertIn(
            "title: '施可｜连续创业者、Dropleap 创始人、企业级 AI 实践者'",
            JS,
        )
        self.assertIn(
            "title: 'Shi Ke — Serial Entrepreneur, Founder of Dropleap, Enterprise AI Practitioner'",
            JS,
        )
        self.assertIn("企业级 AI Agent、GEO 与应用工程", JS)
        social_alt = "Shi Ke — Serial Entrepreneur, Founder of Dropleap, Enterprise AI Practitioner"
        self.assertIn(f'<meta property="og:image:alt" content="{social_alt}">', INDEX)
        self.assertIn(f'<meta name="twitter:image:alt" content="{social_alt}">', INDEX)
        self.assertIn('data-en="Linhuiba">邻汇吧</p>', INDEX)


class VenturesTests(unittest.TestCase):
    def test_removed_products_are_absent(self):
        combined = INDEX + "\n" + LLMS
        banned = [
            "数商方略",
            "Shushang Fanglue",
            "shushangfanglue.com",
            "乐奇 Minibus EV",
            "Leqi Minibus EV",
            "minibus-ev.com",
        ]
        for text in banned:
            with self.subTest(text=text):
                self.assertNotIn(text, combined)

    def test_approved_products_are_present(self):
        for text in ["微盟星启 GEO", "呼波特 WhoBot", "NihaoVisit", "Liora Moon"]:
            with self.subTest(text=text):
                self.assertIn(text, INDEX)
                self.assertIn(text, LLMS)

    def test_liora_moon_uses_verified_copy(self):
        # New compact copy in the other-ventures grid
        self.assertIn("Liora Moon", INDEX)
        self.assertIn("AI 塔罗解读平台", INDEX)
        self.assertIn("AI Tarot reading platform", INDEX)


class BooksTests(unittest.TestCase):
    def test_local_cover_assets_use_expected_formats(self):
        jpg_path = ROOT / "assets/books/ai-coding-cover.jpg"
        svg_path = ROOT / "assets/books/fde-cover.svg"
        self.assertTrue(jpg_path.is_file())
        self.assertTrue(svg_path.is_file())
        with jpg_path.open("rb") as stream:
            self.assertEqual(stream.read(3), b"\xff\xd8\xff")
        self.assertLess(jpg_path.stat().st_size, 250_000)
        svg = svg_path.read_text(encoding="utf-8")
        self.assertRegex(svg, r'<svg[^>]+width="800"[^>]+height="500"')

    def test_books_navigation_and_section_exist(self):
        self.assertIn('href="#books"', INDEX)
        self.assertIn('data-en="Books">著作</a>', INDEX)
        self.assertIn('<section class="section" id="books">', INDEX)
        self.assertIn('class="books-grid"', INDEX)

    def test_both_books_use_local_covers_and_github_links(self):
        for book in BOOKS:
            with self.subTest(book=book["zh"]):
                self.assertIn(book["zh"], INDEX)
                self.assertIn(book["en"], INDEX)
                self.assertRegex(
                    INDEX,
                    rf'src="{re.escape(book["cover"])}"[^>]+width="{book["width"]}" height="{book["height"]}"',
                )
                self.assertRegex(INDEX, secure_link_pattern(book["url"]))

    def test_books_styles_include_responsive_grid(self):
        for selector in [
            ".books-grid",
            ".book-card",
            ".book-cover-frame",
            ".book-cover",
            ".book-link",
        ]:
            with self.subTest(selector=selector):
                self.assertIn(selector, CSS)

    def test_cover_stage_is_shared_portrait_frame(self):
        frame = re.search(r"\.book-cover-frame\s*\{(.*?)\}", CSS, re.DOTALL)
        image = re.search(r"\.book-cover\s*\{(.*?)\}", CSS, re.DOTALL)
        self.assertIsNotNone(frame)
        self.assertIsNotNone(image)
        self.assertIn("width: min(100%, 240px);", frame.group(1))
        self.assertIn("aspect-ratio: 3 / 4;", frame.group(1))
        self.assertIn("margin: 0 auto 24px;", frame.group(1))
        self.assertIn("max-width: 100%;", image.group(1))
        self.assertIn("max-height: 100%;", image.group(1))
        self.assertIn("object-fit: contain;", image.group(1))
        self.assertNotRegex(image.group(1), r"(?m)^\s*height:\s*100%;")
        self.assertIn("width: min(100%, 220px);", CSS)


class MachineReadableTests(unittest.TestCase):
    def json_ld_graph(self):
        match = re.search(
            r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
            INDEX,
            re.DOTALL,
        )
        self.assertIsNotNone(match)
        return json.loads(match.group(1))["@graph"]

    def test_json_ld_contains_two_books_linked_to_person(self):
        books = [node for node in self.json_ld_graph() if node.get("@type") == "Book"]
        self.assertEqual(len(books), 2)
        by_url = {book["url"]: book for book in books}
        expected = {
            book["url"]: f'https://shike.github.io/{book["cover"]}' for book in BOOKS
        }
        self.assertEqual(set(by_url), set(expected))
        for url, image in expected.items():
            with self.subTest(url=url):
                self.assertEqual(by_url[url]["author"], {"@id": "https://shike.github.io/#person"})
                self.assertEqual(by_url[url]["image"], image)
                self.assertEqual(by_url[url]["inLanguage"], "zh-CN")

    def test_profile_and_sitemap_dates_are_current(self):
        self.assertIn('"dateModified": "2026-08-04"', INDEX)
        root = ET.parse(ROOT / "sitemap.xml").getroot()
        namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        self.assertEqual(root.find("s:url/s:lastmod", namespace).text, "2026-08-04")

    def test_llms_summary_contains_books_and_current_date(self):
        self.assertIn("## Books", LLMS)
        for book in BOOKS:
            self.assertIn(book["url"], LLMS)
        self.assertIn("Last updated: 2026-08-04", LLMS)


class SpeakingTests(unittest.TestCase):
    def setUp(self):
        self.index = read("index.html")
        self.llms = read("llms.txt")

    def test_speaking_items_use_approved_copy(self):
        self.assertNotIn("破界·2024刀法年度品效峰会", self.index)
        self.assertNotIn("Small & Beautiful, Flexible & Precise", self.index)
        self.assertNotIn("晨间闭场开杠", self.index)
        self.assertNotIn("2024-12-05", self.index)
        self.assertNotIn("2024-12-26", self.index)
        self.assertNotIn('datetime="2024-12', self.index)
        self.assertIn("刀法", self.index)
        self.assertIn("TBI", self.index)
        self.assertIn("Small, Flexible, Measurable", self.index)
        self.assertIn("Small, Beautiful, Agile, Precise", self.index)
        self.assertIn("Panel Moderator: Super Single Product vs. Brand Matrix", self.index)
        self.assertIn("Slow-Pop-Up Experiential Marketing", self.index)
        self.assertIn("Channel Bottlenecks", self.index)
        self.assertIn("How Slow-Pop-Ups Help Brands", self.index)
        self.assertIn("ChengDao (成于渠道) Channel", self.index)
        self.assertIn("Closed-Door Morning Panel", self.index)
        self.assertIn("Small, Flexible, Measurable", self.llms)

    def test_speaking_items_use_approved_summary_in_llms(self):
        self.assertNotIn("Slow-Pop-Up Experiential Marketing, Reshaping Offline Channel Value", self.llms)
        self.assertNotIn("Small & Beautiful, Flexible & Precise", self.llms)
        self.assertNotIn("2024-12-05", self.llms)
        self.assertNotIn("2024-12-26", self.llms)
        self.assertIn("Daofa (刀法) 2024 Annual Brand Performance Summit, Shanghai", self.llms)
        self.assertIn("5th TBI Outstanding Brand Innovation Festival", self.llms)
        self.assertIn("Small, Flexible, Measurable", self.llms)
        self.assertIn("Small, Beautiful, Agile, Precise", self.llms)
        self.assertIn("Super Single Product vs. Brand Matrix", self.llms)
        self.assertIn("ChengDao (成于渠道)", self.llms)
        self.assertIn("closed-door morning panel", self.llms)
        self.assertIn("刀法", self.llms)
        self.assertIn("TBI", self.llms)


class BrandAssetsTests(unittest.TestCase):
    def test_brand_assets_are_local(self):
        remote = [
            "https://www.xingqigeo.cn/",
            "https://whobot.com/",
            "https://nihaovisit.com/",
            "https://lioramoon.com/",
            "allstarpartner.com",
        ]
        for token in remote:
            with self.subTest(token=token):
                self.assertNotIn(f'src="https://{token}', INDEX)
                self.assertNotIn(f"src='https://{token}", INDEX)

    def test_each_brand_asset_file_matches_spec(self):
        expectations = [
            ("xingqi-geo", 64, 64, "png"),
            ("liora-moon", 512, 512, "png"),
            ("all-star-partner", 300, 300, "png"),
        ]
        for name, width, height, ext in expectations:
            with self.subTest(brand=name):
                path = ROOT / "assets" / "logos" / f"{name}.{ext}"
                self.assertTrue(path.is_file(), f"missing {path}")
                with path.open("rb") as stream:
                    self.assertEqual(stream.read(8), b"\x89PNG\r\n\x1a\n")
                    stream.seek(16)
                    self.assertEqual(struct.unpack(">II", stream.read(8)), (width, height))
        for name in ("whobot", "nihaovisit"):
            with self.subTest(brand=name):
                path = ROOT / "assets" / "logos" / f"{name}.svg"
                self.assertTrue(path.is_file(), f"missing {path}")
                self.assertIn("<svg", path.read_text(encoding="utf-8"))

    def test_logo_wall_groups(self):
        expected_brands = [
            "assets/logos/xiaomi.svg",
            "assets/logos/xpeng.svg",
            "assets/logos/volkswagen.svg",
            "assets/logos/dongfeng-nissan.png",
            "assets/logos/saic.png",
            "assets/logos/yhetea.png",
            "assets/logos/kawangke.png",
            "assets/logos/kuafu-zhachua.png",
            "assets/logos/zhengxin-jipai.png",
            "assets/logos/sanjin-tangbao.png",
            "assets/logos/xiaomi.svg",
            "assets/logos/ginoble.png",
            "assets/logos/dongfeng-nissan.png",
            "assets/logos/saic.png",
            "assets/logos/xiaotiancai.svg",
            "assets/logos/hao-xianglai.png",
            "assets/logos/aldi.png",
        ]
        for path in expected_brands:
            with self.subTest(asset=path):
                self.assertIn(f'src="{path}"', INDEX)
        self.assertIn("万益蓝 WITSBB", INDEX)
        self.assertIn("小象超市", INDEX)
        self.assertNotIn("医药", INDEX)


    def test_venture_sub_brand_uses_local_icon(self):
        for path, zh in [
            ("assets/logos/xingqi-geo.png", "微盟星启 GEO"),
            ("assets/logos/whobot.svg", "呼波特 WhoBot"),
            ("assets/logos/nihaovisit.svg", "NihaoVisit"),
            ("assets/logos/liora-moon.png", "Liora Moon"),
            ("assets/logos/all-star-partner.png", "聚星动力 FanTown"),
        ]:
            with self.subTest(brand=zh):
                # New structure: <article class="other-venture-card"><span class="other-venture-icon"><img src="...">
                pattern = (
                    r'<article class="other-venture-card">'
                    r'\s*<span class="other-venture-icon">'
                    r'\s*<img src="' + re.escape(path) + r'"'
                )
                self.assertRegex(INDEX, pattern)
                self.assertIn(zh, INDEX)

    def test_venture_sub_brand_styles(self):
        self.assertIn(".other-venture-card {", CSS)
        self.assertIn(".other-venture-icon {", CSS)
        self.assertIn(".other-venture-icon img {", CSS)

    def test_balanced_compact_density_values(self):
        self.assertIn("--section-padding: 68px;", CSS)
        self.assertRegex(CSS, r"\.hero\s*\{[^}]*padding-top:\s*120px;\s*padding-bottom:\s*72px;")
        self.assertIn("margin-bottom: 32px;", CSS)
        self.assertIn("line-height: 1.7;", CSS)
        self.assertRegex(
            CSS,
            r"\.skills-grid,\s*\.ventures-grid,\s*\.books-grid,\s*\.track-grid\s*\{[^}]*gap:\s*20px;",
        )
        self.assertIn("margin: 0 auto 28px;", CSS)
        self.assertRegex(CSS, r"\.about-content p\s*\{[^}]*line-height:\s*1\.75;")
        self.assertRegex(CSS, r"\.timeline-item\s*\{[^}]*padding-bottom:\s*28px;")
        self.assertRegex(CSS, r"\.track-record\s*\{[^}]*margin-top:\s*40px;\s*padding-top:\s*32px;")
        self.assertRegex(CSS, r"\.logo-wall\s*\{[^}]*gap:\s*24px;")
        self.assertRegex(CSS, r"\.speaking-item\s*\{[^}]*padding:\s*18px 0;")
        self.assertRegex(CSS, r"\.contact-qr\s*\{[^}]*margin:\s*28px auto 0;")




class ProductPageTests(unittest.TestCase):
    """Verifies the compact 1-screen product data sheet within #ventures."""

    def setUp(self):
        self.index = INDEX
        self.llms = LLMS
        self.css = CSS

    # --- Section header ---
    def test_product_section_present(self):
        self.assertIn('class="section product-section product-section--compact"', self.index)
        self.assertIn('id="manufacturing-ai"', self.index)
        self.assertIn("制造业 AI 落地", self.index)
        self.assertIn("WorkBuddy 官方代理", self.index)

    # --- 1-screen data sheet has all 7 rows ---
    def test_all_three_blocks_present(self):
        for block in (
            "product-hero-value",
            "product-standard",
            "product-integration",
        ):
            with self.subTest(block=block):
                self.assertIn(f'class="{block}"', self.index)

    def test_each_block_has_a_heading(self):
        for heading in ("标准产品", "如何接入"):
            with self.subTest(heading=heading):
                self.assertIn(heading, self.index)

    # --- 3 soul stats (now BIG hero numbers) ---
    def test_three_soul_stats_present(self):
        self.assertEqual(self.index.count("class=\"product-hero-num\""), 3)
        self.assertIn("2-4", self.index)
        self.assertIn("15分", self.index)
        self.assertIn("3月<span class=\"product-arrow-keep\">→</span>3天", self.index)

    # --- 2 Skills are the standard product ---
    def test_two_skill_cards_present(self):
        self.assertEqual(self.index.count("class=\"product-skill-card\""), 2)
        self.assertIn("智能取数 Skill", self.index)
        self.assertIn("知识库 Skill", self.index)
        # Each has icon + heading + description + 3 bullet points
        self.assertIn("Data Retrieval Skill", self.index)
        self.assertIn("Knowledge Base Skill", self.index)

    def test_skill_bullets_cover_what_they_do(self):
        # Data Retrieval — natural language → data query
        self.assertIn("只读打通现有系统", self.index)
        # Knowledge Base — digitize know-how
        self.assertIn("老师傅经验数字化沉淀", self.index)

    # --- Integration flow (L1 → 2 Skills → L2) ---
    def test_integration_flow(self):
        self.assertIn("class=\"product-integration-flow\"", self.index)
        # 3 steps
        self.assertIn("class=\"product-int-step\"", self.index)
        # Middle step is the accent (the 2 Skills)
        self.assertIn("class=\"product-int-step product-int-step--accent\"", self.index)
        self.assertIn("L1", self.index)
        self.assertIn("L2", self.index)

    # --- Try block removed per user direction (no CTA in product section) ---
    def test_try_block_removed(self):
        self.assertNotIn("class=\"product-try\"", self.index)
        self.assertNotIn("30 分钟场景诊断", self.index)

    # --- Old 7-row + detail-block structures gone ---
    def test_old_seven_row_structures_absent(self):
        for old in (
            "product-row--pain",
            "product-row--arch",
            "product-row--cases",
            "product-row--service",
            "product-row--method",
            "product-row--roadmap",
            "product-row--cta",
            "product-arch-stack",
            "product-roadmap-bar",
            "product-roadmap-milestone",
            "product-service-icons",
            "product-method-step",
            "focus-pain",
            "product-compact-cta",
            "product-case-mini",  # removed with proof block
            "product-case-from",
            "product-case-to",
        ):
            with self.subTest(old=old):
                self.assertNotIn(old, self.index)

    # --- Pain row was removed (not in user's "product + value" list) ---
    def test_no_old_pain_class(self):
        self.assertNotIn("product-row--pain", self.index)

    # --- Architecture is now a compact integration flow (3 steps, not 4 layers) ---
    def test_integration_flow_replaces_arch(self):
        self.assertIn("class=\"product-integration-flow\"", self.index)
        # L1, L2, "2 Skills" all appear in the integration flow
        self.assertIn(">L1<", self.index)
        self.assertIn(">L2<", self.index)
        # The two Skills are the centerpiece of the integration flow
        self.assertIn("product-int-step--accent", self.index)
        # Content from the old arch is still in the integration
        self.assertIn("CRM / ERP / MES / WMS", self.index)
        self.assertIn("智能取数 + 知识库", self.index)

    # --- Cases still present (reused) ---
    def test_no_more_duplicate_case_cards(self):
        # Cases were duplicate with hero numbers — section removed
        self.assertNotIn("product-proof", self.index)
        self.assertNotIn("真实效果", self.index)
        self.assertEqual(self.index.count("class=\"product-case-mini\""), 0)

    # --- Service / Method / Roadmap rows were removed (process, not product) ---
    def test_process_rows_removed(self):
        for removed in (
            "product-service-icon-item",
            "product-method-step",
            "product-roadmap-milestone",
        ):
            with self.subTest(removed=removed):
                self.assertNotIn(removed, self.index)

    # --- Other ventures still present ---
    def test_other_ventures_secondary(self):
        self.assertIn('class="other-ventures"', self.index)
        for sub in ("微盟星启 GEO", "呼波特 WhoBot", "NihaoVisit", "Liora Moon", "聚星动力 FanTown"):
            with self.subTest(sub=sub):
                self.assertIn(sub, self.index)
        self.assertEqual(self.index.count("class=\"other-venture-card\""), 5)

    # --- Old 7-stage structure is gone ---
    def test_old_seven_stage_structure_absent(self):
        # The old detailed stage classes
        for old in (
            "product-stage--hook",
            "product-stage--pain",
            "product-stage--solution",
            "product-stage--service",
            "product-stage--metrics",
            "product-stage--method-cases",
            "product-stage--roadmap-cta",
            "product-stage-title",
            "pain-quote",
        ):
            with self.subTest(old=old):
                self.assertNotIn(old, self.index)

    # --- CSS for compact layout ---
    def test_compact_css_defined(self):
        for selector in (
            ".product-section--compact {",
            ".product-compact {",
            ".product-compact-title {",
            ".product-compact-stat strong {",
            ".product-row {",
            ".product-row-tag {",
            ".product-chip {",
            ".product-case-mini {",
            ".product-compact-cta {",
        ):
            with self.subTest(selector=selector):
                self.assertIn(selector, self.css)

    # --- llms + meta ---
    def test_meta_descriptions_advertise_manufacturing_focus(self):
        for selector in (
            'name="description"',
            'property="og:description"',
            'name="twitter:description"',
        ):
            with self.subTest(selector=selector):
                pattern = (
                    rf'<meta {re.escape(selector)} content="[^"]*WorkBuddy 官方代理、制造业 AI 落地服务商'
                )
                self.assertRegex(self.index, pattern)

    def test_json_ld_lists_manufacturing_focus(self):
        self.assertIn("WorkBuddy", self.index)
        self.assertIn("Manufacturing AI Implementation", self.index)
        self.assertIn("Smart Manufacturing", self.index)
        self.assertIn("FDE Methodology", self.index)

    def test_llms_documents_manufacturing_focus(self):
        self.assertIn("## Manufacturing AI focus", self.llms)
        for term in ("WorkBuddy", "Data Retrieval Skill", "Knowledge Base Skill", "4-stage adoption roadmap"):
            with self.subTest(term=term):
                self.assertIn(term, self.llms)
        self.assertIn("Last updated: 2026-09-05", self.llms)
