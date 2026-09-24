---
tier: T1  # T分级: T2=直接做 / T1=先请示 / T0=一律拒
---

# 技能结构规范 · 布局质量

> 吸收自原 skill-organization。Use when: 创建新 skill、重构老旧 skill、检查技能库布局一致性，或者需要将技能从类别目录移到顶层。

## 规范结构

```
skills/<skill-name>/
├── SKILL.md               # 主内容（必须）
├── references/            # 补充文档（可选）
│   └── *.md
├── scripts/               # 可执行脚本（可选）
│   └── *.py / *.sh
└── templates/             # 模板文件（可选）
    └── *.md / *.yaml / *.js
```

## 铁律

### ① 禁止类别嵌套

```
❌ skills/system/voice-output/SKILL.md    # 类别目录叠一层
✅ skills/voice-output/SKILL.md           # 直接在顶层
```

所有 skill 必须平铺在 `skills/` 根目录下。类别目录会导致 skill 被预载索引挤掉或遗漏。

### ② 禁止 skill 内嵌 skill

```
❌ skills/xxx/references/子任务/SKILL.md    # 引用目录里不能有 SKILL.md
✅ skills/xxx/references/子任务/笔记.md     # 引用目录只放引用文档
```

Skill 的子目录（references/ scripts/ templates/）只能存放内容文件和脚本，不能包含另一个完整的 skill 结构（不能有 SKILL.md）。

### ③ 子目录层级深度 ≤ 3

层级 4（内容文件深度）是极限值，超过需重构。

## 结构迁移

### 从类别目录移到顶层

```bash
cd /opt/data/skills
mv category/skill-name ./skill-name     # 移动目录
rm -rf category/                         # 清理空类别
```

纯文件系统操作。Hermes 自动扫描索引。

### 从扁平 SKILL.md 拆出标准结构

SKILL.md 太长时拆出 references/：
1. 详细记录（测试过程、踩坑复盘、API 参数）移入 references/
2. SKILL.md 保留：Setup + 基本用法 + 推荐策略 + Pitfalls
3. SKILL.md 末尾加指针：`skill_view("skill-name", "references/xxx.md")`

## 资产归位：模板 vs 参考件

「模板」这词在库里管着四种东西，不判性质就是各放各的——2026-09-18 全库体检：
10 个 skill 有 `templates/`，另有 7 份「模板」躺在 `references/` 里。

### 判据三问

| 问 | 放哪 |
|:---|:-----|
| 是「复制 → 填空 → 成为产物」的骨架吗？（有复制指令、大片占位符） | `templates/` |
| 是「描述规则 / 格式 / 约定」的说明吗？ | `references/` |
| 是「某一类数据的条目骨架」吗？ | **跟数据放一起**（数据目录内的 `_template.md`），**不进 `templates/`** |

第三类最容易被误判成混用：`memes/技术梗/_template.md` 就挨着那类梗文件，新增条目时随手复制——
**就地是对的**，别挪。同理 `purchases/_template.md`、`references/games/_template.md`。

### 命名

- 是模板 → 文件名带 `-template` / `-模板`，一眼能认
- **不是模板别叫 template**——`references/template.md` 点进去是命名与结构约定（一个占位符都没有），该改名，不是该搬家

### 已发布仓库是硬约束

挂在公开仓库当配套文件的（`skill-publishing` 的 extra 机制），改名/移动必须连同仓库侧一起改——
先 `bin/skillrepo <name> status` 看清两侧，别单方面动。

## 维护检查清单

| 检查项 | 标准 |
|:-------|:-----|
| 所有 skill 在顶层？ | `ls -1d skills/*/` 无类别目录 |
| 无子目录含 SKILL.md？ | `find skills -mindepth 3 -name SKILL.md` 空 |
| 有无模板放错位置？ | `find skills -path "*/references/*" \( -name "*template*" -o -name "*模板*" \) -not -path "*/templates/*"` → 逐个点开看内容判性质（名字骗人的只改名、真骨架才搬） |
| 层级深度 ≤ 4？ | `find skills -type f -printf '%d\n' \| sort -rn \| head -1` ≤ 4 |

## 使用纪律：先报告再动手 ⚠️

检查/审计/重构技能库时，**发现的问题先登记，不要自行执行修改。**

| 应该做 | 不应该做 |
|:-------|:---------|
| 列出问题清单 + 建议方案 → 向用户报告 | 觉得「这很明显」就直接 rm/mv/absorb |
| 等用户确认后再执行迁移 | 顺手「顺便修了」 |
| 拿不准的先标记，不擅自决定 | 替用户做取舍 |

这个纪律适用于任何涉及技能库结构的操作——移动、删除、合并、改名，一律先问。
