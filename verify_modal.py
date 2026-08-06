#!/usr/bin/env python3
"""验证弹层功能：点击卡片后检查 .modal.show 是否存在，并截图弹层局部。"""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 900, "height": 1800})
    page.goto("https://hhao9817.github.io/agent-daily/", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(1500)
    page.click(".item")
    page.wait_for_timeout(800)
    modal_visible = page.evaluate("document.querySelector('.modal.show') !== null")
    modal_count = page.evaluate("document.querySelectorAll('.modal').length")
    svg_in_modal = page.evaluate(""" 
        (() => { const m = document.querySelector('.modal.show'); 
                 return m ? m.querySelectorAll('svg').length : 0; })()
    """)
    sec_count = page.evaluate("""
        (() => { const m = document.querySelector('.modal.show'); 
                 return m ? m.querySelectorAll('.modal-sec').length : 0; })()
    """)
    h2 = page.evaluate("""
        (() => { const m = document.querySelector('.modal.show'); 
                 return m ? m.querySelector('h2').textContent : ''; })()
    """)
    print("弹层可见:", modal_visible)
    print("弹层总数:", modal_count)
    print("弹层内SVG示意图数:", svg_in_modal)
    print("弹层内详情区块数:", sec_count)
    print("弹层标题:", h2)
    # 截图弹层局部（非全页）
    page.screenshot(path="/Users/huanghao/agent-daily/modal_crop.png")
    b.close()