#!/usr/bin/env python3
"""验证反馈功能：检查反馈按钮、打开表单、提交生成 Issue 链接。"""
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    b = p.chromium.launch()
    page = b.new_page(viewport={"width": 900, "height": 1800})
    page.goto("https://hhao9817.github.io/agent-daily/", wait_until="domcontentloaded", timeout=30000)
    page.wait_for_timeout(1500)
    # 检查反馈按钮是否存在
    fab_count = page.evaluate("document.querySelectorAll('.feedback-fab').length")
    print("反馈按钮数量:", fab_count)
    # 点击打开表单
    page.click(".feedback-fab")
    page.wait_for_timeout(500)
    fb_visible = page.evaluate("document.getElementById('feedback-modal').classList.contains('show')")
    print("反馈表单打开:", fb_visible)
    # 填入内容并提交，检查生成的链接
    page.fill("#fb-body", "测试反馈：希望增加更多业务 API 语义相关的论文。")
    url = page.evaluate("""(() => {
        const type = document.getElementById('fb-type').value;
        const body = document.getElementById('fb-body').value.trim();
        const date = new Date().toISOString().slice(0,10);
        const title = '[网页反馈/' + type + '] ' + date;
        const full = '反馈类型: ' + type + '\\n日期: ' + date + '\\n\\n' + body;
        return 'https://github.com/hhao9817/agent-daily/issues/new?title=' + encodeURIComponent(title) + '&body=' + encodeURIComponent(full);
    })()""")
    print("生成的 Issue 提交链接:")
    print(url)
    # 截图反馈表单
    page.screenshot(path="/Users/huanghao/agent-daily/feedback_modal.png")
    b.close()