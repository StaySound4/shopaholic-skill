# 06 — 多子代理消融基准与全链路端到端验证套件 (Ablation Benchmark & End-to-End Suite)

**What to build:** 更新自动化消融评测套件 `scripts/ablation-suite.js`，加入对仓库级安装、全价格带广度探索、双轮递进质询（含二手偏好）、跨轮次证据聚合与四维代价守恒的端到端自动化量化验证。

**Blocked by:** 05 — 冷峻抗谄媚接入与形态跃迁四维代价守恒

**Status:** closed

- [x] 更新 `scripts/ablation-suite.js`，覆盖广度探索、双轮质询、二手偏好、跨轮次聚合、双轨分档与四维代价的量化断言
- [x] 运行自动化评测，确保 Oracle 组得分 100 分通过，各消融组呈现预期的显著性下降
- [x] 完成端到端场景（跨界相机、二手数码、大家电选购）的链路验证
