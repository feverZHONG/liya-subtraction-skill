---
tier: T1  # T分级: T2=直接做 / T1=先请示 / T0=一律拒
---

# 踩坑记录

1. **absorbed_into 不搬文件** — `skill_manage(action='delete', absorbed_into='X')` 只记录元数据关系，不移动脚本。手动拷贝。
2. **同名技能不一定真重复** — 不同天使可能有同名但内容不同的 skill，读全文判断，不能简单覆盖。
3. **空壳目录没有 SKILL.md** — `diagramming`、`domain`、`feeds` 等只是分类占位，`skill_manage(action='delete')` 找不到它们，必须 `rm -rf` 从文件系统删。
4. **超过 70 行的方法论文档例外** — `tech-workflow`(465行)、`skill-curation` 这类是思路性内容，没法脚本化，合理保留。
5. **凭描述做决策撞过车** — `web-search` 和 `global-search` 描述都写「搜索」，读完全文才发现完全一样。必须读全文。
6. **confirmed-unused 不等于 skill_manage-deletable** — 确认无用的 skill（有 SKILL.md）可通过 `skill_manage(action='delete')` 正常删除。但只有 DESCRIPTION.md 无 SKILL.md 的空壳必须 `rm -rf`。
7. **删技能前先列出清单给用户确认** — 批量删除前先列举分组，让用户一次性过目。拿不准的先移 temp/。
8. **一轮清理不够** — 大合并+移temp 之后重新审视列表再做一轮。第二轮会发现薄技能吸收的机会。
9. **temp/ 要加 gitignore** — 从 gitignored 的目录移技能到 temp/ 时，如果 temp/ 本身不在 gitignore 中，这些文件反而从「被忽略」变成了「可追踪」。
10. **类别目录会把 skill 挤出预载索引** — `system/voice-output/` 这种类别嵌套会让 skill 在系统提示的预载索引中不可见。所有 skill 必须平铺在 `skills/` 根目录，不要套类别文件夹。
11. **一个 skill 里不能叠另一个 skill** — `skill/references/` `skill/scripts/` 只能放内容文件和脚本，不能放另一个完整的 skill 结构（即不能有 SKILL.md）。违反这条会导致：
    - 子 skill 被隐藏在父 skill 目录下，永远进不了预载索引
    - `skills_list` 可能扫不到（取决于深度）
    - 维护时容易误删或漏迁
    - 正确做法：每个 skill 独立一个目录，references/ 下只放 .md 文档
12. **游离脚本归位前先查 cron 软链依赖（2026-08-05）** — SKILL.md 里写 `python3 workspace/scripts/xxx.py` 而 skill 下无 `scripts/` = 脚本没归位。但 `workspace/scripts/` 的脚本可能是 cron 硬依赖：`/opt/data/scripts/` 下常有软链指向它（如 `bili_hot_push.py`、`patch_qqbot_send_target.py`），cron wrapper（no_agent script 字段）经软链调用。归位动作：`git mv` 保留历史 → 同步改 SKILL.md 引用 → **检查 `/opt/data/scripts/` 软链并重新指向新位置** → 语法验证 `python3 -m py_compile` → 全库 grep 残留引用。判别：被 cron wrapper/`sys.path.insert` 硬编码依赖的脚本（如 `qq_group_roster.py` 被 `qq_group_sync_cron.py` import）留原地，skill 引用保持绝对路径。
13. **死引用标注「不可直接运行」而不是改指别处（2026-08-05）** — location references 引用了已删除的 `weather_cn.py`（fetch/parse_alarms/CITY_ID 接口已不存在），先试着改指 `weather_report.py` 但该脚本没有这些函数——改错。正确做法：确认原接口彻底消失后，在文件顶部标注「历史参考，不可直接运行」+ 给出当前可用命令，代码块保留原文。改引用前必须验证目标脚本确实提供被调用的接口。
