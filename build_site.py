#!/usr/bin/env python3
"""
从简报数据(JSON)渲染 GitHub Pages 网站。

用法:
    python3 build_site.py <data.json> [--out index.html] [--mode interactive|full]

mode:
    interactive = 列表页 + 点击详情弹层（默认，用于首页 index.html）
    full       = 完整展开所有详情（无需 JS，用于归档页面 archive/YYYY-MM-DD.html）

data.json 结构:
{
  "date": "2026-08-06",
  "banner": "今日速览：...",
  "items": [
    {"tag": "paper|github|product|blog", "title": "...", "date": "...",
     "source": "arXiv", "summary": "...", "insight": "...", "link": "...",
     "detail": {
        "why": "...", "mechanism": "...", "deep": "...", "apply": "...", "caveats": "...",
        "diagram": {"title": "...", "flow": [{"label":"...","sub":"...","type":"..."}], "notes": [...]}
     }}
  ]
}
"""
import json
import sys
import os
import html

from diagram_gen import gen_flow_svg

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


def build_detail_blocks(detail):
    """把 detail 渲染成详情区块 HTML（供弹层和完整页复用）。增补来源溯源区块。"""
    d_blocks = []
    if detail.get("diagram"):
        d_blocks.append(
            f'<div class="modal-sec"><h4>📊 架构示意</h4>'
            f'<div class="diagram-box">{gen_flow_svg(detail["diagram"])}</div></div>'
        )
    if detail.get("why"):
        d_blocks.append(f'<div class="modal-sec"><h4>🎯 为什么值得关注</h4><p>{esc(detail["why"])}</p></div>')
    if detail.get("mechanism"):
        d_blocks.append(f'<div class="modal-sec"><h4>⚙️ 核心机制</h4><p>{esc(detail["mechanism"])}</p></div>')
    if detail.get("deep"):
        d_blocks.append(f'<div class="modal-sec"><h4>🧠 深度解读</h4><p>{esc(detail["deep"])}</p></div>')
    if detail.get("business"):
        d_blocks.append(f'<div class="modal-sec modal-business"><h4>💼 商业启示</h4><p>{esc(detail["business"])}</p></div>')
    if detail.get("apply"):
        d_blocks.append(f'<div class="modal-sec"><h4>🛠️ 落地建议</h4><p>{esc(detail["apply"])}</p></div>')
    if detail.get("caveats"):
        d_blocks.append(f'<div class="modal-sec"><h4>⚠️ 局限与风险</h4><p>{esc(detail["caveats"])}</p></div>')
    # 来源溯源区块（grounded-citations 风格）
    srcs = detail.get("sources")
    if srcs:
        src_list = []
        for i, src in enumerate(srcs, 1):
            url = src.get("url", "")
            title = src.get("title", url)
            if url:
                src_list.append(f'<li><span class="src-id">[{i}]</span> '
                                f'<a href="{esc(url)}" target="_blank" rel="noopener" class="src-link">{esc(title)}</a></li>')
            else:
                src_list.append(f'<li><span class="src-id">[{i}]</span> {esc(title)}</li>')
        d_blocks.append(
            f'<div class="modal-sec modal-sources"><h4>🔗 来源溯源</h4>'
            f'<ol class="sources-list">{"".join(src_list)}</ol></div>'
        )
    return d_blocks


def render(data, mode="interactive"):
    """mode='interactive' → 列表页+JS弹层；mode='full' → 完整展开页（无需JS，适合归档）。"""
    with open(os.path.join(os.path.dirname(__file__), "template.html"), "r", encoding="utf-8") as f:
        tpl = f.read()

    date = esc(data.get("date", ""))
    banner = data.get("banner", "")
    if banner:
        b = f'<div class="banner"><h2>📌 今日速览</h2><p>{esc(banner)}</p></div>'
    else:
        b = ""

    items_html = []
    modals_html = []
    items = data.get("items", [])
    if not items:
        items_html.append('<div class="empty">今日暂无值得关注的更新。</div>')

    for idx, it in enumerate(items):
        tag = it.get("tag", "blog")
        tag_label = TAG_LABEL.get(tag, "📝")
        tag_class = TAG_CLASS.get(tag, "tag-blog")
        title = esc(it.get("title", "未命名"))
        link = it.get("link", "")
        title_html = f'<a href="{esc(link)}" target="_blank" rel="noopener">{title}</a>' if link else title

        meta_parts = []
        if it.get("date"):
            meta_parts.append(esc(it["date"]))
        if it.get("source"):
            meta_parts.append(esc(it["source"]))
        meta = " · ".join(meta_parts)
        summary = esc(it.get("summary", ""))
        insight = esc(it.get("insight", ""))

        if mode == "full":
            # ===== 完整展开模式（归档页）：直接渲染所有详情，无需 JS =====
            detail = it.get("detail", {})
            d_blocks = build_detail_blocks(detail)
            d_html = "\n".join(d_blocks) if d_blocks else ""
            source_link = (f'<div class="modal-foot"><a href="{esc(link)}" target="_blank" rel="noopener" '
                           f'class="modal-link">🔗 原文链接：{esc(link)}</a></div>' if link else "")
            items_html.append(
                f'<div class="item item-full">'
                f'<div class="item-top"><span class="tag {tag_class}">{tag_label}</span></div>'
                f'<h3>{title_html}</h3>'
                f'<div class="meta">{meta}</div>'
                f'<div class="summary">{summary}</div>'
                f'<div class="insight"><strong>🔍 技术视角：</strong>{insight}</div>'
                f'{d_html}{source_link}'
                f'</div>'
            )
            continue

        # ===== 列表卡片（interactive 模式） =====
        items_html.append(
            f'<div class="item" onclick="openDetail({idx})" role="button" tabindex="0" '
            f'onkeydown="if(event.key===\'Enter\'||event.key===\' \')openDetail({idx})">'
            f'<div class="item-top">'
            f'<span class="tag {tag_class}">{tag_label}</span>'
            f'<span class="detail-hint">点击查看详情 →</span>'
            f'</div>'
            f'<h3>{title_html}</h3>'
            f'<div class="meta">{meta}</div>'
            f'<div class="summary">{summary}</div>'
            f'<div class="insight"><strong>🔍 技术视角：</strong>{insight}</div>'
            f'</div>'
        )

        # ===== 详情弹层（interactive 模式） =====
        detail = it.get("detail", {})
        d_blocks = build_detail_blocks(detail)
        source_link = (f'<a href="{esc(link)}" target="_blank" rel="noopener" '
                       f'class="modal-link">🔗 原文链接：{esc(link)}</a>' if link else "")

        modals_html.append(
            f'<div class="modal" id="modal-{idx}" onclick="if(event.target===this)closeDetail({idx})">'
            f'<div class="modal-content">'
            f'<button class="modal-close" onclick="closeDetail({idx})" aria-label="关闭">×</button>'
            f'<span class="tag {tag_class}">{tag_label}</span>'
            f'<h2>{title}</h2>'
            f'<div class="meta">{meta}</div>'
            f'<div class="modal-body">' + "\n".join(d_blocks) + '</div>'
            f'<div class="modal-foot">{source_link}</div>'
            f'</div></div>'
        )

    items_block = "\n".join(items_html)
    modals_block = "\n".join(modals_html)

    page = (tpl
            .replace("{{DATE}}", date)
            .replace("{{BANNER}}", b)
            .replace("{{ITEMS}}", items_block)
            .replace("{{MODALS}}", modals_block))
    return page


def main():
    if len(sys.argv) < 2:
        print("用法: build_site.py <data.json> [--out index.html] [--mode interactive|full]", file=sys.stderr)
        sys.exit(2)
    with open(sys.argv[1], "r", encoding="utf-8") as f:
        data = json.load(f)
    mode = "interactive"
    out = "index.html"
    if "--mode" in sys.argv:
        mode = sys.argv[sys.argv.index("--mode") + 1]
    if "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
    page = render(data, mode=mode)
    with open(out, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"已生成 {out} ({len(page)} 字节, mode={mode})")


if __name__ == "__main__":
    main()