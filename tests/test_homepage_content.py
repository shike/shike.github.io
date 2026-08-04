from pathlib import Path
import json
import re
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
        "zh": "《FDE：AI 竞赛不在于模型》",
        "en": "FDE: The AI Race Isn't Won on Models",
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
            "《FDE：AI 竞赛不在于模型》",
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
        banned = [
            "+80%",
            "-15%",
            "-60%",
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

    def test_liora_moon_uses_verified_copy_and_secure_link(self):
        self.assertIn(
            "AI 塔罗解读平台，提供个性化洞察、每日一牌与 AI 塔罗师对话",
            INDEX,
        )
        self.assertIn(
            "AI Tarot reading platform for personalized insights, daily cards, and AI reader chat",
            INDEX,
        )
        self.assertRegex(INDEX, secure_link_pattern("https://lioramoon.com/"))


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
