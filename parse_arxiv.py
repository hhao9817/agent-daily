#!/usr/bin/env python3
"""解析 arXiv API 的 XML 响应，打印标题/日期/链接。用法: python3 parse_arxiv.py <xml文件> [条数]"""
import sys, re

def parse(xml_path, limit=10):
    with open(xml_path, "r", encoding="utf-8") as f:
        xml = f.read()
    entries = re.findall(r"<entry>(.*?)</entry>", xml, re.S)
    print(f"共 {len(entries)} 条")
    for e in entries[:limit]:
        t = re.search(r"<title>(.*?)</title>", e, re.S)
        p = re.search(r"<published>(.*?)</published>", e, re.S)
        l = re.search(r"<id>(.*?)</id>", e, re.S)
        title = re.sub(r"\s+", " ", t.group(1).strip()) if t else "?"
        date = p.group(1)[:10] if p else "?"
        link = l.group(1) if l else "?"
        print(f"- [{date}] {title}")
        print(f"    {link}")

if __name__ == "__main__":
    parse(sys.argv[1], int(sys.argv[2]) if len(sys.argv) > 2 else 10)