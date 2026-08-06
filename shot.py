#!/usr/bin/env python3
"""用 Playwright 无头浏览器截图 GitHub Pages 网站（列表页 + 点击详情弹层）。"""
from playwright.sync_api import sync_playwright
import sys

url = sys.argv[1] if len(sys.argv) > 1 else "https://hhao9817.github.io/agent-daily/"
out = sys.argv[2] if len(sys.argv) > 2 else "screenshot.png"
mode = sys.argv[3] if len(sys.argv) > 3 else "list"  # list | detail

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 900, "height": 1800}, device_scale_factor=2)
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(1500)
    if mode == "detail":
        # 点击第一个卡片打开详情弹层
        try:
            page.click(".item")
            page.wait_for_timeout(1200)
            # 滚动到弹层顶部
            page.evaluate("window.scrollTo(0,0)")
            page.wait_for_timeout(400)
        except Exception as e:
            print(f"警告: 点击卡片失败: {e}")
    page.screenshot(path=out, full_page=True)
    browser.close()
print(f"已保存: {out} (mode={mode})")