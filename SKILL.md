---
name: skill-curation
tier: T1  # T分级: T2=直接做 / T1=先请示 / T0=一律拒
description: >-
  技能库精简与维护。减法哲学在技能库维度的具体落地——
  冗余检测、跨工作区合并、脚本化精简。
---

# Skill Curation · 技能库精简

## 这是什么

技能库精简与维护的方法论。减法哲学在技能库维度的具体落地。

## 怎么用

| 你要做什么 | 打开 |
|:-----------|:-----|
| 理解核心原则（含 SKILL.md 总入口化） | `references/01-core-principles.md` |
| 执行一次完整的精简流程 | `references/02-curation-workflow.md` |
| 合并另一个天使的工作区 | `references/03-cross-workspace-absorption.md` |
| 审查技能的实际用途 | `references/04-usage-review.md` |
| 把厚 SKILL.md 拆薄（功能拆分+实操流程+GROUP 优先级） | `references/skill-thinning-workflow.md` |
| **拆薄工具（spec 驱动、守恒校验，规矩留案例搬；三种定位：整节／单条／行段）** | `scripts/skill_thin.py` |
| 增量反馈沉淀到技能 | `references/06-runtime-enrichment.md` |
| 确定哪些技能入仓/排除 | `references/07-version-control-classification.md` |
| 快速识别什么情况该做什么 | `references/08-signal-recognition.md` |
| 技能结构规范（平铺/嵌套禁止/先报告再动手） | `references/skill-organization.md` |
| **T 分级标注（给 skill md 标 T0/T1/T2）** | `references/10-tier-annotation.md` |
| **技能库统一入口（`bin/sk`）** | `bin/sk --help` |
| ↳ `sk stats` 全库一览（行/字符/字节/refs/scripts/description 长度 + 汇总，排序看**字符数**不看行数） | `bin/sk stats --sort desc` |
| ↳ `sk skeleton <skill>` 章节骨架（每节行/字符，标出可搬的展开型节） | 拆薄前先跑这个再写 spec |
| ↳ `sk verify <skill>...` 拆薄/合并**收尾验收**（守恒复核 ＋ mdcheck 对基线；全过才提交） | 退出码 0=不欠账 |
| ↳ `sk refs <skill>` 双向引用分布（谁引用它／它引用了谁） | 合并改名之前必查 |
| **清点技能库（空壳/厚薄/无脚本/T分级 一次跑）** | `scripts/skill_audit.py`（`sk audit`） |
| **进出门规则（新建三问 / 季度对账四条判据 / 合并必同步七件套）** | `references/growth-gate.md` |
| **出库候选扫描（季度对账一条命令：谁很久没被调用＋事实）** | `scripts/skill_retire_scan.py`（`sk retire`） |
| **md 格式体检（体积/\\n字面量/重复标题/编号跳号/断链 一键扫）** | `scripts/mdcheck.py`（bin/mdcheck）|
| 踩坑列表 | `references/09-pitfalls.md` |
| 精简历史（为什么删过/合并过，避免重复决策） | `references/pruning-history.md` |
| **对外仓库 / 双向同步（curation CLI）** | `references/11-public-repo-sync.md` |

**注意：** 本文档只是索引。具体内容在 references/ 下，按需打开对应文件。

## 并行会话防撞

- **多 hermes 会话并行时**：建 skill / 改共享文件前先查重（同日撞过车，造出过功能重复的 skill）；改 INDEX 类共享文件时**防列头**（并行写入别把表头挤掉）。

## 技能结构规范（用户偏好）

- 技能一律**平铺顶层**，内部只分 `references/` `scripts/` `templates/`。
- **禁嵌套、禁内嵌**；目录深度 ≤ 4 层。
- 自用技能的唯一判断标准 ＝ **顺不顺手**，用不上就是噪音。
