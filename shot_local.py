#!/usr/bin/env python3
"""截图本地 index.html（验证结构化速览 UI，不依赖线上缓存）。"""
from playwright.sync_api import sync_playwright
import os

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 900, "height": 1600})
    # 用 file:// 加载本地文件
    path = os.path.abspath(os.path.expanduser("~/agent-daily/index.html"))
    page.goto(f"file://{path}", wait_until="domcontentloaded", timeout=15000)
    page.wait_for_timeout(1000)
    # 检查速览内部结构
    snap_groups = page.evaluate("document.querySelectorAll('.snap-group').length")
    snap_titles = page.evaluate("""() => Array.from(document.querySelectorAll('.snap-title')).map(e => e.textContent.trim())""")
    print("速览分组数:", snap_groups)
    print("分组标题:", snap_titles)
    page.screenshot(path="/Users/huanghao/agent-daily/snap_local.png", full_page=False)
    b.close()
print("已保存 snap_local.png")