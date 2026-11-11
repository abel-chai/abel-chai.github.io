# -*- coding: utf-8 -*-
"""从 arXiv 新投稿里筛「够格写进博客」的论文。

标准（2026-11-09 定）：
- 优先：已被顶会/顶刊接收（CoRL / RSS / ICRA / IROS 的正会、NeurIPS / ICML / ICLR / CVPR / ICCV / ECCV、TRO / IJRR / Science Robotics）
- 跳过：workshop-only、纯 benchmark 刷分

用法：
    python screen_paper.py            # 最近 150 条 cs.RO，列出命中顶会的
    python screen_paper.py --days 14  # 只看最近 14 天
"""
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

API = "http://export.arxiv.org/api/query"

TOP = {
    "CoRL": "CoRL", "Conference on Robot Learning": "CoRL",
    "RSS": "RSS", "Robotics: Science and Systems": "RSS",
    "ICRA": "ICRA", "IROS": "IROS",
    "NeurIPS": "NeurIPS", "NIPS": "NeurIPS",
    "ICML": "ICML", "ICLR": "ICLR",
    "CVPR": "CVPR", "ICCV": "ICCV", "ECCV": "ECCV",
    "T-RO": "T-RO", "Transactions on Robotics": "T-RO",
    "IJRR": "IJRR", "Science Robotics": "Science Robotics",
}

WORKSHOP = re.compile(r"workshop|workshop track", re.I)


def fetch(cat="cs.RO", n=150):
    url = (f"{API}?search_query=cat:{cat}&sortBy=submittedDate"
           f"&sortOrder=descending&max_results={n}")
    req = urllib.request.Request(url, headers={"User-Agent": "aria-blog-screener/1.0"})
    return urllib.request.urlopen(req, timeout=60).read()


def parse(xml_bytes):
    ns = {"a": "http://www.w3.org/2005/Atom", "arxiv": "http://arxiv.org/schemas/atom"}
    root = ET.fromstring(xml_bytes)
    out = []
    for e in root.findall("a:entry", ns):
        title = re.sub(r"\s+", " ", e.findtext("a:title", "", ns)).strip()
        link = e.findtext("a:id", "", ns).strip()
        published = e.findtext("a:published", "", ns)[:10]
        comment = (e.findtext("arxiv:comment", "", ns) or "").strip()
        summary = re.sub(r"\s+", " ", e.findtext("a:summary", "", ns)).strip()
        cats = [c.get("term") for c in e.findall("a:category", ns)]

        venue = ""
        for key, label in TOP.items():
            if re.search(rf"\b{re.escape(key)}\b", comment, re.I):
                venue = label
                break
        # 先判 workshop：很多稿子写「accepted to CoRL 2026 XXX workshop」，不能算正会
        if WORKSHOP.search(comment):
            kind = "workshop"
            venue = f"{venue} workshop" if venue else "workshop"
        else:
            kind = "顶会" if venue else "预印本"
        out.append({
            "title": title, "link": link, "date": published,
            "comment": comment, "kind": kind, "venue": venue,
            "summary": summary, "cats": cats,
        })
    return out


def main(argv):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

    days = 30
    if "--days" in argv:
        days = int(argv[argv.index("--days") + 1])
    cutoff = (datetime.now(timezone.utc) - timedelta(days=days)).strftime("%Y-%m-%d")

    entries = [e for e in parse(fetch()) if e["date"] >= cutoff]
    top = [e for e in entries if e["kind"] == "顶会"]
    ws = [e for e in entries if e["kind"] == "workshop"]
    pre = [e for e in entries if e["kind"] == "预印本"]

    print(f"最近 {days} 天 cs.RO 新稿 {len(entries)} 条：顶会 {len(top)}、workshop {len(ws)}、其他预印本 {len(pre)}")
    print("\n=== 已录用顶会（优先读这些）===")
    for e in top[:15]:
        print(f"[{e['venue']}] {e['date']}  {e['title']}")
        print(f"    {e['link']}")
    if not top:
        print("（这周没有已录用的，退而求其次：从预印本里挑强组的，并在文中标注“未录用”）")
        print("\n=== 预印本候选（前 8 条）===")
        for e in pre[:8]:
            print(f"{e['date']}  {e['title']}")
            print(f"    {e['link']}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
