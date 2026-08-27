# 01 — 仓库级与跨运行时本地安装体系 (Repo-Level & Multi-Runtime Local Installation)

**What to build:** 增强 CLI 安装器与中英文文档，支持通过命令行与脚本将 `shopaholic` 一键注入到当前项目仓库（Local Repo: `.agents/skills/shopaholic`、`skills/shopaholic` 等），提供完整的工程级版本控制方案。

**Blocked by:** None — can start immediately

**Status:** closed

- [x] 在 `bin/cli.js` 增加 `--repo` / `--local` 项目级安装模式，自动检测当前目录并注入到 `.agents/skills/shopaholic` 或 `skills/shopaholic`
- [x] 在 `README.md` 与 `README_EN.md` 置顶增补“仓库级/项目级本地安装指南”
- [x] 确保全局模式与项目级模式均可无缝执行，支持在当前仓库协同版本控制
