# 个人站向 dropleap.cn 设计系统与业务口径迁移 — 设计规范

日期：2026-09-18
参考源：https://dropleap.cn/ （苏州水滴跃动科技有限公司官网）

## 背景

shike.github.io 目前的视觉体系是 2026-05-06 建站时定的靛蓝方案（`--accent: #4f46e5` / 容器 1100px / section 68px）。此后产品区块经历了四代推翻重做，`css/style.css` 累积到 3915 行，其中约 1900 行作用在 HTML 中已不存在的类上；文件尾部有 94 处 `!important` 互相打架；第 3538-3542 行混入了 shell 残留（裸 `EOF` 与 `echo "appended"`），按 CSS 错误恢复规则会吞掉紧随其后的 `.product-hero-value` 规则。

同时，站点内容与 dropleap.cn 出现了口径分叉：llms.txt 声称「30+ 家制造企业」而公司站对外是「100+ 家」；llms.txt 声称有一套「4 阶段 Diagnose → Deliver → Review → Distill 方法论」，但公司站页面上并未发布这套东西。

本规范记录把个人站迁移到公司站设计系统与业务口径的全部决策。

## 参考源的技术同构性

dropleap.cn 与本站技术形态完全一致，迁移不引入新依赖：

| 维度 | dropleap.cn | 本站 |
|---|---|---|
| 架构 | 纯静态 HTML + 单 CSS + 单 JS | 同 |
| 字体 | 系统字体栈，零 webfont | 同 |
| 框架/构建 | 无 | 同 |
| 图片 | JPEG + SVG | 同 |
| JS 依赖 | 零 | 同 |

差异仅在于它把组件样式内联在 HTML head，本站放在外部 `css/style.css`。**本站保持外部样式表**（更适合 3915 → 重写的体量）。

## 设计 token

### 色板决策：沿用色相，加深文字角色

按 WCAG 2.x 相对亮度公式验算，dropleap.cn 的原始调色板**无法通过本站的 Lighthouse 门禁**（accessibility 阈值 0.95 为 error 级），因为它自身没有 CI 检查：

| dropleap 原值 | 用途 | 白底对比度 | 判定 |
|---|---|---|---|
| `#3370ff` | 品牌主色 | 4.28:1 | ❌ 低于 4.5 |
| 白字压 `#3370ff` | 主按钮文字 | 4.28:1 | ❌ 低于 4.5 |
| `#77809c` | 次要文字 | 3.92:1 | ❌ 低于 4.5 |
| `#a4abc4` | 最弱文字 | 2.28:1 | ❌ 严重不足 |

因此**保留其色相与设计语言，文字相关角色一律加深一档**。最终 token 全部经过脚本验算（白底与浅底 `#f6f8fd` 双背景）：

```css
:root {
  /* 品牌蓝 —— 色相取自 dropleap.cn，文字角色加深 */
  --blue:        #3370ff;  /* 品牌色：仅用于大字标题、大色块、深色区装饰 */
  --blue-text:   #2b5ce0;  /* 链接、按钮填充（白底 5.66:1；白字压其上 5.66:1）*/
  --blue-strong: #1a3a8a;  /* hover、深色底（白底 10.42:1）*/
  --blue-soft:   #eef3ff;  /* 标签底、图标底（装饰）*/
  --blue-line:   #dbe6ff;  /* hover 边框（装饰）*/

  /* 文字四级 —— 全部通过 AA（白底 / 浅底）*/
  --ink:   #141c33;  /* 标题      16.89 / 15.89 */
  --body:  #3d4663;  /* 正文       9.31 /  8.77 */
  --mut:   #5c6580;  /* 次要文字   5.79 /  5.45 */
  --faint: #646d88;  /* 最弱标签   5.14 /  4.84 */

  /* 底与线 */
  --line: #e7ebf4;  /* 边框（装饰，无对比度要求）*/
  --soft: #f6f8fd;  /* 浅底 / tint section */
  --dark: #0d1b3e;  /* 深色 CTA 块起点（白字压其上 16.89:1）*/

  /* 圆角 */
  --r: 14px;
  --r-l: 20px;

  /* 阴影（照搬 dropleap.cn）*/
  --sh-1: 0 1px 2px rgba(20,28,51,.05), 0 4px 16px rgba(20,28,51,.05);
  --sh-2: 0 6px 20px rgba(20,28,51,.07), 0 16px 40px rgba(20,28,51,.06);
  --sh-3: 0 12px 32px rgba(20,28,51,.10), 0 32px 72px rgba(20,28,51,.10);
}
```

**使用纪律**（后续测试会断言）：

- `--blue` **不得**用于正文尺寸的文字。它只允许出现在：≥24px 的标题、大色块填充、深色区装饰。
- 正文链接与按钮填充一律用 `--blue-text`。
- `--blue-soft` / `--blue-line` / `--line` 是装饰色，不得承载文字，除非该文字自身颜色达标（`--blue-text` 压 `--blue-soft` 为 5.09:1 ✅）。

### 版式

```
容器      1200px（原 1100px）· gutter 40px · 移动 22px
section   上下 104px（原 68px）· 移动 72px
标题间距  标题到内容 64px
字体      -apple-system, BlinkMacSystemFont, "PingFang SC", "Microsoft YaHei", sans-serif
基准      body 16px / 1.75
```

字号层级（标题一律 800 字重 + 负字距，取自 dropleap.cn）：

| 元素 | 字号 | 字重 | 字距 | 行高 |
|---|---|---|---|---|
| h1 | 44px | 800 | -1.2px | 1.28 |
| h2 | 42px | 800 | -1px | 1.25 |
| h3 | 23px | 800 | -0.4px | 1.3 |
| lede | 17px | 400 | — | 1.8 |
| body | 16px | 400 | — | 1.75 |
| 小字 | 13/14px | 400-600 | — | 1.6-1.7 |
| 微标签 | 11-12.5px | 600-700 | +0.2-0.5px | — |

移动端：h1 36px / -0.8px，h2 30px。

### 组件与母题

- **导航**：sticky、72px、`rgba(255,255,255,.92)` + `backdrop-filter: blur(18px)`、底部 1px `--line`；激活态 `--blue-text` 文字 + 3px 蓝色下划线（`border-radius: 3px 3px 0 0`，贴在导航底边上）。
- **按钮**：统一 12px 圆角。primary = `--blue-text` 填充 + 白字；ghost = 白底 + `--line` 描边，hover 变 `--blue-text` 描边与文字。hover 统一 `translateY(-2px)`。
- **卡片**：`--r` / `--r-l` 圆角、1px `--line` 边框、hover 变 `--blue-line` 边框 + `--sh-2` 阴影 + `translateY(-2~3px)`。
- **虚线分隔**：`border-top: 1px dashed var(--line)` 作为反复出现的母题，用于列表行、卡片内分区。
- **编号圆形标注**：22px 蓝底白字圆形，用于产品界面示意的注释点。
- **eyebrow pill**：白底 + `--blue-line` 描边 + `--sh-1`，内含 7px 蓝点带 2s 脉冲动画。
- **深色 CTA 块**：全站唯一的深色区块，`linear-gradient(135deg,#0d1b3e 0%,#1a2f6d 55%,#3370ff 130%)`。
- **图标**：一律 inline SVG stroke 图标（`fill:none; stroke:currentColor; stroke-width:1.8; stroke-linecap:round; stroke-linejoin:round`），不引入图标字体或图标库。

### 断点

收敛为两个（原文件有 9 个 media query）：`1024px`（4 列 → 2 列）、`768px`（→ 单列，导航折叠）。

### 背景交替

原实现用 `.section:nth-of-type(2n/2n+1)` 交替底色，导致**插入或删除任何 section 都会翻掉其后所有 section 的底色**。改为显式 class：`.sec`（白）与 `.sec--tint`（`--soft`）。

## 信息架构

9 → 12 个板块。导航取 8 项，其余为次级板块从页脚可达。

| # | 板块 id | 名称 | 底色 | 导航 | 来源 |
|---|---|---|---|---|---|
| 1 | `hero` | 首屏 | 渐变 | — | 改造 |
| 2 | `cases` | 客户案例 | 白 | ✓ 案例 | **新增** |
| 3 | `product` | 产品 | tint | ✓ 产品 | 重构原 `#ventures` 旗舰块 |
| 4 | `services` | 服务与培训 | 白 | ✓ 服务 | **新增** |
| 5 | `industries` | 行业 | tint | ✓ 行业 | **新增** |
| 6 | `books` | 著作 | 白 | ✓ 著作 | 保留 |
| 7 | `agent-skills` | WorkBuddy Skills | tint | — | 保留 |
| 8 | `about` | 关于 | 白 | ✓ 关于 | 原 about + skills 合并 |
| 9 | `experience` | 履历 | tint | ✓ 履历 | 保留 |
| 10 | `speaking` | 演讲 | 白 | — | 保留 |
| 11 | `ventures` | 其他业务线 | tint | — | 保留但降权 |
| 12 | `contact` | 联系 | 深色渐变 | ✓ 联系 | 改造 |

导航顺序跟随 DOM 顺序，以保证 IntersectionObserver 高亮自然：案例 · 产品 · 服务 · 行业 · 著作 · 关于 · 履历 · 联系。

**移动端保留汉堡菜单**。dropleap.cn 删除了汉堡是因为它只有 6 项且实现是死代码；本站有 8 个导航项，需要折叠菜单，且现有实现可访问（`aria-expanded` + Escape 关闭 + 焦点返还）。

## 内容口径决策

以下三项此前在两站之间分叉，本规范统一：

1. **客户数量统一为「100+ 家制造企业」** —— 以公司对外口径为准，覆盖 llms.txt 里此前的「30+」。
2. **「4 阶段 Diagnose → Deliver → Review → Distill 方法论」** —— 该方法论在公司站并未发布，而 llms.txt 已对外声称其存在。改为在「服务与培训」板块把真实交付节奏写进可见页面（2-4 周跑通首个场景、驻场交付、首个场景验收合格后再定下一步），使 llms.txt 与页面自洽。
3. **客户信息保持匿名** —— 沿用公司站写法（「某工业紧固件与密封件分销企业」），仅以角色署名引语（「企业 CEO」「数字化负责人」），不出现公司名与个人名。

## 素材

新增素材全部复用自有公司资产，从 dropleap.cn 下载后本地化（不热链，沿用项目既有约束）：

| 路径 | 用途 | 尺寸 | 体积 |
|---|---|---|---|
| `assets/hero/hero-engineer.jpg` | 首屏右栏 | 1200×727 | 80KB |
| `assets/cases/case-fastener.jpg` | 案例 01 | 1200×618 | 90KB |
| `assets/cases/case-cnc.jpg` | 案例 02 | 1200×675 | 175KB |
| `assets/industries/ind-*.jpg` ×9 | 行业宫格 | 112×112 | 共 72KB |

行业图已从原始的 160×160 / 480×280 统一裁切压缩为 112×112（56px 显示尺寸的 2 倍图），9 张合计从约 175KB 降到 72KB。

图片格式保持 JPEG/SVG，与 dropleap.cn 一致。环境无 `cwebp`，不为此引入构建依赖。

## 非目标

- 不引入框架、构建步骤、npm 依赖或 CSS 预处理器
- 不新增滚动动画、轮播、视差、进场动画（沿用 2026-08-05 spec 的「不新增动画、轮播、弹窗或第三方组件」）
- 不接入 CMS 或运行时 API
- 不做深色模式（dropleap.cn 也没有）
- 不删除 `4B` 决策下保留的任何现有板块内容（含 Liora Moon、NihaoVisit 等非 AI 主业业务线）
- 不改 `main` 以外的分支，不创建 worktree

## 风险与回滚

| 风险 | 应对 |
|---|---|
| 页面从 9 屏增至 12 板块，滚动距离明显增加 | 保持顺序阅读，不做折叠；板块内信息密度向 dropleap.cn 对齐（短句 + 网格） |
| 双语成本：新增约 6 个板块的英文文案 | 贴近 dropleap.cn 的直白短句风格；交付后需人工过一遍 |
| 与 dropleap.cn 内容重叠可能稀释 SEO/GEO | 个人站保持「人的视角」（案例带客户原话、履历、演讲），公司站保持「产品视角」 |
| CSS 重写期间 Lighthouse 分数波动 | 以最终本地 Lighthouse 结果为准，验收线 accessibility ≥0.95（error 级） |
| 重写 diff 巨大 | 按板块逐个 diff 检查点验收，而非一次性 review |

回滚：全部改动集中在 `css/style.css`、`index.html`、`js/main.js`、`tests/`、`llms.txt`、`sitemap.xml`、`og-cover.*` 与新增素材目录；未提交前 `git checkout` 即可完全回滚。按项目既有约定，本工作**不 commit、不 push**，除非用户明确要求。

## 修订（同日）：个人主页化修正

首版实现把 dropleap.cn 的板块结构、话术与素材整套搬了过来，页面读起来像公司站的镜像而非个人主页。经确认执行两项修正：

1. **业务内容压成一个板块（2A）**：客户案例保留但改第一人称（「我带队接入……」），产品压缩为一段第一人称导语 + 2 个核心 Skill 卡 + 通往 dropleap.cn 的外链；删去产品界面 mockup、WorkBuddy 4 件套详解卡、培训课程三卡、9 宫格行业。培训方法论在著作板块以一句 lede 带过（「把交付方法沉淀成可传授内容」），行业收敛为导语中的一个从句。
2. **首屏配图换成本人登台照（3A）**：`assets/hero/onstage.jpg`（2024 刀法年度峰会演讲照，952×638）。演讲板块因此移除重复的同一张图；`assets/speaking/`、`assets/industries/`、`assets/hero/hero-engineer.jpg` 删除。

修正后的信息架构（12 → 9，个人内容前置）：

| # | 板块 | 底色 | 导航 |
|---|---|---|---|
| 1 | `hero` 首屏（个人定位 + 登台照） | 渐变 | — |
| 2 | `about` 关于我（简介 + 核心能力） | 白 | ✓ |
| 3 | `work` 我在做什么（导语 + 2 Skill 卡 + 2 案例） | tint | ✓ |
| 4 | `books` 著作 | 白 | ✓ |
| 5 | `agent-skills` WorkBuddy Skills | tint | — |
| 6 | `experience` 履历（时间线 + 战绩 + logo 墙） | 白 | ✓ |
| 7 | `speaking` 演讲 | tint | ✓ |
| 8 | `ventures` 其他业务线 | 白 | — |
| 9 | `contact` 联系（深色渐变，个人式邀请） | 深色 | ✓ |

口吻原则：**公司站保持产品视角，个人站保持人的视角**。`llms.txt` 与 JSON-LD 保留业务细节（GEO 资产，机器可读层允许比页面更详尽），但 FAQ 中「培训体系」一问替换为著作一问以与页面对齐。

验证：契约测试 40 项全绿（移除行业缩略图断言）；Lighthouse 桌面 accessibility / best-practices / SEO = 1.00，performance = 0.99（首屏图不再懒加载所致，阈值 0.9）。
