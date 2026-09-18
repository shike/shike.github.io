# 个人站 dropleap 化改造 — 执行计划

日期：2026-09-18
Spec：`docs/superpowers/specs/2026-09-18-dropleap-rebrand-design.md`

> **给执行者：** 本计划按阶段推进，每个阶段结束产出一个 diff 检查点。按项目既有约定，**除非用户明确要求，否则不 commit、不 push**。

## 全局约束

- 保持零依赖静态站架构；不新增 npm 包、CMS、运行时 API 或构建步骤
- 所有可见文案双语：中文写在 `textContent`，英文写在 `data-en`，ARIA 覆盖写在 `data-en-aria`
- `data-en` 只能标注**叶子文本节点**，绝不可标注含子元素的元素（否则切换语言会抹掉子元素）
- 外链一律 HTTPS + `target="_blank"` + `rel="noopener noreferrer"`
- 图片必须声明内在尺寸、`loading="lazy"`、`decoding="async"`、描述性 `alt`
- 所有内容文字颜色必须通过 AA（≥4.5:1），按白底与 `--soft` 浅底双背景验算
- 机器可读层（JSON-LD / llms.txt / sitemap）必须与可见页面同源一致
- 只在 `main` 修改；不建分支、不建 worktree

## 阶段 1 — 决策文档与素材

- [x] 下载并本地化素材：hero 1、案例 2、行业 9（`assets/hero`、`assets/cases`、`assets/industries`）
- [x] 行业图统一裁切压缩至 112×112
- [x] 按 WCAG 公式验算最终色板，产出可访问 token
- [ ] 写 spec 文档（本文件同目录 specs/）
- [ ] 写 plan 文档（本文件）

**验收**：`git status` 显示新增素材均为本地文件，无外链引用。

## 阶段 2 — 设计系统基础层

重写 `css/style.css`，从 3915 行收敛为按职责分区的单一文件：

1. reset
2. `:root` token（见 spec）
3. 基础层：`html/body`、字号层级、链接（正文内链必须带下划线，不再只靠颜色区分）、`:focus-visible`、`.skip-link`、图片
4. 布局层：容器、`.sec` / `.sec--tint`、区块头、网格
5. 组件层：导航、按钮、卡片、虚线分隔、编号标注、eyebrow pill

**删除**：`.focus-*` 与 `.venture-card--focus`（L1271-1456）、七阶段产品页（L1518-2321）、compact 数据表（L2342-2610）、visual overhaul（L2677-3224）、visual fixes（L3263-3435）、`.product-proof`（L3761-3849）、`.project-*` / `.venture-*` / `.tag` / `.speaking-date`，以及全部 94 处 `!important`。

**验收**：新 CSS 无 `!important`、无重复定义的选择器、无 hardcode 品牌色（`#4f46e5` / `#4338ca` 清零）、断点只有 1024 与 768。

## 阶段 3 — 12 板块迁移

按 DOM 顺序逐个迁移，每个板块一个检查点：

| # | 板块 | 关键工作 |
|---|---|---|
| 1 | hero | eyebrow pill + 44px h1 + lede + **双 CTA**（本站此前一个按钮都没有）+ 右栏照片 |
| 2 | cases | **新增**：2 个案例整卡（序号 pill、大图左栏、标题、客户元信息、蓝色竖线引语、`做了什么`、KPI 三宫格） |
| 3 | product | `.screen` 仿应用窗口 + 4 处编号标注 + CSS 柱状图 + 报表卡片 + 4 件套四卡 + 接入链路 L1→2 Skills→L2 |
| 4 | services | **新增**：4 类服务（stroke SVG 图标 + capability 标签）+ 3 档培训 + 交付节奏 |
| 5 | industries | **新增**：9 行业 3×3（56px 方形缩略图 + h4 + 一行说明） |
| 6 | books | 换视觉，保留 3 本与 GitBook 链接 |
| 7 | agent-skills | 换视觉 + 修 `data-en` 抹掉行内链接的 bug |
| 8 | about | 原 about 与 skills 合并为一个板块 |
| 9 | experience | 时间线 + 过往战绩 + 19 logo 墙换视觉 |
| 10 | speaking | 换视觉 |
| 11 | ventures | 5 条业务线全部保留，移到履历之后 |
| 12 | contact | 深色渐变 CTA + 邮箱 + 微信二维码 + **修好失效弹窗** |

**验收**：导航 8 项的每个 `href` 都能命中对应 `section[id]`；每个 section 有且仅有一个 h2；标题层级不跳级。

## 阶段 4 — 脚本与 bug 修复

`js/main.js` 调整与 bug 清单：

1. `data-en` 改为只在叶子节点生效，或在替换时保留子元素（配合阶段 3 的 markup 修正）
2. `META` 与 `<head>` 的 title/description 双份真相收敛为一处
3. 游离在 i18n 之外的元素（hero 数字单位、`#qrModalDesc`）纳入
4. 语言切换按钮 `aria-label` 包含可见文本（WCAG 2.5.3）
5. 二维码弹窗补上 `[data-qr-trigger]`
6. 弹窗打开时保持 `body` 滚动锁与焦点返还（现有实现保留）

**已由阶段 2/3 自然修复**：CSS shell 残留导致规则被吞、`.product-section-h3` 无样式、`.logo-card.has-text` 缺 fallback、`.section:nth-of-type()` 底色脆弱、正文内链只靠颜色区分。

## 阶段 5 — 机器可读层

- `index.html` JSON-LD：更新 `ProfilePage.dateModified`；FAQ 扩写为覆盖新增板块（客户案例、4 件套、培训体系）；保留 3 个 `Book` 节点；新增 `Organization` 节点（水滴跃动）
- `llms.txt`：新增「客户案例 / 产品四件套 / 服务与培训 / 行业」段落与页面同步；客户数量统一为 100+；日期修正
- `sitemap.xml`：`lastmod` 对齐实际发布日
- `og-cover.svg` → `rsvg-convert -w 1200 -h 630` 重新导出 PNG（品牌色换 `#3370ff`）
- favicon 与 `theme-color`：`index.html` 中两个 `data:image/svg+xml` URI 内的硬编码 `%234f46e5` 一并更新

**验收**：三处日期（JSON-LD / sitemap / llms.txt）完全一致且非未来日期。

## 阶段 6 — 测试套件重写

现有 46 条测试约 20 条冻结营销文案、约 30 条冻结 px 值与死 CSS 选择器，且存在两条互相矛盾的断言（`llms.txt` 的 "Last updated" 被要求同时等于 `2026-08-04` 和 `2026-09-05`）。重写为五组契约测试：

1. **结构与锚点**：section id 唯一且与导航对齐；每板块有 h2；标题层级不跳级
2. **双语契约**：可见文本节点均有 `data-en`；`data-en` 不落在含子元素的元素上；langSwitch 可访问名称包含可见文本
3. **设计系统**：token 齐全；**用 Python 按 WCAG 公式断言所有文字色在双背景下 ≥4.5:1**；断点只有 1024/768；无 `!important`
4. **机器可读层一致性**：JSON-LD / llms.txt / sitemap 与页面交叉断言（书名、URL、案例数字、三处日期一致且非未来）
5. **内容红线**：保留禁用旧口径清单（数商方略、乐奇 Minibus EV、阿里云 AI 大赛银奖、已删的邻汇吧经营数字）；外链安全属性；图片 alt/尺寸/lazy

**删除**：冻结营销字面量的断言、冻结 px 值的断言、要求死 CSS 选择器存在的断言（11 条）。

## 阶段 7 — 验证

1. `python3 -m unittest discover -s tests` 全绿
2. `python3 -m http.server` 起本地服务，在 1440 / 1024 / 768 / 375 四个宽度自查
3. 本地 Lighthouse（desktop preset，3 次取中位）：accessibility ≥0.95、SEO ≥0.95、performance ≥0.9、best-practices ≥0.9
4. 输出 diff 检查点，等待用户指示后再考虑提交
