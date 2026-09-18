"""Contract tests for the homepage.

Five groups:
  1. Structure     — section ids, anchors, heading order
  2. Bilingual     — the data-en / data-en-aria / data-en-alt contract
  3. Design system — tokens, WCAG contrast, breakpoints, CSS hygiene
  4. Machine layer — page facts cross-checked against JSON-LD / llms.txt / sitemap
  5. Red lines     — retired claims, link safety, image rules, asset integrity

These deliberately assert *invariants*, not marketing copy or pixel values:
rewording a section or retuning a spacing value should not fail the suite, but
breaking the i18n contract, dropping contrast below AA, or letting the
machine-readable layer drift from the visible page should.

Run: python3 -m unittest discover -s tests
"""

import json
import re
import struct
import unittest
import xml.etree.ElementTree as ET
from datetime import date
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "param", "source", "track", "wbr",
}

# WCAG AA for normal-size text.
AA = 4.5


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class Doc(HTMLParser):
    """Minimal DOM collector: element tree, own text, and attribute lookup."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = {"tag": "[root]", "attrs": {}, "children": [], "text": []}
        self.open = [self.root]

    def _add(self, tag, attrs):
        el = {
            "tag": tag,
            "attrs": attrs,
            "children": [],
            "parent": self.open[-1],
            "text": [],
        }
        self.open[-1]["children"].append(el)
        return el

    def handle_starttag(self, tag, attrs):
        el = self._add(tag, dict(attrs))
        if tag not in VOID:
            self.open.append(el)

    def handle_startendtag(self, tag, attrs):
        self._add(tag, dict(attrs))

    def handle_endtag(self, tag):
        for i in range(len(self.open) - 1, 0, -1):
            if self.open[i]["tag"] == tag:
                del self.open[i:]
                return

    def handle_data(self, data):
        self.open[-1]["text"].append(data)


def walk(el):
    yield el
    for child in el["children"]:
        yield from walk(child)


def own_text(el):
    return re.sub(r"\s+", " ", "".join(el["text"])).strip()


def classes(el):
    return set((el["attrs"].get("class") or "").split())


def first(doc, tag=None, cls=None, attr=None):
    for el in walk(doc.root):
        if tag and el["tag"] != tag:
            continue
        if cls and cls not in classes(el):
            continue
        if attr and attr not in el["attrs"]:
            continue
        return el
    return None


def find_all(doc, tag=None, cls=None, attr=None):
    out = []
    for el in walk(doc.root):
        if tag and el["tag"] != tag:
            continue
        if cls and cls not in classes(el):
            continue
        if attr and attr not in el["attrs"]:
            continue
        out.append(el)
    return out


INDEX_SRC = read("index.html")
CSS = read("css/style.css")
JS = read("js/main.js")
LLMS = read("llms.txt")
SITEMAP = read("sitemap.xml")
DOC = Doc()
DOC.feed(INDEX_SRC)


def jsonld():
    m = re.search(
        r'<script type="application/ld\+json">(.*?)</script>', INDEX_SRC, re.S
    )
    return json.loads(m.group(1))


def graph():
    return {node.get("@id"): node for node in jsonld()["@graph"]}


# --------------------------------------------------------------- colour maths


def _channel(value):
    value = value / 255
    return value / 12.92 if value <= 0.04045 else ((value + 0.055) / 1.055) ** 2.4


def luminance(hex_colour):
    hex_colour = hex_colour.lstrip("#")
    r, g, b = (int(hex_colour[i:i + 2], 16) for i in (0, 2, 4))
    return 0.2126 * _channel(r) + 0.7152 * _channel(g) + 0.0722 * _channel(b)


def contrast(a, b):
    la, lb = luminance(a), luminance(b)
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def tokens():
    block = re.search(r":root\s*\{(.*?)\}", CSS, re.S).group(1)
    return dict(re.findall(r"--([a-z0-9-]+):\s*([^;]+);", block))


TOKENS = tokens()
WHITE = "#ffffff"
TINT = TOKENS.get("soft", "#f6f8fd").strip()


def image_size(path):
    """Return (width, height) for a PNG, JPEG or SVG on disk."""
    data = (ROOT / path).read_bytes()
    if data[:8] == b"\x89PNG\r\n\x1a\n":
        w, h = struct.unpack(">II", data[16:24])
        return w, h
    if b"<svg" in data[:400]:
        head = data[:400].decode("utf-8", "replace")
        w = re.search(r'\bwidth="(\d+)"', head)
        h = re.search(r'\bheight="(\d+)"', head)
        if w and h:
            return int(w.group(1)), int(h.group(1))
        raise AssertionError(f"SVG without explicit dimensions: {path}")
    i = 2
    while i < len(data) - 9:
        if data[i] != 0xFF:
            i += 1
            continue
        marker = data[i + 1]
        if marker in (0xD8, 0x01) or 0xD0 <= marker <= 0xD7:
            i += 2
            continue
        if marker in (0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7,
                      0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF):
            h, w = struct.unpack(">HH", data[i + 5:i + 9])
            return w, h
        i += 2 + struct.unpack(">H", data[i + 2:i + 4])[0]
    raise AssertionError(f"could not read image dimensions: {path}")


def dequoted(text):
    """Drop quote glyphs so typographic and straight quotes compare equal."""
    return re.sub(r"[\u201c\u201d\u2018\u2019“”\"']", "", text)


# ------------------------------------------------------------- 1. structure


class StructureTests(unittest.TestCase):
    def setUp(self):
        self.sections = [el for el in walk(DOC.root) if el["tag"] == "section"]

    def test_page_chrome_exists(self):
        self.assertIsNotNone(first(DOC, tag="main"), "main#main missing")
        self.assertIsNotNone(first(DOC, tag="nav"), "nav missing")
        self.assertIsNotNone(first(DOC, tag="footer"), "footer missing")
        self.assertTrue(find_all(DOC, cls="skip-link"), "skip link missing")

    def test_sections_have_unique_ids(self):
        ids = [el["attrs"].get("id") for el in self.sections]
        self.assertNotIn(None, ids, "every section must carry an id")
        self.assertEqual(len(ids), len(set(ids)), f"duplicate section ids: {ids}")

    def test_every_nav_link_points_at_a_section(self):
        ids = {el["attrs"]["id"] for el in self.sections}
        links = find_all(DOC, tag="a", cls="nav-link")
        self.assertGreaterEqual(len(links), 6)
        for link in links:
            href = link["attrs"].get("href", "")
            self.assertTrue(href.startswith("#"), f"nav link not an anchor: {href}")
            self.assertIn(href[1:], ids, f"nav link {href} has no matching section id")

    def test_exactly_one_h1_and_one_h2_per_section(self):
        headings = [el for el in walk(DOC.root)
                    if re.fullmatch(r"h[1-6]", el["tag"])]
        h1s = [h for h in headings if h["tag"] == "h1"]
        self.assertEqual(len(h1s), 1, "the page must have exactly one h1")
        for section in self.sections:
            h2s = [el for el in walk(section) if el["tag"] == "h2"]
            if section["attrs"]["id"] == "hero":
                self.assertEqual(h2s, [], "hero is headed by the h1")
            else:
                self.assertEqual(
                    len(h2s), 1,
                    f"#{section['attrs']['id']} must have exactly one h2",
                )

    def test_heading_levels_never_skip(self):
        levels = [int(el["tag"][1]) for el in walk(DOC.root)
                  if re.fullmatch(r"h[1-6]", el["tag"])]
        self.assertTrue(levels, "no headings found")
        self.assertEqual(levels[0], 1, "the first heading must be an h1")
        for prev, cur in zip(levels, levels[1:]):
            self.assertLessEqual(
                cur, prev + 1, f"heading level jumps from h{prev} to h{cur}"
            )

    def test_sections_are_in_nav_order(self):
        order = [el["attrs"]["id"] for el in self.sections]
        links = [l["attrs"]["href"][1:] for l in find_all(DOC, tag="a", cls="nav-link")]
        positions = [order.index(target) for target in links]
        self.assertEqual(
            positions, sorted(positions),
            "nav links must follow the document order of their sections",
        )


# ------------------------------------------------------------- 2. bilingual


class BilingualTests(unittest.TestCase):
    def test_language_attributes(self):
        html = first(DOC, tag="html")
        self.assertEqual(html["attrs"].get("lang"), "zh-CN")
        hreflang = {
            el["attrs"].get("hreflang")
            for el in find_all(DOC, tag="link")
            if el["attrs"].get("rel") == "alternate"
        }
        self.assertEqual(hreflang, {"zh-CN", "en", "x-default"})

    def test_no_data_en_on_elements_with_children(self):
        """data-en replaces textContent, so tagged elements must be leaves.

        An element with markup inside would have its inline links and <code>
        nodes deleted on the first language switch, unrecoverably.
        """
        offenders = [
            f"<{el['tag']} class=\"{el['attrs'].get('class', '')}\">"
            for el in find_all(DOC, attr="data-en")
            if el["children"]
        ]
        self.assertEqual(
            offenders, [],
            "data-en must only sit on leaf elements; found containers: "
            + ", ".join(offenders),
        )

    def test_translation_attributes_are_well_formed(self):
        for el in find_all(DOC, attr="data-en"):
            value = el["attrs"]["data-en"].strip()
            self.assertTrue(value, f"empty data-en on <{el['tag']}>")
            self.assertNotEqual(
                value, own_text(el),
                f"data-en duplicates the Chinese text on <{el['tag']}>",
            )
        for el in find_all(DOC, attr="data-en-aria"):
            self.assertIn("aria-label", el["attrs"])
            self.assertTrue(el["attrs"]["data-en-aria"].strip())
        for el in find_all(DOC, attr="data-en-alt"):
            self.assertEqual(el["tag"], "img")
            self.assertTrue(el["attrs"]["data-en-alt"].strip())

    def test_coverage_is_substantial(self):
        self.assertGreaterEqual(
            len(find_all(DOC, attr="data-en")), 100,
            "most visible strings should carry an English variant",
        )
        self.assertGreaterEqual(len(find_all(DOC, attr="data-en-alt")), 8)

    def test_language_switch_accessible_name_contains_visible_text(self):
        button = first(DOC, tag="button", cls="lang-switch")
        self.assertIsNotNone(button, "language switch button missing")
        for lang in ("zh", "en"):
            visible = own_text(button) if lang == "zh" else button["attrs"]["data-en"]
            name = (button["attrs"]["aria-label"] if lang == "zh"
                    else button["attrs"]["data-en-aria"])
            self.assertIn(
                visible, name,
                f"accessible name {name!r} must contain the visible label {visible!r}",
            )

    def test_js_guards_against_overwriting_markup(self):
        self.assertIn(
            "el.children.length > 0", JS,
            "js/main.js must refuse to replace textContent on elements with children",
        )
        self.assertIn("data-en-alt", JS, "js/main.js must handle image alt text")

    def test_meta_has_a_single_source_of_truth(self):
        """Chinese title/description live in the HTML only; JS holds English."""
        self.assertNotIn(
            "连续创业者", JS,
            "js/main.js must not duplicate the Chinese metadata",
        )
        self.assertIn("EN_META", JS)


# --------------------------------------------------------- 3. design system


class DesignSystemTests(unittest.TestCase):
    REQUIRED_TOKENS = [
        "blue", "blue-text", "blue-strong", "blue-soft", "blue-line", "blue-light",
        "ink", "body", "mut", "faint", "line", "soft", "dark", "white",
        "r", "r-l", "sh-1", "sh-2", "sh-3", "font", "max-width", "gutter", "sec-pad",
    ]

    TEXT_TOKENS = ["ink", "body", "mut", "faint"]

    def test_required_tokens_are_defined(self):
        missing = [t for t in self.REQUIRED_TOKENS if t not in TOKENS]
        self.assertEqual(missing, [], f"missing design tokens: {missing}")

    def test_text_tokens_pass_wcag_aa_on_both_surfaces(self):
        for name in self.TEXT_TOKENS:
            colour = TOKENS[name].strip()
            for surface in (WHITE, TINT):
                ratio = contrast(colour, surface)
                self.assertGreaterEqual(
                    round(ratio, 2), AA,
                    f"--{name} {colour} on {surface} is only {ratio:.2f}:1",
                )

    def test_accent_pairings_pass_wcag_aa(self):
        pairs = [
            (WHITE, TOKENS["blue-text"].strip(), "button label on accent fill"),
            (TOKENS["blue-text"].strip(), TOKENS["blue-soft"].strip(), "accent on chip"),
            (TOKENS["blue-text"].strip(), TINT, "accent on tinted section"),
            (TOKENS["blue-light"].strip(), TOKENS["dark"].strip(), "accent on dark block"),
            (WHITE, TOKENS["dark"].strip(), "white on dark block"),
        ]
        for fg, bg, label in pairs:
            ratio = contrast(fg, bg)
            self.assertGreaterEqual(
                round(ratio, 2), AA, f"{label}: {fg} on {bg} is only {ratio:.2f}:1"
            )

    def test_brand_blue_is_never_used_for_text(self):
        """--blue is 4.28:1 on white: large or decorative use only."""
        offenders = re.findall(r"color:\s*var\(--blue\)", CSS)
        self.assertEqual(
            offenders, [],
            "use --blue-text (or darker) for text; --blue is for fills and large type",
        )

    def test_the_old_low_contrast_palette_is_gone(self):
        for legacy in (
            "#94a3b8", "#475569", "#4f46e5", "#4338ca", "#818cf8",
            "#0f172a", "#1e1b4b", "#312e81", "#6366f1",
            "rgba(79, 70, 229", "rgba(79,70,229",
        ):
            self.assertNotIn(legacy, CSS, f"legacy colour {legacy} still in style.css")

    def test_css_hygiene(self):
        self.assertNotIn("!important", CSS, "style.css must not use !important")
        self.assertEqual(
            CSS.count("{"), CSS.count("}"), "unbalanced braces in style.css"
        )
        self.assertLess(
            len(CSS.splitlines()), 2600,
            "style.css has grown past its post-rewrite budget",
        )

    def test_only_two_responsive_breakpoints(self):
        found = set(re.findall(r"@media \(max-width:\s*(\d+)px\)", CSS))
        self.assertEqual(
            found, {"1024", "768"},
            f"breakpoints should be exactly 1024 and 768, found {sorted(found)}",
        )

    def test_accessibility_basics_are_styled(self):
        self.assertIn(":focus-visible", CSS)
        self.assertIn("prefers-reduced-motion", CSS)
        self.assertIn(".skip-link", CSS)
        self.assertIn(".nav-menu.active", CSS, "mobile menu open state missing")
        self.assertIn(".qr-modal[hidden]", CSS, "modal hidden state must be styled")

    def test_retired_dead_selectors_are_gone(self):
        for dead in (
            ".product-section--compact", ".product-case-mini", ".product-compact",
            ".product-row", ".product-chip", ".venture-card", ".project-badge",
            ".project-tag", ".focus-details", ".product-stage", ".pain-quote",
            ".arch-layer",
        ):
            self.assertNotIn(dead, CSS, f"dead selector {dead} still in style.css")


# ---------------------------------------------------------- 4. machine layer


class MachineReadableTests(unittest.TestCase):
    def setUp(self):
        self.graph = graph()

    def test_graph_has_the_expected_nodes(self):
        types = {node.get("@type") for node in self.graph.values()}
        for expected in ("Person", "Organization", "WebSite", "ProfilePage",
                         "FAQPage", "Book"):
            self.assertIn(expected, types, f"JSON-LD is missing a {expected} node")
        books = [n for n in self.graph.values() if n.get("@type") == "Book"]
        self.assertEqual(len(books), 3)

    def test_faq_answers_are_populated(self):
        faq = [n for n in self.graph.values() if n.get("@type") == "FAQPage"][0]
        questions = faq["mainEntity"]
        self.assertGreaterEqual(len(questions), 6)
        for q in questions:
            self.assertTrue(q["name"].strip())
            self.assertTrue(q["acceptedAnswer"]["text"].strip())

    def test_person_links_to_organization(self):
        person = self.graph["https://shike.github.io/#person"]
        org_id = person["worksFor"]["@id"]
        self.assertIn(org_id, self.graph)
        self.assertEqual(self.graph[org_id]["founder"]["@id"], person["@id"])

    def test_book_facts_match_the_page_and_llms_txt(self):
        books = [n for n in self.graph.values() if n.get("@type") == "Book"]
        for book in books:
            title = re.sub(r"[《》]", "", book["name"]).strip()
            self.assertIn(title, INDEX_SRC, f"book {title} missing from index.html")
            self.assertIn(title, LLMS, f"book {title} missing from llms.txt")
            self.assertIn(book["url"], INDEX_SRC, f"{book['url']} not linked on the page")
            self.assertIn(book["url"], LLMS, f"{book['url']} missing from llms.txt")

    def test_case_figures_match_between_page_and_llms(self):
        quotes = [
            "Quoting speed is our biggest competitive advantage right now",
            "The master craftsmen's experience is finally captured",
        ]
        stripped = dequoted(INDEX_SRC)
        stripped_llms = dequoted(LLMS)
        for quote in quotes:
            needle = dequoted(quote)
            self.assertIn(needle, stripped, "case quote missing from index.html")
            self.assertIn(needle, stripped_llms, "case quote missing from llms.txt")
        for figure in ("99.2%", "25%", "30%", "45%"):
            self.assertIn(figure, INDEX_SRC, f"{figure} missing from index.html")
            self.assertIn(figure, LLMS, f"{figure} missing from llms.txt")

    def test_client_footprint_is_stated_once(self):
        self.assertIn("100+", INDEX_SRC)
        self.assertIn("100+", LLMS)
        self.assertNotIn("30+", LLMS, "llms.txt still claims the old 30+ footprint")

    def test_llms_documents_every_section_theme(self):
        for heading in (
            "## Manufacturing AI focus",
            "## Client cases",
            "## Career path",
            "## Books",
            "## Public speaking",
            "## Contact",
        ):
            self.assertIn(heading, LLMS, f"llms.txt is missing {heading}")

    def test_all_three_dates_agree_and_are_not_in_the_future(self):
        page = re.search(r'"dateModified":\s*"(\d{4}-\d{2}-\d{2})"', INDEX_SRC).group(1)
        sitemap = ET.fromstring(SITEMAP).find(
            "s:url/s:lastmod", {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        ).text
        llms = re.search(r"Last updated:\s*(\d{4}-\d{2}-\d{2})", LLMS).group(1)
        self.assertEqual(
            {page, sitemap, llms}, {page},
            f"dateModified={page} lastmod={sitemap} llms={llms} must match",
        )
        self.assertLessEqual(
            date.fromisoformat(page), date.today(), "lastmod is in the future"
        )

    def test_canonical_and_open_graph_are_consistent(self):
        canonicals = [
            el["attrs"]["href"] for el in find_all(DOC, tag="link")
            if el["attrs"].get("rel") == "canonical"
        ]
        self.assertEqual(canonicals, ["https://shike.github.io/"])
        og_url = [
            el["attrs"]["content"] for el in find_all(DOC, tag="meta")
            if el["attrs"].get("property") == "og:url"
        ]
        self.assertEqual(og_url, ["https://shike.github.io/"])
        for prop in ("og:image", "twitter:image"):
            found = [
                el["attrs"]["content"] for el in find_all(DOC, tag="meta")
                if el["attrs"].get("property") == prop or el["attrs"].get("name") == prop
            ]
            self.assertEqual(len(found), 1, f"{prop} missing")
            self.assertTrue(found[0].startswith("https://shike.github.io/"))

    def test_meta_descriptions_share_the_positioning(self):
        for attr, name in (("name", "description"), ("property", "og:description"),
                           ("name", "twitter:description")):
            found = [
                el["attrs"]["content"] for el in find_all(DOC, tag="meta")
                if el["attrs"].get(attr) == name
            ]
            self.assertEqual(len(found), 1, f"{name} missing")
            self.assertIn("WorkBuddy", found[0])
            self.assertIn("2-4 周", found[0])


# -------------------------------------------------------------- 5. red lines


RETIRED = [
    "数商方略", "Shushang Fanglue", "shushangfanglue.com",
    "乐奇 Minibus EV", "Leqi Minibus EV", "minibus-ev.com",
    "阿里云 AI 大赛银奖", "Alibaba Cloud AI Competition Silver Award",
    "业绩增长 80%", "成本下降 15%", "应收下降 60%",
    "医药",
]


class RedLineTests(unittest.TestCase):
    def test_retired_claims_never_reappear(self):
        for term in RETIRED:
            for source, name in ((INDEX_SRC, "index.html"), (LLMS, "llms.txt"),
                                 (JS, "js/main.js")):
                self.assertNotIn(term, source, f"{name} still mentions {term!r}")

    def test_external_links_open_safely(self):
        for el in find_all(DOC, tag="a"):
            href = el["attrs"].get("href", "")
            if not href.startswith("http"):
                continue
            if href.startswith("https://shike.github.io"):
                continue
            self.assertTrue(href.startswith("https://"), f"non-https link: {href}")
            self.assertEqual(
                el["attrs"].get("target"), "_blank", f"{href} must open in a new tab"
            )
            self.assertIn(
                "noopener", el["attrs"].get("rel", ""), f"{href} needs rel=noopener"
            )

    def test_images_declare_dimensions_and_loading(self):
        images = find_all(DOC, tag="img")
        self.assertGreaterEqual(len(images), 20)
        for el in images:
            src = el["attrs"].get("src", "")
            self.assertIn("alt", el["attrs"], f"{src} has no alt attribute")
            self.assertIn("width", el["attrs"], f"{src} has no width")
            self.assertIn("height", el["attrs"], f"{src} has no height")
            self.assertEqual(
                el["attrs"].get("decoding"), "async", f"{src} should decode async"
            )
            if src.startswith("assets/hero/"):
                self.assertNotIn(
                    "loading", el["attrs"],
                    "the hero image is above the fold and must not be lazy",
                )
            else:
                self.assertEqual(
                    el["attrs"].get("loading"), "lazy", f"{src} should lazy-load"
                )

    def test_no_hotlinked_images(self):
        for el in find_all(DOC, tag="img"):
            src = el["attrs"].get("src", "")
            self.assertFalse(
                src.startswith("http"), f"image is hotlinked instead of local: {src}"
            )

    def test_referenced_local_assets_exist(self):
        refs = {
            el["attrs"]["src"] for el in find_all(DOC, tag="img")
            if el["attrs"].get("src", "").startswith("assets/")
        }
        self.assertGreaterEqual(len(refs), 20)
        for ref in sorted(refs):
            self.assertTrue((ROOT / ref).is_file(), f"missing asset: {ref}")

    def test_asset_dimensions_match_their_declarations(self):
        """Raster assets must declare their true size, or the layout reserves
        the wrong box and shifts when the image lands. SVGs scale to the box
        their CSS gives them, so only the presence of a size is required."""
        for el in find_all(DOC, tag="img"):
            src = el["attrs"].get("src", "")
            if not src.startswith("assets/") or src.endswith(".svg"):
                continue
            actual = image_size(src)
            declared = (int(el["attrs"]["width"]), int(el["attrs"]["height"]))
            self.assertEqual(
                declared, actual,
                f"{src} declares {declared} but is {actual} on disk",
            )

    def test_social_preview_is_renderable(self):
        self.assertTrue((ROOT / "og-cover.svg").is_file())
        self.assertEqual(image_size("og-cover.jpg"), (1200, 630))

    def test_qr_modal_is_reachable(self):
        """The modal used to be dead code: the JS listened for a trigger that
        did not exist anywhere in the markup."""
        self.assertTrue(
            find_all(DOC, attr="data-qr-trigger"),
            "no element carries data-qr-trigger, so the QR modal cannot open",
        )
        self.assertTrue(find_all(DOC, attr="data-qr-close"))
        modal = first(DOC, tag="div", cls="qr-modal")
        self.assertIsNotNone(modal)
        self.assertIn("hidden", modal["attrs"], "modal should start hidden")
        self.assertEqual(modal["attrs"].get("role"), "dialog")


if __name__ == "__main__":
    unittest.main()
