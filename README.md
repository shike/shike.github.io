# 施可 · Shi Ke

Personal homepage. Static HTML/CSS/JS, deployed on GitHub Pages.

**Live:** https://shike.github.io/ · **Company site:** https://dropleap.cn/

## Stack

- Pure HTML / CSS / Vanilla JS — zero dependencies, no build step
- Bilingual (zh-CN / en) — `data-en` attribute pattern + `localStorage` persistence
- Active section highlight via `IntersectionObserver`
- Accessible: skip link, focus styles, `prefers-reduced-motion`, ARIA on mobile nav.
  All text colours pass WCAG AA (≥4.5:1) against both the white and the tinted
  section background — `tests/test_homepage_content.py` computes the ratios and
  fails the suite if any token regresses.
- SEO: complete OG / Twitter Card / canonical / hreflang / sitemap / robots
- GEO (Generative Engine Optimization): `llms.txt`, enriched JSON-LD `@graph`
  (Person · Organization · WebSite · ProfilePage · FAQPage · 3×Book),
  permissive AI crawler policy

## Design system

The visual system is ported from [dropleap.cn](https://dropleap.cn/) (brand blue
`#3370ff`, 1200px container, 104px section rhythm, 800-weight tight-tracked
headings, 14/20px radii, three-layer soft shadows, dashed dividers, a single dark
gradient CTA block, two breakpoints at 1024px and 768px).

**This stays a personal homepage.** The corporate site is a style reference and a
source of business evidence (two first-person case cards + two Skill cards live
in one "what I'm working on" section), not a template: sections are ordered
personal-first, copy is first-person, and everything beyond that one section
links out to dropleap.cn. See the amendment in the spec below.

One deliberate deviation: dropleap.cn's own text colours fail AA (`#77809c` is
3.92:1 on white; white on `#3370ff` is 4.28:1), so text-bearing roles are one
step darker here while the hue is preserved. See
`docs/superpowers/specs/2026-09-18-dropleap-rebrand-design.md` for the full
rationale and the measured ratios.

## Local Development

Open `index.html` directly, or serve over HTTP:

```sh
python3 -m http.server 8000
# then open http://localhost:8000
```

## Structure

```
.
├── index.html               # Page content + meta + JSON-LD (9 sections)
├── css/style.css            # Design tokens + all component styles
├── js/main.js               # i18n, nav highlight, mobile menu, QR modal
├── og-cover.jpg             # 1200x630 social preview
├── og-cover.svg             # SVG source for the preview
├── sitemap.xml              # Search engine sitemap
├── robots.txt               # Crawler policy (incl. AI bots)
├── llms.txt                 # AI-readable summary for LLM crawlers
├── assets/
│   ├── hero/                # Hero photograph (Shi Ke on stage)
│   ├── cases/               # Client case photographs
│   ├── books/               # Book covers
│   ├── logos/               # Brand logo wall + venture marks
│   └── wechat/              # WeChat QR code
├── tests/                   # Contract test suite (stdlib unittest)
├── docs/superpowers/        # Dated spec + plan documents
├── .lighthouserc.json       # Lighthouse CI thresholds
├── .github/workflows/
│   └── lighthouse.yml       # PR / push Lighthouse audit
└── README.md
```

## Deploy

Pushed to `main`; GitHub Pages serves automatically from the root.

## Quality Gates

`.github/workflows/lighthouse.yml` runs Lighthouse CI against the built site on
push and pull request. Thresholds in `.lighthouserc.json`:

- Accessibility ≥ 0.95 (error)
- SEO ≥ 0.95 (error)
- Performance / Best Practices ≥ 0.9 (warn)

Locally, run the contract suite:

```sh
python3 -m unittest discover -s tests
```

It checks five things: section/anchor structure, the bilingual contract, the
design tokens and their contrast ratios, consistency between the page and the
machine-readable layer (JSON-LD / llms.txt / sitemap), and a content red-line
list of retired claims that must never reappear.

## Notes

- To refresh the social preview: edit `og-cover.svg`, render it, then convert to
  JPEG (a JPEG keeps this gradient-plus-text image around 88KB, versus ~470KB as
  a PNG). `rsvg-convert` is not installed on this machine, so headless Chrome is
  the working path:
  ```sh
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless \
    --disable-gpu --hide-scrollbars --force-device-scale-factor=1 \
    --screenshot=/tmp/og-cover.png --window-size=1200,630 \
    "file://$PWD/og-cover.svg"
  sips -s format jpeg -s formatOptions 92 /tmp/og-cover.png --out og-cover.jpg
  ```
- To add a new translatable string: put the Chinese in the element's text and add
  `data-en` with the English. Images take `data-en-alt`, ARIA labels take
  `data-en-aria`.
- **`data-en` must only sit on leaf elements.** `js/main.js` replaces
  `textContent`, so tagging an element that contains markup deletes its children
  permanently — the suite asserts this never happens.
- The JSON-LD `@graph` and `llms.txt` are the main GEO levers — keep them in
  sync with the visible page content when career updates land. The suite
  cross-checks book titles, URLs, case figures and the three `Last updated` /
  `dateModified` / `lastmod` dates against each other.
- Every `section[id]` needs a unique id, and each nav link must point at one, or
  the active-section highlight silently stops working.

## License

© 2026 Shi Ke. All rights reserved.
