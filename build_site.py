#!/usr/bin/env python3
"""
从简报数据(JSON)渲染 GitHub Pages 的 index.html。

用法:
    python3 build_site.py <data.json>  [--out index.html]

data.json 结构:
{
  "date": "2026-08-06",
  "banner": "今日速览：...",
  "items": [
    {"tag": "paper|github|product|blog", "title": "...", "date": "...",
     "source": "arXiv", "summary": "...", "insight": "...", "link": "..."}
  ]
}
"""
import json
import sys
import os
import html

TAG_LABEL = {
    "paper": "📄 论文",
    "github": "🐙 GitHub",
    "product": "🏢 业界动态",
    "blog": "📝 技术博客",
}
TAG_CLASS = {
    "paper": "tag-paper",
    "github": "tag-github",
    "product": "tag-product",
    "blog": "tag-blog",
}


def esc(s):
    return html.escape(str(s), quote=False)


def render(data):
    with open(os.path.join(os.path.dirname(__file__), "template.html"), "r", encoding="utf-8") as f:
        tpl = f.read()

    date = esc(data.get("date", ""))
    banner = data.get("banner", "")
    if banner:
        b = (f'<div class="banner"><h2>📌 今日速览</h2><p>{esc(banner)}</p></div>')
    else:
        b = ""

    items_html = []
    items = data.get("items", [])
    if not items:
        items_html.append('<div class="empty">今日暂无值得关注的更新。</div>')
    for it in items:
        tag = it.get("tag", "blog")
        tag_label = TAG_LABEL.get(tag, "📝")
        tag_class = TAG_CLASS.get(tag, "tag-blog")
        title = esc(it.get("title", "未命名"))
        link = it.get("link", "")
        if link:
            title_html = f'<a href="{esc(link)}" target="_blank" rel="noopener">{title}</a>'
        else:
            title_html = title
        meta_parts = []
        if it.get("date"):
            meta_parts.append(esc(it["date"]))
        if it.get("source"):
            meta_parts.append(esc(it["source"]))
        meta = " · ".join(meta_parts)
        summary = esc(it.get("summary", ""))
        insight = esc(it.get("insight", ""))
        items_html.append(
            f'<div class="item">'
            f'<span class="tag {tag_class}">{tag_label}</span>'
            f'<h3>{title_html}</h3>'
            f'<div class="meta">{meta}</div>'
            f'<div class="summary">{summary}</div>'
            + (f'<div class="insight"><strong>🔍 技术视角：</strong>{insight}</div>' if insight else "")
            + '</div>'
        )

    items_block = "\n".join(items_html)
    page = tpl.replace("{{DATE}}", date).replace("{{BANNER}}", b).replace("{{ITEMS}}", items_block)
    return page


def main():
    if len(sys.argv) < 2:
        print("用法: build_site.py <data.json> [--out index.html]", file=sys.stderr)
        sys.exit(2)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    page = render(data)
    out = "index.html"
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"已生成 {out} ({len(page)} 字节)")


if __name__ == "__main__":
    main()