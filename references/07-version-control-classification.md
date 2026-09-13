---
tier: T1  # T分级: T2=直接做 / T1=先请示 / T0=一律拒
---

# 版本控制分类（Curation 的延伸）

当需要确定哪些 skill 入仓、哪些排除时（如初始化 git 仓库或排查 .gitignore）：

1. 遍历 `ls -d /opt/data/skills/*/`，逐项检查 SKILL.md 内容
2. **分类标准：**
   - **自建** — 内容为中文，引用用户特有工具路径（amap/mmx wrapper/高德 API/B站），有独立的 `scripts/`、`references/` 或 `templates/` 目录
   - **改造内置** — 原本是英文内置 skill，但被添加了自定义脚本（如 docx 加了 5 个脚本、pdf 加了 9 个、xlsx 加了 2 个）、或 SKILL.md 被重写为中文
   - **纯内置** — 纯英文、零脚本、零附属文件，SKILL.md 内容通用
3. 自建 + 改造内置入仓，纯内置每目录一行写入 .gitignore
4. 注意符号链接 skill（如 mmx-cli -> ../home/.agents/skills/mmx-cli）：git 无法跟踪外部链接，需先 rm 链接再 cp -r 实际内容
