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
| description 太长怎么裁（>60 字符的收紧法） | `references/description-trimming.md` |
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
| **出库候选扫描（季度对账一条命令：谁很久没被调用＋事实＋cron 绑定状态）** | `scripts/skill_retire_scan.py`（`sk retire`；`cron` 列标「暂停:」＝任务停了，不是 skill 废了） |
| **md 格式体检（体积/\\n字面量/重复标题/编号跳号/断链 一键扫）** | `scripts/mdcheck.py`（bin/mdcheck）|
| 踩坑列表 | `references/09-pitfalls.md` |
| 精简历史（为什么删过/合并过，避免重复决策） | `references/pruning-history.md` |
| **对外仓库 / 单向发布（publish CLI）** | `references/11-public-repo-sync.md` |

**注意：** 本文档只是索引。具体内容在 references/ 下，按需打开对应文件。

## 并行写入防撞（Hermes 自动机制 · 2026-09-30 口径）

- **Hermes 侧会自动同步往 skill 里写条目**（与本人会话并行落笔。2026-09-30 实战：同一天两处都在写
  `job-eta-tracking`，内容都是当场实战的教训）——**不是另一个会话，当助手看待**，别当冲突处理。
- 但**落笔前仍要先看现状**：`git diff` 一眼 ＋ 读目标节，撞重复的当场合并归位（一条规则一个位置，不留两遍）。
- 改 INDEX 类共享文件时**防列头**（并行写入别把表头挤掉）。
- **curator 归档只动磁盘、不 stage（2026-10-11 实证）**：Hermes 自带 curator 按「30 天未用」自动把 skill `mv` 进 `skills/.archive/`，但**从不 stage git 删除** → `git ls-files` 留幽灵路径，每日文字存档（`scripts/backup_text.py` 按 ls-files 取文件）连日报警、更早的版本整包失败。已复发两轮（09-27 九条、10-11 十条）。查/复位：`hermes curator status` / `list-archived` / `restore <name>`；收尾一条命令 `bin/tidy index --fix` ＋ **单独提交**（自动补推脚本只推不提交，staged 删除不会自己落库）。
- **它不认 growth-gate 的五类保留**：季节性（`typhoon-monitor`）、内容型数值库（`build-analysis`）都被纯闲置时间吃掉；这类原本靠「被 cron 引用＝当 pinned」护着（curator 把 cron 引用视为 pinned），cron 一停护身符就没了。
- **2026-10-11 起已把自动归档关掉（用户拍「丙」）**：`hermes config set curator.archive_after_days 3650` —— 只留 14d stale 标记，**归档改人工**（季度对账 `bin/sk retire` 出表 → 用户裁 → `hermes curator archive <name>`）。闸的原因：61 件受管件里 43 件属五类，逐件 pin 与关阀等效；且与本节「候选清单只交用户垂裁」一致。⚠️ `config.yaml` 在 `.gitignore` 里，**换机/重装后要补这一行**。

## 技能结构规范（用户偏好）

> **自留地（2026-10-11 用户点名）：** 库内结构问题——skill 落点错/嵌进分类目录、索引脏、空壳残骸——**是 agent 的职责，发现即办，不挂账等用户驱动**。挂账只留给需要用户拍板的（删谁、花钱、对外发布）。「先说后做」也适用于此：办完报一声，不必先问。

- 技能一律**平铺顶层**，内部只分 `references/` `scripts/` `templates/`。
- **禁嵌套、禁内嵌**；目录深度 ≤ 4 层。
- 自用技能的唯一判断标准 ＝ **顺不顺手**，用不上就是噪音。
- **新建 skill 后核对落点**（2026-10-05 判例）：Hermes 侧 curator 自动写入可能带 `category` 子目录，把自建 skill 建到 `skills/devops/` 这类分类目录里——而 `.gitignore:58-75` 把 18 个分类目录整体忽略，后果是**自建 skill 不进库**（连带不进每日文字备份，备份按 `git ls-files` 取件）。落笔后 `ls` 一眼：在子目录里就 `mv` 回顶层并清空目录，再 `bin/sk refs <skill>` 复查（`sk` 只按顶层路径找，子目录里会直接 `FileNotFoundError`）。
  - 2026-10-11 实摸：`skills/research/` 下抓到两件（`web-content-harvesting`／`community-dispute-archive`，5 文件）——都已 `mv` 回顶层（5/5 守恒）并核 `backup_text.collect_files()` 实收录。另 5 件仍在**未被 ignore** 的 `career/`／`life/`／`work/` 下：它们在 git 里、备份不掉，只是违反「禁嵌套」，待下次整理时一并挪（挂账，不推）。
