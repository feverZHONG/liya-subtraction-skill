#!/usr/bin/env python3
"""技能库审计——做减法前的清点工具。

一次跑出：
- 活跃 skill 数 / 空壳目录（无 SKILL.md）
- SKILL.md 厚薄排行（找「厚技能候选」）
- 无脚本目录清单（找「少说废话」候选）
- T 分级统计
用法: python3 skill_audit.py [--root 技能目录] [--top N]（也认 SKILLS_ROOT 环境变量）
"""
import os, re, sys
from pathlib import Path

DEFAULT_ROOT = os.environ.get("SKILLS_ROOT", "/opt/data/skills")


def main():
    argv = sys.argv[1:]
    root = Path(argv[argv.index("--root") + 1]) if "--root" in argv else Path(DEFAULT_ROOT)
    if not root.is_dir():
        print(f"ERROR: 技能目录不存在：{root}")
        return 1
    top_n = 12
    if "--top" in argv:
        top_n = int(argv[argv.index("--top") + 1])

    dirs = sorted(d for d in root.iterdir() if d.is_dir())
    with_md = [d for d in dirs if (d / "SKILL.md").exists()]
    shells = [d for d in dirs if not (d / "SKILL.md").exists()]
    print(f"目录总数: {len(dirs)}  活跃 skill: {len(with_md)}  空壳: {len(shells)}")
    if shells:
        print("空壳目录(无SKILL.md): " + ", ".join(d.name for d in shells))

    # 厚薄排行
    sizes = []
    tiers = {"T0": 0, "T1": 0, "T2": 0, "未标": 0}
    for d in with_md:
        txt = (d / "SKILL.md").read_text(encoding="utf-8")
        lines = txt.count("\n") + 1
        sizes.append((lines, d.name))
        m = re.search(r"^tier:\s*(T[0-9])", txt, re.M)
        tiers[m.group(1) if m else "未标"] += 1
    sizes.sort(reverse=True)
    print(f"\nT分级: T1={tiers['T1']} T2={tiers['T2']} T0={tiers['T0']} 未标={tiers['未标']}")
    print(f"\n厚 SKILL.md TOP{top_n}（>80行可考虑拆薄/入口化）:")
    for lines, name in sizes[:top_n]:
        flag = " ⚠️厚" if lines > 80 else ""
        print(f"  {lines:4d} 行  {name}{flag}")

    # 无脚本目录
    no_scripts = [d.name for d in with_md if not (d / "scripts").exists()]
    print(f"\n无脚本目录（{len(no_scripts)} 个，可脚本化候选）:")
    print("  " + ", ".join(no_scripts))

if __name__ == "__main__":
    main()
