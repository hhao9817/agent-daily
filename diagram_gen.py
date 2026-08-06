#!/usr/bin/env python3
"""
示意图生成器：把结构化的 flow 数据渲染成深色主题 SVG 流程图（内嵌 HTML）。
用于详情弹层，实现"图文并茂"。

flow 结构:
{
  "title": "图标题",
  "flow": [
    {"label": "节点名", "sub": "子标签", "type": "frontend|backend|database|cloud|security|external"}
  ],
  "notes": [{"label": "要点名", "text": "要点说明"}]
}
"""
import html

COLORS = {
    "frontend": ("rgba(8, 51, 68, 0.4)", "#22d3ee"),
    "backend":  ("rgba(6, 78, 59, 0.4)", "#34d399"),
    "database": ("rgba(76, 29, 149, 0.4)", "#a78bfa"),
    "cloud":    ("rgba(120, 53, 15, 0.3)", "#fbbf24"),
    "security": ("rgba(136, 19, 55, 0.4)", "#fb7185"),
    "external": ("rgba(30, 41, 59, 0.5)", "#94a3b8"),
}

BOX_W, BOX_H = 150, 58
GAP = 46  # 箭头区域
PAD = 30
ROW_GAP = 70
WIDTH = 900


def esc(s):
    return html.escape(str(s), quote=False)


def gen_flow_svg(diagram):
    flow = diagram.get("flow", [])
    notes = diagram.get("notes", [])
    title = diagram.get("title", "")

    # 计算每行放几个（宽度约束）
    per_row = max(1, min(len(flow), (WIDTH - 2 * PAD) // (BOX_W + GAP)))
    rows = [flow[i:i + per_row] for i in range(0, len(flow), per_row)] or [[]]

    content_h = len(rows) * BOX_H + (len(rows) - 1) * ROW_GAP
    notes_h = 0
    if notes:
        notes_h = 30 + len(notes) * 46
    total_h = PAD + 30 + 20 + content_h + (40 if notes else 0) + notes_h + PAD

    parts = []
    parts.append(f'<svg viewBox="0 0 {WIDTH} {total_h}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block">')
    parts.append('<defs>')
    parts.append('<marker id="ah" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">'
                 '<polygon points="0 0, 10 3.5, 0 7" fill="#64748b"/></marker>')
    parts.append('<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">'
                 '<path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="0.5"/></pattern>')
    parts.append('</defs>')
    parts.append(f'<rect width="{WIDTH}" height="{total_h}" fill="url(#grid)"/>')

    # 标题
    if title:
        parts.append(f'<text x="{PAD}" y="{PAD + 18}" fill="#cbd5e1" font-size="14" font-weight="600" '
                     f'font-family="system-ui,sans-serif">{esc(title)}</text>')

    # 绘制节点与箭头
    abs_y = PAD + 50
    prev_right = None
    for ri, row in enumerate(rows):
        row_w = len(row) * BOX_W + (len(row) - 1) * GAP
        start_x = (WIDTH - row_w) / 2
        if ri > 0:
            abs_y += ROW_GAP
        for ci, node in enumerate(row):
            x = start_x + ci * (BOX_W + GAP)
            fill, stroke = COLORS.get(node.get("type", "external"), COLORS["external"])
            # 双矩形遮罩：先画不透明底
            parts.append(f'<rect x="{x}" y="{abs_y}" width="{BOX_W}" height="{BOX_H}" rx="8" fill="#0f172a"/>')
            parts.append(f'<rect x="{x}" y="{abs_y}" width="{BOX_W}" height="{BOX_H}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
            cx = x + BOX_W / 2
            label = node.get("label", "?")
            sub = node.get("sub", "")
            if sub:
                parts.append(f'<text x="{cx}" y="{abs_y + 26}" fill="#f1f5f9" font-size="12" font-weight="600" '
                             f'text-anchor="middle" font-family="system-ui,sans-serif">{esc(label)}</text>')
                parts.append(f'<text x="{cx}" y="{abs_y + 44}" fill="{stroke}" font-size="10" '
                             f'text-anchor="middle" font-family="system-ui,sans-serif">{esc(sub)}</text>')
            else:
                parts.append(f'<text x="{cx}" y="{abs_y + BOX_H / 2 + 4}" fill="#f1f5f9" font-size="12" font-weight="600" '
                             f'text-anchor="middle" font-family="system-ui,sans-serif">{esc(label)}</text>')
            # 箭头（同一行内）
            if ci > 0:
                ax1 = start_x + (ci - 1) * (BOX_W + GAP) + BOX_W
                ay = abs_y + BOX_H / 2
                parts.append(f'<line x1="{ax1}" y1="{ay}" x2="{ax1 + GAP - 4}" y2="{ay}" '
                             f'stroke="#64748b" stroke-width="1.5" marker-end="url(#ah)"/>')
        abs_y += BOX_H

    # 要点区
    if notes:
        ny = abs_y + 40
        parts.append(f'<text x="{PAD}" y="{ny}" fill="#fbbf24" font-size="12" font-weight="600" '
                     f'font-family="system-ui,sans-serif">▎关键要点</text>')
        ny += 26
        for n in notes:
            parts.append(f'<rect x="{PAD}" y="{ny - 16}" width="6" height="30" rx="2" fill="#fbbf24"/>')
            parts.append(f'<text x="{PAD + 16}" y="{ny + 2}" fill="#e2e8f0" font-size="11" '
                         f'font-family="system-ui,sans-serif">'
                         f'<tspan font-weight="600" fill="#fbbf24">{esc(n.get("label", ""))}</tspan>'
                         f'　{esc(n.get("text", ""))}</text>')
            ny += 42

    parts.append('</svg>')
    return "".join(parts)


if __name__ == "__main__":
    import sys, json
    d = {"title": "测试图", "flow": [
        {"label": "业务问题", "sub": "自然语言", "type": "frontend"},
        {"label": "Schema理解", "sub": "LLM", "type": "backend"},
        {"label": "精确查询", "sub": "SQL/API", "type": "database"},
    ], "notes": [{"label": "要点", "text": "schema 条件化是核心"}]}
    print(gen_flow_svg(d))