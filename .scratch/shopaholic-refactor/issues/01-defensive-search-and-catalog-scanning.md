# 01 — 防御性检索与品牌全系拉网扫描机制实现 (Defensive Search & Catalog Scanning)

**What to build:** 在 `skills/shopaholic/SKILL.md` 及 `references/research-protocol.md` 中构建“零信任防御性检索”和“品牌全系在售图谱拉网扫描”协议。彻底杜绝依赖预训练记忆断言“某产品不存在”的幻觉，确保在进入推荐前必须拉网扫描头部品牌全谱系。

**Blocked by:** None — can start immediately.

**Status:** completed

- [x] 在 `SKILL.md` 总原则中新增【认知零信任与防御性检索】强制条款：严禁依据静态内部权重断言品牌产品线或型号存在性；面对具体品牌/品类质询，强制前置执行 ≥2 组多角度全网检索。
- [x] 在 `references/research-protocol.md` 中重构“阶段零与 4-Lane 协议”，正式确立【品牌全谱系扫描（Catalog Scanning）】标准作业流程（SOP）：明确要求先扫描品类头部品牌（至少 3 个主流大厂 + 2 个新锐品牌 + 1 个代工/极客源头）的完整在售矩阵，再进入具体型号筛选。
- [x] 增加检索关键词构造规范：强制包含当前年份（如 2025/2026）、最新型号尾缀、官方发布会/官网资讯、垂直社区拆解等时效性锚点词。
- [x] 规范信源覆盖：普通品类总信源不少于 8 条，高风险/数码电器品类不少于 10 条，且必须包含官方规格与独立第三方实测的双重佐证。
- [x] 增加执行环境自适应契约：支持 Sub-agent 4-Lane 并发探针与单 Agent 串行多轮状态机降级运行。
