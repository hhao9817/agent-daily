#!/usr/bin/env python3
"""截图详情弹层（浅色验证）。"""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 900, "height": 1800})
    page.goto("https://hhao9817.github.io/agent-daily/", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(1500)
    # 点击第一个卡片打开弹层
    page.click(".item")
    page.wait_for_timeout(1000)
    # 检查弹层背景色
    bg = page.evaluate("""() => {
        const m = document.querySelector('.modal-content');
        return m ? getComputedStyle(m).backgroundColor : 'none';
    }""")
    print("弹层背景色:", bg)
    # 截图弹层可视区域（非全页）
    page.screenshot(path="/Users/huanghao/agent-daily/light_modal.png")
    b.close()
print("已保存 light_modal.png")