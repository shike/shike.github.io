# 计划:新增 WorkBuddy 与三本书迁移到 GitBook

## 任务拆解

按依赖顺序执行,每步完成后做最小化本地校验(grep / 文件大小 / 文件存在)。

### 1. 准备 WorkBuddy 封面
- 用 `image_synthesize` 生成 3:4 比例、2K 分辨率、深蓝紫渐变、企业培训风格的 WorkBuddy 封面,落盘到 `assets/books/workbuddy-cover.png`
- 用 `sips -s format jpeg -s formatOptions 82 -Z 1200` 转为 JPEG、等比缩放到长边 1200px,落盘到 `assets/books/workbuddy-cover.jpg`
- 校验:文件存在、体积 < 500 KB、维度正确(`file` 读取元数据)

### 2. 写 spec 文档
- 新建 `docs/superpowers/specs/2026-08-20-add-workbuddy-book.md`,定义文案、URL、JSON-LD 结构、布局与验证标准

### 3. 写 plan 文档
- 新建 `docs/superpowers/plans/2026-08-20-add-workbuddy-book.md`(本文件),记录实现步骤

### 4. 修改 `index.html`

按从上到下的顺序编辑:

- `<meta name="keywords">`:末尾追加 `,WorkBuddy`
- JSON-LD `@graph`:
  - FDE `Book` 实体的 `url` 改为 `https://shike.gitbook.io/fde-1`
  - AI Coding `Book` 实体的 `url` 改为 `https://shike.gitbook.io/ai-coding/`
  - 在 FDE 之后追加 WorkBuddy `Book` 实体
  - ProfilePage `dateModified` 改为 `2026-08-20`
- Books 区块 (`#books` 内的 `.books-grid`):
  - 在第二个 `book-card`(FDE)之后追加 WorkBuddy `book-card`
  - 改 3 张卡片的 CTA 文案与 `href` 到 GitBook
- About 区块:
  - 统计 `2 本` / `2 Books` 改为 `3 本` / `3 Books`
  - 中英文两版"著有"句子追加 WorkBuddy

### 5. 修改 `css/style.css`

- `.books-grid` 的 `grid-template-columns`:
  - 桌面默认:`repeat(2, minmax(0, 1fr))` → `repeat(3, minmax(0, 1fr))`
  - 中等屏断点(769–1100px)新增:`repeat(2, minmax(0, 1fr))`,避免 3 列过窄
  - 移动端断点(<769px)已有 `1fr`,不动

### 6. 修改 `llms.txt`

- `## Books` 章节追加 WorkBuddy 条目
- 两条已有条目的 URL 改为 GitBook
- `Last updated` 改为 `2026-08-20`

### 7. 修改 `sitemap.xml`

- 首页 `<lastmod>` 从 `2026-08-04` 改为 `2026-08-20`

### 8. 全站一致性校验

- `grep -n "github.com/shike/" index.html llms.txt` → 应只剩 `shike/lotus-tarot`(在 Skill 区块文案里,不是书)、`me` 链接(在 `<link rel="me">`)、`@shike` 等非书链接。书籍相关应无残留
- `grep -n "2 本\|2 Books" index.html llms.txt` → 应为空
- `grep -n "在 GitHub 阅读\|Read on GitHub" index.html` → 应为空
- `grep -n "WorkBuddy" index.html llms.txt` → 应至少 8 处(3 卡 × 2 文案 + 3 JSON-LD 字段 + 1 keywords + 2 About 中英 + 1 统计英文 + 1 llms.txt)

### 9. Git 提交

- `git add assets/books/workbuddy-cover.jpg index.html css/style.css llms.txt sitemap.xml docs/`
- `git commit -m "feat(books): add WorkBuddy + migrate 3 books to GitBook"`
- 不主动 push,等用户确认

## 关键决策

- **WorkBuddy 文案定位**:突出"3 卷 24 章 / 18 附录 / 6 序与目录"的结构化标签,以及"可切片、可重印、培训与咨询交付件"的差异化定位(对应 user memory 中 WorkBuddy 三部曲的定位)
- **CTA 文案统一为 GitBook**:即便之前 FDE/AI Coding 的 GitHub 仓库还在,所有阅读入口都指向 GitBook
- **书籍展示顺序**:AI Coding → FDE → WorkBuddy,WorkBuddy 作为最新一本放最后,符合时间与重要性直觉
- **中间断点 2 列**:避免 769–1100px 范围 3 列时卡片窄到简介折行过多;用户实际部署到 GitHub Pages 后,中等屏长宽比通常能直接进 3 列,这里只作为保险

## 风险与回滚

- 风险 1:WorkBuddy 封面视觉与现有两本不一致 → 通过生成时显式声明"蓝紫渐变 + 三卷竖带 + 标题与底注"控制
- 风险 2:三本书 URL 漏改 → 通过 grep 全站校验兜底
- 风险 3:`books-grid` 3 列导致中等屏卡片过窄 → 中等屏断点回落到 2 列
- 回滚:`git revert HEAD`(单 commit)或 `git reset --hard HEAD~1`
