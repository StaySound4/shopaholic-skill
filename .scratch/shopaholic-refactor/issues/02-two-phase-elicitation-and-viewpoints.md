# 02 — 两阶段需求澄清与决策视角自适应架构 (Two-Phase Elicitation & Adaptive Viewpoints)

**What to build:** 重构 `SKILL.md` 的模式 A 与需求澄清机制，由原本的一轮死板单选问卷升级为“两阶段偏好诱导”。第一阶段提取硬约束与好恶特质，第二阶段让用户自选报告呈现视角（综合排序 / 细分场景矩阵 / 黑名单剔除），彻底解决“选了下巴机位就误杀全景”的问题。

**Blocked by:** 01 — 防御性检索与品牌全系拉网扫描机制实现

**Status:** completed

- [x] 在 `SKILL.md` 模式 A 中定义清晰的【两阶段交互契约】：
  - **Phase 1（画像与偏好萃取）**：调用 `ask_user_question` 收集空间、预算及对画质、重量、后期工作量、品牌的具体倾向（Preferences & Dislikes）。
  - **Phase 2（交付视角自适应选择）**：基于 Phase 1 提取的矛盾点与特征，通过 `ask_user_question` 让用户从 3 种视角中选择：① 综合优先级全局排布；② 按细分场景矩阵罗列；③ 硬性特征黑名单剔除。
- [x] 引入 H 类硬物理红线与 S 类软场景偏好语义解耦机制，严禁将 S 类偏好用于物理级候选池一票否决。
- [x] 更新 `references/category-checklists.md` 第 13 节，为典型品类（运动相机、洗烘设备、清洁电器、数码电脑）预置两阶段画像萃取与形态漂移速查表。
