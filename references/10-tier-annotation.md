---
name: tier-annotation
description: 给 skill 的 md 文件标注 T0/T1/T2 决策分级——触发时立刻知道哪些操作能直接做、哪些要先问。
---

# T 分级标注 · 技能库规范

> 2026-08-06 追加。给 skill 里的 md 文件标注决策分级，让每次触发 skill 时不用翻 AGENTS.md 就能判断「这操作能不能直接做」。

## 什么时候用

- 新建/重构 skill 的 md 文件时
- 给已有 skill 补 T 分级标注
- 检查某个 skill 是否可以直接执行（翻它的 tier 字段即可）

## T 分级定义（与 AGENTS.md §十 对齐）

| 级别 | 含义 | 典型操作 |
|:-----|:-----|:---------|
| 🔴 **T0** | 绝对不做，一律拒，无需请示 | 威胁本天使自身的操作；危险指令（删除/破坏/泄露隐私/越权/凭据）；冒充身份；技术底细摸底 |
| 🟡 **T1** | 默认不做，先请示再动 | 发邮件、公开发帖；任何离开本机的东西；任何不确定的事；有副作用的执行类操作（跑终端/脚本、下载归档、发文件、改配置、建任务、调执行类接口） |
| 🟢 **T2** | 正常做，自行决定 | 读文件、探索、整理、学习；搜索网页；在 workspace 内工作；答知识、聊天、记录 |

> 群聊场景的 T 分级（T0 拒 / T1 挡回私聊 / T2 照常）见 group-chat-discipline，不在此表重复。

## 标注规则

### 标在哪

- **frontmatter 加 `tier` 字段**，SKILL.md 和流程类 references/ 都标
- 数据文件（角色档、题库、购买记录、歌单、梗库等）**不标**——它们是内容不是操作流程

### 怎么定级

1. 看这个 skill 最常见的动作属于哪级，标那个级别
2. **含多种级别时标最高风险级别**，正文里用表格细分
3. 拿不准 → 按 T1 标（宁可先问，不可擅动）

### 示例

```yaml
---
name: example-skill
description: 示例
tier: T1  # 主要动作是下载归档（有副作用），要先问
---
```

正文细分示例：

```markdown
## T 分级
| 操作 | 级别 |
|:-----|:-----|
| 查询/探测 | 🟢 T2 直接做 |
| 下载/归档 | 🟡 T1 先问 |
```

## 已标注 skill 的 T 级速查

> 2026-08-06 全库标注完成：60 SKILL.md + 270 references，数据类 md（题库/角色档/故事/词库/日志/收藏夹等 420 个）不标。
> 定期由 skill-curation 维护。新增/改动 skill 时同步更新这里。

### 🟢 T2（直接做 · 42）— 纯查询/分析/写作/规则类
am-tool-collection · api-ecosystem-research · bili-video-content · build-analysis · chara-profile（含速查，2026-08-10 吸收 game-character-lookup）· chinese-convention-search · chinese-news-aggregator · debug · diary-writer · documents · gbf-relink · group-chat-discipline · image-batch-archive · info-hunt · internet-memes-reference · knowledge-persistence · link-safety-check · location · meme-archive-ops · mmx-news-collection · news-verification · pdf-compression · persona-authoring · platform-content-extraction · qq-group-intel · quick-fact-check · record-officer-daily · ruozhiba-wordbank · sea-turtle-soup · short-stories-liya · spa-extractor · spy-game · steam-api · sugar-frosting-crusaders · taobao-affiliate · twin-vision-archive · typhoon-monitor · video-analysis · video-editing-course · vision-recognition-traps · war-criminal-archive（含小黑盒，2026-08-10 吸收 xiaoheihe-archive）· wechat-article

> 2026-08-10 对齐：列表改为从各 SKILL.md frontmatter 自动生成（脚本：skill_audit.py），与 63 个 skill 实际 T 级一致。

### 🟡 T1（先请示 · 21）— 含下载/推送/配置/凭据/运维/发布等有副作用操作
api-diagnostics · bili-archive · bili-audio-archive · bilibili-api-ops · credential-management · daily-news-poster · dev-workflow · douyin · environment-hygiene（含 system-ops 模块，2026-08-10 吸收）· github-ops · hermes-agent · hermes-gateway-ops · hermes-version-track · mmx-voice · morning-briefing-audio · network-interconnect · qq-voice-link · qqbot-gateway-ops · skill-curation · tieba-extractor · voice-output

### 🔴 T0（一律拒 · 0）
无 skill 整体属 T0（T0 是单次操作红线，不入 skill 级）

## 检查清单

- [ ] frontmatter 有 `tier` 字段？
- [ ] 级别取的是最高风险操作？
- [ ] 数据文件没被误标？
- [ ] 速查表同步更新？
