# 施可 · Shi Ke

Personal homepage. Static HTML/CSS/JS, deployed on GitHub Pages.

**Live:** https://shike.github.io/

## Stack

- Pure HTML / CSS / Vanilla JS — zero dependencies, no build step
- Bilingual (zh-CN / en) — `data-en` attribute pattern + `localStorage` persistence
- Active section highlight via `IntersectionObserver`
- Accessible: skip link, focus styles, `prefers-reduced-motion`, ARIA on mobile nav
- SEO: complete OG / Twitter Card / canonical / hreflang / sitemap / robots
- GEO (Generative Engine Optimization): `llms.txt`, enriched JSON-LD `@graph`
  (Person · WebSite · ProfilePage · FAQPage), permissive AI crawler policy

## Local Development

Open `index.html` directly, or serve over HTTP:

```sh
python3 -m http.server 8000
# then open http://localhost:8000
```

## Structure

```
.
├── index.html               # Page content + meta + JSON-LD
├── css/style.css            # All styles
├── js/main.js               # Nav highlight, mobile menu, i18n
├── og-cover.png             # 1200x630 social preview (PNG)
├── og-cover.svg             # SVG source for the preview
├── sitemap.xml              # Search engine sitemap
├── robots.txt               # Crawler policy (incl. AI bots)
├── llms.txt                 # AI-readable summary for LLM crawlers
├── .lighthouserc.json       # Lighthouse CI thresholds
├── .github/workflows/
│   └── lighthouse.yml       # PR / push Lighthouse audit
├── docs/                    # Original spec & plan
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

## Notes

- To refresh the social preview: edit `og-cover.svg` and regenerate the PNG:
  ```sh
  rsvg-convert -w 1200 -h 630 -o og-cover.png og-cover.svg
  ```
- To add a new translatable string: set the original text in `textContent` /
  `aria-label`, then add `data-en` / `data-en-aria` with the English version;
  `js/main.js` picks it up automatically.
- The JSON-LD `@graph` and `llms.txt` are the main GEO levers — keep them in
  sync with the visible page content when career updates land.

## License

© 2026 Shi Ke. All rights reserved.
