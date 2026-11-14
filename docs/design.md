# 站点设计规范

本文件是站点的唯一设计文档，只描述系统现状。规则的机器强制点在各节标注（`tests/test_homepage_content.py`，下称「契约测试」）。

## 1. 站点定位与内容原则

- 站点是**个人主页**：施可（Shi Ke），企业级 AI 落地实战讲师、水滴跃动 Dropleap 创始人。叙述主轴为「培训为主、FDE 驻场交付为辅」：课程体系是核心板块，交付板块定位为课堂案例的出处。
- 视觉系统采用 dropleap.cn 的品牌蓝与企业风；文案保持**第一人称**，个人内容前置。公司站是业务证据的来源，不是内容模板——板块层面的产品与案例细节一律链接到 dropleap.cn，不在本站展开第二份。
- 口吻分工：公司站保持产品视角，本站保持人的视角。
- 客户案例中的客户名称匿名，引语仅以角色署名（企业 CEO、数字化负责人）。
- 内容红线：已废弃的口径（数商方略、乐奇 Minibus EV、阿里云 AI 大赛银奖、邻汇吧任内经营数字等）永不回归，完整清单由契约测试 `RedLineTests.RETIRED` 强制；客户规模对外口径为「100+ 家制造企业」，由 `test_client_footprint_is_stated_once` 强制。

## 2. 信息架构

页面共 10 个板块（`index.html`），顺序即导航顺序：

| # | id | 板块 | 底色 | 导航 |
|---|---|---|---|---|
| 1 | `hero` | 首屏（讲师定位 + 登台照 + 双 CTA，主 CTA 指向培训） | 浅蓝渐变 | — |
| 2 | `about` | 关于我（讲师档案 + 数据 + 核心能力） | 白 | 关于 |
| 3 | `training` | AI 实战培训（导语 + 2 旗舰课程卡 + 四条课程线 + 课堂现场照片行 + 免费内容一句话） | 浅灰 | 培训 |
| 4 | `books` | 著作（3 本，课程的教材底座） | 白 | 著作 |
| 5 | `work` | 实战交付（导语 + 2 Skill 卡 + 2 案例卡，课堂案例的出处） | 浅灰 | 交付 |
| 6 | `agent-skills` | WorkBuddy SkillHub 的 2 个 skill | 白 | — |
| 7 | `experience` | 履历（时间线 + 战绩 + logo 墙） | 浅灰 | 履历 |
| 8 | `speaking` | 演讲（3 场） | 白 | 演讲 |
| 9 | `ventures` | 其他业务线（5 条） | 浅灰 | — |
| 10 | `contact` | 联系（深色渐变 CTA + 微信二维码） | 深色渐变 | 联系 |

- 底色交替用显式 class（`.sec` / `.sec--tint`），不依赖 `nth-of-type` 计数。
- 叙述顺序即页面顺序：`training` 紧随 `about`（培训为主），`work`（实战交付）紧随 `books`（交付为课程背书），由 `test_training_leads_and_delivery_backs_it_up` 强制；课程事实以 workshop 讲师资料库（产区口径）为源，班型全表、价格、报名方式只在 dropleap.cn/training，本站不展开第二份。
- 每个 `section` 有唯一 `id`，导航链接必须指向其中之一——当前板块高亮依赖此契约（`js/main.js` 的 IntersectionObserver；`test_every_nav_link_points_at_a_section`）。
- 每个板块恰有一个 `h2`，标题层级不跳级（`StructureTests`）。
- 语言解析顺序：`?lang=` URL 参数（命中后持久化）→ `localStorage` → 中文默认。

## 3. 设计系统

品牌蓝 `#3370ff` 源自 dropleap.cn；承载文字的颜色角色较其原色板加深一档，使其在白底与浅灰底（`--soft`）双背景下均满足 WCAG AA（≥4.5:1）。全部 token 定义于 `css/style.css` 的 `:root`，实测对比度写在各 token 行内注释。

| 角色 | token | 用途 |
|---|---|---|
| 品牌蓝 | `--blue` | 仅限大字号、大色块、深色区装饰；**禁止**用于正文尺寸文字（`test_brand_blue_is_never_used_for_text`） |
| 文字蓝 | `--blue-text` | 正文链接、按钮填充 |
| 深蓝 | `--blue-strong` | hover、深色底 |
| 装饰蓝 | `--blue-soft` / `--blue-line` / `--blue-light` | 标签底、hover 边框、深色区高亮文字 |
| 文字四级 | `--ink` / `--body` / `--mut` / `--faint` | 标题 → 正文 → 次要 → 最弱，双背景 AA 由 `DesignSystemTests` 实算强制 |
| 底与线 | `--line` / `--soft` / `--dark` | 边框、浅底、深色 CTA |

版式：容器 1200px，gutter 40px（移动 22px）；section 上下 104px（移动 72px）；标题 800 字重配负字距（h1 44px、h2 42px、h3 23px）；正文 16px/1.75；系统字体栈，零 webfont。

组件母题：虚线分隔线、22px 编号圆标、脉冲点 eyebrow pill、3:4 书封框、深色渐变 CTA（全站唯一深色区块）、卡片 hover 抬升 2–3px。交互保持最小：不引入轮播、视差、进场动画或第三方组件库。

断点仅两个：1024px（4 列→2 列）与 768px（→单列，导航折叠为汉堡菜单）。CSS 无 `!important`、无重复定义，行数预算 <2600（`test_css_hygiene`、`test_only_two_responsive_breakpoints`）。

## 4. 双语机制

- 中文写在元素文本里，英文写在 `data-en`；ARIA 覆盖用 `data-en-aria`，图片用 `data-en-alt`。英文元数据（title/description）在 `js/main.js` 的 `EN_META`，中文元数据只存在于 `<head>`——单一真相。
- **`data-en` 只能标注叶子元素**：切换语言用 `textContent` 覆盖，带子元素的元素会被抹掉且不可恢复。JS 端有运行时守卫，契约测试 `test_no_data_en_on_elements_with_children` 静态强制。
- 语言切换按钮的可访问名称必须包含可见文本（WCAG 2.5.3）。

## 5. 素材规范

### 5.1 目录与通用规则

| 目录 | 内容 |
|---|---|
| `assets/hero/` | 首屏照片（本人登台照 `onstage.jpg`，952×638） |
| `assets/cases/` | 两张案例配图 |
| `assets/training/` | 课堂现场照片（苏州 FDE 社区沙龙 2026-11，4 张） |
| `assets/books/` | 三本书封（两 JPEG 一 SVG） |
| `assets/logos/` | logo 墙品牌标 + 业务线 icon |
| `assets/wechat/` | 个人微信二维码 |
| 根目录 | `og-cover.svg`（源）→ `og-cover.jpg`（1200×630 社交预览）、`apple-touch-icon.png`（180×180） |

- 所有图片本地存储，不热链；声明 `width`/`height` 与磁盘实际一致（`test_asset_dimensions_match_their_declarations`）、`decoding="async"`、首屏外 `loading="lazy"`（`test_images_declare_dimensions_and_loading`）。
- 图片只做格式兼容与体积优化，**不改变图形内容**；单文件目标 <500KB。
- 社交预览再生成：改 `og-cover.svg` 后用无头 Chrome 截图渲染、`sips` 转 JPEG（流程见 README Notes）。
- 注意：`assets/books/` 的封面文件扩展名与真实字节格式可能不一致（存在 PNG 文件名、JPEG 字节的文件）；重新导出时须核对真实字节格式再定扩展名。

### 5.2 品牌素材红线

- **不重新绘制或仿制任何品牌标识**；只用下表来源获取的官方图形。
- **不使用 `fantown.com`**（域名属墨西哥体育周边商店，与中国聚星动力无关）与不存在的 `mallfantown.com`。
- 聚星动力展示名为「聚星动力 FanTown」，使用其母公司 ALL STAR PARTNER 的 icon；该 icon 不错配给「世界杯」事件标题。
- 业务线 icon 与可见品牌名相邻，因此一律 `alt=""` + `aria-hidden="true"`，避免辅助技术重复朗读。

溯源表（官方来源 → 本地文件）：

| 本地文件 | 来源 | 格式说明 |
|---|---|---|
| `assets/logos/xingqi-geo.png` | xingqigeo.cn 官方 favicon | ico 转 PNG，64×64 |
| `assets/logos/whobot.svg` | whobot.com 官方 | SVG（内嵌位图路径） |
| `assets/logos/nihaovisit.svg` | nihaovisit.com 官方 | SVG |
| `assets/logos/liora-moon.png` | lioramoon.com 官方 icon | PNG，512×512 |
| `assets/logos/all-star-partner.png` | allstarpartner.com（聚星动力母公司） | PNG，300×300 |

logo 墙的其余品牌标为各品牌官方渠道获取的图形文件，同样适用「不重绘」红线。

### 5.3 展示规则

- 书封：3:4 海报框（`.book-cover-frame`，`width: min(100%, 240px)`）+ `object-fit: contain` 完整保留原始封面，**不裁剪、不拉伸**；框建立视觉节奏，不依赖源图尺寸。
- 展示顺序：AI Coding → FDE → WorkBuddy（最新出版在最后）。

## 6. 机器可读层（GEO）

- `index.html` 内嵌 JSON-LD `@graph`：Person（jobTitle 讲师前置）、Organization、WebSite、ProfilePage、FAQPage（8 问）、Book ×3、Course ×6（FDE 实战营、企业定制内训、WorkBuddy 全员应用实战、大模型技术基础实战、企业级大模型私有化实战、制造业企业主 AI 通识课，`instructor` 指向 Person）。节点间用 `@id` 互链（Person `worksFor` Organization，Organization `founder` Person）。
- `llms.txt` 是面向 LLM 爬虫的英文摘要，比页面更详尽（含完整培训体系、行业清单）；`robots.txt` 对 AI 爬虫全量放行。
- 一致性契约：书名、书 URL、课程名、课程 URL、案例数字、引语在页面 / JSON-LD / llms.txt 三处同源；`dateModified`、sitemap `lastmod`、llms.txt `Last updated` 三处日期一致且不晚于今天（`MachineReadableTests` 交叉断言）。

## 7. 质量门

- 契约测试：`python3 -m unittest discover -s tests`，44 项，分五组——结构锚点、双语契约、设计系统（含 WCAG 对比度实算）、机器可读层一致性、内容红线。只断言不变量，不冻结营销文案与像素值。
- Lighthouse CI：accessibility ≥0.95、SEO ≥0.95 为 error；performance、best-practices ≥0.9 为 warn；desktop preset。当前基线四项 1.00。
- CI（`.github/workflows/lighthouse.yml`）：push/PR 先跑契约测试，通过后跑 Lighthouse。

## 8. 维护约定

- 零依赖：纯 HTML/CSS/原生 JS，不引入 npm 包、CMS、运行时 API 或构建步骤。
- 文档只写终态：本文件与 README 描述系统现状；变更过程、验收与回滚不落入仓库文档。
- 协作：未经明确指示不 commit、不 push。
