# GitHub 个人主页 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 构建一个部署在 GitHub Pages 上的单页滚动式个人主页，纯 HTML/CSS/JS，中英双语。

**Architecture:** 单文件 HTML 结构，CSS 变量控制主题，JS 处理导航高亮和中英切换。无构建步骤，GitHub Pages 原生部署。

**Tech Stack:** HTML5, CSS3 (CSS Variables, Flexbox, Grid, IntersectionObserver), Vanilla JavaScript

---

## File Structure

```
github-homepage/
├── index.html          # 完整页面结构 + 内容
├── css/
│   └── style.css       # 全部样式：重置、变量、布局、组件、响应式
├── js/
│   └── main.js         # 导航高亮、平滑滚动、中英切换、移动菜单
└── assets/
    └── (empty - no avatar provided)
```

---

### Task 1: 创建基础文件结构

**Files:**
- Create: `index.html`
- Create: `css/style.css`
- Create: `js/main.js`

- [ ] **Step 1: 创建 index.html 骨架**

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>施可 - 个人主页</title>
  <link rel="stylesheet" href="css/style.css">
</head>
<body>
  <!-- Navigation -->
  <!-- Hero -->
  <!-- About -->
  <!-- Skills -->
  <!-- Experience -->
  <!-- Speaking -->
  <!-- Projects -->
  <!-- Contact -->
  <!-- Footer -->
  <script src="js/main.js"></script>
</body>
</html>
```

- [ ] **Step 2: 创建空的 css/style.css**

```css
/* CSS Reset & Variables */
```

- [ ] **Step 3: 创建空的 js/main.js**

```javascript
// Main JavaScript
```

- [ ] **Step 4: Commit**

```bash
git add index.html css/style.css js/main.js
git commit -m "chore: create project file structure"
```

---

### Task 2: 编写 CSS 基础样式

**Files:**
- Modify: `css/style.css`

- [ ] **Step 1: 添加 CSS Reset 和变量**

```css
/* Reset */
*, *::before, *::after {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

html {
  scroll-behavior: smooth;
}

/* CSS Variables */
:root {
  --bg-primary: #ffffff;
  --bg-secondary: #f9fafb;
  --bg-nav: #111827;
  --text-primary: #111827;
  --text-secondary: #6b7280;
  --text-muted: #9ca3af;
  --accent: #2563eb;
  --accent-hover: #1d4ed8;
  --border: #e5e7eb;
  --max-width: 1100px;
  --section-padding: 80px;
  --font-family: -apple-system, "PingFang SC", "Microsoft YaHei", sans-serif;
}

body {
  font-family: var(--font-family);
  color: var(--text-primary);
  line-height: 1.75;
  background: var(--bg-primary);
}

a {
  color: var(--accent);
  text-decoration: none;
}

a:hover {
  color: var(--accent-hover);
}

.container {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 24px;
}
```

- [ ] **Step 2: 验证样式已保存**

Run: `wc -l css/style.css`
Expected: 至少 40 行

- [ ] **Step 3: Commit**

```bash
git add css/style.css
git commit -m "feat: add CSS reset and variables"
```

---

### Task 3: 构建导航栏 HTML 和样式

**Files:**
- Modify: `index.html`
- Modify: `css/style.css`

- [ ] **Step 1: 在 index.html body 开头添加导航栏**

```html
<nav class="navbar" id="navbar">
  <div class="nav-container">
    <a href="#" class="nav-logo">施可</a>
    <button class="nav-toggle" id="navToggle" aria-label="切换菜单">
      <span></span>
      <span></span>
      <span></span>
    </button>
    <ul class="nav-menu" id="navMenu">
      <li><a href="#about" class="nav-link" data-zh="关于" data-en="About">关于</a></li>
      <li><a href="#experience" class="nav-link" data-zh="履历" data-en="Experience">履历</a></li>
      <li><a href="#speaking" class="nav-link" data-zh="演讲" data-en="Speaking">演讲</a></li>
      <li><a href="#projects" class="nav-link" data-zh="项目" data-en="Projects">项目</a></li>
      <li><a href="#contact" class="nav-link" data-zh="联系" data-en="Contact">联系</a></li>
    </ul>
    <button class="lang-switch" id="langSwitch" data-zh="EN" data-en="中">EN</button>
  </div>
</nav>
```

- [ ] **Step 2: 在 css/style.css 末尾添加导航样式**

```css
/* Navigation */
.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: var(--bg-nav);
  z-index: 1000;
  transition: box-shadow 0.3s;
}

.nav-container {
  max-width: var(--max-width);
  margin: 0 auto;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 60px;
}

.nav-logo {
  color: #fff;
  font-size: 20px;
  font-weight: 700;
}

.nav-logo:hover {
  color: #fff;
}

.nav-menu {
  display: flex;
  list-style: none;
  gap: 32px;
}

.nav-link {
  color: rgba(255,255,255,0.8);
  font-size: 14px;
  font-weight: 500;
  transition: color 0.2s;
  position: relative;
}

.nav-link:hover,
.nav-link.active {
  color: #fff;
}

.nav-link.active::after {
  content: '';
  position: absolute;
  bottom: -4px;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--accent);
}

.lang-switch {
  background: transparent;
  border: 1px solid rgba(255,255,255,0.3);
  color: #fff;
  padding: 4px 12px;
  border-radius: 4px;
  cursor: pointer;
  font-size: 13px;
  transition: all 0.2s;
}

.lang-switch:hover {
  border-color: #fff;
}

.nav-toggle {
  display: none;
  background: none;
  border: none;
  cursor: pointer;
  flex-direction: column;
  gap: 4px;
}

.nav-toggle span {
  display: block;
  width: 22px;
  height: 2px;
  background: #fff;
  transition: all 0.3s;
}
```

- [ ] **Step 3: 用浏览器打开 index.html 验证导航栏显示**

Run: `open /Users/shike/github-homepage/index.html`
Expected: 看到深色导航栏，左侧"施可"，右侧导航链接，最右"EN"按钮

- [ ] **Step 4: Commit**

```bash
git add index.html css/style.css
git commit -m "feat: add navbar with navigation links"
```

---

### Task 4: 构建 Hero 区域

**Files:**
- Modify: `index.html`
- Modify: `css/style.css`

- [ ] **Step 1: 在导航后添加 Hero 区域**

```html
<section class="hero" id="hero">
  <div class="container">
    <h1 class="hero-name" data-zh="施可" data-en="Shi Ke">施可</h1>
    <p class="hero-title" data-zh="邻汇吧 &amp; 可计算开店科技 副总裁" data-en="VP at Linhuiba &amp; Kejisuan">邻汇吧 &amp; 可计算开店科技 副总裁</p>
    <p class="hero-desc" data-zh="专注线下体验营销与商业空间运营，推动「开小、开灵活、可计算」的慢闪店新模式" data-en="Focused on offline experiential marketing &amp; commercial space operations, pioneering the new 'Small, Flexible, Measurable' slow-pop-up model">专注线下体验营销与商业空间运营，推动「开小、开灵活、可计算」的慢闪店新模式</p>
  </div>
</section>
```

- [ ] **Step 2: 添加 Hero 样式**

```css
/* Hero */
.hero {
  padding-top: 140px;
  padding-bottom: var(--section-padding);
  background: var(--bg-secondary);
  text-align: center;
}

.hero-name {
  font-size: 48px;
  font-weight: 700;
  margin-bottom: 12px;
  letter-spacing: 2px;
}

.hero-title {
  font-size: 20px;
  color: var(--text-secondary);
  margin-bottom: 16px;
  font-weight: 500;
}

.hero-desc {
  font-size: 16px;
  color: var(--text-secondary);
  max-width: 600px;
  margin: 0 auto;
  line-height: 1.8;
}
```

- [ ] **Step 3: 刷新浏览器验证 Hero 显示**

Expected: 看到大标题"施可"，副标题职位，描述文字居中

- [ ] **Step 4: Commit**

```bash
git add index.html css/style.css
git commit -m "feat: add hero section"
```

---

### Task 5: 构建关于我区块

**Files:**
- Modify: `index.html`
- Modify: `css/style.css`

- [ ] **Step 1: 添加关于我区块**

```html
<section class="section" id="about">
  <div class="container">
    <div class="section-header">
      <span class="section-label" data-zh="关于我" data-en="ABOUT">关于我</span>
      <h2 class="section-title" data-zh="个人简介" data-en="Personal Profile">个人简介</h2>
    </div>
    <div class="about-content">
      <p data-zh="我是施可，现任邻汇吧及可计算开店科技副总裁。多年来深耕线下商业空间运营领域，致力于通过数据化手段重塑线下渠道价值。" data-en="I am Shi Ke, currently VP at Linhuiba and Kejisuan. For years I've been deeply involved in offline commercial space operations, dedicated to reshaping offline channel value through data-driven approaches.">我是施可，现任邻汇吧及可计算开店科技副总裁。多年来深耕线下商业空间运营领域，致力于通过数据化手段重塑线下渠道价值。</p>
      <p data-zh="我主导的「开小、开灵活、可计算」慢闪店模式，已帮助众多品牌实现从0到1、从1到100的线下渠道扩张。邻汇吧平台覆盖全国100+城市，累计服务10,000+品牌，落地60万+商业空间案例。" data-en="The 'Small, Flexible, Measurable' slow-pop-up model I've championed has helped numerous brands expand offline channels from 0 to 1 and from 1 to 100. Linhuiba covers 100+ cities nationwide, serving 10,000+ brands with 600,000+ commercial space cases.">我主导的「开小、开灵活、可计算」慢闪店模式，已帮助众多品牌实现从0到1、从1到100的线下渠道扩张。邻汇吧平台覆盖全国100+城市，累计服务10,000+品牌，落地60万+商业空间案例。</p>
      <p data-zh="我相信，线下商业正从「人找货」转向「货找人」，大型购物中心已成为核心流量池。通过灵活租期、精准选址和数据复盘，品牌可以用更轻的资产、更低的成本触达目标人群。" data-en="I believe offline commerce is shifting from 'people finding products' to 'products finding people.' Major shopping centers have become core traffic pools. Through flexible leases, precise site selection, and data-driven reviews, brands can reach target audiences with lighter assets and lower costs.">我相信，线下商业正从「人找货」转向「货找人」，大型购物中心已成为核心流量池。通过灵活租期、精准选址和数据复盘，品牌可以用更轻的资产、更低的成本触达目标人群。</p>
    </div>
  </div>
</section>
```

- [ ] **Step 2: 添加区块通用样式和关于我样式**

```css
/* Section Common */
.section {
  padding: var(--section-padding) 0;
}

.section:nth-child(even) {
  background: var(--bg-secondary);
}

.section-header {
  margin-bottom: 40px;
}

.section-label {
  display: block;
  font-size: 12px;
  font-weight: 600;
  color: var(--accent);
  text-transform: uppercase;
  letter-spacing: 2px;
  margin-bottom: 8px;
}

.section-title {
  font-size: 28px;
  font-weight: 600;
  color: var(--text-primary);
}

/* About */
.about-content p {
  font-size: 16px;
  color: var(--text-secondary);
  margin-bottom: 16px;
  max-width: 720px;
}
```

- [ ] **Step 3: 刷新浏览器验证**

Expected: "关于我"区块显示，有蓝色小标签、大标题、三段文字

- [ ] **Step 4: Commit**

```bash
git add index.html css/style.css
git commit -m "feat: add about section"
```

---

### Task 6: 构建技能栈区块

**Files:**
- Modify: `index.html`
- Modify: `css/style.css`

- [ ] **Step 1: 添加技能栈区块**

```html
<section class="section" id="skills">
  <div class="container">
    <div class="section-header">
      <span class="section-label" data-zh="技能栈" data-en="SKILLS">技能栈</span>
      <h2 class="section-title" data-zh="核心能力" data-en="Core Competencies">核心能力</h2>
    </div>
    <div class="skills-grid">
      <div class="skill-card">
        <h3 data-zh="商业空间运营" data-en="Commercial Space Operations">商业空间运营</h3>
        <p data-zh="购物中心、社区、写字楼等多元商业空间的标准化整合与运营管理" data-en="Standardized integration and operations management of diverse commercial spaces">购物中心、社区、写字楼等多元商业空间的标准化整合与运营管理</p>
      </div>
      <div class="skill-card">
        <h3 data-zh="线下体验营销" data-en="Offline Experiential Marketing">线下体验营销</h3>
        <p data-zh="快闪店、慢闪店、地推等线下营销活动全链路策划与执行" data-en="Full-cycle planning and execution of pop-up stores, slow-pop-ups, and ground promotions">快闪店、慢闪店、地推等线下营销活动全链路策划与执行</p>
      </div>
      <div class="skill-card">
        <h3 data-zh="数据驱动决策" data-en="Data-Driven Decision Making">数据驱动决策</h3>
        <p data-zh="客流实时监测、营销数据深度复盘、UCR模型构建与优化" data-en="Real-time footfall monitoring, marketing data deep-dive, UCR model building and optimization">客流实时监测、营销数据深度复盘、UCR模型构建与优化</p>
      </div>
      <div class="skill-card">
        <h3 data-zh="渠道战略规划" data-en="Channel Strategy Planning">渠道战略规划</h3>
        <p data-zh="从0到1品牌孵化、从1到100规模化扩张的渠道布局策略" data-en="Channel layout strategies for brand incubation (0 to 1) and scalable expansion (1 to 100)">从0到1品牌孵化、从1到100规模化扩张的渠道布局策略</p>
      </div>
      <div class="skill-card">
        <h3 data-zh="团队建设与管理" data-en="Team Building &amp; Management">团队建设与管理</h3>
        <p data-zh="跨部门协调、人才培养、组织文化塑造与绩效体系搭建" data-en="Cross-department coordination, talent development, organizational culture, and performance systems">跨部门协调、人才培养、组织文化塑造与绩效体系搭建</p>
      </div>
      <div class="skill-card">
        <h3 data-zh="公开演讲与传播" data-en="Public Speaking &amp; Communication">公开演讲与传播</h3>
        <p data-zh="行业峰会主题演讲、品牌故事讲述、专业知识分享与媒体传播" data-en="Keynote speeches at industry summits, brand storytelling, knowledge sharing, and media communication">行业峰会主题演讲、品牌故事讲述、专业知识分享与媒体传播</p>
      </div>
    </div>
  </div>
</section>
```

- [ ] **Step 2: 添加技能卡片样式**

```css
/* Skills */
.skills-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.skill-card {
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 28px;
  transition: box-shadow 0.2s, transform 0.2s;
}

.skill-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transform: translateY(-2px);
}

.skill-card h3 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 10px;
  color: var(--text-primary);
}

.skill-card p {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
}
```

- [ ] **Step 3: 刷新浏览器验证**

Expected: 6个技能卡片，3列网格布局，hover有轻微上浮效果

- [ ] **Step 4: Commit**

```bash
git add index.html css/style.css
git commit -m "feat: add skills section with grid cards"
```

---

### Task 7: 构建履历时间线

**Files:**
- Modify: `index.html`
- Modify: `css/style.css`

- [ ] **Step 1: 添加履历时间线区块**

```html
<section class="section" id="experience">
  <div class="container">
    <div class="section-header">
      <span class="section-label" data-zh="履历" data-en="EXPERIENCE">履历</span>
      <h2 class="section-title" data-zh="职业经历" data-en="Professional Experience">职业经历</h2>
    </div>
    <div class="timeline">
      <div class="timeline-item">
        <div class="timeline-marker"></div>
        <div class="timeline-content">
          <span class="timeline-date">2018 - 至今</span>
          <h3 data-zh="副总裁" data-en="Vice President">副总裁</h3>
          <p class="timeline-company" data-zh="邻汇吧 &amp; 可计算开店科技" data-en="Linhuiba &amp; Kejisuan">邻汇吧 &amp; 可计算开店科技</p>
          <p class="timeline-desc" data-zh="负责公司战略制定与执行，主导「慢闪店」体验营销模式从概念到规模化落地。建立UCR可复制单店模型，服务爱棵米、慕思等品牌实现线下渠道扩张。" data-en="Responsible for corporate strategy and execution, leading the 'slow-pop-up' experiential marketing model from concept to scale. Established the UCR replicable single-store model, serving brands like Aikemi and Muzi to expand offline channels.">负责公司战略制定与执行，主导「慢闪店」体验营销模式从概念到规模化落地。建立UCR可复制单店模型，服务爱棵米、慕思等品牌实现线下渠道扩张。</p>
        </div>
      </div>
      <div class="timeline-item">
        <div class="timeline-marker"></div>
        <div class="timeline-content">
          <span class="timeline-date">2015 - 2018</span>
          <h3 data-zh="合伙人 / 高管" data-en="Partner / Executive">合伙人 / 高管</h3>
          <p class="timeline-company">邻汇吧</p>
          <p class="timeline-desc" data-zh="作为创始团队核心成员参与邻汇吧早期搭建。负责商业空间资源整合、品牌客户拓展及运营体系搭建，推动平台从杭州拓展至全国15个直营城市。" data-en="Core founding team member involved in Linhuiba's early setup. Responsible for commercial space resource integration, brand client expansion, and operations system building, driving platform expansion from Hangzhou to 15 direct-operated cities nationwide.">作为创始团队核心成员参与邻汇吧早期搭建。负责商业空间资源整合、品牌客户拓展及运营体系搭建，推动平台从杭州拓展至全国15个直营城市。</p>
        </div>
      </div>
    </div>
  </div>
</section>
```

- [ ] **Step 2: 添加时间线样式**

```css
/* Timeline */
.timeline {
  position: relative;
  max-width: 720px;
}

.timeline::before {
  content: '';
  position: absolute;
  left: 7px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: var(--border);
}

.timeline-item {
  position: relative;
  padding-left: 40px;
  padding-bottom: 40px;
}

.timeline-marker {
  position: absolute;
  left: 0;
  top: 4px;
  width: 16px;
  height: 16px;
  border-radius: 50%;
  background: var(--accent);
  border: 3px solid var(--bg-primary);
}

.timeline-date {
  font-size: 14px;
  font-weight: 600;
  color: var(--accent);
  display: block;
  margin-bottom: 6px;
}

.timeline-content h3 {
  font-size: 18px;
  font-weight: 600;
  margin-bottom: 4px;
}

.timeline-company {
  font-size: 14px;
  color: var(--text-secondary);
  margin-bottom: 10px;
  font-weight: 500;
}

.timeline-desc {
  font-size: 15px;
  color: var(--text-secondary);
  line-height: 1.7;
}
```

- [ ] **Step 3: 刷新浏览器验证**

Expected: 纵向时间线，左侧蓝色圆点，右侧显示职位、公司、描述

- [ ] **Step 4: Commit**

```bash
git add index.html css/style.css
git commit -m "feat: add experience timeline section"
```

---

### Task 8: 构建演讲与发表区块

**Files:**
- Modify: `index.html`
- Modify: `css/style.css`

- [ ] **Step 1: 添加演讲区块**

```html
<section class="section" id="speaking">
  <div class="container">
    <div class="section-header">
      <span class="section-label" data-zh="演讲" data-en="SPEAKING">演讲</span>
      <h2 class="section-title" data-zh="演讲与发表" data-en="Speaking &amp; Publications">演讲与发表</h2>
    </div>
    <div class="speaking-list">
      <div class="speaking-item">
        <span class="speaking-date">2024.12</span>
        <div class="speaking-content">
          <h3 data-zh="主题演讲：慢闪店体验营销，重塑线下渠道价值" data-en="Keynote: Slow-Pop-Up Experiential Marketing, Reshaping Offline Channel Value">主题演讲：慢闪店体验营销，重塑线下渠道价值</h3>
          <p data-zh="破界·2024刀法年度品效峰会 | 上海" data-en="Breakthrough · 2024 Daofa Annual Brand Summit | Shanghai">破界·2024刀法年度品效峰会 | 上海</p>
        </div>
      </div>
      <div class="speaking-item">
        <span class="speaking-date">2024.12</span>
        <div class="speaking-content">
          <h3 data-zh="主题演讲：小而美、灵而准——慢闪店如何助力品牌实现渠道突围" data-en="Keynote: Small &amp; Beautiful, Flexible &amp; Precise — How Slow-Pop-Ups Help Brands Break Through">主题演讲：小而美、灵而准——慢闪店如何助力品牌实现渠道突围</h3>
          <p data-zh="2024第五届TBI杰出品牌创新节 | 上海" data-en="5th TBI Outstanding Brand Innovation Festival | Shanghai">2024第五届TBI杰出品牌创新节 | 上海</p>
        </div>
      </div>
      <div class="speaking-item">
        <span class="speaking-date">2024.12</span>
        <div class="speaking-content">
          <h3 data-zh="主持：超级单品与品牌矩阵如何选择" data-en="Moderator: Super Single Product vs. Brand Matrix">主持：超级单品与品牌矩阵如何选择</h3>
          <p data-zh="2024第五届TBI杰出品牌创新节 晨间闭门开杠 | 上海" data-en="5th TBI Innovation Festival Morning Debate | Shanghai">2024第五届TBI杰出品牌创新节 晨间闭门开杠 | 上海</p>
        </div>
      </div>
    </div>
  </div>
</section>
```

- [ ] **Step 2: 添加演讲样式**

```css
/* Speaking */
.speaking-list {
  max-width: 720px;
}

.speaking-item {
  display: flex;
  gap: 24px;
  padding: 24px 0;
  border-bottom: 1px solid var(--border);
}

.speaking-item:last-child {
  border-bottom: none;
}

.speaking-date {
  font-size: 14px;
  font-weight: 600;
  color: var(--accent);
  white-space: nowrap;
  min-width: 70px;
}

.speaking-content h3 {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 6px;
  line-height: 1.5;
}

.speaking-content p {
  font-size: 14px;
  color: var(--text-secondary);
}
```

- [ ] **Step 3: 刷新浏览器验证**

Expected: 3条演讲记录，左侧日期，右侧标题和会议名

- [ ] **Step 4: Commit**

```bash
git add index.html css/style.css
git commit -m "feat: add speaking section"
```

---

### Task 9: 构建项目展示区块

**Files:**
- Modify: `index.html`
- Modify: `css/style.css`

- [ ] **Step 1: 添加项目展示区块**

```html
<section class="section" id="projects">
  <div class="container">
    <div class="section-header">
      <span class="section-label" data-zh="项目" data-en="PROJECTS">项目</span>
      <h2 class="section-title" data-zh="项目展示" data-en="Featured Projects">项目展示</h2>
    </div>
    <div class="projects-grid">
      <div class="project-card">
        <h3 data-zh="可计算开店科技" data-en="Kejisuan">可计算开店科技</h3>
        <p class="project-desc" data-zh="以数据驱动的线下开店决策平台，提供选址分析、客流预测、ROI评估等全链路服务，帮助品牌实现「可计算」的线下扩张。" data-en="A data-driven offline store opening decision platform providing site selection analysis, footfall prediction, ROI evaluation, and full-chain services to help brands achieve 'measurable' offline expansion.">以数据驱动的线下开店决策平台，提供选址分析、客流预测、ROI评估等全链路服务，帮助品牌实现「可计算」的线下扩张。</p>
        <div class="project-tags">
          <span class="tag">数据选址</span>
          <span class="tag">客流预测</span>
          <span class="tag">ROI评估</span>
        </div>
      </div>
      <div class="project-card">
        <h3 data-zh="邻汇吧平台" data-en="Linhuiba Platform">邻汇吧平台</h3>
        <p class="project-desc" data-zh="全国领先的商业空间短租交易平台，整合购物中心、社区、写字楼等多元场景，为品牌提供快闪店、慢闪店、地推等线下营销场地服务。" data-en="China's leading commercial space short-term rental platform, integrating diverse scenarios such as shopping centers, communities, and office buildings, providing offline marketing venue services.">全国领先的商业空间短租交易平台，整合购物中心、社区、写字楼等多元场景，为品牌提供快闪店、慢闪店、地推等线下营销场地服务。</p>
        <div class="project-tags">
          <span class="tag">商业空间</span>
          <span class="tag">快闪店</span>
          <span class="tag">慢闪店</span>
        </div>
      </div>
      <div class="project-card">
        <h3 data-zh="UCR可复制单店模型" data-en="UCR Replicable Store Model">UCR可复制单店模型</h3>
        <p class="project-desc" data-zh="总结提炼的慢闪店标准化运营模型，覆盖选址、搭建、运营、复盘全周期，已帮助爱棵米、慕思等品牌实现线下渠道快速复制。" data-en="A standardized slow-pop-up operations model covering site selection, setup, operations, and review. Helped brands like Aikemi and Muzi rapidly replicate offline channels.">总结提炼的慢闪店标准化运营模型，覆盖选址、搭建、运营、复盘全周期，已帮助爱棵米、慕思等品牌实现线下渠道快速复制。</p>
        <div class="project-tags">
          <span class="tag">标准化</span>
          <span class="tag">可复制</span>
          <span class="tag">全周期</span>
        </div>
      </div>
    </div>
  </div>
</section>
```

- [ ] **Step 2: 添加项目卡片样式**

```css
/* Projects */
.projects-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.project-card {
  background: var(--bg-primary);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 28px;
  transition: box-shadow 0.2s;
}

.project-card:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.project-card h3 {
  font-size: 17px;
  font-weight: 600;
  margin-bottom: 12px;
}

.project-desc {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 16px;
}

.project-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag {
  font-size: 12px;
  padding: 4px 10px;
  background: var(--bg-secondary);
  border-radius: 4px;
  color: var(--text-secondary);
  font-weight: 500;
}
```

- [ ] **Step 3: 刷新浏览器验证**

Expected: 3个项目卡片，每卡有标题、描述、标签

- [ ] **Step 4: Commit**

```bash
git add index.html css/style.css
git commit -m "feat: add projects section"
```

---

### Task 10: 构建联系方式和页脚

**Files:**
- Modify: `index.html`
- Modify: `css/style.css`

- [ ] **Step 1: 添加联系方式和页脚**

```html
<section class="section" id="contact">
  <div class="container">
    <div class="section-header">
      <span class="section-label" data-zh="联系" data-en="CONTACT">联系</span>
      <h2 class="section-title" data-zh="联系方式" data-en="Get In Touch">联系方式</h2>
    </div>
    <div class="contact-content">
      <p class="contact-desc" data-zh="欢迎就线下体验营销、商业空间运营、慢闪店合作等话题与我交流。" data-en="Feel free to reach out about offline experiential marketing, commercial space operations, or slow-pop-up collaborations.">欢迎就线下体验营销、商业空间运营、慢闪店合作等话题与我交流。</p>
      <div class="contact-links">
        <a href="mailto:contact@linhuiba.com" class="contact-link">
          <span class="contact-icon">@</span>
          <span>contact@linhuiba.com</span>
        </a>
        <a href="https://www.linhuiba.com" target="_blank" rel="noopener" class="contact-link">
          <span class="contact-icon">&#127760;</span>
          <span data-zh="邻汇吧官网" data-en="Linhuiba Website">邻汇吧官网</span>
        </a>
      </div>
    </div>
  </div>
</section>

<footer class="footer">
  <div class="container">
    <p data-zh="&amp;copy; 2025 施可. 保留所有权利。" data-en="&amp;copy; 2025 Shi Ke. All rights reserved.">&copy; 2025 施可. 保留所有权利。</p>
  </div>
</footer>
```

- [ ] **Step 2: 添加联系和页脚样式**

```css
/* Contact */
.contact-content {
  text-align: center;
}

.contact-desc {
  font-size: 16px;
  color: var(--text-secondary);
  margin-bottom: 28px;
  max-width: 520px;
  margin-left: auto;
  margin-right: auto;
}

.contact-links {
  display: flex;
  justify-content: center;
  gap: 32px;
  flex-wrap: wrap;
}

.contact-link {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 15px;
  color: var(--text-primary);
  padding: 12px 20px;
  border: 1px solid var(--border);
  border-radius: 8px;
  transition: all 0.2s;
}

.contact-link:hover {
  border-color: var(--accent);
  color: var(--accent);
}

.contact-icon {
  font-size: 18px;
}

/* Footer */
.footer {
  background: var(--bg-nav);
  color: rgba(255,255,255,0.5);
  text-align: center;
  padding: 24px 0;
  font-size: 14px;
}
```

- [ ] **Step 3: 刷新浏览器验证**

Expected: 联系方式区块有描述和两个链接按钮，底部深色页脚

- [ ] **Step 4: Commit**

```bash
git add index.html css/style.css
git commit -m "feat: add contact section and footer"
```

---

### Task 11: 实现 JavaScript 交互

**Files:**
- Modify: `js/main.js`
- Modify: `css/style.css` (for mobile nav)

- [ ] **Step 1: 编写 main.js**

```javascript
// Mobile menu toggle
const navToggle = document.getElementById('navToggle');
const navMenu = document.getElementById('navMenu');

if (navToggle) {
  navToggle.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    navToggle.classList.toggle('active');
  });
}

// Close mobile menu when clicking a link
document.querySelectorAll('.nav-link').forEach(link => {
  link.addEventListener('click', () => {
    navMenu.classList.remove('active');
    navToggle.classList.remove('active');
  });
});

// Active nav link highlighting with IntersectionObserver
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.nav-link');

const observerOptions = {
  root: null,
  rootMargin: '-50% 0px -50% 0px',
  threshold: 0
};

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      const id = entry.target.getAttribute('id');
      navLinks.forEach(link => {
        link.classList.remove('active');
        if (link.getAttribute('href') === '#' + id) {
          link.classList.add('active');
        }
      });
    }
  });
}, observerOptions);

sections.forEach(section => observer.observe(section));

// Language switching
const langSwitch = document.getElementById('langSwitch');
let currentLang = 'zh';

function switchLanguage() {
  currentLang = currentLang === 'zh' ? 'en' : 'zh';
  
  // Update switch button text
  if (langSwitch) {
    langSwitch.textContent = langSwitch.getAttribute('data-' + currentLang);
  }
  
  // Update all elements with data-zh and data-en
  document.querySelectorAll('[data-zh][data-en]').forEach(el => {
    const newText = el.getAttribute('data-' + currentLang);
    if (newText) {
      // For elements with child elements (like footer), set innerHTML
      if (el.tagName === 'FOOTER' || el.querySelector('*')) {
        // Only update if it's a simple text element or has the attributes directly
        if (el.children.length === 0) {
          el.textContent = newText;
        }
      } else {
        el.textContent = newText;
      }
    }
  });
  
  // Update HTML lang attribute
  document.documentElement.lang = currentLang === 'zh' ? 'zh-CN' : 'en';
}

if (langSwitch) {
  langSwitch.addEventListener('click', switchLanguage);
}
```

- [ ] **Step 2: 添加移动端导航样式**

```css
/* Mobile Navigation */
@media (max-width: 768px) {
  .nav-toggle {
    display: flex;
  }
  
  .nav-menu {
    position: fixed;
    top: 60px;
    left: 0;
    right: 0;
    background: var(--bg-nav);
    flex-direction: column;
    padding: 16px 24px;
    gap: 0;
    transform: translateY(-100%);
    opacity: 0;
    pointer-events: none;
    transition: all 0.3s;
  }
  
  .nav-menu.active {
    transform: translateY(0);
    opacity: 1;
    pointer-events: auto;
  }
  
  .nav-menu li {
    border-bottom: 1px solid rgba(255,255,255,0.1);
  }
  
  .nav-menu li:last-child {
    border-bottom: none;
  }
  
  .nav-link {
    display: block;
    padding: 12px 0;
  }
  
  .nav-link.active::after {
    display: none;
  }
  
  /* Hero mobile */
  .hero-name {
    font-size: 36px;
  }
  
  .hero-title {
    font-size: 16px;
  }
  
  /* Grid mobile */
  .skills-grid,
  .projects-grid {
    grid-template-columns: 1fr;
  }
  
  /* Section padding mobile */
  .section {
    padding: 40px 0;
  }
  
  .hero {
    padding-top: 100px;
    padding-bottom: 40px;
  }
  
  /* Timeline mobile */
  .timeline-item {
    padding-left: 32px;
  }
  
  /* Contact links mobile */
  .contact-links {
    flex-direction: column;
    align-items: center;
  }
}
```

- [ ] **Step 3: 测试交互功能**

1. 刷新浏览器，向下滚动各区块，验证导航高亮跟随
2. 点击"EN"按钮，验证文本切换为英文
3. 缩小浏览器窗口到手机宽度，验证汉堡菜单出现并可展开

- [ ] **Step 4: Commit**

```bash
git add js/main.js css/style.css
git commit -m "feat: add JavaScript interactions - nav highlight, language switch, mobile menu"
```

---

### Task 12: 最终验证和清理

**Files:**
- Modify: `index.html` (if needed for any fixes)

- [ ] **Step 1: 完整页面功能检查清单**

打开 `index.html` 在浏览器中，逐项验证：

- [ ] 导航栏固定在顶部，深色背景
- [ ] 点击导航链接平滑滚动到对应区块
- [ ] 滚动时导航高亮自动切换
- [ ] 点击"EN"切换为英文，点击"中"切换回中文
- [ ] 移动端（< 768px）显示汉堡菜单，点击展开导航
- [ ] 所有8个区块内容正确显示
- [ ] 技能卡片和项目卡片hover有效果
- [ ] 时间线样式正确
- [ ] 页脚显示正常

- [ ] **Step 2: 最终 Commit**

```bash
git add -A
git commit -m "feat: complete personal homepage - all sections, interactions, responsive design"
```

---

## 自审检查

**1. Spec coverage:**
- ✅ 8个页面区块：导航、Hero、关于、技能、履历、演讲、项目、联系+页脚
- ✅ 专业商务风配色（白底、深色文字、蓝色点缀）
- ✅ 中英双语切换（data属性方案）
- ✅ 单页滚动 + 导航高亮（IntersectionObserver）
- ✅ 纯HTML/CSS/JS，无依赖
- ✅ 响应式设计（768px断点）
- ✅ GitHub Pages部署就绪

**2. Placeholder scan:**
- ✅ 无TBD/TODO
- ✅ 所有步骤包含完整代码
- ✅ 所有步骤包含验证命令

**3. Type consistency：**
- ✅ data-zh / data-en 属性命名一致
- ✅ CSS变量命名一致
- ✅ 类名命名一致
