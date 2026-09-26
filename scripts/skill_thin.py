#!/usr/bin/env python3
"""skill_thin.py — spec 驱动的「厚 SKILL.md 拆薄」工具（规矩留、案例搬）。

原则（见 skill-curation/references/skill-thinning-workflow.md）：
  SKILL.md 只留「可执行的那一句 + 去处」，判例/反例/实测数字/长流程搬到 references/。
  本工具保证**搬运字节守恒**：搬走的原文逐字进 references，不做任何改写。

用法：
  python3 skill_thin.py <spec.json>            # dry-run，只出报告与预览
  python3 skill_thin.py <spec.json> --write    # 落盘（先自行备份）

spec.json 结构：
{
  "skill_dir": "/opt/data/skills/xxx",
  "ref_meta": {                      # 每个要新建的 references 文件的题头
    "references/trigger-cases.md": {"title": "# 触发详案 · …", "note": "> 2026-09-22 从 SKILL.md 拆出，内容一条未删。"}
  },
  "section_moves": [                 # 整节搬走
    {"heading": "## 维护自检",        # 以该前缀定位 ## 标题（须唯一）
     "ref": "references/maintenance-selfcheck.md",
     "mode": "verbatim",             # verbatim=正文原样进 ref；auto_index=每条截断成索引行留正文
     "keep_text": "## 维护自检\n…",   # 替换该节的文字（mode=auto_index 时用 keep_intro）
     "keep_intro": "## 参考\n\n…"}
  ],
  "moves": [                         # 逐条（行）搬走
    {"match": "- **日期碰撞",         # 行首前缀，须唯一匹配
     "ref": "references/trigger-cases.md",
     "label": "T2",
     "keep": "- **日期碰撞…**（详案 T2）"}
  ],
  "append": "…"                      # 追加到 SKILL.md 末尾（拆分记录块）
}

校验：
  ① 每条搬走的原文，取中段 25 字当指纹，必须「不在新 SKILL.md、在 ref 里」；
  ② 每条 keep 文本必须出现在新 SKILL.md；
  ③ 报告搬出字节 / ref 落盘字节 / SKILL.md 前后体积。
"""
import json, os, sys


def kb(n):
    return f"{n / 1024:.1f}KB"


def load_spec(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def find_heading(lines, heading):
    hits = [i for i, l in enumerate(lines) if l.startswith(heading)]
    if len(hits) != 1:
        raise SystemExit(f"标题定位失败（{len(hits)} 处）：{heading}")
    return hits[0]


def section_end(lines, start):
    """节尾 = 下一个**同级或更高级**的标题（`###` 节不会被 `##` 兄弟节吞掉）。
    2026-09-25 修：早先只认 `## `，对 `###` 子节会一路吞到父节末尾。"""
    lvl = len(lines[start]) - len(lines[start].lstrip("#"))
    for i in range(start + 1, len(lines)):
        s = lines[i]
        if s.startswith("#"):
            n = len(s) - len(s.lstrip("#"))
            if n <= lvl and len(s) > n and s[n] == " ":
                return i
    return len(lines)


def truncate_entry(line, overrides=None):
    """参考索引行：超长条目在第一个全角冒号处截断（冒号太靠前则视为叙述冒号，不切）；
    无冒号的长条目用 overrides 手工给。"""
    s = line.rstrip()
    if overrides:
        for pref, short in overrides.items():
            if s.strip().startswith(pref):
                return short
    if len(s) <= 90:
        return s
    cut = s.find("：")
    if 30 <= cut <= 120:
        return s[:cut].rstrip()
    return s


def main():
    spec_path = sys.argv[1]
    write = "--write" in sys.argv
    spec = load_spec(spec_path)
    sdir = spec["skill_dir"]
    src = os.path.join(sdir, "SKILL.md")
    raw = open(src, encoding="utf-8").read()
    before = len(raw.encode("utf-8"))
    lines = raw.rstrip("\n").split("\n")

    ref_buf = {}      # rel -> [chunk, ...]
    moved = []        # (label, ref, original_text, probe)
    keeps = []        # keep 文本

    def probe_of(text):
        """指纹取**原文尾部** 25 字：keep 行总是比原文短，正文里不该再出现原尾。
        短行（<25 字）不作指纹——```` ```bash ````、表格分隔行这类格式行必然与保留节撞车（假残留）。"""
        t = text.strip()
        if len(t) < 25:
            return None
        return t[-25:] if len(t) > 45 else t

    def detail_probe(orig, keep):
        """真正被搬走的那段细节 = 原文里最长的一个「不在 keep 里」的 12 字窗口。
        返回 None 表示这条没搬动（keep＝原文），或短行（<30 字，格式行不做指纹）。"""
        o, k = orig.strip(), (keep or "").strip()
        if o == k or len(o) < 30:
            return None
        wins = [o[i:i + 12] for i in range(0, max(1, len(o) - 11))]
        cands = [w for w in wins if w not in k]
        return max(cands, key=len) if cands else None

    # ⓪ 按原始行号搬（line_moves；坐标基于**原文件**，倒序执行避免索引漂移）
    #    适用：厚 SKILL.md 里「顶层条目行保留、缩进展开整块搬走」的拆法
    for lm in sorted(spec.get("line_moves", []), key=lambda x: -x["start"]):
        s, e = lm["start"] - 1, lm["end"]
        block = lines[s:e]
        ref = lm["ref"]
        label = lm.get("label", "")
        title = lm.get("title", "")
        chunk = "\n".join(x.rstrip() for x in block).rstrip()
        head = (f"### {label} · {title}\n\n" if title else
                (f"### {label}\n\n" if label else ""))
        ref_buf.setdefault(ref, []).append(head + chunk + "\n")
        for ln in block:
            if ln.strip():
                moved.append((label or title, ref, ln,
                              detail_probe(ln, lm["keep"]) or probe_of(ln)))
        keeps.append(lm["keep"])
        lines[s:e] = [lm["keep"]]

    # ① 整节搬
    for sm in spec.get("section_moves", []):
        h = find_heading(lines, sm["heading"])
        e = section_end(lines, h)
        body = lines[h + 1:e]
        ref = sm["ref"]
        buf = ref_buf.setdefault(ref, [])
        if sm.get("mode") == "auto_index":
            buf.append((lines[h] + "\n\n" + "\n".join(body)).rstrip())
            ov = sm.get("index_overrides", {})
            repl = sm["keep_intro"].rstrip("\n").split("\n")
            for ln in body:
                if not ln.strip():
                    continue
                if ln.strip().startswith("- "):
                    short = truncate_entry(ln, ov)
                    repl.append(short)
                else:
                    short = ln
                    repl.append(ln)
                p = detail_probe(ln, short)
                if p:
                    moved.append((sm.get("label", sm["heading"]), ref, ln, p))
            repl += [""] if repl[-1] != "" else []
        else:
            buf.append((lines[h] + "\n\n" + "\n".join(body)).rstrip())
            for ln in [lines[h]] + body:
                if ln.strip():
                    moved.append((sm.get("label", sm["heading"]), ref, ln,
                                  probe_of(ln)))
            repl = sm["keep_text"].rstrip("\n").split("\n")
        if repl and repl[-1] != "":
            repl.append("")   # 节后留空行，别把下一个 ## 顶上来
        keeps.append(sm.get("keep_intro", sm.get("keep_text", "")))
        lines[h:e] = repl

    # ② 逐条搬
    for mv in spec.get("moves", []):
        hits = [i for i, l in enumerate(lines)
                if l is not None and l.strip().startswith(mv["match"])]
        if len(hits) != 1:
            raise SystemExit(f"逐条定位失败（{len(hits)} 处）：{mv['match']}")
        i = hits[0]
        orig = lines[i]
        ref = mv["ref"]
        label = mv.get("label", "")
        title = orig.strip().lstrip("-| ").split("**")
        title = (title[1] if len(title) > 1 else title[0])[:40].strip()
        ref_buf.setdefault(ref, []).append(
            f"### {label} · {title}\n\n{orig.strip()}\n")
        probe = detail_probe(orig, mv["keep"]) or probe_of(orig)
        moved.append((label, ref, orig, probe))
        keeps.append(mv["keep"])
        # keep 为空串＝这条整体搬走，正文里不留占位（别留一堆空行）
        lines[i] = mv["keep"] if mv["keep"] != "" else None

    lines = [l for l in lines if l is not None]

    new_text = "\n".join(lines).rstrip("\n")
    if spec.get("append"):
        new_text += "\n\n" + spec["append"].rstrip("\n") + "\n"
    else:
        new_text += "\n"
    new_text = new_text.replace("#SIZE#", kb(len(new_text.encode("utf-8"))))

    # ③ 落 refs
    ref_texts = {}
    skill_name = os.path.basename(sdir.rstrip("/"))
    for rel, chunks in ref_buf.items():
        meta = spec.get("ref_meta", {}).get(rel, {})
        body = "\n\n".join(chunks).rstrip() + "\n"
        if meta.get("append"):
            # 并入既有 ref（一个主题一档，不重复存两遍）：原样保留再追加一节
            path = os.path.join(sdir, rel)
            old = open(path, encoding="utf-8").read().rstrip() if os.path.exists(path) else ""
            marker = meta.get("marker", "## 追加 · 从 SKILL.md 并入（2026-09-22 拆薄）")
            ref_texts[rel] = (old + "\n\n---\n\n" + marker + "\n\n" + body) if old \
                else body
        else:
            head = f"---\ntier: T2  # 随 {skill_name} 主 skill\n---\n\n"
            head += (meta.get("title", "# 拆档") + "\n\n")
            head += (meta.get("note", "") + "\n\n---\n\n").lstrip("\n")
            ref_texts[rel] = head + body

    # ④ 校验
    problems = []
    for label, ref, orig, probe in moved:
        if probe and probe in new_text:
            problems.append(f"[残留] {label} 的原文还在 SKILL.md：{probe[:20]}")
        if probe and probe not in ref_texts.get(ref, ""):
            problems.append(f"[丢失] {label} 的原文没进 {ref}：{probe[:20]}")
    for k in keeps:
        first = [l for l in k.split("\n") if l.strip()]
        if first and first[0].strip() not in new_text:
            problems.append(f"[keep 缺失] {first[0][:40]}")

    print(f"SKILL.md: {kb(before)} → {kb(len(new_text.encode('utf-8')))}"
          f"  ({len(raw.splitlines())} 行 → {len(new_text.splitlines())} 行)")
    moved_bytes = sum(len(o.encode('utf-8')) for _, _, o, _ in moved)
    print(f"搬出条目 {len(moved)} 条 / {kb(moved_bytes)}；"
          f"写入 refs {len(ref_texts)} 个 / "
          f"{kb(sum(len(v.encode('utf-8')) for v in ref_texts.values()))}")
    for rel, v in ref_texts.items():
        print(f"  + {rel}  {kb(len(v.encode('utf-8')))}")
    print("校验：" + ("全部通过（原文 0 残留 / 0 丢失，keep 全在）"
                     if not problems else f"{len(problems)} 处问题"))
    for p in problems:
        print("  ✗ " + p)

    if write and not problems:
        for rel, v in ref_texts.items():
            path = os.path.join(sdir, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            open(path, "w", encoding="utf-8").write(v)
        open(src, "w", encoding="utf-8").write(new_text)
        print(f"已落盘：{src} + {len(ref_texts)} 个 references")
    elif write:
        print("有校验问题，未落盘")
    else:
        print("dry-run（加 --write 落盘）")


if __name__ == "__main__":
    main()
