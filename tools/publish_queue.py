# -*- coding: utf-8 -*-
"""按确认时间发布草稿。

规则（2026-11-03 定）：
- 当天 24:00 前确认 → 次日 09:00 发布；
- 次日及以后确认 → 以确认时刻为发布时间，立即发布。

草稿在 source/_drafts/ 里，frontmatter 带：
    approved: true
    publish_at: 2026-11-04 09:00:00

用法：
    python tools/publish_queue.py            # 只看不搬
    python tools/publish_queue.py --apply    # 到期的搬进 _posts
"""
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DRAFTS = ROOT / "source" / "_drafts"
POSTS = ROOT / "source" / "_posts"


def split_fm(text):
    m = re.match(r"(?s)^(---\s*\n)(.*?)(\n---\s*\n)", text)
    if not m:
        return None, None, text
    return m.group(1), m.group(2), text[m.end():]


def get(fm, key):
    m = re.search(rf"(?m)^{key}:\s*(.+?)\s*$", fm)
    return m.group(1).strip() if m else ""


def main(argv):
    apply = "--apply" in argv
    now = datetime.now()
    moved, waiting, broken = [], [], []

    for path in sorted(DRAFTS.glob("*.md")):
        text = path.read_text(encoding="utf-8")
        head, fm, body = split_fm(text)
        if fm is None:
            continue
        if get(fm, "approved").lower() != "true":
            continue

        raw_at = get(fm, "publish_at").strip('"\'')
        if not raw_at:
            broken.append((path, "approved: true 但没有 publish_at"))
            continue
        try:
            publish_at = datetime.strptime(raw_at, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            broken.append((path, f"publish_at 格式不对：{raw_at}"))
            continue

        if publish_at > now:
            waiting.append((path, publish_at))
            continue

        if not apply:
            moved.append((path, publish_at, "(不搬，只报告)"))
            continue

        # 改 date，删掉发布用的两个字段
        fm_lines = [ln for ln in fm.splitlines()
                    if not re.match(r"^\s*(approved|publish_at):", ln)]
        fm_lines = [re.sub(r"^date:.*$", f"date: {publish_at:%Y-%m-%d %H:%M:%S}", ln)
                    if ln.startswith("date:") else ln for ln in fm_lines]
        if not any(ln.startswith("date:") for ln in fm_lines):
            fm_lines.insert(0, f"date: {publish_at:%Y-%m-%d %H:%M:%S}")

        target = POSTS / f"{publish_at:%Y-%m-%d}-{path.name.split('-', 3)[-1]}"
        target.write_text(head + "\n".join(fm_lines) + "\n---\n" + body, encoding="utf-8")
        path.unlink()
        moved.append((path.name, publish_at, f"-> {target.name}"))

    print(f"到期发布：{len(moved)} 篇")
    for name, at, extra in moved:
        print(f"  [go] {name}  publish_at={at:%Y-%m-%d %H:%M}  {extra}")
    print(f"还没到时间：{len(waiting)} 篇")
    for path, at in waiting:
        print(f"  [..] {path.name}  publish_at={at:%Y-%m-%d %H:%M}")
    if broken:
        print(f"配置有问题：{len(broken)} 篇")
        for path, why in broken:
            print(f"  [!!] {path.name}  {why}")
    return 1 if broken else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main(sys.argv[1:]))
