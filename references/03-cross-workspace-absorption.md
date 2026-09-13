---
tier: T1  # T分级: T2=直接做 / T1=先请示 / T0=一律拒
---

# 跨工作区吸收

当用户丢来另一个天使的工作区压缩包时：

1. **解压到独立目录** — 不直接覆盖当前 skills/
2. **读 SOUL.md/README.md** — 理解对方身份和技能体系
3. **对比技能清单** — 哪些是已有的、哪些是新的、哪些是空壳
4. **合并有用的** — 工具脚本复制到 `workspace/scripts/`，有 SKILL.md 的技能复制，空壳目录跳过
5. **去重** — 同名技能读全文判断是否真重复。相同功能的吸收合并
6. **瘦身** — 新导入的技能按减法公式缩到 70 行以内。原技能保留为 `references/` 存档

**本 session 实例：** 从 XueLing 工作区吸收了 12 个技能，合并 3 个（web-search→global-search、skill-library-maintenance→skill-curation、character-profile-writing→chara-profile），删 6 个空壳，最终净增 3 个活跃技能。
