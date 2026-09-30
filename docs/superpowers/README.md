# docs/superpowers — 决策文档索引

本目录存放站点的 spec（设计规范）与 plan（执行计划），约定：

- **命名**：`specs/YYYY-MM-DD-<slug>-design.md` 与 `plans/YYYY-MM-DD-<slug>.md`，日期为决策日
- **流程**：先写 spec 定决策，再写 plan 定步骤，逐任务实现；契约测试先行
- **append-only**：历史文档是当时的决策记录，**事后不回写**。过时的内容靠本索引标注状态，修正记录在新 spec 里（如 2026-09-18 rebrand spec 的「修订」一节）

## 现行

| 文档 | 内容 |
|---|---|
| [specs/2026-09-18-dropleap-rebrand-design.md](specs/2026-09-18-dropleap-rebrand-design.md) | 当前设计系统（dropleap 蓝、AA 加深）、个人主页化修订、token 对照表 |
| [plans/2026-09-18-dropleap-rebrand.md](plans/2026-09-18-dropleap-rebrand.md) | 上述 spec 的执行计划与全局约束（双语契约、外链规则等仍有效） |

## 历史（已被后续决策部分或全部取代，仅作记录）

| 文档 | 状态 | 被取代的原因 |
|---|---|---|
| specs/2026-05-06-github-homepage-design.md | 过时 | 建站 spec。8 板块结构、靛蓝 `#2563EB`、1100px、`data-zh` 双属性 i18n、「邻汇吧 VP」定位均已被后续迭代替换 |
| plans/2026-05-06-github-homepage.md | 过时 | 实现上述建站 spec 的计划，同上 |
| specs/2026-08-04-homepage-products-books-design.md | 部分过时 | 「2 本著作 + GitHub 链接」已变为 3 本 + GitBook；业务线 4 条已变 5 条（+FanTown）；「不引入新视觉体系」已被 2026-09-18 rebrand 取代 |
| plans/2026-08-04-homepage-products-books-profile.md | 部分过时 | 同上；其中 Global Constraints（零依赖、双语、外链规则、图片规范、不主动 commit）**仍然有效** |
| plans/2026-08-04-books-cover-layout.md（仅有 plan，无对应 spec） | 部分过时 | 3:4 封面框尺寸与 `object-fit: contain` 规则仍有效；「两张书卡 / 双列」背景已过时 |
| specs/2026-08-05-brand-icons-density-design.md | 大体有效 | 素材来源与「不重绘品牌标识」规则仍有效；密度数值已被 rebrand 的 104px 节奏取代 |
| plans/2026-08-05-brand-icons-density.md | 部分过时 | 「移动端 section 保持 40px」已被 72px 取代 |
| specs/2026-08-20-add-workbuddy-book.md | 有效 | 第三本书 + GitBook 迁移，与现状一致 |
| plans/2026-08-20-add-workbuddy-book.md | 有效 | 同上 |
