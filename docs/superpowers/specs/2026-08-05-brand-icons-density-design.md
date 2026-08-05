# 官网品牌图标与页面紧凑化设计

## 项目概述

在不删除现有内容、不改变纯静态架构的前提下，为 Ventures 中五个项目加入官方真实品牌 icon，并采用“平衡紧凑”方案收紧全站纵向空间。目标是在保留个人品牌官网层级和可读性的同时，减少桌面端过度留白和无效滚动。

## 已确认决策

- 使用五个品牌官方公开图标，并保存为本地资源，不使用长期热链
- FanTown 使用其运营主体北京聚星动力文化传媒有限公司的官方母公司品牌 ALL STAR PARTNER / 聚星动力 icon
- 页面密度采用方案 A“平衡紧凑”
- 保留所有现有区块、文案、Books 3:4 封面框、双语切换和交互
- 只在 `main` 分支工作，完成后提交并推送
- 已核对本地和远端分支：除 `main` 外无其他分支，不需要执行删除操作

## 官方图标来源

| 项目 | 官方站 | 下载源 | 本地目标 | 格式与说明 |
|---|---|---|---|---|
| 微盟星启 GEO | `https://www.xingqigeo.cn/` | `https://www.xingqigeo.cn/favicon.ico` | `assets/logos/xingqi-geo.png` | 官方 64×64 favicon；转换为同尺寸 PNG，避免 ICO 浏览器差异 |
| 呼波特 WhoBot | `https://whobot.com/` | `https://whobot.com/Logo.svg` | `assets/logos/whobot.svg` | 官方页眉与 favicon 共用 SVG；文件内部含品牌位图数据，保持原文件 |
| NihaoVisit | `https://nihaovisit.com/` | `https://nihaovisit.com/icon.svg` | `assets/logos/nihaovisit.svg` | 官方 PWA manifest 矢量 icon |
| Liora Moon | `https://lioramoon.com/` | `https://lioramoon.com/icon-512.png` | `assets/logos/liora-moon.png` | 官方 512×512 应用 icon；按页面需求优化但不裁剪 |
| 聚星动力 FanTown | `http://www.allstarpartner.com/` | `https://nwzimg.wezhan.cn/sitefiles10323/10323482/asp.png` | `assets/logos/all-star-partner.png` | 官方母公司 ALL STAR PARTNER / 聚星动力 300×300 icon |

### 使用约束

- 不使用 `fantown.com`：该域名属于墨西哥体育周边商店，与中国聚星动力无关
- 不使用不存在的 `mallfantown.com`
- 不重新绘制或仿制任何品牌标识
- 下载后验证真实格式、像素尺寸和透明背景；只进行格式兼容或体积优化，不改变图形内容
- icon 与可见品牌名相邻，因此图片使用 `alt=""` 和 `aria-hidden="true"`，避免辅助技术重复朗读

## Ventures 结构设计

### 内联品牌单元

在现有 `.venture-sub-head` 内加入 `.venture-sub-brand`：

```html
<div class="venture-sub-brand">
  <span class="venture-sub-logo" aria-hidden="true">
    <img src="assets/logos/…" alt="" width="32" height="32" loading="lazy" decoding="async">
  </span>
  <span class="venture-sub-name" data-en="…">…</span>
</div>
```

视觉规范：

- icon 槽位：桌面 32×32px，移动端 28×28px
- 图标使用 `max-width: 100%`、`max-height: 100%`、`object-fit: contain`
- 品牌单元使用 Flexbox，icon 与名称间距 10px
- `.venture-sub-head` 仍负责品牌单元与“咨询 / 访问”CTA 的两端对齐
- 小屏幕允许品牌单元压缩，但 CTA 保持不换行

### FanTown 卡片

“近期操盘”卡片的子项标题从“2026 世界杯正版授权快闪店”调整为：

- 中文：`聚星动力 FanTown`
- English: `FanTown by All Star Partner`

描述保留并重组为：

- 中文：`运营 2026 世界杯正版授权快闪店，落地常锡沪三城，把赛事流量转化为可衡量的客流与销售。`
- English: `Operated officially licensed 2026 World Cup pop-ups across Changzhou, Wuxi, and Shanghai, turning event traffic into measurable footfall and sales.`

该调整使 icon、标题和运营主体一致；不把聚星动力母公司 icon 错配给“世界杯”事件标题。

## 平衡紧凑参数

### 全局节奏

| 项目 | 当前值 | 目标值 |
|---|---:|---:|
| `--section-padding` | 100px | 68px |
| Hero 顶部 / 底部 | 160px / 120px | 120px / 72px |
| `.section-header` 底部 | 48px | 32px |
| `body` 行高 | 1.75 | 1.70 |

移动端现有 `.section { padding: 40px 0; }` 保持不变。

### 卡片与网格

| 项目 | 当前值 | 目标值 |
|---|---:|---:|
| Skills / Project 卡片 padding | 32px | 24px |
| Venture / Book 卡片 padding | 28px | 24px |
| Track 卡片 padding | 28px | 24px |
| Ventures / Track / Books gap | 24px | 20px |
| `.ventures-grid` 底部 margin | 48px | 0 |
| 主 Venture 卡片底部 margin | 24px | 20px |

Books 已批准的 3:4 封面框尺寸和响应式规则保持不变。

### About 与履历

| 项目 | 当前值 | 目标值 |
|---|---:|---:|
| About stats 底部 | 40px | 28px |
| About 段落底部 | 20px | 16px |
| About 段落行高 | 1.9 | 1.75 |
| Timeline item 底部 | 40px | 28px |
| Track record 上 margin / padding | 64px / 48px | 40px / 32px |
| Track 标题底部 | 36px | 24px |
| Track grid 顶部 | 40px | 24px |
| Logo wall 组间距 | 40px | 24px |
| Logo group 标题底部 | 20px | 14px |

### 演讲与联系

| 项目 | 当前值 | 目标值 |
|---|---:|---:|
| Speaking item 上下 padding | 24px | 18px |
| Contact description 底部 | 28px | 20px |
| Contact links gap | 24px | 16px |
| Contact QR 顶部 | 40px | 28px |

## 受影响文件

- `index.html`
  - 为五个项目加入 icon 单元
  - 调整 FanTown 标题和描述的中英文文案
- `css/style.css`
  - 新增 `.venture-sub-brand`、`.venture-sub-logo` 样式
  - 应用已确认的紧凑参数
- `assets/logos/xingqi-geo.png`
- `assets/logos/whobot.svg`
- `assets/logos/nihaovisit.svg`
- `assets/logos/liora-moon.png`
- `assets/logos/all-star-partner.png`
- `tests/test_homepage_content.py`
  - 验证官方本地资源、HTML icon 槽位、FanTown 口径与紧凑参数
- 本设计文档及对应实施计划

`js/main.js`、`llms.txt`、JSON-LD 与 `sitemap.xml` 无需修改；本次不改变产品范围、书籍内容、个人介绍或机器可读事实。

## 错误处理与稳定性

- 官网运行时不请求第三方 logo URL，所有图标均从本地加载
- 下载阶段若官方资源不可访问或格式与预期不符，停止实施并重新核实，不以截图、搜索结果缩略图或仿制图替代
- `<img>` 声明宽高、懒加载和异步解码，减少布局偏移
- 图标加载失败时仍保留可见品牌名称和 CTA，不影响主要功能
- 不添加运行时 JavaScript 或图片加载监听器

## 验证标准

### 图标

- 五个目标项目各有一个本地官方 icon
- 页面源码不直接引用五个官方站的远程图片 URL
- 图标在 320、768、1024 和宽屏下不拉伸、不溢出
- FanTown 使用聚星动力母公司 icon，且标题明确运营主体
- 图标不会导致按钮换行、卡片横向滚动或语言切换缺字

### 紧凑化

- 桌面端所有 Section 使用 68px 上下间距
- Hero、Section header、卡片、履历、Logo 墙、演讲和联系区采用本规格中的目标值
- 移动端 Section 仍为 40px，不进一步压缩
- 全部内容保留，页面区块顺序和交替底色保持不变
- Books 3:4 封面框保持现有尺寸

### 回归

- 中英文切换、移动导航、导航高亮正常
- 微盟星启 GEO 与呼波特 WhoBot QR 咨询正常
- NihaoVisit 与 Liora Moon 外链正常
- JSON-LD、`llms.txt`、Sitemap 内容不发生非预期变化
- Python 契约测试全部通过
- Lighthouse Performance、Accessibility、Best Practices、SEO 继续满足现有阈值

## Git 流程

- 开始实施前再次确认当前分支为 `main`
- 列出本地和远端分支；若出现非 `main` 分支，按用户明确授权删除
- 只在 `main` 修改，不创建功能分支或 worktree
- 验证通过后提交一次聚合 commit
- 通过 SSH 推送 `main` 到 `github.com:shike/shike.github.io.git`
- 推送后用 `git ls-remote` 确认远端 `main` 指向本地提交

## 非目标

- 不删除、合并或重排任何页面区块
- 不删减文案或履历内容
- 不重做现有 logo 墙
- 不改变 Books 封面布局
- 不新增动画、轮播、弹窗或第三方组件
- 不创建非 `main` 分支
