#!/usr/bin/env python3
"""sk — 技能库运维入口（skill-curation 的统一 CLI）。

子命令：
  stats [--sort kb|lines|chars|desc] [--top N] [--min KB]
        全库一览：行数/字符/字节/refs/scripts/description 长度 + 汇总。
        **排序看字符数（chars），不看行数**——行数会被表格与清单撑虚高。
  skeleton <skill> [--min-chars N]
        单个 skill 的章节骨架：每节行数/字符，标出可搬的肥节。
        拆薄前先跑这个，再写 spec。
  verify <skill>... [--base REF]
        拆薄/合并后的**收尾验收**（默认 --base HEAD＝要求改动尚未提交）：
        ① 守恒复核：基线里 SKILL.md 每行 >25 字必须出现在「新 SKILL ∪ 全部 references」
        ② mdcheck 对基线：整理后问题数**不得高于**基线
        两关全过才算没欠账；任一关报 MISS/欠账，先修再提交。
  refs <skill>
        双向引用分布：谁引用它（改动前必查）／它引用了谁。
  另有转发：audit（清点库）｜retire [--days N]（出库候选）｜thin <spec.json>（拆薄）

约定：/opt/data/skills 下的**点开头目录**（.archive/.curator_backups/.hub）不是技能，一律跳过。
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

SKILLS = os.environ.get("SKILLS_ROOT", "/opt/data/skills")
SCRIPTS = os.path.join(SKILLS, "skill-curation", "scripts")
def _find_repo(start):
    """往上找第一个含 .git 的目录＝仓库根（别用固定层数——脚本换位置就错）。"""
    d = start
    while d != "/":
        if os.path.isdir(os.path.join(d, ".git")):
            return d
        d = os.path.dirname(d)
    return start


REPO = _find_repo(os.path.dirname(os.path.abspath(__file__)))


def skill_names():
    return sorted(d for d in os.listdir(SKILLS)
                  if not d.startswith(".") and os.path.exists(os.path.join(SKILLS, d, "SKILL.md")))


def read(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        return f.read()


def extract_description(txt):
    """抓 frontmatter 的 description（含 `>-` 折叠块），返回压平后的字符串。"""
    m = re.search(r"^description:\s*(.*?)(?=\n[a-z_]+:\s|\n---)", txt, re.S | re.M)
    if not m:
        return ""
    return re.sub(r"\s+", " ", m.group(1)).strip().strip('"').strip("'").strip()


def walk_stats(skill_dir):
    """返回 (总字节, references 文件数, scripts 文件数)。"""
    total = nref = nscr = 0
    for dp, dn, fn in os.walk(skill_dir):
        for f in fn:
            fp = os.path.join(dp, f)
            try:
                total += os.path.getsize(fp)
            except OSError:
                pass
            rel = os.path.relpath(fp, skill_dir)
            if rel.startswith("references" + os.sep):
                nref += 1
            elif rel.startswith("scripts" + os.sep):
                nscr += 1
    return total, nref, nscr


def collect(name):
    d = os.path.join(SKILLS, name)
    sk = os.path.join(d, "SKILL.md")
    txt = read(sk)
    total, nref, nscr = walk_stats(d)
    return {
        "name": name,
        "lines": txt.count("\n") + 1,
        "chars": len(txt),
        "bytes": os.path.getsize(sk),
        "kb": total / 1024,
        "refs": nref,
        "scripts": nscr,
        "desc": len(extract_description(txt)),
    }


def cmd_stats(argv):
    sort_key = "chars"
    top = None
    min_kb = 0.0
    if "--sort" in argv:
        sort_key = argv[argv.index("--sort") + 1]
    if "--top" in argv:
        top = int(argv[argv.index("--top") + 1])
    if "--min" in argv:
        min_kb = float(argv[argv.index("--min") + 1])
    rows = [collect(n) for n in skill_names()]
    if min_kb:
        rows = [r for r in rows if r["kb"] >= min_kb]
    rows.sort(key=lambda r: -r[sort_key])
    if top:
        rows = rows[:top]
    print(f"{'skill':30} {'行':>5} {'字符':>7} {'字节':>7} {'总KB':>8} {'refs':>4} {'scr':>4} {'desc':>5}")
    for r in rows:
        flag = ""
        if r["chars"] > 15000:
            flag = " ⚠️字符肥"
        elif r["lines"] > 200:
            flag = " ⚠️行数高(查是否表格撑的)"
        elif r["lines"] > 95:
            flag = " ·"
        print(f"{r['name']:30} {r['lines']:>5} {r['chars']:>7} {r['bytes']:>7} "
              f"{r['kb']:>8.1f} {r['refs']:>4} {r['scripts']:>4} {r['desc']:>5}{flag}")
    allr = [collect(n) for n in skill_names()]
    print(f"\n技能数 {len(allr)}｜description 合计 {sum(r['desc'] for r in allr)} 字符"
          f"（中位 {sorted(r['desc'] for r in allr)[len(allr) // 2]}）"
          f"｜SKILL.md 合计 {sum(r['chars'] for r in allr)} 字符")
    print("口径：排序看 chars 不看 lines——表格/清单多的 skill 行数会虚高（实测 rimworld 243 行只有 6.8K 字符）。")
    return 0


def cmd_skeleton(argv):
    if not argv:
        print("用法: sk skeleton <skill> [--min-chars N]")
        return 1
    name = argv[0]
    min_chars = int(argv[argv.index("--min-chars") + 1]) if "--min-chars" in argv else 0
    lines = read(os.path.join(SKILLS, name, "SKILL.md")).split("\n")
    idx = [i for i, l in enumerate(lines) if l.startswith("## ")] + [len(lines)]
    print(f"### {name}：{len(lines)} 行 / {sum(len(l) for l in lines)} 字符")
    for a, b in zip(idx[:-1], idx[1:]):
        seg = "\n".join(lines[a:b])
        if min_chars and len(seg) < min_chars:
            continue
        heavy = " ⬅️ 可搬" if len(seg) > 1200 else ""
        print(f"  {lines[a][:54]:56} {b - a:>4} 行 {len(seg):>6} 字符{heavy}")
    print("\n提示：>1200 字符的节**先判性质**——展开型（流程／判例／案例）才适合搬 references；"
          "清单与索引用表（收录范围、标号索引 N1/F5/S3 这类）属检索件，搬了反而拆散锚点，别动。")
    return 0


def _git(*args, **kw):
    return subprocess.run(["git", "-C", REPO] + list(args), capture_output=True, text=True, **kw)


def cmd_verify(argv):
    base = "HEAD"
    if "--base" in argv:
        i = argv.index("--base")
        base = argv[i + 1]
        argv = argv[:i] + argv[i + 2:]
    names = [a for a in argv if not a.startswith("--")]
    if not names:
        print("用法: sk verify <skill>... [--base REF]   （改动未提交时 base 用默认 HEAD 即可）")
        return 1
    mdcheck = os.path.join(SCRIPTS, "mdcheck.py")
    tmp_root = os.path.join(REPO, "workspace", "tmp")

    def run_mdcheck(path):
        if not os.path.isdir(path):
            return -1
        r = subprocess.run([sys.executable, mdcheck, path], capture_output=True, text=True)
        m = re.search(r"问题总数: (\d+)", r.stdout)
        return int(m.group(1)) if m else -1

    bad = []
    for name in names:
        d = os.path.join(SKILLS, name)
        old = _git("show", f"{base}:skills/{name}/SKILL.md").stdout
        if not old:
            # 同理：核对不了 ≠ 通过（基线写错、或这是新建的 skill）——一律计入欠账，别静默放过
            print(f"{name:26} 🔴 无法核对：基线里没有这个 skill（基线写错？还是新建的？）")
            bad.append(name)
            continue
        new = read(os.path.join(d, "SKILL.md"))
        pool = new
        for dp, dn, fn in os.walk(os.path.join(d, "references")):
            for f in fn:
                pool += read(os.path.join(dp, f))
        miss = [l for l in old.split("\n") if len(l.strip()) > 25 and l not in pool]

        os.makedirs(tmp_root, exist_ok=True)
        tmp = tempfile.mkdtemp(dir=tmp_root, prefix="skverify-")
        try:
            p1 = subprocess.run(f"git -C {REPO} archive {base} skills/{name} | tar -x -C {tmp}",
                                shell=True, capture_output=True, text=True)
            if p1.returncode != 0:
                # ⚠️ 不能只 print 就 continue——那会让末尾误报「全部不欠账」（假绿）
                print(f"{name:26} 🔴 基线解压失败：{p1.stderr.strip()[:60]}")
                bad.append(name)
                continue
            b_md = run_mdcheck(os.path.join(tmp, "skills", name))
            n_md = run_mdcheck(d)
            ok = (not miss) and (n_md <= b_md)
            if not ok:
                bad.append(name)
            print(f"{name:26} 守恒缺失 {len(miss):>2} ｜ mdcheck {b_md} → {n_md}  "
                  f"{'✅ 不欠账' if ok else '🔴 欠账'}")
            for m in miss[:5]:
                print(f"    MISS: {m[:90]}")
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
    if bad:
        print(f"\n🔴 欠账 {len(bad)} 件：{', '.join(bad)}——先补再提交。")
        return 1
    print("\n✅ 全部不欠账。")
    return 0


def cmd_refs(argv):
    if not argv:
        print("用法: sk refs <skill>")
        return 1
    name = argv[0]
    d = os.path.join(SKILLS, name)
    print(f"=== 谁引用 {name}（改动它之前必查）===")
    r = subprocess.run(["grep", "-rn", name, "--include=*.md", "--include=*.py", "--include=*.sh",
                        "--include=*.json", SKILLS, os.path.join(REPO, "bin")],
                       capture_output=True, text=True)
    hits = [l for l in r.stdout.split("\n")
            if l and not l.startswith(d + os.sep) and ".usage.json" not in l]
    if not hits:
        print("  （无外部引用——合并/改名最省事的类型）")
    for l in hits[:40]:
        print("  " + l.replace(SKILLS + "/", "").replace(REPO + "/", ""))
    if len(hits) > 40:
        print(f"  …另有 {len(hits) - 40} 处")
    print(f"\n=== {name} 引用了谁 ===")
    body = read(os.path.join(d, "SKILL.md"))
    for dp, dn, fn in os.walk(os.path.join(d, "references")):
        for f in fn:
            body += read(os.path.join(dp, f))
    outs = sorted(set(re.findall(r"skill:\s*([a-z0-9-]+)", body)) |
                  set(re.findall(r"`([a-z0-9-]+)/references/", body)))
    print("  " + ("、".join(outs) if outs else "（无跨 skill 引用）"))
    return 0


def forward(script, argv):
    return subprocess.call([sys.executable, os.path.join(SCRIPTS, script)] + list(argv))


USAGE = __doc__


def main():
    argv = sys.argv[1:]
    if not argv or argv[0] in ("-h", "--help", "help"):
        print(USAGE)
        return 0
    cmd, rest = argv[0], argv[1:]
    table = {
        "stats": cmd_stats,
        "skeleton": cmd_skeleton,
        "verify": cmd_verify,
        "refs": cmd_refs,
        "audit": lambda a: forward("skill_audit.py", a),
        "retire": lambda a: forward("skill_retire_scan.py", a),
        "thin": lambda a: forward("skill_thin.py", a),
    }
    if cmd not in table:
        print(f"未知子命令：{cmd}\n")
        print(USAGE)
        return 1
    return table[cmd](rest)


if __name__ == "__main__":
    sys.exit(main())
