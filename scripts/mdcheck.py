#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mdcheck · md 文件格式体检（skill references/ 通用）

把「格式乱」从人肉 grep 变成一键扫。检查项：
  1. 体积排行          — >12KB ⚠️ 拆分候选（writing-guide 22KB 教训）；>20KB 强烈建议拆
  2. 反斜杠n 字面量     — patch 塞了 \\n 没转真换行（writing-guide 十一节教训：整节挤一行）
  3. 重复标题           — 同层同文本出现多次（「## 十一」双标题教训）
  4. 编号连续性/重复     — 中文序数（一~二十）与阿拉伯编号（### 1.）重复/跳号
  5. 断链引用提示        — 反引号 .md 引用找不到目标（详细扫描/修复跑 fix_md_links.py）

用法:
  python3 mdcheck.py <目录>                 # 体检目录下所有 .md
  python3 mdcheck.py <目录> --grep '4000|5000'   # 追加自定义旧词残留检查
  python3 mdcheck.py <目录> --top 5          # 只看体积排行前 N
"""

import argparse
import os
import re
import sys
from collections import Counter, defaultdict

def is_placeholder(ref):
    # 模板/占位示例：含尖括号、glob 通配符、篇号占位 ##、或明确示例词
    if '<' in ref or '*' in ref or '?' in ref or '##' in ref:
        return True
    return any(m in ref for m in ('demo', '示例', '<id>'))

CN_NUM = {'一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '十': 10,
          '十一': 11, '十二': 12, '十三': 13, '十四': 14, '十五': 15, '十六': 16, '十七': 17, '十八': 18, '十九': 19, '二十': 20}


def cn2int(s: str):
    return CN_NUM.get(s)


def iter_md(root: str):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in ('.git', '.venv', 'venv', '__pycache__', 'cache', 'images')]
        for f in filenames:
            if f.endswith('.md'):
                yield os.path.join(dirpath, f)


def check_backslash_n(path):
    """字面反斜杠n：\\n 出现在正文（不是代码块/路径）"""
    hits = []
    for i, line in enumerate(open(path, encoding='utf-8'), 1):
        if '\\n' in line:
            hits.append(i)
    return hits


def check_dup_headings(path):
    """同层同文本标题重复"""
    dups = []
    seen = Counter()
    for line in open(path, encoding='utf-8'):
        m = re.match(r'^(#{1,6})\s+(.*)', line)
        if m:
            seen[(m.group(1), m.group(2).strip())] += 1
    for (level, text), c in seen.items():
        if c > 1:
            dups.append(f'"{text}" ×{c} ({level})')
    return dups


def check_numbering(path):
    """编号标题连续性与重复：## 中文序数 / ### 阿拉伯"""
    problems = []
    seq_cn, seq_ar = [], []
    for line in open(path, encoding='utf-8'):
        m = re.match(r'^##\s+([一二三四五六七八九十]+)[、.．]', line)
        if m:
            n = cn2int(m.group(1))
            if n:
                seq_cn.append(n)
            continue
        m = re.match(r'^#{2,4}\s+(\d+)[.、．](?!\d)', line)
        if m:
            seq_ar.append(int(m.group(1)))
    for label, seq in (('中文序数(##)', seq_cn), ('阿拉伯(### N.)', seq_ar)):
        if not seq:
            continue
        cnt = Counter(seq)
        for n, c in cnt.items():
            if c > 1:
                problems.append(f'{label} 重复编号 {n} ×{c}')
        for prev, cur in zip(sorted(seq), sorted(seq)[1:]):
            if cur - prev > 1:
                problems.append(f'{label} 跳号: {prev} → {cur}（中间缺 {prev+1}，若刻意留空请忽略）')
    return problems


def check_refs(path, ref_re, root):
    """反引号 .md 引用：目标相对当前文件不存在 → 提示（跨库/占位不算）"""
    hits = []
    for i, line in enumerate(open(path, encoding='utf-8'), 1):
        for m in ref_re.finditer(line):
            ref = m.group(1)
            if is_placeholder(ref):
                continue
            target = os.path.normpath(os.path.join(os.path.dirname(path), ref))
            if os.path.exists(target):
                continue
            # 相对仓库根存在 = 跨库/素材来源标注，不算断
            if os.path.exists(os.path.normpath(os.path.join(root, ref))):
                continue
            hits.append((i, ref))
    return hits


def main():
    ap = argparse.ArgumentParser(description='md 文件格式体检')
    ap.add_argument('dir')
    ap.add_argument('--grep', default='', help='自定义残留词检查，| 分隔')
    ap.add_argument('--top', type=int, default=0, help='只看体积排行前 N（0=全检）')
    ap.add_argument('--root', default='/opt/data', help='仓库根，识别跨库引用')
    args = ap.parse_args()

    scan_root = os.path.abspath(args.dir)
    repo_root = os.path.abspath(args.root)
    files = sorted(iter_md(scan_root))
    if not files:
        print('无 md 文件'); sys.exit(1)

    # 体积排行
    sizes = []
    for p in files:
        rel = os.path.relpath(p, scan_root)
        try:
            sz = os.path.getsize(p)
        except OSError:
            continue
        sizes.append((sz, rel))
    sizes.sort(reverse=True)
    print(f'═══ mdcheck · {scan_root}  ({len(files)} 个 md) ═══')
    print('\n📄 体积排行（>12KB ⚠️ 拆分候选，>20KB 强烈建议拆）:')
    big = False
    for sz, rel in sizes:
        flag = ''
        if sz > 20000:
            flag = ' 🔴 强烈建议拆'; big = True
        elif sz > 12000:
            flag = ' ⚠️ 考虑拆'; big = True
        print(f'  {sz:6d}B  {rel}{flag}')
    if args.top:
        return

    ref_re = re.compile(r'`([^`]*\.md)`')
    total_problems = 0

    for p in files:
        rel = os.path.relpath(p, scan_root)
        problems = []
        # 反斜杠n
        for ln in check_backslash_n(p):
            problems.append(f'    L{ln}: 含字面 \\\\n（patch 时 \\n 没转真换行）')
        # 重复标题
        for d in check_dup_headings(p):
            problems.append(f'    重复标题: {d}')
        # 编号
        for num in check_numbering(p):
            problems.append(f'    {num}')
        # 自定义残留词
        if args.grep:
            for i, line in enumerate(open(p, encoding='utf-8'), 1):
                if re.search(args.grep, line):
                    problems.append(f'    L{i}: 命中 --grep: {line.strip()[:60]}')
        # 断链
        for ln, ref in check_refs(p, ref_re, repo_root):
            problems.append(f'    L{ln}: 引用不存在: `{ref}`（详细扫描/修复: fix_md_links.py）')

        if problems:
            total_problems += len(problems)
            print(f'\n❌ {rel}')
            for pr in problems:
                print(pr)
        else:
            print(f'✅ {rel}')

    print(f'\n问题总数: {total_problems}' + ('（0 = 格式干净）' if total_problems == 0 else ''))


if __name__ == '__main__':
    main()
