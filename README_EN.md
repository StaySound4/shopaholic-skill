<div align="center">

<img src="assets/logo.png" alt="Shopaholic.skill Logo" width="140" height="140" style="border-radius: 24px; margin-bottom: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.15);">

# Shopaholic.skill

> **Open-source evidence-based consumer decision support & supply chain intelligence Agent Skill for shoppers using AI across Chinese e-commerce**  
> *Grounded in physical manufacturing principles, published industry standards, independent teardowns, and verified long-term consumer feedback to minimize post-purchase regret.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Agent Skills](https://img.shields.io/badge/Agent%20Skills-Standard-green)](https://agentskills.io)
[![skills.sh](https://img.shields.io/badge/skills.sh-Compatible-blue)](https://skills.sh)
[![Multi-Runtime](https://img.shields.io/badge/Runtime-Claude%20Code%20·%20Codex%20·%20Cursor%20·%20Pi%20·%20OpenClaw-blueviolet)](#-quick-installation-guide)
[![Version](https://img.shields.io/badge/Release-v0.9.5-orange)](https://github.com/StaySound4/shopaholic-skill/releases/tag/v0.9.5)

<br>

**Shopaholic is an objective consumer decision support tool designed for shoppers using AI across Chinese e-commerce platforms (Taobao, Tmall, JD.com, Pinduoduo, Douyin).**  
**Zero affiliate bias, zero CPS commissions. Shopaholic focuses strictly on genuine material quality, engineering teardowns, and verified long-term user feedback so you understand exactly what you are paying for.**

<sub>Built on the open [Agent Skills specification](https://agentskills.io), natively compatible with Claude Code, OpenAI Codex, Cursor, Pi Agent, OpenClaw, and 50+ agent runtimes.</sub>

<br>

[⚡ Installation](#-quick-installation-guide) · [🔍 Pre-Research Mechanism](#-core-mechanism-how-domain-pre-research-works) · [📱 Live Examples](#-live-examples-real-world-dialogue) · [🧭 4 Workflows](#-decision-workflow--4-output-modes) · [📚 12 Categories](#-12-category-reference-checklists) · [⚖️ Compliance & Disclaimer](#-compliance--disclaimer)

<br>

**Other Languages / 其他语言:**  
[中文说明文档 (Chinese)](README.md)

<br>

[![Star History Chart](https://api.star-history.com/svg?repos=StaySound4/shopaholic-skill&type=Date)](https://star-history.com/#StaySound4/shopaholic-skill&Date)

</div>

---

## ⚡ Quick Installation Guide

**Shopaholic supports natural-language installation, repo-level local integration, and global multi-agent configurations.**

### Method 1: Natural Language Prompt (Recommended 🌟)

Open any AI client you are using (Claude Code, ChatGPT/Codex, Cursor, Pi Agent, OpenClaw, etc.), and simply say:

> **"Please install this skill for me: https://github.com/StaySound4/shopaholic-skill"**

---

### Method 2: Repo-Level / Project-Level Installation (Team Collaboration & VCS 📦)

If you want to maintain the skill directly inside your project repository for team sharing and version control:

```bash
# Option 1: NPX Repo Mode (automatically injects to .agents/skills/shopaholic or .claude/skills/shopaholic)
npx StaySound4/shopaholic-skill --repo

# Option 2: Clone directly into current repo
git clone https://github.com/StaySound4/shopaholic-skill.git .agents/skills/shopaholic
# Or for Claude Code repo configuration
git clone https://github.com/StaySound4/shopaholic-skill.git .claude/skills/shopaholic
```

---

### Method 3: Global Multi-Runtime Setup (Global User Profile 🌐)

<details open>
<summary><b>Click to expand / collapse CLI commands</b></summary>

```bash
# Universal NPX Cross-Platform Installer (automatically detects and syncs across all global agent directories)
npx StaySound4/shopaholic-skill

# Pi Coding Agent
pi install git:StaySound4/shopaholic-skill

# Claude Code (Global)
git clone https://github.com/StaySound4/shopaholic-skill.git ~/.claude/skills/shopaholic

# OpenAI Codex / ChatGPT Agent (Global User Profile)
git clone https://github.com/StaySound4/shopaholic-skill.git ~/.agents/skills/shopaholic

# OpenClaw / ClawHub
clawhub install shopaholic
```
</details>

---

## 🔍 Core Mechanism: How Defensive Search & Catalog Scanning Work

Unlike generic AI assistants that rely on outdated training memory and generate hallucinations about product lines, Shopaholic executes **Phase 0: Cognitive Zero-Trust & Bounded Catalog Sweeping (3+2+1 Scanning)** in the background:

```
                    ┌────────────── Target Category Root ──────────────┐
                    │                                                  │
         【Top 3 Market Incumbents】                         【Top 2 Emerging Pioneers】
     (Full catalog sweep of active models/events)       (High-spec challengers & supply-chain brands)
                    │                                                  │
                    └──────────────── 【Top 1 OEM / Geek Source】 ──────┘
                                  (Upstream solution providers & forums)
                                                 │
                                                 ▼
                                  【Global Pool (10~15 Candidates)】
                                                 │
                                                 ▼
                 ┌───────────────────────────────┴───────────────────────────────┐
                 ▼                                                               ▼
     【A-Tier: Mainstream Validated (3~5)】                          【B-Tier: Emerging Speculative (3~5)】
     (Large-sample track record & teardowns)                         (BOM whitebox + L2 teardowns + Compromise alert)
```

1. **Cognitive Zero-Trust & Defensive Retrieval**: Strictly prohibits asserting that a brand "has no such product" based on internal memory; mandates $\ge 2$ rounds of temporal retrieval (2025/2026).
2. **3+2+1 Catalog Sweeping**: Scans 3 major brands + 2 emerging brands + 1 OEM source to build a 10~15 model initial pool, delivering 6~10 representative candidates.
3. **Dual-Track Evidence Matrix & BOM Whitebox**: Parallel presentation of A-tier mature products and B-tier high-spec newcomers with mandatory compromise disclosures.
4. **Anti-Sycophancy & 4D Cost of Pivoting**: Maintains a high-status objective consultant persona upon corrections; enforces upfront accounting of workflow, safety, compute, and fragility TCO upon constraint drift.

---

## 💡 Core Positioning & Problems Solved

**Shopaholic empowers consumers with supply-chain logic, material transparency, and evidence-based decision rules.**

| Common Frustrations | How Shopaholic Solves It & Value Provided |
|---|---|
| **Unclear/conflicting needs, prone to category elimination** | **Decoupled Two-Phase State Machine**: Turn 1 extracts scenario & pain points cleanly (no meta-formatting); Turn 2 echoes profile & adapts viewpoints automatically. |
| **Model claims a product does not exist (Hallucinations)** | **Defensive Search**: Mandatory multi-angle temporal retrieval across brand catalogs to prevent outdated assertions. |
| **New high-spec flagships unfairly downgraded** | **Dual-Track Matrix**: Parallel A-tier and B-tier tables with BOM whitebox admission criteria. |
| **AI sycophantically reverses stance after user pushback** | **Anti-Sycophancy Protocol**: Neutral fact intake and independent teardown verification without excessive apologies. |
| **Unnoticed hidden costs when switching setups** | **4D Cost of Pivoting**: Enforces structured disclosure of workflow, dynamics, compute, and fragility TCO. |
---

## 📱 Live Examples (Real-World Dialogue)

### Example 1: Clarifying Incomplete Needs (Mode A: Ask Before Recommending · Coffee Machine)

```text
User       ❯ Recommend a coffee machine.

Shopaholic ❯ 【Pause Before Buying: These Key Factors Directly Change the Answer】
             
             Based on physical extraction and maintenance workflows across machine categories:
             1. Daily usage routine & maintenance willingness: Quick 1-minute morning caffeine fix, or willing to spend 10 minutes grinding, tamping, and cleaning portafilters? (Semi-automatic machines have high abandonment rates without dedicated routines; quick mornings favor super-automatic or capsule units).
             2. Preferred beverage type: Mostly black coffee (Americano, cold brew) or milk drinks (Latte, Cappuccino)? (Drip or capsule handles black coffee well; quality milk drinks require dedicated steam boilers or automatic frothing systems).
             3. Ongoing consumable cost tolerance: Are you comfortable with ¥3.5-¥5 ($0.50-$0.70) per capsule? (At 2-3 cups daily, capsules cost thousands annually, whereas whole beans in super-automatics cost ¥1-¥1.5 per cup).

             Once clarified, I will narrow down the 3-4 best-matching candidates on the market.
```

### Example 2: Budget Gaming Monitor (Mode B: Deliver Recommendation · Parameters & Compromises)

```text
User       ❯ Looking for a 2K gaming monitor around $150, mostly FPS games and daily office work.

Shopaholic ❯ 【Core Selection Criteria】
             Focus on 3 practical mechanical points rather than marketing claims:
             1. Prioritize native GtG response time: Be wary of "1ms MPRT" claims (black-frame insertion causes invisible flicker and eye fatigue);
             2. Panel packaging & DC dimming: Look for genuine Fast-IPS panels with full-range DC dimming and hardware-level low blue light (>455nm peak);
             3. Stand ergonomics & bandwidth: Budget models often cut costs on plastic chassis and fixed stands; check for height adjustment and DP 1.4.

             【Tiered Recommendation (Anonymized)】
             • Option A (FPS Response Priority · Approx. ¥999):
               - Strengths: Genuine Fast-IPS tuning, ~1.5ms real GtG with minimal overshoot, hardware low blue light.
               - Trade-offs: Mild IPS corner glow on full black screens; plastic chassis feel.
             • Option B (Color & Ergonomics Priority · Approx. ¥1,099):
               - Strengths: 99% sRGB with factory ΔE<2 calibration, fully adjustable ergonomic stand.
               - Trade-offs: Slightly slower peak response than Option A; best for mixed photo editing and casual gaming.

             • Why Bestselling Model X Was Not Prioritized:
               - Advertises 240Hz, but tests reveal severe pixel overshoot/inverse ghosting on highest overdrive, combined with non-DC dimming causing visual fatigue.

             【Inspection Checklist】Check for dead pixels on pure black/white screens, and verify G-Sync/FreeSync tear-free functionality.
```

### Example 3: Robot Vacuum Elimination (Mode D: Candidate Teardown · Structured Verdict)

```text
User       ❯ I am deciding between [Model A] and [Model B], both ~$350 robot vacuums. Help me eliminate one.

Shopaholic ❯ 【Candidate Teardown Verdict】

             | Candidate | Verdict | Engineering & Material Differences | Potential Risk |
             |---|---|---|---|
             | **Model A** | **Keep (Top Pick)** | Dual-sensor AI structured light obstacle avoidance + dual counter-rotating rubber roller; dock features 55°C hot air drying against mildew. | 9.8cm chassis height; may struggle with furniture gaps <10cm. |
             | **Model B** | **Eliminate** | Advertises higher raw suction, but uses traditional bristle-rubber brush where long hair severely tangles into bearings; cold air drying leaves damp odors in humid seasons. | Base station tray is non-removable, creating dirt buildup over time. |

             【Final Verdict】: Keep **Model A**. Practical satisfaction depends on anti-tangle efficiency and mold-free hot-air drying rather than theoretical suction numbers.
```

---

## 🧭 Decision Workflow & 4 Output Modes

**Shopaholic dynamically switches between four operational modes depending on user query clarity:**

```
                    [ Receive User Query & Context ]
                                   │
              ┌────────────────────┴────────────────────┐
              ▼                                         ▼
     【Incomplete Constraints】                【Clear Requirements】
              │                                         │
              ▼                                         ▼
     Mode A: Decoupled 2-Phase Flow            Mode B: Deliver Recommendation
     - Turn 1: 2-3 pure scenario questions     - Core engineering fundamentals
     - Explains trade-offs & factor impact     - 4-Lane cross-verification
     - Turn 2: Echoes profile & adapts view    - Tiered matrix + Pitfall checklist
              ┌─────────────────────────────────────────┼─────────────────────────────────────────┐
              ▼                                                                                   ▼
     Mode C: Category Dissuasion                                                         Mode D: Candidate Teardown
     - Market-wide inflated pricing / transition period                                  - User provides specific model list
     - Detail why purchasing now is unadvisable                                          - Keep / Replace / Eliminate table
     - Suggest bridge alternatives & timing                                              - Highlight safest vs. overrated picks
```

---

## 📚 12 Category Reference Checklists

**Shopaholic provides pre-built material and pitfall references across 12 common categories** (`references/category-checklists.md`). For unlisted categories, the agent automatically conducts real-time web research:

- 🍎 **Food, Beverages & Fresh Produce**: Freeze-drying (FD) vs. spray-drying (SD), single-cut vs. restructured meat, ingredient list cleanliness.
- 📱 **Phones, Computers & Digital Gear**: Panel quality and dimming, sustained TDP power dissipation, SSD controller & NAND binning (TLC vs. QLC).
- 🧊 **Major Home Appliances & HVAC**: Heat-pump drying vs. condensing heat, independent dual-cycle refrigeration, condenser coil materials, universal vs. proprietary water filter cartridges.
- 🧹 **Cleaning & Personal Care Electronics**: Robot vacuum obstacle avoidance, wet-dry vacuum hot-air drying vs. cold air odor, anti-tangle cutting blades, hair dryer thermal control.
- 💄 **Skincare, Cosmetics & Daily Care**: Active ingredient concentration and delivery systems, regulatory registry verification, micro-dosing detection, acid peeling tolerance warnings.
- 🍼 **Baby Care, Toys & Child Safety**: Safety certifications and car seat standards (GB 27887 / ECE R129 i-Size), food-contact materials, multi-stage car seat sizing.
- 🛏️ **Furniture, Bedding & Home Living**: Certified explosion-proof gas cylinders (TUV Class 4), mattress springs and eco-friendly comfort layers, bulky return freight logistics.
- 🏃 **Outdoor, Sportswear & Bags**: Waterproof breathable membrane tech (ePTFE), midsole supercritical foaming, wet-surface outsole grip, seam tape aging.
- 🚗 **Automotive Electronics & Gear**: Dashcam image sensors and high-temp supercapacitors, helmet safety standards, jump starter protection circuits.
- 🐱 **Pet Food, Supplies & Smart Hardware**: Fresh meat inclusion ratio in kibble, water-electricity separation in pet fountains, anti-pinch litter box sensors.
- 🎮 **Audio-Visual, Gaming & Peripherals**: Mechanical keyboard gasket structures and magnetic switches, optical mouse sensors, native projector resolution and real lumens.
- 🩺 **Health Monitoring & Home Medical Devices**: Certified Class II medical device registration, measurement accuracy standards, ongoing consumable test strip costs.

---

## ⚖️ Compliance & Disclaimer

**Shopaholic operates as an open-source analytical protocol, strictly observing statutory regulations and neutrality:**

1. **Compliance & Public Information Sourcing**:
   - Shopaholic is an open-source prompt protocol and analytical skill. **It strictly adheres to all applicable laws, regulations, and intellectual property rights**.
   - This project does not contain proprietary or secret commercial databases. **All evaluated parameters, standards, and references are sourced exclusively from publicly accessible online materials, published national/industry standards, official manufacturer manuals, and public teardown reviews**. No automated scraping violations or unauthorized data access are conducted.
2. **Execution Runtime & LLM Limitations**:
   - The actual search execution, parsing, and inference are **performed autonomously by the user's host LLM (e.g., Claude, GPT, DeepSeek) and Agent runtime harness**.
   - Due to LLM generation characteristics, search index freshness, and real-time e-commerce price changes, analyses may carry occasional discrepancies. **All outputs are provided for educational, informational, and personal consumer reference only, and do not constitute financial advice, commercial warranties, or legal guarantees**.
3. **Strict Neutrality & Non-Commercial Nature**:
   - This repository is purely non-profit and open-source. **It maintains zero affiliate relationships, charges zero CPS commissions, and receives zero sponsorships from any e-commerce platform, manufacturer, or distributor**.
4. **Regulated Categories Notice**:
   - For home medical devices, child car seats, and high-risk outdoor equipment, always prioritize guidance from licensed healthcare practitioners, certified safety manuals, and statutory inspection reports.

---

## Repository Structure

```text
shopaholic-skill/
├── package.json               # Package descriptor and agent registry metadata
├── llms.txt                   # LLM crawler entrypoint and summary
├── README.md                  # Chinese comprehensive documentation
├── README_EN.md               # English technical documentation
├── LICENSE                    # MIT Open Source License
├── bin/
│   └── cli.js                 # Cross-platform interactive installation utility
├── scripts/
│   └── ablation-suite.js      # Multi-agent ablation benchmark & automated evaluation harness
├── assets/
│   └── logo.png               # Project official logo icon
├── engineering/               # Engineering verification framework (40 atomic tickets & eval engines)
│   ├── tickets/               # Atomic engineering tickets with acceptance criteria
│   ├── scripts/               # Evidence ledger, source routing, statistics & release gate engines
│   ├── schemas/               # JSON Schemas: run-record / decision-record / manifests
│   └── evals/                 # Experiment protocol, seed cases & metric dictionary
└── skills/
    └── shopaholic/
        ├── SKILL.md           # Master workflow specification and execution protocol
        └── references/        # Deep-dive knowledge modules
            ├── category-checklists.md   # 12 category standards, teardown checks & pitfalls
            ├── evidence-and-risks.md    # Evidentiary accounting, anti-GEO & regret audits
            ├── research-protocol.md     # 4-Lane protocol & verification standards
            └── categories/               # Modular category playbooks (progressive loading)
                ├── INDEX.md              # Category router index
                ├── coffee.md             # Coffee & grinding equipment
                ├── hifi-audio.md         # HiFi audio
                ├── display-monitors.md   # Display devices
                └── infant-gear.md        # Infant & nursery gear
```

---

## Changelog

### v0.9.5 (2026-08-28)

- Added modular category playbooks (coffee / HiFi audio / display monitors / infant gear) with on-demand progressive loading and strict context isolation
- Added Claimed/Measured Deviation (CMD) asymmetric audit: independent measured deviation rates and fidelity factors, one-vote veto on severe mislabeling
- Expanded evidence ledgers: silent hardware revision tracking, price-water dehydration, used/discontinued-item verification, return friction & total cost of ownership
- Hardened safety boundaries: retrieved content treated strictly as untrusted evidence data, prompt-injection payloads neutralized; explicit degraded modes on source/tool unavailability; stale standards auto-corrected with confidence downgrades

---

## License

Distributed under the [MIT License](LICENSE).

Copyright (c) 2026 StaySound4
