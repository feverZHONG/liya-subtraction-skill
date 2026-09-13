# 对外仓库 · 双向同步

## 一 skill 一仓库（不是两份拷贝，是原件 + 对外工作副本）

| 位置 | 角色 | 谁跟踪 |
|:-----|:-----|:-------|
| `/opt/data/skills/<name>` | 本天使随时调用的**原件** | NAS 私有库（Liya-NAS-Hermes） |
| `/opt/data/repos/<repo>` | **公开仓库工作副本** | 自己的 git，远程 = GitHub |

注册表：`config/skill-repos.json`（一 skill 一行，`extra` 挂配套文件）

| skill | 公开仓库 |
|:------|:---------|
| `skill-curation` | [liya-subtraction-skill](https://github.com/feverZHONG/liya-subtraction-skill) |
| `persona-authoring` | [liya-persona-authoring](https://github.com/feverZHONG/liya-persona-authoring)（+ 配套模板） |

## CLI

`bin/skillrepo`（= `python3 /opt/data/scripts/curation_sync.py`）；`bin/curation` 是 `skillrepo skill-curation` 的快捷方式。

| 命令 | 干什么 |
|:-----|:-------|
| `skillrepo list` | 看注册了哪些 skill↔仓库对 |
| `skillrepo <name> status` | 三方状态只读：本地↔副本 / 副本↔远程 / 远程自上次同步以来 / 本地自上次同步 / 配套文件 |
| `skillrepo <name> sync` | 本地改动 → 提交 → 与远程三方合并 → 推送 → 回灌本地（NAS 私有库同时登记） |
| `skillrepo <name> resolve` | 冲突处理完的收尾：提交合并 → 推送 → 回灌 |
| `skillrepo <name> abort` | 退回冲突前（本地原件一个字节不动） |
| `skillrepo <name> log` / `diff` | 提交历史 / 差异细节 |

## 机制（为什么双向不会互相盖掉）

- **共同祖先** = git tag `last-sync`（上次同步成功时的状态）→ 用 git 原生三方合并，重命名/删除都跟得上
- **冲突不自动选边**：两边改了同一处 → `sync` 停下、exit 3、冲突标记留在副本里等人看，`resolve` 才收尾
- **推送失败不回退 tag**：提交留在本地，`status` 如实显示「领先 N 个提交（待推）」，下次 `sync` 自动补推
- **同步前自动备份** 本地原件到 `cache/skillrepo-backup/<name>/`（滚动留 5 份）
- **仓库专属文件** README.md / LICENSE / .gitignore 只活在仓库，不回灌本地 skill 目录

## 配套文件（extra）——跟仓库走、但不属于本 skill 的文档

用途：某篇文档要随仓库分发、却不属于该 skill（例：阁下 B站《角色设定写作模板 v1.2》挂在 persona 仓库里，
源文件却是 sillytavern-cards 的 reference）。

- 本地源 = 某个 skill 里的文件；仓库侧 = 仓库里的某个路径
- **判分歧看「上游版本」（`origin/main:路径`）**，不是还没合并的工作副本——工作副本落后时拿它比对，会把「上游改了」误判成一致（2026-09-13 沙盒实测踩中）
- 只有一侧改了 → sync 自动带过去；**两边都改过 → 停下来**，按提示把两边内容改成一致（要保住本地就照本地改仓库侧那份，要采纳上游/PR 就照仓库侧改本地源）再 sync
- 改完的本地源会跟 skill 一起在 NAS 私有库登记

## 别处有新思路时怎么进来

1. 对方在 GitHub 开 Issue / PR（或直接推 main）→ 合并
2. `bin/skillrepo <name> status` → 看到「远程有新提交」/「配套文件：仓库有新改动」+ commit 列表
3. `bin/skillrepo <name> diff` → 看具体改了什么
4. `bin/skillrepo <name> sync` → 落到本地原件

## 新增一对仓库（配方）

1. GitHub 建仓：public、`main`、空仓（API 建仓可能回 500/502 但其实建成了——建完 GET 一次确认）
2. 复制 skill → `/opt/data/repos/<repo>`，补 README.md / LICENSE / .gitignore（这三个是仓库专属，双向都绕开）
3. `git init -b main` + `git config user.name/email` + commit + push（github.com 的 443 时好时坏，push 要重试）
4. `config/skill-repos.json` 加一行（有配套文件就加 `extra`）
5. `bin/skillrepo <name> sync` 建基线；`bin/skillrepo list` 复核

## 维护

改完同步 CLI（`scripts/curation_sync.py`）**必须跑两个沙盒**（file:// 远程，不碰网络也不碰真仓库）：

```bash
python3 scripts/test_skillrepo_sync.py      # 基线/推/拉/自动合并/冲突保护/resolve/abort/删除跟随
python3 scripts/test_skillrepo_extras.py   # 配套文件：基线/推/拉/冲突保护/人工对齐后放行
```

两套都过再收工——2026-09-13 建仓当天，就是配套文件那套沙盒揪出了「分歧判据看错对象」的真 bug。

## 踩坑

1. **配套文件分歧判据看上游版本，不看工作副本**（见上，2026-09-13）
2. **冲突是否解决看文件里还有没有 `<<<<<<<`**，不能看 `git diff --diff-filter=U`——index 的未合并记录在 `git add` 之前一直在，人手改干净了也照样报「没改完」（2026-09-13）
3. **`repos/` 要进 `.gitignore`**：外层 NAS 库若把独立仓库当目录收进去，会变成 gitlink（伪 submodule），commit 时提示「embedded git repository」
4. **独立仓库的内容不进每日文字包**——除非在 `scripts/backup_text.py` 的 `EXTRA_REPOS` 里登记（已登记，每天扫进去）
