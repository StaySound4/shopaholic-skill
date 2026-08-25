# 🛒 Shopper — 循证购物决策与全景行业调研 Skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Pi Agent Compatible](https://img.shields.io/badge/Pi%20Agent-Compatible-brightgreen)](https://github.com/StaySound4/pi-shopper)
[![ClawHub](https://img.shields.io/badge/ClawHub-Ready-blue)](https://clawhub.ai)
[![Ecosystem](https://img.shields.io/badge/Supports-Claude%20%7C%20OpenClaw%20%7C%20Pi-orange)](https://github.com/StaySound4/pi-shopper)

> **打破营销信息差，买前先做文献级行业深研与硬件拆解通病反查。**
> 专为中国电商生态（淘宝、京东、拼多多、抖音等）打造的完全自包含 AI 购物决策顾问。

---

## ⚡ 一行命令安装 (Installation)

### 1. 在 Pi Coding Agent 中安装：
```bash
pi install git:StaySound4/pi-shopper
```

### 2. 任意终端 npx 本地一键安装（拷贝至本地 Agent Skills 目录）：
```bash
npx pi-shopper
```

### 3. 在 OpenClaw / ClawHub 中使用：
```bash
clawhub install shopper
```

### 4. 手动克隆至你的 Agent 目录：
```bash
git clone https://github.com/StaySound4/pi-shopper.git ~/.agents/skills/shopper
```

---

## 🌟 核心特性 (Key Features)

1. **🔬 阶段零：行业前置深研（文献标准级调研）**
   - 绝不一上来就向用户抛出繁琐问卷或直接推荐商品。
   - 自动深入底层制造工艺、物理化学机理、供应链核心元器件等级，检索国家强制标准（GB/T）、国际权威机构认证（FDA/EFSA/WHO）与核心专利。
2. **🚫 绝对不问预算**
   - 用户需要预算限制时会主动说明；未说明时，通过清晰的分层矩阵（第一梯队/高性价比口粮/小众特定选/淘汰不建议）全价格带自然覆盖。
3. **🛰️ 4 轨并行深度核验协议（4-Lane Investigation）**
   - **Lane 1: 市场全景与价格带**（主流/新锐/黑马/代工线全景扫描与真实到底价）
   - **Lane 2: 规格参数与标准溯源**（铭牌参数、CCC编号、成分配方表去伪存真）
   - **Lane 3: 独立拆解实测与真实客诉**（第三方实验室拆机图、红外热成像、老化测试、黑猫投诉与高频硬件暗病）
   - **Lane 4: 定向反查与水军公关清洗**（定向检索 `[型号] + 偷偷降级/虚标/翻车/通病`，剥离 MCN 种草软文）
4. **🛡️ 强制披露真实缺点与已知通病**
   - 拒绝商业互吹与只夸不贬，候选表格中强制要求列出每款产品的真实缺点、已知翻车点与不适合人群。
5. **🎯 全自闭环交付**
   - 包含【模块零：前置调研综述】、【模块一：决策核心与底层判断法】、【模块二：品类雷点与避坑红线】、【模块三：分层矩阵】与【模块四：下单验货防翻车清单】。

---

## 📊 覆盖品类知识库 (Category Coverage)

- ☕ **咖啡与食品饮料**：冷冻升华干燥(FD) vs 喷雾干燥(SD)、SCA 杯测分级、丙烯酰胺安全阈值、开封抗氧化
- 💻 **电脑数码与消费电子**：Mini-LED vs OLED 像素排列、主控与闪存颗粒防 QLC 混用、功耗释放与散热规格
- ❄️ **大型家电（空调/冰箱/洗衣机/烘干机）**：热泵压缩机 vs 冷凝烘干、循环风路防串味、铜铝缩水防漏氟
- 🧹 **生活电器与清洁个护（扫地机/洗地机/电吹风）**：双目避障、真热风烘干($>60^\circ\text{C}$) vs 冷风发臭、上下水防爆管泡水
- 🧴 **日化、美妆护肤与清洁用品**：核心有效活性成分浓度促渗、国妆特字/网备字查验、防“概念性添加”
- 👶 **母婴、儿童、玩具与安全座椅**：GB 27887、ECE R129 (i-Size) 侧撞认证、食品接触级材质安全
- 🪑 **家具、人体工学椅与床垫寝具**：TUV Class 4 级防爆气压棒、ENF 级环保检测报告、防劣质胶水硬棕
- 🧗 **户外、鞋服与运动装备**：PTFE 膨体微孔膜防水透湿量、超临界发泡中底、Vibram 防滑大底实测

---

## 📂 项目结构 (Structure)

```text
pi-shopper/
├── package.json               # npm & Pi Package 描述配置
├── README.md                  # 详细使用与说明文档
├── LICENSE                    # MIT 开源协议
├── bin/
│   └── cli.js                 # npx 一键安装脚本
└── skills/
    └── shopper/
        ├── SKILL.md           # 核心 Skill 指令与五步法工作流
        └── references/        # 深度参考知识库与协议
            ├── category-checklists.md   # 8 大品类供应链与避坑清单
            ├── evidence-and-risks.md    # 证据链、信息污染与电商套路反查
            └── research-protocol.md     # 4-Lane 调研模型与文献级取证协议
```

---

## 🤝 贡献与反馈 (Contributing)

欢迎提交 Issue 和 Pull Request，共同丰富各品类的避坑清单与供应链反查规则！

## 📄 License

[MIT License](LICENSE) © 2026 StaySound4
