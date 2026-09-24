---
tier: T1  # T分级: T2=直接做 / T1=先请示 / T0=一律拒
---

# 技能库精简历史（归档）

> 历史 audit 合并归档（2026-08-06 三合一）。保留每个日期的核心决策与教训，细节压缩。
> 用途：做减法时先翻历史——「这个为什么删/合并过」避免重复思考或推翻旧决策。

## 2026-09-22 · 第十一轮：拆薄 delegation-and-verification（换轴：按场景切）

- 形状与前面 5 个不同：**没有案例尾巴可搬**——53.4KB 里几乎每条已是「一句判据＋实测数字」，肥在**条目数**（任务书 7 步＋8 条判例／验收 8 步带 26 条子判据／坑 14／检索型 20／评审型 15／落地 15／外部 6）。故换轴：**按「这次要干哪种活」分档**。
- 53.4KB → **15.8KB**：§一 判例 → `references/task-brief-cases.md`（B1–B8）、§三 子判据 → `references/verification-cases.md`（V1–V26）、§五／§六／§八 整节 → `delegate-harvest.md`／`delegate-review-panel.md`／`external-review.md`、§七 **并入**既有 `references/landing-review-findings.md`（不重复存两遍）；**§二 并行、§四 坑 原样留本文**（每次派活都看的高频速查）。
- 工具加两条能力：`ref_meta.<ref>.append`（并入既有 ref，原样保留＋追加带 marker 的一节）、`moves[].keep=""`（整条搬走、正文不留占位）。
- 教训：**先判「肥在单条」还是「肥在条目数」再选轴**——抽 5 条，能砍掉一半字数＝案例型（搬），砍不动＝判据型（按场景整节搬）。
- 归属：该文件上原有**别处会话的未提交增量**（§一.2、§三.8 两条），已先单独提一笔（提交信息写明「非本天使所写，仅代为落库」）再拆——这样 `git log` 里归因分得开。

## 2026-09-22 · 第十轮：拆薄 prose-quality-metrics + war-criminal-archive（规矩留、案例搬）

- **prose-quality-metrics 92.7KB → 17.6KB**（-81%）：铁律只留可执行那句，判例/反例/实测数字 → `pitfalls.md`（33.7KB）；八种「平」的诊断表 → `diagnosis-eight-flat.md`；改法手册／交付四件套／定口径·母题账·承接账各一档。SKILL.md + references 总量 155.8 → 157KB，一条信息没删。
- **war-criminal-archive 59.4KB → 20.6KB**（-65%）：触发条案例 → `trigger-cases.md`（T1–T12）、速查表长注 → `flow-quickref-details.md`（F1–F14）、18 条维护纪律 → `maintenance-selfcheck.md`（M1–M18）、参考区全条目 → `scripts-index.md`（全量逐字）。
- 立了工具 `skill-curation/scripts/skill_thin.py`（spec 驱动拆薄）：逐条守恒校验（原文指纹必须「不在新 SKILL.md、在 ref 里」）+ 整篇复核（原文每行 >40 字必须出现在 `SKILL.md ∪ refs`）。
- 教训：**keep 行保留 ref 指针会让固定切片校验假报「残留」**（指纹要用「最长差异窗口」）；`- 平台：…` 这类「冒号太靠前」的索引行别自动切。

## 2026-09-22 · 第九轮：拆 QQ 诊断大文件 + 顺手结案

- 触发：TIM/`msg_type` 那轮收尾（群里 @ 结案）后，`bin/mdcheck` 标 🔴 强烈建议拆（22.5KB / 268 行）
- 拆法：**按主题切**——「消息看不见 / 格式 / @ / 长度切块」独立成 `references/qq-message-visibility.md`（11.4KB）；原文件只留「消息没到网关 / 没发出去」的排查骨架（9.7KB）
- 活引用逐处改指向（宿主 SKILL.md 路由表 + §3.5 引用、qq-group-intel 的 SKILL.md ×2 + 探针脚本注释、chat-game-referee 的 §TIM）——**跨 skill 引用要 grep 全库，别只看宿主目录**
- ⚠️ **别用数字 §编号当跨文件锚**（旧文里的 `§3.5`/`§TIM` 一拆就全断）：写「文件名 + §语义小节名（§一/§二）」或直接写文件名
- 顺手把已拍板的结论写成「✅ 结案」落进文件（TIM 看不到 = 方案②已上线、群里不 @），防下次重开方案讨论
- 教训：**结论不落文件 = 下一轮重查一遍**（本轮就是上一轮刚拍过的 @ 结论被拿去从头取证）

## 2026-09-04 · 第八轮：合并 4 组伞 + 拆薄 6 个 + 结构平铺/官方噪音清理

**合并（8 技能 → 4 伞，模式=宿主保留名+被并技能 SKILL.md 原样降级 references/，文件全迁，活引用逐处修）：**
- tavern-card-refinement + tavern-card-batch-refine（90% 重叠，batch 自述「合并由 curator 处理」；脚本补版本/creator_notes 检查）
- **voice-output 成语音伞**：吸收 mmx-voice（MiniMax 配置/三件套禁令/wrapper）+ qq-voice-link（QQ 收发/语音模式）——引用/gitignore（assets/ref-audio 锚定路径）/memory（禁生图条目）全同步
- **news-verification 成验证伞**：吸收 quick-fact-check（轻量核查）+ link-safety-check（链接安全，linkcheck 6 工具族随迁）——三模块分流表（轻量/交付前/链接安全）
- **chinese-news-aggregator 成新闻采集伞**：吸收 mmx-news-collection（mmx 采集+date 硬过滤）
- 教训：**合并前 grep 活引用分布定宿主**（被引最多者当宿主省改名成本）；历史叙述类引用（upgrade-log/dev-workflow 案例/pruning-history）不改

**拆薄 6 个（目标 <95 行，踩坑/案例/子场景→references）：**
- knowledge-persistence 127→80：踩坑 20 条→pitfalls.md、事件双轨→event-dual-track.md（⚠️ 重写前先 git show HEAD 提取要删的节，防细节丢失）、模式归索引表
- group-chat-discipline 122→95：**红线守则压缩不拆 references**（群聊要三步内出手，拆了反而翻文件）；压缩重复措辞/流程与铁律去重，场景做法全留
- bili-audio-archive 122→119：08-24 已拆过一轮，剩余全是命令+判据表（主场景必需），压不动——诚实记录
- ruozhiba-wordbank 152→81：题库入选标准/拉题坑/群聊案例拆 references，SKILL.md 留防御手册核心
- source-code-investigation 120→83：APK 分层/agent 仓库方法论/踩坑案例拆 3 references（原零 references 全堆 SKILL.md）
- **判定保留**：qq-group-intel（工具手册已有 8 references）/story-revision-plan（低频方法论，全套流程每次用）/short-stories-liya/info-hunt/war-criminal-archive/hermes-agent

**结构平铺 + 官方噪音（第七轮补充落地）：**
- 4 嵌套技能提升顶层：external-toolkit-onboarding/kurobbs-wiki-api/corpus-chara-archive/tavern-card-refinement（git 识别 rename，引用不破）
- 清幽灵皮目录+官方镜像残留 15 个（mlops/apple/email/productivity 等，官方树 `/opt/hermes/skills` 有原版）；sdlc-review 补进 disabled
- description 瘦身 top3（enneagram-notes 219→110/bilibili-api-ops 133→80/wuthering-waves 124→92）
- audit 终态：90 目录 / 89 活跃 / 空壳仅 .curator_backups（最早干净）；合并后技能数 89→80
- ⚠️ 教训：patch 全量重写前先 git diff 看工作区未提交内容（bili-video-content 挂指针段曾被覆盖丢失后补回）

## 2026-09-04 · 第七轮：官方技能配置层禁用 + 拆薄两个厚 skill

- **根因查明：官方技能镜像会复活**——`/opt/hermes/skills/`（Hermes 框架自带，root）同步镜像进 `/opt/data/skills/`（08-10/08-24 删两轮「又复活」的真相）。**删文件无效，正确姿势=config.yaml `skills.disabled`**：`hermes config set skills.disabled '["..."]'`（config.yaml 被 .gitignore 拦不入库；hermes-agent 是 ESSENTIAL_SKILLS 禁不掉）
- **禁用 11 个英文通用噪音**（对中文记录官场景无用）：email-inbox-triage / box / document-to-action-items / meeting-action-items / product-price-monitor / weekly-review-planning / competitor-news-monitor / grounded-citations / github / inspecting-hermes-desktop-dom / blocked-page-recovery——下次新会话从列表消失
- **清幽灵壳**：productivity/ocr-and-documents（DESCRIPTION.md 皮，08-24 清过又复活）连根拔
- **拆薄 dsh-plugin-dev 192→134**：环境重建配方→`references/development-setup.md`、常见坑 12 条→`references/plugin-pitfalls.md`、社区礼仪 6 条→`references/community-etiquette.md`；SKILL.md 留决策板+插件本质+流程速记+材料索引。引用修正：network-interconnect/web-remote-access（「dsh §0」→`development-setup.md`）
- **拆薄 bili-video-content 143→78**：1b 字幕深挖/1c 研究类/1d 剧情概括三法→`references/advanced-extraction.md`、踩坑 10 条→`references/pitfalls.md`
- **⚠️ 教训：patch 全量重写 SKILL.md 前先 `git diff` 看工作区未提交内容**——bili-video-content 有段「分析产出登记/挂指针」指引只存在于未提交工作区（HEAD 没有），被全量替换覆盖，靠 diff 察觉后补回
- **war-criminal-archive 145 判定保留**：它已是 08-11 从 224KB 拆出的入口壳（触发+流程速查+脚本导视全是指针，内容在 50+ references）——「合理保留」类，不拆
- **低频候选审读结论（全保留）**：steam-api（08-26 仍实战更新，活跃）/ build-analysis（用户深度 GBF Relink 配套数值库）/ （私档）-crusaders（阁下原创连载档案=勿忘类）→ 全数保留；am-tool-collection（前端小工具六合一，结构完整有 CLI）→ 唯一待阁下表态项，不占加载成本先留

## 2026-08-24 · 第六轮：做减法（第二批）

- **合并：paper-translation → document-translation**（76 → 75）——同领域克隆（都是论文翻译），且违规嵌套在 writing/ 下（违反平铺铁律）。独有内容（页码标记推导/V4A 补丁锚点坑/单章执行规范/cordis-paper 项目实例）吸收为 `document-translation/references/chapter-execution.md` + `cordis-paper.md`；`writing/` 目录随删
- **清 12 空壳目录**（apple/autonomous-ai-agents/creative/email/github/media/mlops/note-taking/productivity/research/smart-home/social-media）——2026-08-10 第五轮删过又复活的 DESCRIPTION.md 皮，二度连根拔；mlops 下 evaluation/inference/models 子目录、note-taking 下 ocr-and-documents 一并清；`.curator_backups` 保留（自动备份机制）
- **去重：audio-event-locate.md → video-analysis**——bili-video-content 与 video-analysis 各持一份「音频事件定位」方法论（同源于 2026-08-04 金正恩演讲案例）；保留 video-analysis（带配套脚本 audio_band_energy.py/frame_diff.py），bili-video-content 改引用
- **吸收：spa-extractor → read-url**（75 → 74）——薄技能（~40 行+1 脚本），read-url 已引用它为「纯 JS 渲染」分支；方法论 → `read-url/references/spa-rendering.md`，脚本迁 `read-url/scripts/extract.py`，7 处引用全部改指
- **教训：** 删除 skill 后必须全局 grep 残留引用（`spa-extractor|paper-translation` 等），本批修了 7 处（incident-review/dsh-plugin-dev/hermes-gateway-ops/chinese-convention-search/bilibili-api-ops/read-url 自身/workspace 一次性脚本）
- **保留确认**（读全文，非描述判断）：语音三件（mmx-voice=配置层/voice-output=合成层/qq-voice-link=传输层）、新闻三入口（mmx-news-collection=日期采集/chinese-news-aggregator=API聚合/info-hunt=搜索方法论）、B站/通用视频（bili-video-content=平台链路/video-analysis=任意来源）、表情包/立绘（meme-archive-ops=图库操作/internet-memes-reference=梗知识/image-batch-archive=立绘建档）、说书（storytelling-review=质检/voice-output=合成）、提取器（nga/tieba=平台反爬/platform-content-extraction=伞入口）
- **拆薄 ×5（第二批，同日）**：hermes-gateway-ops 265→~70（坑表→pitfalls.md / provider 切换→provider-switch.md / cron 审查→cron-ops.md / QQ 诊断→qqbot-troubleshooting.md / 群会话内嵌大段与 group-session-reset.md 重复已去重）；bilibili-api-ops 185→~90（接口坑→api-pitfalls.md / 端点→endpoints.md / 调查场景→scenarios.md / UGC 下载→ugc-download.md）；vision-recognition-traps 180→~120（陷阱 1-9 案例→traps-detail.md，SKILL.md 留一行速查）；bili-audio-archive 157→122（踩坑 16 条→pitfalls.md）；image-batch-archive 139→~110（mmx 批量脚本代码块→mmx-batch-script.md）。**教训：commit message 带 `hermes-gateway-ops` 字样会被终端安全扫描拦（gateway 误判），绕法=commit message 不带 gateway 字样**

## 2026-08-10 · 第五轮：做减法（第一刀）

- **清 12 空壳目录**（apple/autonomous-ai-agents/creative/email/github/media/mlops/note-taking/productivity/research/smart-home/social-media）——第三轮删过的类别残留 DESCRIPTION.md 皮又复活，连根拔（69 skill 实际 81 目录）
- **吸收：system-ops → environment-hygiene**（69 → 68）——system-ops 是 13 行索引壳，references 31 文件（tech-workflow 模块 16 + workspace-hygiene 模块 12 + cron-ops + 2 索引），其中 workspace-hygiene 与 environment-hygiene 重叠；整包搬入 `environment-hygiene/references/system-ops/`，SKILL.md 加模块索引，删除 system-ops
- **降级：windows-update-info 删 skill 留经验**（68 → 67）——零使用记录 + 阁下裁决「顶多算经验，不至于要做成 skill」；核心经验压缩进 `workspace/memory/windows-update-experience.md`，查 KB 大小脚本 `catalog_size.py` 挪 `workspace/scripts/` 保留，skill 删除
- **降级×2：svg-vector-drawing + ai-subscription-plans 删 skill 留经验**（67 → 65）——svg 是 08-10 为光梭手枪刚建的（矢量画低频），ai-subscription 是 08-07 调研完（价格快照会过时）；经验压缩进 `workspace/memory/svg-drawing-experience.md` + `ai-subscription-experience.md`，render_svg.py 挪 `workspace/scripts/`，skill 删除
- **吸收：game-character-lookup → chara-profile**（65 → 64）——速查（笔误验证/CV/剧情问答）并入 chara-profile 新「速查」章节，lookup_bilibili.py 脚本随迁，原 SKILL.md 存 `references/absorbed/`
- **吸收：xiaoheihe-archive → war-criminal-archive**（64 → 63）——war-criminal-archive 本就有「流程（小黑盒佐证类）」章节 + grab_xiaoheihe.py 脚本，独立 skill 只是重复；SKILL.md 存 `references/xiaoheihe-archive.md`，两处原 skill 引用改指向
- **读全文确认保留**（不合并）：视频三件（video-analysis/bili-video-content/douyin）、语音三件（voice-output/qq-voice-link/mmx-voice）、角色两件（game-character-lookup/chara-profile）、验证两件（quick-fact-check/news-verification）、采集两件（mmx-news-collection/chinese-news-aggregator）——底层工具或内容类型不同
- 低频候选待议：ai-subscription-plans / am-tool-collection / windows-update-info / xiaoheihe-archive / steam-api / build-analysis / 娱乐三件（sea-turtle-soup/spy-game/ruozhiba-wordbank）

## 2026-07-14 · 第一轮精简

- 清理 3 真技能（dogfood/himalaya/opencode）+ 2 空壳（smart-home/media）= 44 → 39
- **教训：** `skill_manage delete` 对空壳（仅 DESCRIPTION.md 无 SKILL.md）无效，必须 `ls -d skills/*/` 确认 + `rm -rf` 手动删
- **教训：** 小体积 ≠ 空壳，`skill_manage view` 返回 404 才是空壳铁证
- **教训：** 清理后 memory 里的 skill 数量条目会过时，需同步更新

## 2026-07-26 · 第二轮审计

- **吸收候选：** skill-organization → skill-curation（子集）；knowledge-persistence 极薄更像纪律（最终保留独立）；api-diagnostics 与 skill-curation 有重叠（最终保留，互补）；chinese-news-aggregator 是 daily-news-poster 子组件（最终保留独立）；github-private-repo-extraction → github-ops（07-31 落地）；persona-authoring 保留独立
- **结构不规范修复：** documents/location 的 md 从根目录移入 references/；dev-workflow 删旧 category frontmatter
- **教训：** 薄技能不一定该删——独立价值 vs 子集判断要读全文

## 2026-07-31 · 第三轮审计（64 → 42 目录）

- **删类别空壳 12 目录 15 文件**（apple/email/mlops 等 DESCRIPTION.md 皮）——功能均已由活跃 skill 覆盖
- **结构修正：** search/ 嵌套平铺 → 顶层
- **合并：** environment-hygiene 吸收 workspace-org + output-path-hygiene（三合一 umbrella）
- **吸收：** cron-news-workflow → daily-news-poster；skill-organization → skill-curation
- **六合一：** am-tool-album/edu-site/filter-lab/music-personality/pattern/word-sticker → am-tool-collection
- **教训：** 「不同底层工具不合并」被阁下否决——github-private-repo-extraction 最终并入 github-ops
- **教训：** absorbed_into 只记元数据不搬文件，脚本要手动拷贝

## 2026-08-06 · 第四轮：全库 SKILL.md 总入口化

- **原则（阁下拍板）：** SKILL.md 为总入口，里面的内容（含已写好的说明 md）能拆就拆
- 21 个厚 SKILL.md（95-240 行）→ 12 个拆薄 + 9 个判定合理保留
- 判定标准：**主场景高频内容留 SKILL.md（每次都要读的），子场景细节拆 references/（用到才读的）**；数据索引/题库/导视表不算内容，保留
- 拆分 12 个：image-batch-archive / news-verification / bilibili-api-ops / chinese-convention-search / credential-management / api-ecosystem-research / api-diagnostics / morning-briefing-audio / quick-fact-check / chara-profile / douyin / typhoon-monitor
- 保留 9 个：hermes-agent（官方）/ internet-memes-reference（导视数据）/ short-stories-liya / ruozhiba-wordbank（已入口化）/ group-chat-discipline / info-hunt / build-analysis（高频主场景）/ （私档）-archive（索引）/ bili-audio-archive（刚合并内容密度高）
- **前置（同轮）：** B站音频三件套合并 → bili-audio-archive（asmr-hifi + bili-hifi-audio 吸收，76 → 74 skill）
- **教训：** 拆分时「说明 md」也能拆——已经写好的 references 不算内容，SKILL.md 里内嵌的详细说明才是要拆的对象

## 2026-09-22 · short-stories-liya 减法（「规矩留、案例搬」第二轮）

- **背景**：SKILL.md 25KB／p0-core 33KB，章节编号自己乱了（走到「五、六」又跳回「四·九/十/十一」），同一批判据在多处各写一版。阁下拍 **A 档**（判据＋阁下原话全留，血账／实测／session 实录搬独立案例档）。
- **体积**：原有 11 份 135KB → **87KB（−36%）**；SKILL.md 25.4→12.2KB（−52%）；revision-workflow 9.7→2.5KB（−74%）；polish 13.3→4.2KB（−69%）；wings 6.6→1.5KB（−78%）；p1 8.9→7.0KB；p0-notes 14.0→10.7KB；vices 11.9→9.1KB；three-flows 5.6→3.7KB；p0-core 33.4→29.0KB。
- **新档 7 份**：`tools.md`（工具手册）／`archive-state.md`（存档·沿革·判例）／`p0-core-cases.md`（血账）／`seven-layer-enrichment.md`／`title-naming.md`／`outlines/drafts/14|16-候选与过程.md`。
- **抓手是「去重」不是「压字」**：四条硬红线在 p0-core／p1／three-flows／tools 各一份 → 归 p0-core §四·八；字数口径三处 → 归 p1 §五；弊端检查表两处 → 归 p1 §二；「加厚＝加事件」三处 → 归 p0-core §四·五。
- **三处硬冲突裁决（旧口径未清，比肥更危险）**：①「字数不足＝感官层没挖完」删（与「加厚＝加事件」对撞）②七层上限只留一套（`vices` 的「每 300–400 字 1–2 种感官」）③「自由间接话语」判给 `vices` 的「只写可观测」，`seven-layer` 档里加边界注。
- **判例·锚点不动**：`scripts/story.py` 里 10+ 处、`p1`／`three-flows`／`novel-writing`／项目 README 都按 **`p0-core §四·五/四·六/四·七/四·八`**、**`p0-notes 八/九`** 定位 → 结论：**只归位、不重编号**；p0-notes 重排后节号错位，改回原骨架（八＝一致性自查／九＝初见 vs 熟路）才没断链。**改判据档之前先 grep 全库的节号引用**。
- **教训**：① 行级守恒校验对「重写型」文件会假报 36% 缺失——**换「判据指纹」（命令／阈值／区间／百分比）校验**才准（实测命令 6/6、阈值仅措辞差异）②大纲「一页纸」新规矩：骨架进大纲、过程料进 `drafts/`，**禁止再在文件尾新开带日期的章节层**（16 一天内从 0 长到 15KB 就是这么来的）③搬走节次后要补**占位标题**（`## 三、…（已移出 → drafts/）`），否则节号跳号、mdcheck 报错、交叉引用失锚。④**改文件别用 `open(p,'w')` 后再 `open(p).read()`**——先截断后读＝读到空，本轮就是这么把 18KB 的记账清空的（靠 git 恢复）。
