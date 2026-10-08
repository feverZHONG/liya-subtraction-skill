# 减法 skill · Subtraction

> 技能库精简与维护的方法论 —— 让 agent 的技能库保持「薄而准」。
> 适用于任何用 SKILL.md 体系的 agent（Hermes / Claude Skills / 自建 agent 都行）。

## 这是什么

一套「做减法」的实操方法：什么时候该合并、什么时候该拆薄、什么时候该删、删之前先做什么、删完怎么留痕。

核心信念只有一句：**技能库的敌人不是少，是冗余；SKILL.md 只做入口，细节拆到 references/。**

覆盖这些场景：

- **冗余检测** —— 哪些技能在说同一件事，谁该并进谁
- **SKILL.md 拆薄** —— 厚正文 → 「入口 + references 索引表」
- **跨工作区合并** —— 把别处（另一个 agent / 另一份工作区）的技能吸收进来
- **使用情况审查** —— 零使用记录、半死不活的技能怎么办
- **入库判定** —— 哪些该进版本库、哪些该留在本地
- **精简历史与踩坑** —— 记下「为什么删过」，避免同一件事反复决策

## 怎么装

克隆到你的 skills 目录即可：

```bash
git clone https://github.com/feverZHONG/liya-subtraction-skill.git ~/.hermes/skills/skill-curation
```

只当资料读也行 —— `SKILL.md` 是索引，正文在 `references/`。

## 目录

| 路径 | 内容 |
|:-----|:-----|
| `SKILL.md` | 总入口：这是什么 + 什么时候用 + 索引表 |
| `references/` | 方法论正文（核心原则 / 精简流程 / 跨库合并 / 使用审查 / T 分级 / 踩坑 / 精简历史 …） |
| `scripts/mdcheck.py` | md 体检：体积排行 / `\n` 字面量 / 重复标题 / 编号跳号 / 断链 |
| `scripts/skill_audit.py` | 技能库清点：空壳 / 厚薄 / 无脚本 / T 分级，一次跑完 |
| `templates/skill-md.md` | SKILL.md 模板 |

两个脚本的默认路径取自作者环境，**改成你自己的**：

```bash
python3 scripts/mdcheck.py --root ~/.hermes            # 指定仓库根
SKILLS_ROOT=~/.hermes/skills python3 scripts/skill_audit.py
```

## 提思路 / 提修正

这个仓库最想要的不是「更漂亮的文档」，是**别处踩出来的新判据**。

- 有新的减法思路、踩坑、更好用的判据 → 开 [Issue](https://github.com/feverZHONG/liya-subtraction-skill/issues)，说清场景就行（哪一类技能、删/并之前长什么样、之后怎样了）
- 想直接改 → Fork + PR。改动请写清**删了什么、为什么**，只加不删的 PR 会被问
- PR 合并后，作者侧会用 `bin/skillrepo skill-curation sync` 双向同步回本地副本（机制：以「上次同步」为共同祖先，git 三方合并，冲突不自动覆盖而是停下来给人看）

## 姊妹仓库


- [liya-chat-game-referee](https://github.com/feverZHONG/liya-chat-game-referee) · [liya-spy-game](https://github.com/feverZHONG/liya-spy-game) · [liya-sea-turtle-soup](https://github.com/feverZHONG/liya-sea-turtle-soup) —— 聊天里能玩的三件（回合制裁判引擎 / 谁是卧底 / 海龟汤）
- [liya-persona-authoring](https://github.com/feverZHONG/liya-persona-authoring) —— 人格/身份文件维度上的同一套减法（附带《角色设定写作模板 v1.2》）
- [liya-sillytavern-cards](https://github.com/feverZHONG/liya-sillytavern-cards) —— 酒馆(SillyTavern)角色卡：写法（PList + Ali:Chat）、格式规格、三个 Python 工具
- [liya-sillytavern-worldbook](https://github.com/feverZHONG/liya-sillytavern-worldbook) —— 酒馆世界书（Lorebook）：触发链源码实证 + 触发体检 / 模拟 / 生成工具
- [liya-vision-recognition-traps](https://github.com/feverZHONG/liya-vision-recognition-traps) —— 视觉模型识图陷阱：19 条实测陷阱 + 真 OCR 通道 + AI 生图物理体检 + 两图差分
- [liya-delegation-and-verification](https://github.com/feverZHONG/liya-delegation-and-verification) —— 委派与验收：给子代理写任务书、并行隔离、把「自报」验成事实
- [liya-tavern-card-refinement](https://github.com/feverZHONG/liya-tavern-card-refinement) —— 酒馆角色卡精修：7 字段清单 + 槽位归位 + 6 类断言校验 + 可用性验收（不装酒馆也能量）
- [liya-prose-quality-metrics](https://github.com/feverZHONG/liya-prose-quality-metrics) —— 稿子读起来「平」怎么办：先量再改（对话占比·句长σ·台词宽度·标点谱·段均句）＋ 7 个工具
- [liya-ruozhiba-wordbank](https://github.com/feverZHONG/liya-ruozhiba-wordbank) —— 弱智吧题防御手册：中文互联网逻辑陷阱题 160 道逐题拆解 + 三连防御法（拆前提→指谬误→反杀）
- [liya-subtitle-proofreading](https://github.com/feverZHONG/liya-subtitle-proofreading) —— 字幕校对/重建/外挂 SRT：对照成稿逐处修正 + 按原文重建分块 + md→SRT + 多人语音 ASR 导出件解析（5 个纯标准库工具）
- [liya-corpus-line-mining](https://github.com/feverZHONG/liya-corpus-line-mining) —— 从本地语料／会话库挖可复用原句：候选池筛选 + 人审落库（纯标准库，零依赖）
- [liya-story-revision-plan](https://github.com/feverZHONG/liya-story-revision-plan) —— 小说全稿修订方案：评估／缺口清单／逐章大纲／信息融合／优先级（含标准模板）
- [liya-dev-workflow](https://github.com/feverZHONG/liya-dev-workflow) —— 开发全流程方法论：环境侦查／计划／spike／TDD／迭代脚本／调试／预提交审查／推送排障／同步验收
- [liya-news-verification](https://github.com/feverZHONG/liya-news-verification) —— 验证伞：轻量核查／交付前多源验证／链接危险识别／厂商官宣核实／链接考古（含 link_check 工具族）
- [liya-knowledge-persistence](https://github.com/feverZHONG/liya-knowledge-persistence) —— 知识持久化：信息该放记忆层／文件／技能库的分层规范（附记录完整性、语料减法、归档模式）
- [liya-incident-review](https://github.com/feverZHONG/liya-incident-review)
- [liya-document-translation](https://github.com/feverZHONG/liya-document-translation)

## 许可

**双许可**——文档与代码分开：

- **代码**（`scripts/` 下的文件）：**MIT** —— 拿去用、改、再发，保留版权声明即可。
- **文档**（`SKILL.md`、`references/`、本 README 的正文）：**[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)** —— 可以自由使用、改编、连商用都行，**但要署名**（莉娅 / [@feverZHONG](https://github.com/feverZHONG)）并注明来源。

两份许可的全文：`LICENSE`（MIT）／`LICENSE-DOCS`（CC BY 4.0）。

---

*莉娅（[@feverZHONG](https://github.com/feverZHONG)）· 宇宙美好记录官*
