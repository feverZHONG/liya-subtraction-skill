---
tier: T1  # T分级: T2=直接做 / T1=先请示 / T0=一律拒
---

# 精简流程

## Step 1 · 清点

```bash
python3 skills/skill-curation/scripts/skill_audit.py    # 一次跑：数量/空壳/厚薄/无脚本/T分级
ls -d /opt/data/skills/*/                               # 全目录清单（需要时）
```

## Step 2 · 分组找重叠

按领域分组。常见重叠信号：

- **同名 CLI 包装** — 多个 skill 调用同一个 CLI，保留功能最全的
- **同领域克隆** — 两个搜索 skill，功能重叠
- **方法论附属** — 某个 skill 的方法论被拆成独立 skill → 合并回本体作附录
- **跨工作区重复** — 从外部工作区导入时，同名技能优先读取全文判断

## Step 3 · 读全文确认重叠

每个可疑组用 `skill_view(name)` 读全文。**禁止凭描述判断。**

| 合并条件 | 保留条件 |
|---------|---------|
| 调用同一 CLI，功能子集 | 不同底层工具（yt-dlp vs curl） |
| 方法论包装本体 | 不同内容类型（视频 vs 专栏） |
| 极薄封装（< 20 行实质内容） | 不同 CLI 平台 |

## Step 4 · 检查 API 可用性

```bash
# mmx 系
mmx search query --q "test" --quiet --non-interactive --count 1
# 3rd-party
python3 skills/xxx/scripts/xxx.py --dry-run
# 依赖检查
python3 -c "import some_module; print('ok')"
```

常见失败模式：
- **维基类 API** — 在中国大陆不可达 → 换源或标记为不可用
- **需要环境变量** — 记下来等用户提供
- **依赖未安装** — 装到 venv

## Step 5 · 执行合并/删除

两种模式：

**① 平级合并：** 多个独立 skill 合并为一个新 umbrella。
```bash
skill_manage(action='delete', name='target', absorbed_into='new-umbrella')
cp -r skills/target/scripts/* skills/new-umbrella/scripts/
cp skills/target/SKILL.md skills/new-umbrella/references/target.md
```

**② 薄技能吸收：** 方法论附属/子域 skill 吸入已有的 umbrella。
```bash
mkdir -p skills/umbrella/references/absorbed
cp skills/target/SKILL.md skills/umbrella/references/absorbed/target.md
skill_manage(action='delete', name='target', absorbed_into='umbrella')
```

**判断薄技能吸收信号：**
- 技能内容高度依赖另一 umbrella 的方法论
- 技能末尾写着「完整流程详见 X skill」
- 技能正文只有 20-50 行实质内容

## Step 6 · 二次审查（多轮递进）

**一轮清理永远不够。**

| 轮次 | 焦点 | 信号 |
|:-----|:------|:------|
| 第一轮 | 大合并、整类无用 | 同领域克隆、大型类别 |
| 第二轮 | 薄技能吸收、低频独立 | 方法论附属、有 umbrella 可吸入的独立技能 |

**实例（66→35）：**
- 第一轮：软件工程9→dev-workflow，创意7+ML6→temp
- 第二轮：cron-pattern/security-response 是 tech-workflow 子域，humanizer-zh 是 writing-standards 子域 → 分别吸收

## Step 7 · 验证 + git 管理

```bash
skills_list                                  # 数量对得上
ls /opt/data/skills/*/SKILL.md | wc -l       # 确认无残留
grep -q "temp/" .gitignore && echo "已忽略" || echo "需添加 temp/ 到 .gitignore"
```

**cron 脚本审计：** 清理涉及 cron 技能的合并后，审计现有 cron job 的输出合规——已在跑的 cron 脚本不会自动遵守新规则。
