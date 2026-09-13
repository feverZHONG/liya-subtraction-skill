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

## 维护检查清单

| 检查项 | 标准 |
|:-------|:-----|
| 所有 skill 在顶层？ | `ls -1d skills/*/` 无类别目录 |
| 无子目录含 SKILL.md？ | `find skills -mindepth 3 -name SKILL.md` 空 |
| 层级深度 ≤ 4？ | `find skills -type f -printf '%d\n' \| sort -rn \| head -1` ≤ 4 |

## 使用纪律：先报告再动手 ⚠️

检查/审计/重构技能库时，**发现的问题先登记，不要自行执行修改。**

| 应该做 | 不应该做 |
|:-------|:---------|
| 列出问题清单 + 建议方案 → 向用户报告 | 觉得「这很明显」就直接 rm/mv/absorb |
| 等用户确认后再执行迁移 | 顺手「顺便修了」 |
| 拿不准的先标记，不擅自决定 | 替用户做取舍 |

这个纪律适用于任何涉及技能库结构的操作——移动、删除、合并、改名，一律先问。
