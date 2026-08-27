# 06 — 端到端真实复杂场景实测与正式发版验收 (End-to-End Verification & Release)

**What to build:** 对包含摩托车运动相机/全景相机在内的复杂真实选购用例进行端到端全流程实测推演，确保所有规则无缝衔接且无回归缺陷，最终完成代码库与文档的正式同步并完成发布验收。

**Blocked by:** 05 — 多子代理消融/增添实验自动化评测套件与量化验证

**Status:** completed

- [x] 针对“预算4000摩托车相机（兼顾下巴与全景，考察大疆与影石）”执行端到端演练：
  - 触发防御性检索准确召回 DJI Osmo 360；
  - 两阶段视角自适应保全下巴机位（Action）与全景机位（Osmo 360 / X4）；
  - 双轨矩阵完整呈现 A 档与 B 档 6~10 款代表产品；
  - 闭环四维代价守恒（切视角耗时、重载金属夹、8K解码算力、鱼眼碎镜换修成本）。
- [x] 检查 `skills/shopaholic/SKILL.md` 与全部 `references/*.md` 文档，确保 Markdown 格式规范、逻辑闭环、无过时引用。
- [x] 确认 `.scratch/shopaholic-refactor/` 下 `spec.md` 及 01~06 编号 Ticket 文件持久化写入完成。
