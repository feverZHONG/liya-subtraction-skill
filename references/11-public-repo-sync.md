# 对外仓库 · 双向同步

## 两份东西（不是两份拷贝，是原件 + 对外工作副本）

| 位置 | 角色 | 谁跟踪 |
|:-----|:-----|:-------|
| `/opt/data/skills/skill-curation` | 本天使随时调用的**原件** | NAS 私有库（Liya-NAS-Hermes） |
| `/opt/data/repos/liya-subtraction-skill` | **公开仓库工作副本** | 自己的 git，远程 = GitHub |

公开仓库：<https://github.com/feverZHONG/liya-subtraction-skill>（MIT，别人 clone 到自己的 skills 目录就能用）

## CLI

`bin/curation`（= `python3 /opt/data/scripts/curation_sync.py`）

| 命令 | 干什么 |
|:-----|:-------|
| `status` | 三方状态只读：本地↔副本 / 仓库↔远程 / 远程自上次同步以来 / 本地自上次同步 |
| `sync` | 本地改动 → 提交 → 与远程三方合并 → 推送 → 回灌本地（并在 NAS 私有库登记） |
| `resolve` | 冲突处理完的收尾：提交合并 → 推送 → 回灌 |
| `abort` | 退回冲突前（本地原件一个字节不动） |
| `log` | 提交历史 / 远程领先的提交 |
| `diff [文件]` | 差异细节（不指定文件时列远程 vs 上次同步的 stat + 本地↔副本逐文件 diff） |

## 机制（为什么双向不会互相盖掉）

- **共同祖先** = git tag `last-sync`（上次同步成功时的状态）→ 用 git 原生三方合并，重命名/删除都跟得上
- **冲突不自动选边**：两边改了同一处 → `sync` 停下、exit 3、冲突标记留在 REPO 里等人看，`resolve` 才收尾
- **推送失败不回退 tag**：提交留在本地，`status` 如实显示「领先 N 个提交（待推）」，下次 `sync` 自动补推
- **同步前自动备份** 本地原件到 `cache/curation-sync-backup/`（滚动留 5 份）
- **仓库专属文件** README.md / LICENSE / .gitignore 只活在仓库，不回灌本地 skill 目录

## 别处有新思路时怎么进来

1. GitHub 上开 Issue / PR，说清场景（哪类技能、删并之前什么样、之后怎样）→ 合并进 `main`
2. `bin/curation status` → 看到「远程有新提交」+ commit 列表
3. `bin/curation diff` → 看具体改了什么
4. `bin/curation sync` → 落到本地原件（NAS 私有库同时登记），不满意就在本地改完再 sync 推回去
