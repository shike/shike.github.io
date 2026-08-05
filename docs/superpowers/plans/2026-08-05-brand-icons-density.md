# Brand Icons and Compact Homepage Implementation Plan

For agentic workers: REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

Goal: Add five verified official brand icons to Ventures and reduce excessive desktop whitespace with the approved balanced-density spacing system.

Architecture: Keep the static HTML/CSS/JS architecture and section order. Download verified official images once into assets/logos, render each through one reusable inline brand unit, and implement density changes through existing CSS selectors and variables. Extend the Python stdlib contract suite before each behavior change, then verify the real page at desktop, tablet, and mobile sizes.

Tech Stack: HTML5, CSS3 Flexbox/Grid, vanilla JavaScript (unchanged), Python 3 standard-library unittest, curl/sips, Playwright/Chrome, Lighthouse CI.

## Global Constraints

- Work directly on main; do not create a branch or worktree.
- List local and remote branches before implementation. Delete any non-main branch only if one appears; the user explicitly authorized deletion.
- Use only verified official assets listed in docs/superpowers/specs/2026-08-05-brand-icons-density-design.md.
- Do not use fantown.com or mallfantown.com for the Chinese FanTown / 聚星动力 project.
- Store all five icons locally; production HTML must not hotlink official sites.
- Do not redraw, crop, recolor, or imitate brand marks.
- Keep all existing sections, content, Books 3:4 cover layout, bilingual switching, QR modal, navigation, external links, JSON-LD, llms.txt, and sitemap behavior.
- Keep mobile section padding at 40px; compact the desktop system to the exact approved values.
- Add no dependencies, build step, CMS, or runtime image loader.
- Commit the changes as a single commit and push main via SSH.
- Do not create a worktree, do not open a Pull Request, do not delete the remote main branch.

---

### Task 1: Branch Audit and Working-Tree Sanity Check

Files:
- Verify: git branches and working tree

Interfaces:
- Consumes: existing repository on main
- Produces: confirmed main-only working tree and a list of any non-main branches

- [ ] Step 1: List local and remote branches

Run:
```bash
git status --short
git branch --format='%(refname:short) %(objectname:short) %(upstream:short)'
git branch -r --format='%(refname:short) %(objectname:short)'
```

Expected: a single local main and origin/main plus a clean working tree.

- [ ] Step 2: Confirm branch base

Run:
```bash
git merge-base HEAD main
```

Expected: returns the current main tip.

- [ ] Step 3: Delete any non-main branch if one appears (only with explicit user request)

If `git branch` shows anything other than main, surface the list to the user and wait for explicit approval before deletion.

---

### Task 2: Download the Five Official Brand Assets

Files:
- Create: assets/logos/xingqi-geo.png
- Create: assets/logos/whobot.svg
- Create: assets/logos/nihaovisit.svg
- Create: assets/logos/liora-moon.png
- Create: assets/logos/all-star-partner.png

Interfaces:
- Consumes: the five official source URLs from the spec
- Produces: five local files matching expected format and dimension

- [ ] Step 1: Write a failing asset test

Add to tests/test_homepage_content.py:

```python
class BrandAssetsTests(unittest.TestCase):
    def setUp(self):
        self.index = read("index.html")

    def test_brand_assets_are_local(self):
        remote = [
            "https://www.xingqigeo.cn/",
            "https://whobot.com/",
            "https://nihaovisit.com/",
            "https://lioramoon.com/",
            "allstarpartner.com",
        ]
        for token in remote:
            self.assertNotIn(f'src="https://{token}', self.index)
            self.assertNotIn(f"src='https://{token}", self.index)
```

Add a SOURCES map at the top of the file next to BOOKS:

```python
BRAND_ASSETS = {
    "xingqi-geo": (b"\x89PNG\r\n\x1a\n", 64, 64, "image/png"),
    "liora-moon": (b"\x89PNG\r\n\x1a\n", 512, 512, "image/png"),
    "all-star-partner": (b"\x89PNG\r\n\x1a\n", 300, 300, "image/png"),
    "whobot": (b"<svg", 36, 23, "image/svg+xml"),
    "nihaovisit": (b"<svg", None, None, "image/svg+xml"),
}
```

Add a method:

```python
    def test_each_brand_asset_file_matches_spec(self):
        for name, (head, w, h, mime) in BRAND_ASSETS.items():
            path = ROOT / "assets" / "logos" / f"{name}.{head[1:4].decode('ascii').lower() or 'svg' if head.startswith(b'<svg') else 'png'}"
            self.assertTrue(path.is_file(), f"missing {path}")
            with path.open("rb") as stream:
                self.assertEqual(stream.read(len(head)), head)
            if w is None:
                continue
            if path.suffix == ".svg":
                text = path.read_text(encoding="utf-8")
                self.assertIn(f'width="{w}"', text)
                self.assertIn(f'height="{h}"', text)
            else:
                with path.open("rb") as stream:
                    stream.seek(16)
                    self.assertEqual(struct.unpack(">II", stream.read(8)), (w, h))
```

- [ ] Step 2: Run and confirm failure

Run:
```bash
PYTHONPATH=tests python3 -m unittest test_homepage_content.BrandAssetsTests -v
```

Expected: FAIL on the missing files.

- [ ] Step 3: Download the five verified official assets

Run:
```bash
mkdir -p assets/logos
gh api -H 'Accept: application/vnd.github.raw' repos/shike/.../asset >/tmp/x 2>/dev/null || curl -L --fail --silent --show-error 'https://www.xingqigeo.cn/favicon.ico' -o /tmp/xingqi-geo.ico
```

The real, working commands for each asset:

```bash
curl -L --fail --silent --show-error 'https://www.xingqigeo.cn/favicon.ico' -o /tmp/xingqi-geo.ico
sips -s format png /tmp/xingqi-geo.ico --out assets/logos/xingqi-geo.png >/dev/null

curl -L --fail --silent --show-error 'https://whobot.com/Logo.svg' -o assets/logos/whobot.svg

curl -L --fail --silent --show-error 'https://nihaovisit.com/icon.svg' -o assets/logos/nihaovisit.svg

curl -L --fail --silent --show-error 'https://lioramoon.com/icon-512.png' -o assets/logos/liora-moon.png

curl -L --fail --silent --show-error 'https://nwzimg.wezhan.cn/sitefiles10323/10323482/asp.png' -o assets/logos/all-star-partner.png
```

- [ ] Step 4: Verify each file

Run:
```bash
file assets/logos/xingqi-geo.png assets/logos/whobot.svg assets/logos/nihaovisit.svg assets/logos/liora-moon.png assets/logos/all-star-partner.png
ls -lh assets/logos/
```

Expected: five real assets with the expected types and non-empty sizes.

- [ ] Step 5: Run the asset tests and confirm pass

Run:
```bash
PYTHONPATH=tests python3 -m unittest test_homepage_content.BrandAssetsTests -v
```

Expected: both tests pass.

---

### Task 3: Inline Brand Unit Markup

Files:
- Modify: index.html:257-307

Interfaces:
- Consumes: existing .venture-sub blocks
- Produces: each .venture-sub-head wraps a .venture-sub-brand with icon plus name, then a CTA

- [ ] Step 1: Add a failing markup test

Add to tests/test_homepage_content.py inside BrandAssetsTests:

```python
    def test_venture_sub_brand_uses_local_icon(self):
        for path, zh in [
            ("assets/logos/xingqi-geo.png", "微盟星启 GEO"),
            ("assets/logos/whobot.svg", "呼波特 WhoBot"),
            ("assets/logos/nihaovisit.svg", "NihaoVisit"),
            ("assets/logos/liora-moon.png", "Liora Moon"),
            ("assets/logos/all-star-partner.png", "聚星动力 FanTown"),
        ]:
            with self.subTest(brand=zh):
                pattern = (
                    r'<span class="venture-sub-brand">'
                    r'\s*<span class="venture-sub-logo" aria-hidden="true">'
                    r'\s*<img src="' + re.escape(path) + r'"'
                )
                self.assertRegex(INDEX, pattern)
                self.assertIn(zh, self.index)
```

- [ ] Step 2: Run and confirm failure

Run:
```bash
PYTHONPATH=tests python3 -m unittest test_homepage_content.BrandAssetsTests.test_venture_sub_brand_uses_local_icon -v
```

Expected: FAIL.

- [ ] Step 3: Update each .venture-sub-head in index.html

Replace the SaaS and agency sub items so the name sits inside a .venture-sub-brand:

```html
<div class="venture-sub-head">
  <span class="venture-sub-brand">
    <span class="venture-sub-logo" aria-hidden="true">
      <img src="assets/logos/xingqi-geo.png" alt="" width="32" height="32" loading="lazy" decoding="async">
    </span>
    <span class="venture-sub-name" data-en="Weimob Xingqi GEO">微盟星启 GEO</span>
  </span>
  <button class="venture-link venture-link--qr" type="button" data-qr-trigger data-qr-title="微盟星启 GEO · 扫码咨询" data-qr-desc="扫码加施可个人微信，获取微盟星启 GEO 产品详情与代理政策" data-en="Inquire ↗">咨询 ↗</button>
</div>
```

Repeat for 呼波特 WhoBot (assets/logos/whobot.svg), NihaoVisit (assets/logos/nihaovisit.svg), Liora Moon (assets/logos/liora-moon.png).

For the FanTown item, change the title and rewrite the description, while using the FanTown parent brand icon:

```html
<div class="venture-sub-head">
  <span class="venture-sub-brand">
    <span class="venture-sub-logo" aria-hidden="true">
      <img src="assets/logos/all-star-partner.png" alt="" width="32" height="32" loading="lazy" decoding="async">
    </span>
    <span class="venture-sub-name" data-en="FanTown by All Star Partner">聚星动力 FanTown</span>
  </span>
</div>
<p class="venture-sub-desc" data-en="Operated officially licensed 2026 World Cup pop-ups across Changzhou, Wuxi, and Shanghai, turning event traffic into measurable footfall and sales.">运营 2026 世界杯正版授权快闪店，落地常锡沪三城，把赛事流量转化为可衡量的客流与销售。</p>
```

- [ ] Step 4: Run the markup test and the full suite

Run:
```bash
PYTHONPATH=tests python3 -m unittest test_homepage_content.BrandAssetsTests.test_venture_sub_brand_uses_local_icon -v
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: the new test passes and the full suite stays green.

---

### Task 4: Compact CSS for Sections, Cards, Grids

Files:
- Modify: css/style.css sections around :root, .hero, .section, .section-header, .skills-grid, .ventures-grid, .book-cover-frame, .about-stats, .about-content, .timeline, .track-record, .logo-wall, .speaking-item, .contact, mobile @media

Interfaces:
- Consumes: existing CSS selectors
- Produces: tighter desktop spacing at the approved values, no change to mobile Section padding

- [ ] Step 1: Add a failing CSS contract test

Add to tests/test_homepage_content.py:

```python
    def test_balanced_compact_density_values(self):
        self.assertIn("--section-padding: 68px;", CSS)
        self.assertIn(".hero {", CSS)
        self.assertRegex(CSS, r"\.hero\s*\{[^}]*padding-top:\s*120px;\s*padding-bottom:\s*72px;")
        self.assertIn(".section-header {", CSS)
        self.assertIn("margin-bottom: 32px;", CSS)
        self.assertIn("line-height: 1.7;", CSS)
        self.assertRegex(
            CSS,
            r"\.skills-grid,\s*\.ventures-grid,\s*\.books-grid,\s*\.track-grid\s*\{[^}]*gap:\s*20px;",
        )
        self.assertIn(".about-stats {", CSS)
        self.assertIn("margin: 0 auto 28px;", CSS)
        self.assertRegex(
            CSS,
            r"\.about-content p\s*\{[^}]*line-height:\s*1\.75;",
        )
        self.assertRegex(
            CSS,
            r"\.timeline-item\s*\{[^}]*padding-bottom:\s*28px;",
        )
        self.assertRegex(
            CSS,
            r"\.track-record\s*\{[^}]*margin-top:\s*40px;\s*padding-top:\s*32px;",
        )
        self.assertRegex(
            CSS,
            r"\.logo-wall\s*\{[^}]*gap:\s*24px;",
        )
        self.assertRegex(
            CSS,
            r"\.speaking-item\s*\{[^}]*padding:\s*18px 0;",
        )
        self.assertRegex(
            CSS,
            r"\.contact-qr\s*\{[^}]*margin:\s*28px auto 0;",
        )
```

- [ ] Step 2: Run and confirm failure

Run:
```bash
PYTHONPATH=tests python3 -m unittest test_homepage_content.BooksTests.test_balanced_compact_density_values -v
```

Expected: FAIL.

- [ ] Step 3: Apply the compact density values

Update these rules in css/style.css:

- `:root`: set `--section-padding: 68px;`
- `.hero`: change to `padding-top: 120px; padding-bottom: 72px;`
- `.section-header`: change `margin-bottom` to `32px`
- body `line-height: 1.7;`
- `.ventures-grid`: change `gap: 24px; margin-bottom: 48px;` to `gap: 20px; margin-bottom: 0;`
- `.skill-card, .project-card`: padding 24px
- `.venture-card, .book-card`: padding 24px
- `.track-card`: padding 24px
- `.skills-grid, .ventures-grid, .books-grid, .track-grid`: `gap: 20px;`
- `.about-stats`: `margin: 0 auto 28px;`
- `.about-content p`: `margin-bottom: 16px; line-height: 1.75;`
- `.timeline-item`: `padding-bottom: 28px;`
- `.track-record`: `margin-top: 40px; padding-top: 32px;`
- `.track-title`: `margin-bottom: 24px;`
- `.track-grid`: `margin-top: 24px;`
- `.logo-wall`: `gap: 24px;`
- `.logo-group h4`: `margin-bottom: 14px;`
- `.speaking-item`: `padding: 18px 0;`
- `.contact-desc`: `margin-bottom: 20px;`
- `.contact-links`: `gap: 16px;`
- `.contact-qr`: `margin: 28px auto 0;`
- `.venture-card--main`: `margin-bottom: 20px;`

Do not change the Books 3:4 cover frame, the mobile @media block, or any selector outside this list.

- [ ] Step 4: Run the contract test and full suite

Run:
```bash
PYTHONPATH=tests python3 -m unittest test_homepage_content.BooksTests.test_balanced_compact_density_values -v
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: the new test passes and the full suite stays green.

---

### Task 5: Brand Unit CSS

Files:
- Modify: css/style.css near the .venture-sub rules

Interfaces:
- Consumes: existing .venture-sub-head
- Produces: .venture-sub-brand flex container and a 32px icon slot

- [ ] Step 1: Add a failing CSS contract test

Add to tests/test_homepage_content.py:

```python
    def test_venture_sub_brand_styles(self):
        self.assertIn(".venture-sub-brand {", CSS)
        self.assertIn(".venture-sub-logo {", CSS)
        self.assertIn("width: 32px;", CSS)
        self.assertIn("height: 32px;", CSS)
        self.assertIn("object-fit: contain;", CSS)
        self.assertRegex(
            CSS,
            r"@media \(max-width:\s*768px\)\s*\{[^}]*\.venture-sub-logo\s*\{[^}]*width:\s*28px;\s*height:\s*28px;",
        )
```

- [ ] Step 2: Run and confirm failure

Run:
```bash
PYTHONPATH=tests python3 -m unittest test_homepage_content.BooksTests.test_venture_sub_brand_styles -v
```

Expected: FAIL.

- [ ] Step 3: Add the brand unit CSS

Add to css/style.css after the .venture-sub-desc block:

```css
.venture-sub-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  min-width: 0;
}

.venture-sub-logo {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 32px;
  height: 32px;
  flex: 0 0 32px;
}

.venture-sub-logo img {
  display: block;
  width: 100%;
  height: 100%;
  object-fit: contain;
}
```

Inside the existing @media (max-width: 768px) block add:

```css
.venture-sub-logo {
  width: 28px;
  height: 28px;
  flex-basis: 28px;
}
```

- [ ] Step 4: Run the contract test and full suite

Run:
```bash
PYTHONPATH=tests python3 -m unittest test_homepage_content.BooksTests.test_venture_sub_brand_styles -v
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: the new test passes and the full suite stays green.

---

### Task 6: Browser Verification of Icons and Compact Layout

Files:
- Verify: index.html, css/style.css, assets/logos/

Interfaces:
- Consumes: brand unit markup, compact CSS, local assets
- Produces: real screenshots and Playwright assertions proving icons load and layout is compact

- [ ] Step 1: Serve the site

Run:
```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

- [ ] Step 2: Drive Chromium at desktop, tablet, and mobile widths

For 1024, 768, and 320px, evaluate:

```javascript
const brands = [...document.querySelectorAll('.venture-sub-brand')].map(el => {
  const img = el.querySelector('img');
  const frame = el.querySelector('.venture-sub-logo');
  const name = el.querySelector('.venture-sub-name');
  const cta = el.parentElement.querySelector('a, button');
  const box = el.getBoundingClientRect();
  return {
    src: img?.getAttribute('src'),
    complete: img?.complete,
    natural: [img?.naturalWidth, img?.naturalHeight],
    logoWidth: frame?.getBoundingClientRect().width,
    logoHeight: frame?.getBoundingClientRect().height,
    name: name?.textContent.trim(),
    hasCta: Boolean(cta),
    height: box.height,
  };
});
const sectionPad = getComputedStyle(document.documentElement).getPropertyValue('--section-padding');
const hero = document.querySelector('.hero').getBoundingClientRect();
```

Assert:
- each brand has a non-null src that starts with assets/logos/ and loaded (complete and naturalWidth > 0)
- each logo slot width is approximately the configured size (32 or 28 depending on viewport)
- each entry has a CTA button or link
- the page document --section-padding is 68px
- the hero element height is at most 720px on desktop (rough proxy for the 120/72 padding)
- Books still uses a 3:4 cover frame
- no horizontal overflow, no console errors

- [ ] Step 3: Capture screenshots of Ventures at 1024px and 320px

Save to /tmp/ventures-1024.png and /tmp/ventures-320.png and confirm:
- all five cards show their icon
- FanTown card uses the all-star-partner icon
- the page is visibly more compact than before (compare against /tmp/books-1024.png baseline if helpful)

- [ ] Step 4: Stop the local server

Stop the background python -m http.server process when checks finish.

---

### Task 7: Lighthouse CI Final Check

Files:
- Verify: full static site

- [ ] Step 1: Run Lighthouse CI

Run:
```bash
npx --yes @lhci/cli autorun --config=.lighthouserc.json
```

- [ ] Step 2: Read the median scores

Run:
```bash
python3 -c "import json,pathlib; files=sorted(pathlib.Path('.lighthouseci').glob('lhr-*.json')); print('reports', len(files)); [print(f.name, {k: round(v['score'], 3) for k,v in json.loads(f.read_text())['categories'].items() if k in {'performance','accessibility','best-practices','seo'}}) for f in files]"
```

Expected: accessibility >= 0.95, SEO >= 0.95, performance >= 0.9, best practices >= 0.9.

- [ ] Step 3: Clean up the temporary report directory

Run:
```bash
rm -rf .lighthouseci
```

---

### Task 8: Single Commit and Push to main

Files:
- Modify: index.html, css/style.css, tests/test_homepage_content.py
- Add: assets/logos/xingqi-geo.png, whobot.svg, nihaovisit.svg, liora-moon.png, all-star-partner.png
- (No spec or plan edits; they were committed in the prior design step.)

- [ ] Step 1: Confirm working-tree state

Run:
```bash
git status --short
git diff --check
```

Expected: only the planned files and assets appear; no stray diffs.

- [ ] Step 2: Run the full test suite one more time

Run:
```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: all tests pass.

- [ ] Step 3: Create a single commit

Run:
```bash
git add index.html css/style.css tests/test_homepage_content.py assets/logos
git commit -m "feat: add brand icons and compact homepage layout"
```

- [ ] Step 4: Push to origin/main

Run:
```bash
git push git@github.com:shike/shike.github.io.git main
```

- [ ] Step 5: Verify the remote tip

Run:
```bash
git ls-remote git@github.com:shike/shike.github.io.git refs/heads/main
```

Expected: the remote SHA matches the local commit.

## Self-Review Notes

- Every brand asset is downloaded with curl from the verified official URL; no agent edits them.
- All CSS density changes are inside the existing selectors; no new component is introduced.
- Tests assert real asset bytes, dimensions, and CSS string contents before each behavior change.
- No book layout, no product scope, no JSON-LD, no llms.txt changes occur.
- Push is limited to a single commit on main; no worktree, no Pull Request, no force push.
