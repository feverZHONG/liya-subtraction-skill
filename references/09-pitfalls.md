---
tier: T1  # T分级: T2=直接做 / T1=先请示 / T0=一律拒
---

# 踩坑记录

0. **`bin/mdcheck` 的「引用不存在」会误报说明文字里的裸文件名** — 它把反引号里的裸文件名当链接解析，所以**说明文字里列举的文件名**（SKILL.md 表格中「`relationship-web.md`：检查新角色…」、篇目录示例「`article.md` ＋ `逻辑链.md`」）一律被报断链。实测糖霜 skill 报 16 处、真断链只有 2 处（跨 skill 引用没写清是哪个 skill 的）。**判读先看路径**：带 `references/` 或跨 skill 前缀的才是真链，裸文件名＋说明文字＝合理误报，别去改文件。

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
14. **双向同步的完成判据看文件标记，不看 index 状态（2026-09-13）** — 冲突是否解决要检查文件里还有没有 `<<<<<<<`，不能用 `git diff --diff-filter=U`：未合并记录在 `git add` 之前一直在，标记被人手改干净了也照样报「没改完」。同类：`git status --porcelain` 报的是 index 状态，不是内容对错。
15. **并行会话会造出重复 skill（2026-09-18）** — 多个 hermes 会话同时在同一个案子上干活时，两边各自建了功能相同的 skill（`draft-salvage` vs `draft-archaeology`，相隔一分钟）。判别与处理：① 建 skill / 改共享文件**前先查一遍库**；② 撞车时不按新旧、**按完整度留**（本次留下的那份 references 更全、且已引用本案档案）；③ 把另一份里的**独有部分并过去**（收编了工具 `score.py` + 一份确认清单）再删重复；④ 合并后**统一两份之间不一致的参数**（脚本判据阈值与 references 不同 → 以更严的那份为准），并实测跑一遍拿数字。
16. **skill_manage patch 被「frontmatter YAML」拦下时，先修 description 里的裸冒号（2026-09-21）** — 报错写「Patch would break SKILL.md structure: YAML frontmatter parse error: mapping values are not allowed here」，看着像本次改动的问题，实际是**文件里早就存在的**：`description` 里出现 `: `（典型是 `skill: novel-writing` 这类引用写法）＝YAML 裸标量带冒号，本身非法；校验只在 patch 时跑，所以一直没拦到。判别：报错行号指着**前几行的 frontmatter**、不是刚改的段落。做法：**同一批 operations 里顺手把 description 用双引号包起来**（`description: "…"`）即可过，别去改 body。另：patch 会抹掉文件开头的 BOM，无害。
16. **改路径引用别只 grep 字符串形态（2026-09-22 平铺实战）** — 把 `knowledge/`、`writing/` 里的 8 个 skill 提平到顶层时，`grep "skills/writing/x/"` 抓到 26 处并全改了，但漏了**拼接式**的引用 `ROOT / "skills" / "writing" / "x"`（`short-stories-liya/scripts/story.py:369`）——它是几个独立字符串，正则和字符串替换都碰不到，直到 pre-commit 门禁跑挂才暴露。
    规矩：**改完路径要把那几个脚本真的跑一遍**（或对每个路径段单独 grep 一次），别只信「引用全改完了」；门禁拦下来是运气好，拦不下来的会变成下次才炸的坑。
17. **同主题两个 skill 用机器查不出来（2026-09-25）** — 两种机械手段都失效：① 跨 skill 逐字长行比对（同站点两个 skill 的「共同长行」可能是 0 条）② 8-gram Jaccard 全库相似度（只有共享模板的档案库群能到 0.10+，其余同主题对全在 0.02 以下）。这类重复只能**按名点读全文**：同一站点／同一动作／同一产出的名字摆在一起人工判——实例 `wufan-extractor`×`wufan-forum`（同站点）、`legacy-draft-mining`×`draft-archaeology`×`corpus-line-mining/references/legacy-draft-cards.md`（三处同一动作）。
    判「哪些内容是独有的」也**别用整行匹配**——同义改写的两份会假报大片「未覆盖」（本次 legacy 67 行里假报 60 行），要按**判据指纹**查（把专有概念词逐个 `in` 全文：情绪核／去容器／身份一致性…）。
    合并四步：**宿主选被活引用最多的那个**（本次选 `wufan-forum`，它有跨 skill 活引用且在发布候选表里）→ **scripts 先接管再删**（被正文引用着的工具脚本不迁就断链）→ **CLI/wrapper 改指后实测跑一次**（拿回真数据才算过）→ 收尾拿基线目录前后对比 mdcheck（搬进的新文本常欠新账，如泛指 `INDEX.md` 带反引号被当路径）。
18. **移档了但没提交删除 → 每日文字存档整包失败（2026-09-27 实炸）** — 09-26 三批精简把 `bili-manga-download`／`chinese-convention-search`／`storytelling-review` 移进 `.archive/`，磁盘上没了、**git 索引里还在**（`git status` 显示 ` D` 未 stage）。后果不是「少备份几个文件」：`scripts/backup_text.py` 按 `git ls-files` 取文件，`tar.add` 碰到不存在路径直接抛 `Errno 2` → **当天 15k 文件的文字包一个都没打成**（cron 报 error 才发现）。自查命令与修法见 `references/02-curation-workflow.md` Step 7。**连带教训：断头软链同样触发**——skill 目录重组后 `bin/xxx -> skills/旧路径` 变成死链，`os.path.exists` 也是 False（本次同批查出 `bin/draft-score`、`bin/mmx-quota` 两条）。所以「移档收尾」的判据是 **`git ls-files` 与磁盘逐条对得上**，不是「磁盘上没有残留」。
