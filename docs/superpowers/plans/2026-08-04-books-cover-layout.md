# Books Cover Layout Refinement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give both book cards a shared 3:4 cover stage so the portrait AI Coding cover and landscape FDE cover have consistent visual weight without cropping or distortion.

**Architecture:** Keep the existing two-column/one-column Books markup and local assets unchanged. Change only the Books-specific CSS so the frame, not the source image, establishes the visual rhythm; use intrinsic image sizing with `max-width`/`max-height` and `object-fit: contain` so each source ratio remains intact. Extend the existing stdlib contract tests with a small CSS contract for the shared frame.

**Tech Stack:** CSS3 Grid/Flexbox, CSS `aspect-ratio`, vanilla HTML image sizing, Python 3 standard-library `unittest`.

## Global Constraints

- Only modify `css/style.css` and `tests/test_homepage_content.py` during implementation.
- Do not modify `index.html`, image assets, JSON-LD, product content, or other sections.
- Keep the existing Books two-column desktop and one-column mobile grid.
- Use a fixed 3:4 cover stage with maximum desktop width approximately 240px and mobile width approximately 220px.
- Keep both source images complete: no cropping, stretching, or replacement.
- Preserve `loading="lazy"`, `decoding="async"`, local asset paths, book links, bilingual copy, and existing card bottom alignment.
- Do not add dependencies, a build step, or a new component system.
- Do not commit or push unless explicitly authorized; the implementation branch is `fix/books-cover-layout`.

---

### Task 1: Add the Cover-Layout Contract and Refine Books CSS

**Files:**
- Modify: `tests/test_homepage_content.py:173-182`
- Modify: `css/style.css:610-655, mobile Books rule near the existing max-width 768px block`

**Interfaces:**
- Consumes: existing `.books-grid`, `.book-card`, `.book-cover-frame`, `.book-cover`, and `.book-link` selectors.
- Produces: a shared `.book-cover-frame` with `width: min(100%, 240px)`, `aspect-ratio: 3 / 4`, and a mobile max width of `220px`; `.book-cover` keeps its natural ratio while remaining fully inside the frame.

- [ ] **Step 1: Add a failing CSS contract test**

Extend `BooksTests.test_books_styles_include_responsive_grid` in `tests/test_homepage_content.py` with a separate test:

```python
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
```

- [ ] **Step 2: Run the targeted test and confirm it fails for the old frame**

Run:

```bash
PYTHONPATH=tests python3 -m unittest test_homepage_content.BooksTests.test_cover_stage_is_shared_portrait_frame -v
```

Expected: FAIL because the current `.book-cover-frame` has only `height: 280px` and the current `.book-cover` uses `height: 100%` rather than intrinsic `max-height` sizing.

- [ ] **Step 3: Implement the shared 3:4 frame**

Replace the Books frame/image rules in `css/style.css` with:

```css
.book-cover-frame {
  width: min(100%, 240px);
  aspect-ratio: 3 / 4;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 24px;
  padding: 20px;
  overflow: hidden;
  background: var(--bg-tertiary);
  border-radius: 8px;
}

.book-cover {
  display: block;
  width: auto;
  max-width: 100%;
  height: auto;
  max-height: 100%;
  object-fit: contain;
}
```

Inside the existing `@media (max-width: 768px)` block, replace the current `.book-cover-frame { height: 240px; }` rule with:

```css
.book-cover-frame {
  width: min(100%, 220px);
}
```

Do not change `.books-grid`, `.book-card`, `.book-link`, or any HTML.

- [ ] **Step 4: Run the targeted test and then the complete contract suite**

Run:

```bash
PYTHONPATH=tests python3 -m unittest test_homepage_content.BooksTests.test_cover_stage_is_shared_portrait_frame -v
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: the targeted test passes, then all existing contract tests pass with 15+ total tests and zero failures.

- [ ] **Step 5: Check the diff scope**

Run:

```bash
git diff --check
git status --short
git diff --stat
```

Expected: only `css/style.css` and `tests/test_homepage_content.py` are modified; no HTML, asset, metadata, or unrelated-section changes appear.

---

### Task 2: Browser Verification of the Visual Fix

**Files:**
- Verify: `css/style.css`
- Verify: `tests/test_homepage_content.py`

**Interfaces:**
- Consumes: Task 1’s shared frame and intrinsic image sizing.
- Produces: evidence that both cards render equal cover-frame dimensions, images remain contained, and the layout remains responsive.

- [ ] **Step 1: Serve the static site**

Run:

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

- [ ] **Step 2: Drive Chromium at the required viewports**

Use the existing temporary Playwright verification flow to inspect 1024px, 768px, and 320px. For each viewport, evaluate:

```javascript
const frames = [...document.querySelectorAll('.book-cover-frame')].map(el => {
  const box = el.getBoundingClientRect();
  return { width: box.width, height: box.height, ratio: box.width / box.height };
});
const images = [...document.querySelectorAll('.book-cover')].map(el => {
  const box = el.getBoundingClientRect();
  const frame = el.parentElement.getBoundingClientRect();
  return {
    width: box.width,
    height: box.height,
    frameWidth: frame.width,
    frameHeight: frame.height,
    objectFit: getComputedStyle(el).objectFit,
  };
});
```

Assert:

- both frame widths and heights are equal at the same viewport;
- each frame ratio is approximately `0.75`;
- each image has `objectFit === "contain"`;
- each image stays within its frame bounds;
- 1024px remains two columns, 768px and 320px remain one column;
- no horizontal overflow or console errors occurs.

- [ ] **Step 3: Inspect screenshots before finishing**

Capture the Books section at 1024px and 320px. Confirm the AI Coding cover is centered in the same portrait stage as FDE, the FDE artwork is fully visible with intentional surrounding space, and the title/description/CTA blocks remain aligned.

- [ ] **Step 4: Clean up temporary server/output and run final checks**

Stop the local server, then run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
git diff --check
git status --short
```

Expected: all tests pass, diff formatting is clean, and only the two planned files remain modified.

## Scope Review

- No new asset, HTML, metadata, product, or JavaScript work is required.
- The existing 3:4 frame is the single layout abstraction for both source ratios; no per-book special case is introduced.
- The browser check covers the visual behavior that a text-only contract cannot prove.
- No commit or push is part of this plan unless the user separately authorizes it.
