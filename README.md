# 施可 · Shi Ke

Personal homepage. Static HTML/CSS/JS, deployed on GitHub Pages.

**Live:** https://shike.github.io/

## Stack

- Pure HTML / CSS / Vanilla JS — zero dependencies, no build step
- Bilingual (zh-CN / en) — `data-en` attribute pattern + `localStorage` persistence
- Active section highlight via `IntersectionObserver`
- Accessible: skip link, focus styles, `prefers-reduced-motion`, ARIA on mobile nav
- SEO: complete OG / Twitter Card / canonical / hreflang / JSON-LD `Person` schema

## Local Development

Open `index.html` directly, or serve over HTTP:

```sh
python3 -m http.server 8000
# then open http://localhost:8000
```

## Structure

```
.
├── index.html       # Single-page content + meta
├── css/style.css    # All styles
├── js/main.js       # Nav highlight, mobile menu, i18n switching
├── og-cover.svg     # 1200x630 Open Graph preview image
├── docs/            # Original spec & plan
└── README.md
```

## Deploy

Pushed to `main`; GitHub Pages serves automatically from the root.

## Notes

- The Open Graph image is `og-cover.svg`. If a social platform requires PNG, export the SVG to `og-cover.png` and update the `og:image` / `twitter:image` URLs in `index.html`.
- `i18n` does not localize attribute values that lack `data-en` or `data-en-aria`. To add a new translatable string, set both the original text (in `textContent` or `aria-label`) and the English version in the corresponding attribute, then `js/main.js` will pick it up.

## License

© 2026 Shi Ke. All rights reserved.
