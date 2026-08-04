# Homepage Products, Books & Profile Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Update the static homepage so it presents a professional entrepreneur profile, only the approved SaaS/agency and overseas products, and a new bilingual Books section linked to Shi Ke's two GitHub repositories.

**Architecture:** Keep the existing zero-dependency single-page architecture: content and JSON-LD remain in `index.html`, presentation remains in `css/style.css`, language metadata remains in `js/main.js`, and machine-readable summaries remain in `llms.txt` and `sitemap.xml`. Add a small Python standard-library contract test suite so copy, links, structured data, and removals can be verified without introducing a build system.

**Tech Stack:** HTML5, CSS3 Grid/Flexbox, vanilla JavaScript, JSON-LD/Schema.org, Python 3 standard-library `unittest`, GitHub CLI for copying approved cover assets, Lighthouse CI.

## Global Constraints

- Preserve the zero-dependency static-site architecture; do not add npm packages, a CMS, a runtime API, or a build step.
- Keep all visible copy bilingual through the existing `data-en` / `data-en-aria` mechanism.
- Use the approved professional entrepreneur narrative and the exact Chinese/English copy in the design spec.
- Remove Linhuiba operating metrics and the Alibaba Cloud AI Competition Silver Award from visible content, metadata, JSON-LD, FAQ, and `llms.txt`.
- SaaS & agency products must contain only 微盟星启 GEO and 呼波特 WhoBot.
- Overseas products must contain only NihaoVisit and Liora Moon.
- Books must link to `https://github.com/shike/ai_coding_book` and `https://github.com/shike/FDE-AI-race-isn-t-won-on-models`.
- Store both book covers locally under `assets/books/`; do not hotlink GitHub Raw assets.
- External links must use HTTPS, `target="_blank"`, and `rel="noopener noreferrer"`.
- Images must declare intrinsic dimensions, `loading="lazy"`, descriptive `alt`, and `decoding="async"`.
- Update machine-readable dates to `2026-08-04`.
- Do not commit or push unless the user explicitly asks; each task ends with a diff checkpoint instead.

## File Structure

- Create `tests/test_homepage_content.py` — zero-dependency content contract tests for visible copy, removed claims, product scope, books, JSON-LD, and sitemap.
- Create `assets/books/ai-coding-cover.jpg` — optimized 896×1200 JPEG derivative of the approved cover from `shike/ai_coding_book`.
- Create `assets/books/fde-cover.svg` — local copy of the approved 800×500 main cover from `shike/FDE-AI-race-isn-t-won-on-models`.
- Modify `index.html` — metadata, JSON-LD, navigation, Hero, Ventures, Books, About, stats, and selected Experience copy.
- Modify `css/style.css` — expanded About typography and responsive Books cards.
- Modify `js/main.js` — Chinese/English document title and description used by the language switch.
- Modify `llms.txt` — synchronized identity, career, products, Books, and last-updated content.
- Modify `sitemap.xml` — update homepage `lastmod`.

---

### Task 1: Professional Entrepreneur Profile

**Files:**
- Create: `tests/test_homepage_content.py`
- Modify: `index.html:5-167, 198-203, 292-318, 360-376`
- Modify: `css/style.css:280-329`
- Modify: `js/main.js:5-14`
- Modify: `llms.txt:1-35`

**Interfaces:**
- Consumes: the existing `data-en` and `data-en-aria` language-switch contract from `js/main.js`.
- Produces: final Hero/About/stat/Experience copy and synchronized `META.zh` / `META.en` values that later tasks must preserve.

- [ ] **Step 1: Write failing profile contract tests**

Create `tests/test_homepage_content.py` with:

```python
from pathlib import Path
import json
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]


def read(path):
    return (ROOT / path).read_text(encoding="utf-8")


class PersonalProfileTests(unittest.TestCase):
    def setUp(self):
        self.index = read("index.html")
        self.js = read("js/main.js")
        self.llms = read("llms.txt")

    def test_hero_uses_approved_positioning(self):
        self.assertIn(
            "连续创业者 / 水滴跃动 Dropleap 创始人 / 企业级 AI 实践者",
            self.index,
        )
        self.assertIn(
            "Serial Entrepreneur / Founder of Dropleap / Enterprise AI Practitioner",
            self.index,
        )
        self.assertIn("现聚焦企业级 AI Agent 与 GEO", self.index)

    def test_about_covers_approved_narrative(self):
        required = [
            "16 年职业经历横跨软件工程、互联网产品、创业与企业经营",
            "完成从产品构建、团队组建到机构融资的完整创业过程",
            "可靠性、可观测性、可评估性与持续运营能力",
            "GEO 不只是内容投放或关键词优化",
            "《AI Coding：人人都是程序员》",
            "《FDE：AI 竞赛不在于模型》",
        ]
        for text in required:
            with self.subTest(text=text):
                self.assertIn(text, self.index)

    def test_stats_use_experience_venture_and_books(self):
        self.assertIn("年技术、产品与商业实践", self.index)
        self.assertIn("连续创业与产品构建", self.index)
        self.assertIn("AI 主题著作", self.index)
        self.assertIn(">0→1<", self.index)
        self.assertIn(">2 本<", self.index)

    def test_removed_metrics_and_award_are_absent(self):
        combined = "\n".join((self.index, self.js, self.llms))
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
            self.js,
        )
        self.assertIn(
            "title: 'Shi Ke — Serial Entrepreneur, Founder of Dropleap, Enterprise AI Practitioner'",
            self.js,
        )
        self.assertIn("企业级 AI Agent、GEO 与应用工程", self.js)
```

- [ ] **Step 2: Run the tests and confirm the current copy fails**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: failures for the new Hero/About/stats metadata and failures showing the old Linhuiba metrics and Silver Award are still present.

- [ ] **Step 3: Replace document metadata and language-switch metadata**

In `index.html`, use these final values for `<title>`, description, OG, and Twitter metadata:

```html
<title>施可｜连续创业者、Dropleap 创始人、企业级 AI 实践者</title>
<meta name="description" content="施可，水滴跃动 Dropleap 创始人、连续创业者、中科大软件工程硕士。16 年横跨软件工程、互联网产品与企业经营，现聚焦企业级 AI Agent、GEO 与应用工程。">
<meta property="og:title" content="施可｜连续创业者、Dropleap 创始人、企业级 AI 实践者">
<meta property="og:description" content="施可，水滴跃动 Dropleap 创始人、连续创业者、中科大软件工程硕士。16 年横跨软件工程、互联网产品与企业经营，现聚焦企业级 AI Agent、GEO 与应用工程。">
<meta name="twitter:title" content="施可｜连续创业者、Dropleap 创始人、企业级 AI 实践者">
<meta name="twitter:description" content="施可，水滴跃动 Dropleap 创始人、连续创业者、中科大软件工程硕士。16 年横跨软件工程、互联网产品与企业经营，现聚焦企业级 AI Agent、GEO 与应用工程。">
```

Replace `META` in `js/main.js` with:

```javascript
const META = {
  zh: {
    title: '施可｜连续创业者、Dropleap 创始人、企业级 AI 实践者',
    description: '施可，水滴跃动 Dropleap 创始人、连续创业者、中科大软件工程硕士。16 年横跨软件工程、互联网产品与企业经营，现聚焦企业级 AI Agent、GEO 与应用工程。'
  },
  en: {
    title: 'Shi Ke — Serial Entrepreneur, Founder of Dropleap, Enterprise AI Practitioner',
    description: 'Shi Ke is a serial entrepreneur, founder of Dropleap, and an enterprise AI practitioner with 16 years across software engineering, internet products, and business operations. He now focuses on enterprise AI Agents, GEO, and application engineering.'
  }
};
```

In the Person node, replace the identity fields with these exact values and add GEO to `knowsAbout`:

```json
"jobTitle": "Founder, Serial Entrepreneur, Enterprise AI Practitioner",
"description": "Serial entrepreneur and founder of Dropleap. 16 years across software engineering, internet products, entrepreneurship, and business operations, now focused on enterprise AI Agents, GEO, and application engineering.",
"hasOccupation": {
  "@type": "Occupation",
  "name": "Founder · Serial Entrepreneur · Enterprise AI Practitioner",
  "skills": "Enterprise AI implementation, LLM application engineering, Multi-Agent orchestration, Generative Engine Optimization, RAG, Tool Use, Agent evaluation, product management, and business operations"
}
```

Add this item to `knowsAbout`:

```json
"Generative Engine Optimization"
```

Use these exact descriptions in the WebSite and ProfilePage nodes:

```json
"description": "Personal homepage of Shi Ke — serial entrepreneur, founder of Dropleap, and enterprise AI practitioner."
```

```json
"name": "施可 (Shi Ke) — Serial Entrepreneur and Founder of Dropleap"
```

Replace the first, expertise, and Linhuiba FAQ entries with:

```json
{
  "@type": "Question",
  "name": "Who is Shi Ke (施可)?",
  "acceptedAnswer": {
    "@type": "Answer",
    "text": "Shi Ke (施可) is a serial entrepreneur, founder of Dropleap, former Linhuiba COO, and an MSc graduate in Software Engineering from USTC. His 16-year career spans software engineering, internet products, entrepreneurship, and business operations. He previously built a venture-backed internet sports startup and now focuses on enterprise AI Agents, GEO, and application engineering."
  }
},
{
  "@type": "Question",
  "name": "What is Shi Ke's expertise?",
  "acceptedAnswer": {
    "@type": "Answer",
    "text": "Shi Ke works across enterprise AI implementation, AI Agent and LLM application engineering, Generative Engine Optimization, product 0-to-1 development, and business operations. His approach connects technical boundaries, user value, engineering delivery, and long-term operational outcomes."
  }
},
{
  "@type": "Question",
  "name": "What did Shi Ke do at Linhuiba?",
  "acceptedAnswer": {
    "@type": "Answer",
    "text": "As COO of Linhuiba from 2022 to 2026, Shi Ke led company strategy, cross-functional alignment, and business operations. He built the Location AI site intelligence platform from zero to one, established a joint research center with Zhejiang University, served clients including Xiaomi EV, and advanced new business initiatives from exploration to scaled operations."
  }
}
```

Keep the existing Dropleap and contact FAQ entries, but ensure their wording contains none of the banned claims.

- [ ] **Step 4: Replace Hero, About, stats, and selected Experience copy**

Replace the Hero title and description with:

```html
<p class="hero-title" data-en="Serial Entrepreneur / Founder of Dropleap / Enterprise AI Practitioner">连续创业者 / 水滴跃动 Dropleap 创始人 / 企业级 AI 实践者</p>
<p class="hero-desc" data-en="16 years across software engineering, product innovation, and business operations, building products and organizations from zero to one. Now focused on enterprise AI Agents and GEO—turning emerging technology into deployable, operable, and continuously improving business capabilities.">16 年横跨软件工程、产品创新与商业经营，持续推动从 0 到 1 的产品构建与组织实践。现聚焦企业级 AI Agent 与 GEO，将新技术转化为可交付、可运营、可持续迭代的业务能力。</p>
```

Replace the three stats with:

```html
<ul class="about-stats" aria-label="关键履历数据" data-en-aria="Key career indicators">
  <li class="stat">
    <span class="stat-num">16+</span>
    <span class="stat-label" data-en="Years across technology, product &amp; business">年技术、产品与商业实践</span>
  </li>
  <li class="stat">
    <span class="stat-num">0→1</span>
    <span class="stat-label" data-en="Venture building &amp; product creation">连续创业与产品构建</span>
  </li>
  <li class="stat">
    <span class="stat-num" data-en="2 Books">2 本</span>
    <span class="stat-label" data-en="Books on applied AI">AI 主题著作</span>
  </li>
</ul>
```

Replace `.about-content` with the following complete bilingual block:

```html
<div class="about-content">
  <p data-en="Shi Ke is the founder of Dropleap, a serial entrepreneur, and holds an MSc in Software Engineering from the University of Science and Technology of China. His 16-year career spans software engineering, internet products, entrepreneurship, and business operations. Starting as a software engineer and engineering manager, he later held technology and product roles at NCS (Singtel Group), Tongcheng-Elong, and Hellobike. This path shaped a cross-functional approach: understanding technical boundaries through engineering, defining user value through product thinking, and driving execution through an operator's lens.">施可，水滴跃动（Dropleap）创始人，中国科学技术大学软件工程硕士，连续创业者。16 年职业经历横跨软件工程、互联网产品、创业与企业经营。从软件工程师和技术管理者起步，先后在 NCS（新电信集团）、同程艺龙、哈啰出行等企业承担技术与产品职责，逐步形成以工程能力理解技术边界、以产品思维定义用户价值、以经营视角推动组织落地的复合工作方法。</p>
  <p data-en="He built an internet sports startup from the ground up, taking it through product development, team formation, and institutional funding. He later served as COO of Linhuiba, responsible for corporate strategy, cross-functional alignment, and business operations while advancing digital products and new business initiatives. Working at the intersection of technology, product, and commercial execution taught him to evaluate not only whether a product gets used, but whether its business model, organization, and delivery system can support durable growth.">曾从零创办互联网体育项目，完成从产品构建、团队组建到机构融资的完整创业过程；此后担任邻汇吧 COO，负责公司战略、组织协同与业务经营，并推动数字化产品和新业务的建设。这些经历使其长期工作在技术、产品与商业的交界处，既关注产品能否被真正使用，也关注商业模式、组织能力和交付体系能否支撑长期增长。</p>
  <p data-en="In 2026, he founded Dropleap to focus on enterprise AI Agents, GEO, and application engineering. Drawing on experience across technology, product, and commercial operations, he works with enterprises from use-case discovery and AI strategy through Agent solution design, engineering delivery, and deployment operations. The focus is not merely model capability or proof of concept, but the reliability, observability, evaluability, and long-term operability of AI systems in real business environments—moving AI from demos to reusable, scalable business systems.">2026 年创立水滴跃动，聚焦企业级 AI Agent、GEO 与应用工程。依托跨技术、产品和商业运营的复合经验，为企业提供从场景识别、AI 战略、Agent 方案设计到工程交付和部署运营的端到端服务。关注的不只是模型能力或概念验证，而是 AI 系统在真实业务中的可靠性、可观测性、可评估性与持续运营能力，推动 AI 从演示原型走向可复用、可规模化的业务系统。</p>
  <p data-en="In Generative Engine Optimization, he studies how brands can build knowledge systems that AI search engines can accurately understand, credibly cite, and consistently recommend as AI search becomes a new gateway to user decisions. He views GEO not simply as content distribution or keyword optimization, but as a systems discipline spanning brand facts, content structure, authority signals, and continuous evaluation. He also writes and speaks about AI productization and frontline delivery, and is the author of AI Coding: Everyone Is a Programmer and FDE: The AI Race Isn't Won on Models.">在生成式引擎优化（GEO）方向，持续研究 AI 搜索成为用户决策入口后，品牌如何构建可被模型准确理解、可信引用并稳定推荐的知识体系。GEO 不只是内容投放或关键词优化，而是涉及品牌事实、内容结构、权威信号和持续评估的系统工程。围绕 AI 产品化与一线交付持续写作，著有《AI Coding：人人都是程序员》《FDE：AI 竞赛不在于模型》，并通过行业演讲分享产品、技术与商业实践。</p>
</div>
```

Replace the Dropleap Experience paragraph with:

```html
<p class="timeline-desc" data-en="Focused on enterprise AI implementation. From use-case discovery and AI strategy to Agent solution design, engineering delivery, and deployment operations, Dropleap turns LLMs and AI Agents into reliable, measurable capabilities embedded in real business workflows.">聚焦企业级 AI 落地。从场景识别、AI 战略到 Agent 方案设计、工程交付与部署运营，把大模型与 AI Agent 转化为嵌入真实业务流程、可靠且可衡量的业务能力。</p>
```

Replace the Linhuiba Experience paragraph with:

```html
<p class="timeline-desc" data-en="Led company strategy, cross-functional alignment, and business operations. Built Location, an AI-powered site intelligence platform, from zero to one; established a joint research center with Zhejiang University and served clients including Xiaomi EV; led new business initiatives from exploration to scaled operations.">负责公司战略、组织协同与全面经营；推动 Location 数智化选址平台从 0→1 建设，与浙江大学共建研究中心，服务小米汽车等头部客户；主导新业务从探索走向规模化运营。</p>
```

- [ ] **Step 5: Improve expanded About readability**

Replace the current About rules in `css/style.css` with:

```css
/* About */
.about-content {
  max-width: 800px;
  margin: 0 auto;
  text-align: left;
}

.about-content p {
  font-size: 16px;
  color: var(--text-secondary);
  margin-bottom: 20px;
  line-height: 1.9;
}

.about-content p:last-child {
  margin-bottom: 0;
}
```

- [ ] **Step 6: Synchronize the personal summary in `llms.txt`**

Replace the opening through Expertise with this exact content:

```markdown
# Shi Ke (施可)

> Serial entrepreneur, founder of Dropleap (水滴跃动), and enterprise AI practitioner. 16 years across software engineering, internet products, entrepreneurship, and business operations; now focused on enterprise AI Agents, GEO, and application engineering.

施可 (Shi Ke) is a serial entrepreneur with an MSc in Software Engineering from the University of Science and Technology of China (USTC). His career path spans software engineer → engineering manager → product lead → founder → COO → enterprise AI founder.

## Identity

- **Name**: 施可 (Shi Ke)
- **Role**: Founder, Dropleap (水滴跃动)
- **Positioning**: Serial Entrepreneur / Enterprise AI Practitioner
- **Previous**: COO, Linhuiba (2022–2026)
- **Education**: MSc in Software Engineering, USTC
- **Email**: shike@dropleap.cn
- **Website**: https://shike.github.io/
- **GitHub**: https://github.com/shike

## Current focus

Building Dropleap (水滴跃动), an enterprise AI implementation company focused on AI Agents, GEO, and application engineering. Services span use-case discovery, AI strategy, Agent solution design, engineering delivery, and deployment operations, with an emphasis on reliability, observability, evaluability, and long-term operability in real business environments.

## Career path

- 2026–present — Founder, Dropleap (水滴跃动). Enterprise AI Agents, GEO, application engineering, and end-to-end AI implementation.
- 2022–2026 — COO, Linhuiba. Led company strategy, cross-functional alignment, and business operations. Built the Location AI site intelligence platform from 0→1, established a joint research center with Zhejiang University, served clients including Xiaomi EV, and advanced new business initiatives from exploration to scaled operations.
- 2021–2022 — Product Lead, Hellobike Hotel (Hellobike / 哈啰出行). Core BU decision-maker. Built B-side and C-side product systems and membership growth loops.
- 2016–2021 — Product & Tech Lead, Tongcheng-Elong (HK:0780), International Hotels division.
- 2015–2016 — Founder, Ball Chief Tribe (苏州踢来踢去网络). Built the venture from 0→1 and raised institutional angel funding from Zihui Ventures.
- 2009–2014 — Software Engineer → Tech Manager at NCS (Singtel Group) and Founder International. Delivered enterprise projects including Yum! Brands' franchise development system and completed multiple Singapore implementation assignments.

## Expertise

- **Enterprise AI Implementation**: Use-case discovery, AI strategy, Agent solution design, engineering delivery, deployment operations, reliability, observability, and evaluation
- **AI Agent / LLM Engineering**: LLM application development, Multi-Agent orchestration, Tool Use and Function Calling, RAG, agent evaluation and observability
- **Generative Engine Optimization (GEO)**: Brand facts, content structure, authority signals, and continuous evaluation designed for accurate understanding, credible citation, and consistent recommendation by AI search engines
- **Product 0→1**: User insight → PRD → MVP → scaled iteration through a cross-functional engineering, product, and business lens
- **Venture Building & Business Operations**: Team formation, institutional funding, organizational alignment, enterprise operations, and repeatable delivery systems
- **Writing & Speaking**: Books and industry talks on AI productization, frontline delivery, product methodology, and business practice
```

Preserve the later Brands, Ventures, speaking, and contact sections for Tasks 2 and 4.

- [ ] **Step 7: Run profile tests and review the diff**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
git diff --check
git diff -- index.html css/style.css js/main.js llms.txt tests/test_homepage_content.py
```

Expected: all profile tests pass; `git diff --check` prints nothing; the diff contains no removed metrics or award references outside the design/plan documents.

---

### Task 2: Approved Ventures Scope

**Files:**
- Modify: `tests/test_homepage_content.py`
- Modify: `index.html:10, 229-275`
- Modify: `llms.txt:42-51`

**Interfaces:**
- Consumes: existing `.venture-sub`, `.venture-link`, QR trigger, and bilingual attributes.
- Produces: exactly two SaaS/agency entries and two overseas entries for later global verification.

- [ ] **Step 1: Add failing Ventures tests**

Append to `tests/test_homepage_content.py`:

```python
class VenturesTests(unittest.TestCase):
    def setUp(self):
        self.index = read("index.html")
        self.llms = read("llms.txt")
        self.combined = self.index + "\n" + self.llms

    def test_removed_products_are_absent(self):
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
                self.assertNotIn(text, self.combined)

    def test_approved_products_are_present(self):
        for text in ["微盟星启 GEO", "呼波特 WhoBot", "NihaoVisit", "Liora Moon"]:
            with self.subTest(text=text):
                self.assertIn(text, self.index)
                self.assertIn(text, self.llms)

    def test_liora_moon_uses_verified_copy_and_secure_link(self):
        self.assertIn('href="https://lioramoon.com/"', self.index)
        self.assertIn(
            "AI 塔罗解读平台，提供个性化洞察、每日一牌与 AI 塔罗师对话",
            self.index,
        )
        self.assertIn(
            "AI Tarot reading platform for personalized insights, daily cards, and AI reader chat",
            self.index,
        )
        self.assertRegex(
            self.index,
            r'href="https://lioramoon\.com/"[^>]+target="_blank"[^>]+rel="noopener noreferrer"',
        )
```

- [ ] **Step 2: Run tests and confirm removed products still fail**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: `VenturesTests` fails because 数商方略 and Minibus EV remain and Liora Moon is absent.

- [ ] **Step 3: Replace the two supporting Ventures cards**

Keep the 微盟星启 GEO and 呼波特 WhoBot `<li>` elements unchanged. Delete the 数商方略 `<li>`. Replace the overseas list with:

```html
<ul class="venture-sub-list">
  <li class="venture-sub">
    <div class="venture-sub-head">
      <span class="venture-sub-name">NihaoVisit</span>
      <a class="venture-link" href="https://www.nihaovisit.com/" target="_blank" rel="noopener noreferrer" data-en="Visit ↗">访问 ↗</a>
    </div>
    <p class="venture-sub-desc" data-en="Practical China travel guides for foreign visitors — structured long-form content helping overseas travelers plan their own China trips.">面向外国人的实用中国旅行指南，结构化长文帮海外游客自助规划中国行程。</p>
  </li>
  <li class="venture-sub">
    <div class="venture-sub-head">
      <span class="venture-sub-name">Liora Moon</span>
      <a class="venture-link" href="https://lioramoon.com/" target="_blank" rel="noopener noreferrer" data-en="Visit ↗">访问 ↗</a>
    </div>
    <p class="venture-sub-desc" data-en="AI Tarot reading platform for personalized insights, daily cards, and AI reader chat.">AI 塔罗解读平台，提供个性化洞察、每日一牌与 AI 塔罗师对话。</p>
  </li>
</ul>
```

Replace the keywords meta tag with:

```html
<meta name="keywords" content="施可,Shi Ke,连续创业者,水滴跃动,Dropleap,企业级 AI,AI Agent,LLM 应用,GEO,生成式引擎优化,Multi-Agent,RAG,Tool Use,Agent Eval,产品 0到1,企业经营,微盟星启,呼波特,WhoBot,NihaoVisit,Liora Moon,AI Coding,FDE">
```

- [ ] **Step 4: Synchronize Ventures in `llms.txt`**

Replace the Ventures/product lists with:

```markdown
## Ventures & products

- **NihaoVisit** — https://www.nihaovisit.com/ — Practical China travel guides for foreign visitors; structured long-form content covering major China destinations and on-the-ground tips.
- **Liora Moon** — https://lioramoon.com/ — AI Tarot reading platform for personalized insights, daily cards, and AI reader chat.

## Authorized agent

- **微盟星启 GEO (Weimob Xingqi GEO)** — https://www.xingqigeo.cn/ — Weimob Group's Generative Engine Optimization platform, lifting brand reach and acquisition across AI search engines. Shi Ke is an authorized agent.
- **呼波特 WhoBot** — https://www.whobot.com/ — LLM-powered 24/7 AI phone agent for outbound calling and customer operations. Shi Ke is an authorized agent.
```

- [ ] **Step 5: Run Ventures tests and review the diff**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
git diff --check
git diff -- index.html llms.txt tests/test_homepage_content.py
```

Expected: all tests pass and the removed product names/URLs no longer occur in `index.html` or `llms.txt`.

---

### Task 3: Local Covers and Bilingual Books Section

**Files:**
- Modify: `tests/test_homepage_content.py`
- Create: `assets/books/ai-coding-cover.jpg`
- Create: `assets/books/fde-cover.svg`
- Modify: `index.html:184-191, after the closing Ventures section at line 290`
- Modify: `css/style.css:after venture styles around line 606, mobile rules around line 893`

**Interfaces:**
- Consumes: section header classes, color variables, focus styles, navigation observer, and language-switch attributes.
- Produces: `#books`, `.books-grid`, `.book-card`, `.book-cover-frame`, `.book-cover`, and `.book-link` for final structured-data linkage and visual verification.

- [ ] **Step 1: Add failing Books markup and asset tests**

Append to `tests/test_homepage_content.py`:

```python
class BooksTests(unittest.TestCase):
    def setUp(self):
        self.index = read("index.html")
        self.css = read("css/style.css")

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
        self.assertIn('href="#books"', self.index)
        self.assertIn('data-en="Books">著作</a>', self.index)
        self.assertIn('<section class="section" id="books">', self.index)
        self.assertIn('class="books-grid"', self.index)

    def test_both_books_use_local_covers_and_github_links(self):
        expected = [
            (
                "《AI Coding：人人都是程序员》",
                "AI Coding: Everyone Is a Programmer",
                "assets/books/ai-coding-cover.jpg",
                "https://github.com/shike/ai_coding_book",
            ),
            (
                "《FDE：AI 竞赛不在于模型》",
                "FDE: The AI Race Isn't Won on Models",
                "assets/books/fde-cover.svg",
                "https://github.com/shike/FDE-AI-race-isn-t-won-on-models",
            ),
        ]
        for zh, en, cover, url in expected:
            with self.subTest(book=zh):
                self.assertIn(zh, self.index)
                self.assertIn(en, self.index)
                self.assertIn(f'src="{cover}"', self.index)
                self.assertRegex(
                    self.index,
                    rf'href="{re.escape(url)}"[^>]+target="_blank"[^>]+rel="noopener noreferrer"',
                )

    def test_books_styles_include_responsive_grid(self):
        for selector in [
            ".books-grid",
            ".book-card",
            ".book-cover-frame",
            ".book-cover",
            ".book-link",
        ]:
            with self.subTest(selector=selector):
                self.assertIn(selector, self.css)
```

- [ ] **Step 2: Run tests and confirm assets/section are missing**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: Books tests fail because `assets/books/` and `#books` do not exist.

- [ ] **Step 3: Copy the two approved covers from GitHub**

Run:

```bash
mkdir -p assets/books
AI_SHA=$(gh api 'repos/shike/ai_coding_book/contents/promotion/cover.png' --jq .sha)
FDE_SHA=$(gh api 'repos/shike/FDE-AI-race-isn-t-won-on-models/contents/html/covers/main-cover.svg' --jq .sha)
gh api -H 'Accept: application/vnd.github.raw' "repos/shike/ai_coding_book/git/blobs/$AI_SHA" > /tmp/ai-coding-cover-source
gh api -H 'Accept: application/vnd.github.raw' "repos/shike/FDE-AI-race-isn-t-won-on-models/git/blobs/$FDE_SHA" > assets/books/fde-cover.svg
sips -Z 1200 -s format jpeg -s formatOptions 85 /tmp/ai-coding-cover-source --out assets/books/ai-coding-cover.jpg >/dev/null
```

The upstream file is named `cover.png` but contains JPEG bytes. Keep JPEG as the local format, resize proportionally to 896×1200 with quality 85, and use a matching `.jpg` extension. This preserves the artwork without cropping while reducing the lazy-loaded asset to roughly 132 KB.

Then run:

```bash
file assets/books/ai-coding-cover.jpg assets/books/fde-cover.svg
```

Expected: one JPEG image smaller than 250 KB and one SVG document; the HTML declares 896×1200 and 800×500 intrinsic dimensions.

- [ ] **Step 4: Add the Books navigation item and section**

Add this navigation item immediately after Ventures:

```html
<li><a href="#books" class="nav-link" data-en="Books">著作</a></li>
```

Insert after Ventures and before About:

```html
<!-- Books -->
<section class="section" id="books">
  <div class="container">
    <div class="section-header">
      <span class="section-label" data-en="BOOKS">著作</span>
      <h2 class="section-title" data-en="Books">出版与写作</h2>
    </div>
    <div class="books-grid">
      <article class="book-card">
        <div class="book-cover-frame">
          <img class="book-cover" src="assets/books/ai-coding-cover.jpg" alt="《AI Coding：人人都是程序员》封面" width="896" height="1200" loading="lazy" decoding="async">
        </div>
        <div class="book-content">
          <h3 data-en="AI Coding: Everyone Is a Programmer">《AI Coding：人人都是程序员》</h3>
          <p data-en="Helping non-technical builders ship real products with AI.">让非技术人做出可交付的产品。</p>
          <a class="book-link" href="https://github.com/shike/ai_coding_book" target="_blank" rel="noopener noreferrer" data-en="Read on GitHub ↗">在 GitHub 阅读 ↗</a>
        </div>
      </article>
      <article class="book-card">
        <div class="book-cover-frame">
          <img class="book-cover" src="assets/books/fde-cover.svg" alt="《FDE：AI 竞赛不在于模型》封面" width="800" height="500" loading="lazy" decoding="async">
        </div>
        <div class="book-content">
          <h3 data-en="FDE: The AI Race Isn't Won on Models">《FDE：AI 竞赛不在于模型》</h3>
          <p data-en="Why AI projects are won in deployment, not just model selection.">AI 项目的胜负，在部署，不只在模型。</p>
          <a class="book-link" href="https://github.com/shike/FDE-AI-race-isn-t-won-on-models" target="_blank" rel="noopener noreferrer" data-en="Read on GitHub ↗">在 GitHub 阅读 ↗</a>
        </div>
      </article>
    </div>
  </div>
</section>
```

- [ ] **Step 5: Add Books styles and responsive behavior**

Add after the Ventures styles:

```css
/* Books */
.books-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 24px;
}

.book-card {
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 28px;
  display: flex;
  flex-direction: column;
  box-shadow: 0 1px 3px rgba(0,0,0,0.04);
  transition: box-shadow 0.3s, transform 0.3s, border-color 0.3s;
}

.book-card:hover {
  box-shadow: 0 12px 40px rgba(79,70,229,0.1);
  transform: translateY(-6px);
  border-color: rgba(79,70,229,0.15);
}

.book-cover-frame {
  height: 280px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 24px;
  padding: 16px;
  overflow: hidden;
  background: var(--bg-tertiary);
  border-radius: 8px;
}

.book-cover {
  display: block;
  width: auto;
  max-width: 100%;
  height: 100%;
  object-fit: contain;
}

.book-content {
  display: flex;
  flex: 1;
  flex-direction: column;
}

.book-content h3 {
  font-size: 20px;
  line-height: 1.45;
  margin-bottom: 12px;
}

.book-content p {
  flex: 1;
  color: var(--text-secondary);
  font-size: 14px;
  line-height: 1.7;
  margin-bottom: 18px;
}

.book-link {
  align-self: flex-start;
  font-size: 14px;
  font-weight: 600;
}
```

Extend the reduced-motion selector to:

```css
.skill-card:hover,
.project-card:hover,
.book-card:hover,
.client-tag:hover,
a.contact-link:hover {
  transform: none;
}
```

Extend the mobile grid selector and add the cover height inside `@media (max-width: 768px)`:

```css
.skills-grid,
.ventures-grid,
.books-grid,
.track-grid {
  grid-template-columns: 1fr;
}

.book-cover-frame {
  height: 240px;
}
```

- [ ] **Step 6: Run Books tests and review the diff**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
git diff --check
git status --short
git diff -- index.html css/style.css tests/test_homepage_content.py
```

Expected: all tests pass; the two cover files appear as new assets; the Books section is after Ventures and before About; the FDE landscape SVG is contained without distortion inside the fixed-height frame.

---

### Task 4: Structured Data, LLM Summary, and Sitemap

**Files:**
- Modify: `tests/test_homepage_content.py`
- Modify: `index.html:48-170`
- Modify: `llms.txt:after Authorized agent, final Last updated line`
- Modify: `sitemap.xml:5`

**Interfaces:**
- Consumes: the final Book URLs, local cover paths, titles, author Person `@id`, and approved profile/product copy.
- Produces: parseable Book JSON-LD nodes, a synchronized Books summary for LLM crawlers, and the final modification date.

- [ ] **Step 1: Add failing machine-readable tests**

Append to `tests/test_homepage_content.py`:

```python
class MachineReadableTests(unittest.TestCase):
    def setUp(self):
        self.index = read("index.html")
        self.llms = read("llms.txt")

    def json_ld_graph(self):
        match = re.search(
            r'<script type="application/ld\+json">\s*(.*?)\s*</script>',
            self.index,
            re.DOTALL,
        )
        self.assertIsNotNone(match)
        return json.loads(match.group(1))["@graph"]

    def test_json_ld_contains_two_books_linked_to_person(self):
        books = [node for node in self.json_ld_graph() if node.get("@type") == "Book"]
        self.assertEqual(len(books), 2)
        by_url = {book["url"]: book for book in books}
        expected = {
            "https://github.com/shike/ai_coding_book": "https://shike.github.io/assets/books/ai-coding-cover.jpg",
            "https://github.com/shike/FDE-AI-race-isn-t-won-on-models": "https://shike.github.io/assets/books/fde-cover.svg",
        }
        self.assertEqual(set(by_url), set(expected))
        for url, image in expected.items():
            with self.subTest(url=url):
                self.assertEqual(by_url[url]["author"], {"@id": "https://shike.github.io/#person"})
                self.assertEqual(by_url[url]["image"], image)
                self.assertEqual(by_url[url]["inLanguage"], "zh-CN")

    def test_profile_and_sitemap_dates_are_current(self):
        self.assertIn('"dateModified": "2026-08-04"', self.index)
        root = ET.parse(ROOT / "sitemap.xml").getroot()
        namespace = {"s": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        self.assertEqual(root.find("s:url/s:lastmod", namespace).text, "2026-08-04")

    def test_llms_summary_contains_books_and_current_date(self):
        self.assertIn("## Books", self.llms)
        self.assertIn("https://github.com/shike/ai_coding_book", self.llms)
        self.assertIn("https://github.com/shike/FDE-AI-race-isn-t-won-on-models", self.llms)
        self.assertIn("Last updated: 2026-08-04", self.llms)
```

- [ ] **Step 2: Run tests and confirm Book JSON-LD/date coverage fails**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: failures for missing Book nodes, the old `dateModified`, the old sitemap `lastmod`, and the missing `## Books` summary.

- [ ] **Step 3: Add two Book nodes to the JSON-LD graph**

Append these nodes to `@graph` after the existing FAQPage node, preserving valid commas:

```json
{
  "@type": "Book",
  "@id": "https://shike.github.io/#book-ai-coding",
  "name": "AI Coding：人人都是程序员",
  "alternateName": "AI Coding: Everyone Is a Programmer",
  "description": "让非技术人做出可交付的产品",
  "inLanguage": "zh-CN",
  "url": "https://github.com/shike/ai_coding_book",
  "image": "https://shike.github.io/assets/books/ai-coding-cover.jpg",
  "author": { "@id": "https://shike.github.io/#person" }
},
{
  "@type": "Book",
  "@id": "https://shike.github.io/#book-fde",
  "name": "FDE：AI 竞赛不在于模型",
  "alternateName": "FDE: The AI Race Isn't Won on Models",
  "description": "AI 项目的胜负，在部署，不只在模型",
  "inLanguage": "zh-CN",
  "url": "https://github.com/shike/FDE-AI-race-isn-t-won-on-models",
  "image": "https://shike.github.io/assets/books/fde-cover.svg",
  "author": { "@id": "https://shike.github.io/#person" }
}
```

Change ProfilePage `dateModified` to `2026-08-04`.

- [ ] **Step 4: Add Books to `llms.txt` and update dates**

Add after Authorized agent:

```markdown
## Books

- **AI Coding: Everyone Is a Programmer (《AI Coding：人人都是程序员》)** — https://github.com/shike/ai_coding_book — A practical guide for non-technical builders who want to ship real, payable, and maintainable products with AI.
- **FDE: The AI Race Isn't Won on Models (《FDE：AI 竞赛不在于模型》)** — https://github.com/shike/FDE-AI-race-isn-t-won-on-models — A field guide to taking AI projects from proof of concept through engineering delivery, deployment, and sustained operations.
```

Change the final line to:

```text
Last updated: 2026-08-04
```

Change `sitemap.xml` to:

```xml
<lastmod>2026-08-04</lastmod>
```

- [ ] **Step 5: Run machine-readable tests and parse checks**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 -c 'import json,pathlib; s=pathlib.Path("index.html").read_text(); payload=s.split("<script type=\"application/ld+json\">",1)[1].split("</script>",1)[0]; json.loads(payload); print("JSON-LD valid")'
python3 -c 'import xml.etree.ElementTree as ET; ET.parse("sitemap.xml"); print("sitemap valid")'
git diff --check
```

Expected: all tests pass, followed by `JSON-LD valid`, `sitemap valid`, and no `git diff --check` output.

---

### Task 5: End-to-End Verification

**Files:**
- Verify: `index.html`
- Verify: `css/style.css`
- Verify: `js/main.js`
- Verify: `llms.txt`
- Verify: `sitemap.xml`
- Verify: `assets/books/*`
- Verify: `tests/test_homepage_content.py`

**Interfaces:**
- Consumes: all previous tasks.
- Produces: verified static-site behavior with no content drift or responsive regressions.

- [ ] **Step 1: Run the complete contract suite**

Run:

```bash
python3 -m unittest discover -s tests -p 'test_*.py' -v
```

Expected: every profile, Ventures, Books, and machine-readable test passes.

- [ ] **Step 2: Run static diff and banned-content checks**

Run:

```bash
git diff --check
rg -n '\+80%|-15%|-60%|业绩增长 80%|成本下降 15%|应收下降 60%|阿里云 AI 大赛银奖|Alibaba Cloud AI Competition Silver Award|数商方略|Shushang Fanglue|乐奇 Minibus EV|Leqi Minibus EV' index.html js/main.js llms.txt
```

Expected: `git diff --check` prints nothing; `rg` exits with code 1 and prints no matches.

- [ ] **Step 3: Smoke-test the served site**

Run as one shell command:

```bash
python3 -m http.server 8000 --bind 127.0.0.1 >/tmp/shike-homepage-http.log 2>&1 & SERVER_PID=$!; trap 'kill $SERVER_PID 2>/dev/null || true' EXIT; sleep 1; curl --fail --silent --show-error --output /dev/null http://127.0.0.1:8000/; curl --fail --silent --show-error --output /dev/null http://127.0.0.1:8000/assets/books/ai-coding-cover.jpg; curl --fail --silent --show-error --output /dev/null http://127.0.0.1:8000/assets/books/fde-cover.svg; kill $SERVER_PID; trap - EXIT
```

Expected: exit code 0 and no output.

- [ ] **Step 4: Verify real-page behavior and responsive layout**

Invoke the project `run` skill, open the served homepage, and check these exact states:

1. 1024px and wide desktop: Books is a two-column grid; both covers are contained without stretching; seven nav items fit without overlap.
2. 768px and 320px: mobile navigation opens/closes; Books is one column; no horizontal scroll.
3. Chinese mode: all approved Chinese Hero/About/Books/Liora Moon copy is visible.
4. English mode: Hero, About, stats, Books headings/descriptions/CTA, navigation, and metadata switch to English with no blank text.
5. Navigation: `#books` highlights when the Books section crosses the observer midpoint.
6. Links: Liora Moon and both GitHub repository links open the intended HTTPS destinations in new tabs.

Expected: all six checks pass without layout shift, cropped text, distorted images, or console errors.

- [ ] **Step 5: Run Lighthouse CI locally**

Run:

```bash
npx --yes @lhci/cli autorun --config=.lighthouserc.json
```

Expected: accessibility and SEO meet the configured error thresholds of 0.95; performance and best-practices meet the configured warning thresholds of 0.90. If network policy prevents installing `@lhci/cli`, report that local Lighthouse was skipped and rely on the existing GitHub Actions workflow after the user chooses to push.

- [ ] **Step 6: Review final working tree without committing**

Run:

```bash
git status --short
git diff --stat
git diff -- index.html css/style.css js/main.js llms.txt sitemap.xml tests/test_homepage_content.py
```

Expected: only the approved source, asset, test, spec, and plan files are changed; `.superpowers/` remains ignored; no commit or push occurs without explicit user authorization.
