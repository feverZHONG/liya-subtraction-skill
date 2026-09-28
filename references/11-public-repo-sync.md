# 对外仓库 · 双向同步

## 一 skill 一仓库（不是两份拷贝，是原件 + 对外工作副本）

| 位置 | 角色 | 谁跟踪 |
|:-----|:-----|:-------|
| `/opt/data/skills/<name>` | 随时调用的**原件** | NAS 私有库（Liya-NAS-Hermes） |
| `/opt/data/repos/<repo>` | **公开仓库工作副本** | 自己的 git，远程 = GitHub |

注册表：`config/skill-repos.json`（一 skill 一行，`extra` 挂配套文件）

| skill | 公开仓库 |
|:------|:---------|
| `skill-curation` | [liya-subtraction-skill](https://github.com/feverZHONG/liya-subtraction-skill) |
| `persona-authoring` | [liya-persona-authoring](https://github.com/feverZHONG/liya-persona-authoring)（+ 配套模板） |
| `sillytavern-cards` | [liya-sillytavern-cards](https://github.com/feverZHONG/liya-sillytavern-cards)（+ 配套分界文档） |
| `sillytavern-worldbook` | [liya-sillytavern-worldbook](https://github.com/feverZHONG/liya-sillytavern-worldbook) |
| `vision-recognition-traps` | [liya-vision-recognition-traps](https://github.com/feverZHONG/liya-vision-recognition-traps) |
| `chat-game-referee` | [liya-chat-game-referee](https://github.com/feverZHONG/liya-chat-game-referee) |
| `spy-game` | [liya-spy-game](https://github.com/feverZHONG/liya-spy-game) |
| `sea-turtle-soup` | [liya-sea-turtle-soup](https://github.com/feverZHONG/liya-sea-turtle-soup) |
| `delegation-and-verification` | [liya-delegation-and-verification](https://github.com/feverZHONG/liya-delegation-and-verification) |
| `tavern-card-refinement` | [liya-tavern-card-refinement](https://github.com/feverZHONG/liya-tavern-card-refinement) |
| `prose-quality-metrics` | [liya-prose-quality-metrics](https://github.com/feverZHONG/liya-prose-quality-metrics) |

（权威名单看 `bin/skillrepo list`；本表是给人看的对照。）

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
- **仓库专属文件** README.md / LICENSE / LICENSE-DOCS / .gitignore 只活在仓库，不回灌本地 skill 目录

## 配套文件（extra）——跟仓库走、但不属于本 skill 的文档

用途：某篇文档要随仓库分发、却不属于该 skill（例：用户 B站《角色设定写作模板 v1.2》挂在 persona 仓库里，
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

## 建仓前先做「同名邻居体检」（2026-09-18 点出来）

改名前 / 建仓前，先把**名字跟它像的**扫一遍——只看「活着的 skill」会漏掉三类：

```bash
ls -d skills/.archive/*                    # 归档区（.gitignore 锚定）里的同名兄弟：内容可能已被吸收，但名字会撞
find skills -maxdepth 1 -type d -empty     # 空壳目录：改名/搬迁留下的残骸（曾把 skill 建在 skills/devops/ 里 → 被类目目录吞掉、零备份裸奔）
grep -rn '<skill名>' skills scripts bin cron   # 谁按旧名引用着它（改名前必查）
```

再加一条口头确认：**要建的仓名在 GitHub 上有没有被人（包括自己）占了**——私有仓同名 = 发仓时直接撞车（实例：计划里的「玩法组」仓不能叫 `liya-games`，那名字是私有老游戏厅的）。

判据：① 归档区同名兄弟 → 确认内容已被 live 版吸收，归档区不动；② 空壳 → 清（删目录要请示）；③ 旧名引用 → 全改；④ 仓名 → 避开。

## 新增一对仓库（配方）

1. GitHub 建仓：public、`main`、空仓（API 建仓可能回 500/502 但其实建成了——建完 GET 一次确认）
2. **先脱敏，再复制**（无仓库的那份 skill 是最容易忘的——它一直在私有库里裸着）：扫项目名 / 角色名 / 本机路径（`/opt/data`、`workspace/`）/ 对「阁下」的称呼；例子里的专有名词换中性示例（`my-world.json`、`示例键`），**机制与实测数字一字不动**。判据：`grep -rn "项目名\|/opt/data\|workspace/" skills/<name>/` 无输出
3. 复制 skill → `/opt/data/repos/<repo>`，补 README.md / LICENSE / .gitignore（这三个是仓库专属，双向都绕开）
4. `git init -b main` + `git config user.name/email` + commit + push（github.com 的 443 时好时坏，push 要重试；失败就 `bin/gitpush` 切通道补推）
5. `config/skill-repos.json` 加一行（有配套文件就加 `extra`）
6. `bin/skillrepo <name> sync` 建基线；`bin/skillrepo list` 复核
7. **新仓的 README 要跟老仓互列**（「互列不留断链」）——往每个老仓的「姊妹仓库」段加一行，别只在新仓里列别人

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
5. **改了成对出现的样本要重跑自测**：引擎自测里同一份样本常在两处成对出现（卡侧 / WI 侧各一份），只改一处 → 「两侧解析一致」断言必挂（2026-09-24 脱敏时实际踩到，被自测逮住）。改完必跑 `selftest`，别信「只是改了个字符串」——脱敏/改名类改动同样要走这一步
6. **`sync` 的 fetch 会挂死（2026-09-25 实踩）**：本机 `github.com` 时通时不通，`sync` 第一步就是拉远程 → GnuTLS/TCP 挂住，180s 超时，看着像「什么都没干」。**先看副本的 `git log`**：挂住的往往是 push 那一步，提交已经落地（`local: 本地副本同步（<时间>）`）。这时别反复重试 `sync`，直接在副本目录补推：
   ```bash
   cd /opt/data/repos/<repo> && /opt/data/bin/gitpush --channel api   # 直连不通时走 API 重放
   ```
   回读核实**不靠 git 自己**（它连不上）：`api.github.com` 的 `commits/main` 拿 sha、`contents/<路径>?ref=main` 拿 base64 内容对一眼（公开仓免 token）。
7. **新增「仓库专属文件」必须同步改 `curation_sync.py` 的 `REPO_ONLY`（2026-09-28 实踩）**：许可改双份时加了 `LICENSE-DOCS`，文档清单改了、代码没跟 → 副本里这份被当成「本地没有的文件」，**下次任意一仓 `sync` 都会把它删掉**——12 仓的双许可会一起失效，而且删的是已推送的许可文件。症状极隐蔽：`status` 的「本地 ↔ 副本」差异里只有一行 `-LICENSE-DOCS`，看着像正常提示（实测当时 11 个仓全都有这行）。
   判据：**往仓库加任何「只活仓库」的文件，改完立刻 `grep -n REPO_ONLY scripts/curation_sync.py` 核一遍，并按规矩跑两套沙盒**（`test_skillrepo_sync.py` ＋ `test_skillrepo_extras.py`）。`status` 里出现 `-<文件名>` 而本地确实不该有它 = 漏登记，先修再 sync。
