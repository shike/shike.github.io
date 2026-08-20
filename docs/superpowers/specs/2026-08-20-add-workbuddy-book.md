# 新增 WorkBuddy 与三本书迁移到 GitBook

## 项目概述

在 `index.html` 的 Books 区块新增第三本书《WorkBuddy:企业 AI 落地三部曲》,并将三本书的对外阅读链接统一从 GitHub 仓库迁移到 GitBook,同步更新全站相关引用,保证 SEO、GEO、JSON-LD、`llms.txt`、关键词与文案事实一致。

## 已确认范围

### Books 区块新增 WorkBuddy

- 中文书名:`《WorkBuddy:企业 AI 落地三部曲》`
- 英文书名:`WorkBuddy: An Enterprise AI Implementation Trilogy`
- 中文简介:`3 卷 24 章 / 18 附录 / 6 序与目录的企业 AI 落地工作手册,定位为可切片、可重印的培训与咨询交付件。`
- 英文简介:`A 3-volume, 24-chapter field workbook for taking enterprise AI from use-case discovery through engineering delivery to deployment operations. Designed as a training and consulting deliverable.`
- 链接:`https://shike.gitbook.io/workbuddy/`
- 封面:本地 `assets/books/workbuddy-cover.jpg`(`image_synthesize` 生成的 3:4 封面,经 `sips` 等比缩放到长边 1200px、JPEG 质量 82)

### 三本书统一迁移到 GitBook

将现有两本书的对外阅读链接从 GitHub 仓库改为 GitBook 站点,卡片 CTA 文案从"在 GitHub 阅读 ↗ / Read on GitHub ↗"改为"在 GitBook 阅读 ↗ / Read on GitBook ↗"。

| 书目 | 中文名 | English title | GitBook URL | 封面 |
|---|---|---|---|---|
| AI Coding | 《AI Coding:人人都是程序员》 | AI Coding: Everyone Is a Programmer | `https://shike.gitbook.io/ai-coding/` | `assets/books/ai-coding-cover.jpg` |
| FDE | 《FDE:AI 的胜负不在于模型》 | FDE: Winning and Losing in AI Isn't About the Model | `https://shike.gitbook.io/fde-1` | `assets/books/fde-cover.svg` |
| WorkBuddy | 《WorkBuddy:企业 AI 落地三部曲》 | WorkBuddy: An Enterprise AI Implementation Trilogy | `https://shike.gitbook.io/workbuddy/` | `assets/books/workbuddy-cover.jpg` |

### 布局变更

Books 区块的 `.books-grid` 从桌面 2 列改为桌面 3 列,移动端继续单列纵向排列,确保 3 张卡片在同一行视觉对齐,封面展示框尺寸保持现有 3:4 海报框不变。

### 全站文案与数据同步

- `<meta name="keywords">` 增加 `WorkBuddy`
- About 区块的"著有《...》《...》"在中文与英文两版同时追加 WorkBuddy(放在最后,与最新出版顺序一致)
- About 区块的统计标签 `2 本` / `2 Books` 改为 `3 本` / `3 Books`
- JSON-LD `@graph` 新增 WorkBuddy 的 `Book` 实体,并把现有两本书的 `url` 改为 GitBook
- `llms.txt` 的 `## Books` 章节追加 WorkBuddy,两条已有 URL 同步改为 GitBook
- `sitemap.xml` 的 `lastmod` 更新为 `2026-08-20`

## 页面结构与视觉设计

### 区块位置

`#books` 区块位置不变(位于 Ventures 之后、Agent Skills on WorkBuddy 之前),新增第三张卡片作为 `books-grid` 的第三个网格项,排序沿用原 AI Coding → FDE 的顺序,WorkBuddy 作为最新一本放在末尾。

### 书籍卡片

每张卡片继续使用现有结构:封面展示框(3:4 海报框,`object-fit: contain`)→ 中英文书名 → 一句话简介 → 对外 CTA。三列下卡片在中等屏宽(769–1100px)会变窄,简介文案保持单行长度可控,避免折行过多。

### 封面资源

- `assets/books/workbuddy-cover.jpg`:由 `image_synthesize` 生成 2K、3:4 比例的 WorkBuddy 封面,再经 `sips -s format jpeg -s formatOptions 82 -Z 1200` 等比缩放到长边 1200px,目标文件体积 < 500 KB,保留原图的视觉特征(深蓝紫渐变、左侧三卷竖带、WorkBuddy 标题、Enterprise AI Implementation Trilogy 副标题、3 Volumes · 24 Chapters · A Field Workbook 底注)
- 现有 `ai-coding-cover.jpg`、`fde-cover.svg` 不变

## 技术设计

### 受影响文件

- `index.html`
  - `<meta name="keywords">` 增加 `WorkBuddy`
  - JSON-LD 新增 WorkBuddy `Book` 实体,改写两条已有 `Book` 实体的 `url`
  - Books 区块新增 WorkBuddy 卡片,改三张 CTA 文案到 GitBook
  - 统计标签 `2 本` → `3 本`
  - About 中英文两版"著有"句子追加 WorkBuddy
  - ProfilePage `dateModified` 更新为 `2026-08-20`
- `css/style.css`
  - `.books-grid` 由 `repeat(2, minmax(0, 1fr))` 改为 `repeat(3, minmax(0, 1fr))`
  - 移动端断点(已在 `.books-grid` 上叠加 `1fr`)无需调整
  - 视情况在中等屏宽断点加 `repeat(2, minmax(0, 1fr))` 避免 3 张卡片在 769–1100px 范围过窄
- `assets/books/workbuddy-cover.jpg`(新增,本地封面)
- `llms.txt`
  - `## Books` 追加 WorkBuddy 条目
  - 已有两条 URL 同步改为 GitBook
  - 最后修改日期更新为 `2026-08-20`
- `sitemap.xml`
  - 首页 `lastmod` 更新为 `2026-08-20`

`js/main.js` 不动。新元素遵循现有 `data-en` 约定即可自动支持中英文切换。

### 静态内容流

所有书籍内容继续硬编码在 `index.html`,不引入数据文件、构建工具或运行时接口。封面使用本地资源,链接统一使用 GitBook 站点的 HTTPS URL,外链在新标签页打开并带 `rel="noopener noreferrer"`。

## SEO、GEO 与结构化数据

- `keywords` 增加 `WorkBuddy`
- JSON-LD `@graph` 现有 3 个 `Book` 实体保持作者指向 `#person` 的关系,WorkBuddy 实体用同样的 `author` 结构
- 三个 `Book` 实体的 `image` 字段使用 `https://shike.github.io/assets/books/...` 绝对 URL,方便 LLM/搜索引擎抓取
- `llms.txt` 的 `## Books` 与页面 JSON-LD 保持事实一致
- `sitemap.xml` 的 `lastmod` 反映本次更新

## 响应式与可访问性

- 桌面端(≥1100px)3 列,中等屏(769–1100px)回落 2 列,移动端(<769px)单列
- 所有可点击元素保留清晰键盘焦点状态
- 卡片标题、简介、CTA 中英文完整,英文版不留中文文案
- 封面 `alt` 文案分别使用三本书的中文全名

## 验证标准

### 内容

- 三本书在 Books 区块以 3 张卡片呈现,顺序为 AI Coding → FDE → WorkBuddy
- 统计标签显示 `3 本` / `3 Books`
- About 中英文两版的"著有"句子列出全部三本书
- `keywords` 包含 `WorkBuddy`
- 三本书的 GitBook URL 在卡片、JSON-LD、`llms.txt` 中一致

### 交互

- 中英文切换覆盖三本书的标题、简介与 CTA 文案
- 桌面导航与 `#books` 锚点正常
- 三个外链均在新标签页打开,带 `rel="noopener noreferrer"`

### 展示

- 桌面 3 列 / 移动单列,无横向滚动
- 三张卡片的封面展示框在桌面端尺寸一致,使用 3:4 海报框
- WorkBuddy 封面正常加载,体积 < 500 KB
- 现有 FDE 横向 SVG 封面、AI Coding 竖向 JPG 封面继续完整居中

### 机器可读内容

- JSON-LD 可解析,三个 `Book` 节点均关联作者 `#person`
- `llms.txt` 与页面可见内容一致
- `sitemap.xml` 日期已更新

## 非目标

- 不重写 Books 区块的视觉体系
- 不新增书籍详情页或站内阅读器
- 不修改 `js/main.js`
- 不修改 FDE、AI Coding 仓库或 GitBook 站点本身的内容
- 不修改 Agent Skills on WorkBuddy 区块(那是 WorkBuddy SkillHub 上的 skills,不是书)
- 不重新生成 FDE、AI Coding 的封面
