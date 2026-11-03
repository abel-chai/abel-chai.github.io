# -*- coding: utf-8 -*-
"""按《Aria的博客创作准则》做机械自查。

用法：python check_draft.py <markdown 文件> [...]
只查能被规则判定的东西（模板词、结构、来源、篇幅、结尾），
至于「有没有真正的判断」，机器查不出来，得自己看。
"""
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

BANNED = [
    "随着科技的发展", "随着", "值得深思", "总而言之", "综上所述",
    "不可否认", "毋庸置疑", "首先", "其次", "最后，",
    "在这个时代", "让我们一起", "不得不说",
]

REQUIRED = ["title", "date", "permalink", "categories", "description"]


def parse(path: Path):
    text = path.read_text(encoding="utf-8-sig")
    m = re.match(r"(?s)^---\s*\n(.*?)\n---\s*\n", text)
    if not m:
        return None, text
    fm, cur = {}, None
    for line in m.group(1).splitlines():
        item = re.match(r"^\s+-\s+(.*)$", line)
        if item and cur:
            fm[cur] = (fm[cur] + " " + item.group(1).strip()).strip()
            continue
        kv = re.match(r"^([A-Za-z_][\w-]*):\s*(.*)$", line)
        if kv:
            cur = kv.group(1)
            fm[cur] = kv.group(2).strip()
    return fm, text[m.end():]


def check(path: Path):
    issues, notes = [], []
    fm, body = parse(path)
    if fm is None:
        return ["没有 frontmatter"], []

    for k in REQUIRED:
        if not fm.get(k):
            issues.append(f"frontmatter 缺 {k}")

    cats = fm.get("categories", "")
    if "论文笔记" in cats:
        if not re.search(r"https?://(arxiv\.org|export\.arxiv\.org|browse-export\.arxiv\.org|huggingface\.co/papers)", body):
            issues.append("论文笔记但正文没有 arXiv 链接（准则要求来源可核查）")

    plain = re.sub(r"!\[[^\]]*\]\([^)]*\)|\[[^\]]*\]\([^)]*\)", "", body)
    plain = re.sub(r"(?m)^#{1,6}\s.*$", "", plain)
    plain = re.sub(r"[`*>|_-]", "", plain)
    chars = len(re.sub(r"\s", "", plain))

    if chars < 600:
        notes.append(f"篇幅偏短（约 {chars} 字），确认是不是想写这么短")
    if chars > 3200:
        notes.append(f"篇幅偏长（约 {chars} 字）")

    hits = [w for w in BANNED if w in body]
    if hits:
        issues.append("模板词：" + "、".join(hits))

    h2 = len(re.findall(r"(?m)^## ", body))
    h3 = len(re.findall(r"(?m)^### ", body))
    if h2 + h3 > 4:
        issues.append(f"小标题 {h2 + h3} 个，容易写成报告体")
    elif h2 + h3 >= 3:
        notes.append(f"小标题 {h2 + h3} 个，注意别和上一篇撞结构")

    enum = len(re.findall(r"\*\*第[一二三四]，", body))
    if enum >= 2:
        issues.append("用了「第一/第二」式编号论证，准则不鼓励固定论证顺序")

    paras = [p.strip() for p in re.split(r"\n\s*\n", body) if p.strip()]
    if paras:
        last = paras[-1]
        if re.match(r"^(总之|综上|概括地说|总的来说)", last):
            issues.append("结尾是总结陈词，准则要求可以不升华")
        if last.count("！") >= 1 or body.count("！") >= 2:
            notes.append("感叹号偏多")
    return issues, notes


def main(paths):
    failed = 0
    for p in paths:
        path = Path(p)
        issues, notes = check(path)
        status = "通过" if not issues else "有问题"
        print(f"\n[{status}] {path.name}")
        for i in issues:
            print(f"  [x] {i}")
        for n in notes:
            print(f"  [-] {n}")
        failed += 1 if issues else 0
    return 1 if failed else 0


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python check_draft.py <md 文件> [...]")
        sys.exit(2)
    sys.exit(main(sys.argv[1:]))
