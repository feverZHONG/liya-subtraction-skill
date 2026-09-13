---
tier: T1  # T分级: T2=直接做 / T1=先请示 / T0=一律拒
---

## Description 精简（本轮新发现）

Description 字段是 Hermes 匹配 skill 的唯一入口。过长的描述浪费 token 且降低匹配精度。

### 精简原则

| 原则 | 说明 |
|------|------|
| **一句话** | 不超过 30 字，说清楚做什么 |
| **不要堆关键词** | `diary-writer` 原来有「日记、日記、diary、daily log、memory记录」→ 删 |
| **不要教 LLM 什么时候用** | `docx` 原来写 20 行「whenever...triggers include...」→ 删，LLM 知道 |
| **不要说明书** | `music-download` 原来写「TV-size/Full Size 识别、去重、花名册」→ 一行搞定 |
| **不要 `|` 多行 YAML** | `xbrowser` 和 `humanizer-zh` 原来用 `|` 块 → 压成一行 |
| **全中文** | `bilibili-dl`/`img-vision` 原来英文 → 统一中文 |

### 精简测试

description 修改后不需要 reload：Hermes 下次匹配时自动读更新后的 frontmatter。

### 实际效果（本 session）

21 个 skill 的 description 从平均 60 字压到 15 字。总字数从 ~1260 字降到 ~315 字，减 75%。

### 精简要有度（2026-08-24 教训）⚠️

**精简过头 = 工具找不到。** 描述是匹配入口，压到只剩「做什么」而删掉「触发词」，本天使扫列表时不知道这个 skill 能解决当前问题，工具躺在那被忽略。

- **柿崎惠查证翻车实录**：read-url 描述只写「网页正文净化器」→ 想不到它能读百度百科（wapbaike 降级 08-16 就内置）；bilibili-api-ops 描述只写「热搜/字幕」→ 想不到它能查专栏文章。四个卡点三个有现成工具没用上。
- **57 字符窗口**：Hermes 技能索引只显示 description 前 57 字符。核心触发词（能力名+场景词）必须在前 57 字符内命中，否则扫列表看不到。
- **触发词怎么放**：`能力名（脚本名/命令名）+ 场景触发词`。例：`B站接口查询——热搜推送/CC字幕/专栏文章搜索直读(bili_article)/番剧分集/视频详情。触发：热搜榜、字幕、cv号、B站文章、接口坑。`
- **新工具建档同步补**：新增脚本/新能力（如 bili_article.py、bin/baike）时，description 必须同步更新——skill 正文写再多，索引不标就等于没有。
- **体检**：描述明显短于 references/scripts/ 实际能力的，属于「窄描述」，要补（2026-08-24 已补 8 个：read-url/bilibili-api-ops/chinese-news-aggregator/info-hunt/news-verification/hermes-agent/taobao-affiliate/documents）。
