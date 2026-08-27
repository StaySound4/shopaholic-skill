# 循证导购防冷门幸存者偏差与长尾风险防御规范 (Specification)

## Problem Statement

在现有的循证导购体系中，系统过度依赖“全网同类客诉 ≥ 3 起判定为通病”这一静态数量门槛，并对纸面法定参数（L1）与独立实测（L2）赋予绝对置信度。这导致面对**低销量、冷门、小众贴牌或长尾白牌商品**时，产生严重的“证据缺失谬误（Absence of Evidence is not Evidence of Absence）”：
1. **冷门幸存者偏差**：冷门商品因总保有量极低、全网缺乏公开差评，被初筛机制误判为“零缺陷、品控极佳”，在排除法中胜出。
2. **纸面高配与特挑送测**：冷门公模贴牌产品纸面堆料高，且少数评测多为厂商送测的特挑工程样机，无法反映流水线量产的真实装配公差、虚焊与品控一致性。
3. **后勤与售后断层**：冷门产品缺少全国联保、原厂零配件与长期耗材易断供、二手流动性近乎归零，但在矩阵中却与成熟大厂产品平起平坐，甚至挤占第一梯队首选位。

## Solution

建立**“样本量置信度校准 + 致命缺陷单起熔断 + 分轨推荐隔离 + 售后履约透明度”**的纵深防御体系：
1. **未验证惩罚（Unverified Penalty）**：低保有量或缺乏长期大样本真实追踪的商品，其质量状态强制标记为“长期耐用度与批次一致性未经验证”，且**严禁直接列入普通消费者的【第一梯队·大众稳妥首选】**。
2. **客诉判定动态化（Severity over Count）**：针对低保有量型号，取消“3 起通病门槛”；一旦存在 1 起涉及电源安全、主板烧毁、结构断裂等**致命安全/核心功能缺陷**，立即触发高危预警并强制披露。
3. **双轨推荐矩阵隔离**：在推荐体系中明确区分【大众稳妥首选（经大规模市场检验）】与【极客探索/高配小众参考（参数亮眼但需承担折腾与售后风险）】。
4. **供应链白盒化与售后通路核查**：小众商品必须穿透代工厂背景与上游方案；对比表格中强制披露【售后通路（全国联保 vs 寄修/店铺保）】与【耗材通用性】。

## User Stories

1. As a general household consumer, I want the system to recommend battle-tested products with national warranty networks as default choices, so that I can minimize post-purchase regret and maintenance friction.
2. As a general consumer, I want the system not to place untested niche products with zero bad reviews at the top of the ranking just because of their specs, so that I am not treated as an unpaid beta tester.
3. As a tech-savvy / enthusiast shopper, I want the system to isolate niche high-spec options into a dedicated exploratory tier with clear trade-off disclaimers, so that I can knowingly take calculated risks for extreme performance.
4. As a value-conscious buyer, I want the system to penetrate the OEM/ODM supply chain and public tooling origins of niche brands, so that I know their true manufacturing pedigree.
5. As a safety-conscious user, I want the system to immediately flag critical safety failures (e.g., thermal runaway, fire, structural collapse) even if there is only 1 reported incident, so that catastrophic risks are never overlooked due to low sales volume.
6. As a buyer comparing products, I want to see explicit "Market Verification Level" and "After-sales Channel" columns in comparison matrices, so that I can evaluate full-lifecycle ownership costs.
7. As a long-term user, I want the system to factor in proprietary consumable availability and low second-hand liquidity for niche goods into Total Cost of Ownership (TCO), so that I understand decision reversibility.
8. As the shopping decision consultant, I want the evaluation protocol to dynamically adjust complaint thresholds based on market volume, so that long-tail survivor bias is eliminated.

## Implementation Decisions

### 1. 市场验证度三级模型 (Market Verification Level Schema)
- `高验证 (V-High)`: 上市 ≥ 6 个月，全网保有量与独立长周期使用反馈充足，批次一致性经受检验。
- `中验证 (V-Mid)`: 成熟品牌新上市迭代款，或上游方案成熟且出货量稳定。
- `未充分验证 (V-Low / Unverified)`: 长尾白牌、新锐小众定制、众筹或出货量极小产品。强制施加置信度降级。

### 2. 缺陷严重度双轨判定规则 (Defect Severity Protocol)
- **一级致命缺陷 (Safety Critical)**: 自燃起火、高压击穿、主板批量烧毁、核心承重断裂。
  - *判定规则*: **单起即预警 (1 Incident Alert)**，不设保有量门槛，必须在落选说明或风险提示中置顶披露。
- **二级体验缺陷 (Quality of Life)**: 异响公差、按键虚位、漆面脱落、软件偶发 Bug。
  - *判定规则*: 主流高保有量商品维持 ≥ 3 起判定为通病；低保有量小众商品出现 1~2 起记录为“潜在批次公差风险”。

### 3. 推荐梯队准入红线 (Tier Admission Contract)
- **第一梯队（大众稳妥首选）**: 必须满足 `L1/L2 扎实用料` + `V-High/V-Mid 验证度` + `全国联保或成熟售后履约网络`。
- **第三梯队（极客探索/特定场景）**: `V-Low` 级商品即便纸面性价比极高，最高仅允许归入此梯队，并必须强制加注【极客尝鲜与售后妥协声明】。

### 4. 矩阵对比字段扩充 (Matrix Schema Expansion)
在推荐对比矩阵和终审淘汰矩阵中，统一扩展两项核心字段：
- `市场验证度`: 高验证 / 中验证 / 未充分验证
- `售后通路与保障`: 全国联保（官方上门）/ 品牌寄修 / 店铺自保

## Testing Decisions

- 仅测试外部决策行为与输出一致性，不测试内部实现细节。
- 覆盖三大核心用例：
  1. 冷门公模堆料产品测试：验证是否正确拦截第一梯队准入，并归入极客探索款；
  2. 单起致命安全故障测试：验证是否触发 1 起熔断机制；
  3. 大牌溢价款 vs 成熟高性价比款测试：验证是否在排除冷门陷阱的同时避免误导推崇大牌溢价。

## Out of Scope

- 不涉及底层 CLI 代码、打包构建逻辑变更。
- 不针对特定品牌维护静态黑白名单。
