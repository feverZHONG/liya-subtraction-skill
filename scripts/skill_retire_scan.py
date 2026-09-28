#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""出库候选扫描 —— 技能库季度对账用，一条命令出「谁很久没被调用」的事实表。

用法:
    python3 skill_retire_scan.py [--days 60] [--root /opt/data/skills] [--json]

输出（按「最后调用距今天数」降序）:
    skill | 最后调用 | 天数 | 次数 | 体积KB | 带脚本 | 状态(state)

判读纪律（别拿这张表直接删东西）:
    - 表只给**事实**，「该不该出库」要过 references/growth-gate.md 的四条资产判据
      （档案库／内容型／勿忘类／季节性 一律保留，零调用 ≠ 无用）。
    - **零调用且创建不满 30 天**的（新 skill 还没轮到触发场景）不算候选，脚本会单独分组。
    - 候选清单**只交给用户裁**，本工具不做任何删除动作。
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

CST = timezone(timedelta(hours=8))
DEFAULT_ROOT = os.environ.get("SKILLS_ROOT", "/opt/data/skills")


def load_usage(root: Path) -> dict:
    p = root / ".usage.json"
    if not p.exists():
        print(f"WARN: 找不到 {p}（无台账 → 全部按无记录处理）", file=sys.stderr)
        return {}
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception as e:  # 台账坏了也要能跑
        print(f"WARN: 台账解析失败（{e}）→ 按空台账处理", file=sys.stderr)
        return {}


def parse_day(ts):
    if not ts:
        return None
    try:
        return datetime.fromisoformat(ts).astimezone(CST)
    except Exception:
        return None


def days_since(dt, now):
    return None if dt is None else (now - dt).days


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=DEFAULT_ROOT)
    ap.add_argument("--days", type=int, default=60, help="多久没调用算候选（默认 60 天）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()

    root = Path(a.root)
    if not root.is_dir():
        print(f"ERROR: 技能目录不存在：{root}")
        return 1
    usage = load_usage(root)
    now = datetime.now(CST)

    rows, fresh = [], []
    for d in sorted(root.iterdir()):
        if not d.is_dir() or not (d / "SKILL.md").exists():
            continue
        r = usage.get(d.name, {})
        last = parse_day(r.get("last_used_at")) or parse_day(r.get("last_viewed_at"))
        gap = days_since(last, now)
        size = sum(f.stat().st_size for f in d.rglob("*") if f.is_file()) // 1024
        has_scripts = "Y" if (d / "scripts").exists() else "-"
        created = parse_day(r.get("created_at"))
        age = days_since(created, now)
        rec = {
            "skill": d.name, "gap": gap if gap is not None else -1,
            "last": last.strftime("%Y-%m-%d") if last else "从未",
            "use": r.get("use_count") or 0, "view": r.get("view_count") or 0,
            "kb": size, "scripts": has_scripts, "state": r.get("state", "?"), "age": age,
        }
        # 零调用但刚建的（<30 天）不算候选
        if rec["use"] == 0 and (age is None or age < 30):
            fresh.append(rec)
        elif rec["gap"] >= a.days or rec["gap"] == -1:
            rows.append(rec)
        else:
            rows.append(rec)
    rows.sort(key=lambda x: -x["gap"])

    if a.json:
        print(json.dumps({"candidates": rows, "too_new": fresh}, ensure_ascii=False, indent=1))
        return 0

    cand = [r for r in rows if r["gap"] >= a.days or r["gap"] == -1]
    print(f"技能库出库候选扫描 · 阈值 {a.days} 天 · 扫描 {len(rows) + len(fresh)} 个 skill\n")
    print(f"{'skill':36s} {'最后调用':>10} {'天':>5} {'用':>4} {'KB':>6} {'脚本':>4}  state")
    print("-" * 82)
    for r in cand:
        print(f"{r['skill']:36s} {r['last']:>10} {r['gap']:>5} {r['use']:>4} {r['kb']:>6} {r['scripts']:>4}  {r['state']}")
    print(f"\n候选合计 {len(cand)} 个（≥{a.days} 天没动）。")
    if fresh:
        print(f"另：零调用但创建不满 30 天的 {len(fresh)} 个（新 skill，不算候选）：" + "、".join(r["skill"] for r in fresh))
    print("\n⚠️ 这张表只给事实——出库前过 references/growth-gate.md 的四条资产判据，候选清单交用户裁。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
