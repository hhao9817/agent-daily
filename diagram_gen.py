#!/usr/bin/env python3
"""
示意图生成器：把结构化的 flow 数据渲染成浅色主题 SVG 流程图（内嵌 HTML）。
用于详情弹层，实现"图文并茂"，与浅色页面风格统一。

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

# 浅色主题配色：浅色填充 + 深色描边 + 深色文字
COLORS = {
    "frontend": ("#e0f2fe", "#0284c7"),   # 浅蓝 / 深蓝
    "backend":  ("#d1fae5", "#059669"),   # 浅绿 / 深绿
    "database": ("#ede9fe", "#7c3aed"),   # 浅紫 / 深紫
    "cloud":    ("#fef3c7", "#d97706"),   # 浅琥珀 / 深琥珀
    "security": ("#fee2e2", "#dc2626"),   # 浅红 / 深红
    "external": ("#f1f5f9", "#64748b"),   # 浅灰 / 深灰
}

BOX_W, BOX_H = 150, 58
GAP = 46  # 箭头区域
PAD = 30
ROW_GAP = 70
WIDTH = 900

# 文字颜色（浅色背景用深色文字）
TEXT_MAIN = "#1e293b"
TEXT_TITLE = "#334155"
TEXT_NOTE = "#334155"
ACCENT_NOTE = "#b45309"
GRID_LINE = "#e2e8f0"
ARROW = "#94a3b8"


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
    parts.append(f'<marker id="ah" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">'
                 f'<polygon points="0 0, 10 3.5, 0 7" fill="{ARROW}"/></marker>')
    parts.append(f'<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">'
                 f'<path d="M 40 0 L 0 0 0 40" fill="none" stroke="{GRID_LINE}" stroke-width="0.5"/></pattern>')
    parts.append('</defs>')
    # 浅色背景
    parts.append(f'<rect width="{WIDTH}" height="{total_h}" fill="#f8fafc"/>')
    parts.append(f'<rect width="{WIDTH}" height="{total_h}" fill="url(#grid)"/>')

    # 标题（深色文字）
    if title:
        parts.append(f'<text x="{PAD}" y="{PAD + 18}" fill="{TEXT_TITLE}" font-size="14" font-weight="600" '
                     f'font-family="system-ui,sans-serif">{esc(title)}</text>')

    # 绘制节点与箭头
    abs_y = PAD + 50
    for ri, row in enumerate(rows):
        row_w = len(row) * BOX_W + (len(row) - 1) * GAP
        start_x = (WIDTH - row_w) / 2
        if ri > 0:
            abs_y += ROW_GAP
        for ci, node in enumerate(row):
            x = start_x + ci * (BOX_W + GAP)
            fill, stroke = COLORS.get(node.get("type", "external"), COLORS["external"])
            # 浅色节点：浅填充 + 深色描边
            parts.append(f'<rect x="{x}" y="{abs_y}" width="{BOX_W}" height="{BOX_H}" rx="8" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>')
            cx = x + BOX_W / 2
            label = node.get("label", "?")
            sub = node.get("sub", "")
            if sub:
                parts.append(f'<text x="{cx}" y="{abs_y + 26}" fill="{TEXT_MAIN}" font-size="12" font-weight="600" '
                             f'text-anchor="middle" font-family="system-ui,sans-serif">{esc(label)}</text>')
                parts.append(f'<text x="{cx}" y="{abs_y + 44}" fill="{stroke}" font-size="10" '
                             f'text-anchor="middle" font-family="system-ui,sans-serif">{esc(sub)}</text>')
            else:
                parts.append(f'<text x="{cx}" y="{abs_y + BOX_H / 2 + 4}" fill="{TEXT_MAIN}" font-size="12" font-weight="600" '
                             f'text-anchor="middle" font-family="system-ui,sans-serif">{esc(label)}</text>')
            # 箭头（同一行内）
            if ci > 0:
                ax1 = start_x + (ci - 1) * (BOX_W + GAP) + BOX_W
                ay = abs_y + BOX_H / 2
                parts.append(f'<line x1="{ax1}" y1="{ay}" x2="{ax1 + GAP - 4}" y2="{ay}" '
                             f'stroke="{ARROW}" stroke-width="1.5" marker-end="url(#ah)"/>')
        abs_y += BOX_H

    # 要点区（深色文字）
    if notes:
        ny = abs_y + 40
        parts.append(f'<text x="{PAD}" y="{ny}" fill="{ACCENT_NOTE}" font-size="12" font-weight="600" '
                     f'font-family="system-ui,sans-serif">▎关键要点</text>')
        ny += 26
        for n in notes:
            parts.append(f'<rect x="{PAD}" y="{ny - 16}" width="6" height="30" rx="2" fill="{ACCENT_NOTE}"/>')
            parts.append(f'<text x="{PAD + 16}" y="{ny + 2}" fill="{TEXT_NOTE}" font-size="11" '
                         f'font-family="system-ui,sans-serif">'
                         f'<tspan font-weight="600" fill="{ACCENT_NOTE}">{esc(n.get("label", ""))}</tspan>'
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