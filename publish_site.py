#!/usr/bin/env python3
"""
发布脚本：把最新简报 data.json 渲染成 index.html 并推送到 GitHub Pages，
同时归档为历史早报（archive/YYYY-MM-DD.html + archive/YYYY-MM-DD.json），
并更新归档索引 archive/index.html。

用法:
    publish_site.py <data.json>

前提:
    - /Users/huanghao/agent-daily 仓库已克隆并配置好 git 凭据
    - gh 已认证（用于提供 token），REST API 可用
"""
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime

REPO_DIR = os.path.expanduser("~/agent-daily")
BUILD = os.path.join(REPO_DIR, "build_site.py")
GH = os.path.expanduser("~/.local/bin/gh")
ARCHIVE_DIR = os.path.join(REPO_DIR, "archive")
ARCHIVE_TPL = os.path.join(REPO_DIR, "archive_template.html")


def run(cmd, cwd=None, timeout=120):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout, cwd=cwd)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return -1, str(e)


def build_index(data_file):
    """渲染首页 index.html（interactive 模式）。"""
    return run(f'{sys.executable} "{BUILD}" "{data_file}" --out {os.path.join(REPO_DIR, "index.html")} --mode interactive')


def preserve_old_version(date):
    """覆盖前保留旧版：把 archive/{date}.json 改名为 {date}-{HHMMSS}.json。
    旧版 html 由 archive() 对改名后的 json 重新生成。
    时间戳冲突时追加序号，保证同日多版本不互相覆盖。"""
    base_json = os.path.join(ARCHIVE_DIR, f"{date}.json")
    if not os.path.exists(base_json):
        return False
    ts = datetime.now().strftime("%H%M%S")
    new_json = os.path.join(ARCHIVE_DIR, f"{date}-{ts}.json")
    # 时间戳冲突（同秒多次发布）：追加 -N 序号
    n = 1
    while os.path.exists(new_json):
        new_json = os.path.join(ARCHIVE_DIR, f"{date}-{ts}-{n}.json")
        n += 1
    os.replace(base_json, new_json)
    print(f"📦 保留旧版: {os.path.basename(new_json)}")
    return True


def archive(data):
    """归档本期：生成 archive/YYYY-MM-DD.html（full 模式）+ 复制 data.json + 重建 archive/index.html。"""
    date = data.get("date") or datetime.now().strftime("%Y-%m-%d")
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    # 1. 完整展开页
    html_path = os.path.join(ARCHIVE_DIR, f"{date}.html")
    data_path = os.path.join(ARCHIVE_DIR, f"{date}.json")
    rc, out = run(f'{sys.executable} "{BUILD}" "{data_path}" --out "{html_path}" --mode full')
    if rc != 0:
        print(f"⚠️ 归档页渲染失败: {out}")
        return False

    # 2. 归档索引
    archive_index(date)
    return True


def archive_index(current_date):
    """重建 archive/index.html，列出所有历史期（含同日多版本，按名称倒序）。"""
    if not os.path.exists(ARCHIVE_DIR):
        os.makedirs(ARCHIVE_DIR)
    with open(ARCHIVE_TPL, "r", encoding="utf-8") as f:
        tpl = f.read()

    items = []
    for fn in sorted(os.listdir(ARCHIVE_DIR), reverse=True):
        # 匹配 YYYY-MM-DD.json 或 YYYY-MM-DD-HHMMSS.json 或 YYYY-MM-DD-HHMMSS-N.json
        m = re.match(r"^(\d{4}-\d{2}-\d{2})(?:-(\d{6})(?:-\d+)?)?\.json$", fn)
        if not m:
            continue
        d = m.group(1)
        ver = m.group(2)
        # 读取该期的速览/条数作为元信息
        try:
            with open(os.path.join(ARCHIVE_DIR, fn), "r", encoding="utf-8") as f:
                jd = json.load(f)
            count = len(jd.get("items", []))
            summary = jd.get("banner", "")[:60]
        except Exception:
            count = 0
            summary = ""
        meta = f"{count} 条资讯" + (f" · {summary}…" if summary else "")
        # 页面文件名：带版本号的用完整名，最新版用日期
        page_name = f"{d}-{ver}" if ver else d
        label = f"{d} 晨报" + (f" (第{ver}版)" if ver else "")
        items.append(f'<div class="arch-item">'
                     f'<a href="{page_name}.html">{label}</a>'
                     f'<span class="meta">{meta}</span>'
                     f'</div>')

    if not items:
        items_html = '<div class="empty">暂无历史归档。</div>'
    else:
        items_html = "\n".join(items)

    page = tpl.replace("{{ARCHIVE_ITEMS}}", items_html)
    with open(os.path.join(ARCHIVE_DIR, "index.html"), "w", encoding="utf-8") as f:
        f.write(page)
    print(f"📚 归档索引已更新 ({len(items)} 期)")


def main():
    if len(sys.argv) < 2:
        print("用法: publish_site.py <data.json>", file=sys.stderr)
        sys.exit(2)
    data_file = os.path.abspath(sys.argv[1])
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    date = data.get("date") or datetime.now().strftime("%Y-%m-%d")
    os.makedirs(ARCHIVE_DIR, exist_ok=True)

    # 0. 覆盖前保留旧版（若存在），并为其生成独立 html
    if preserve_old_version(date):
        old_json = [f for f in os.listdir(ARCHIVE_DIR)
                    if re.match(rf"^{re.escape(date)}-\d{{6}}\.json$", f)]
        if old_json:
            old_path = os.path.join(ARCHIVE_DIR, sorted(old_json)[-1])
            old_html = old_path.replace(".json", ".html")
            run(f'{sys.executable} "{BUILD}" "{old_path}" --out "{old_html}" --mode full')
            print(f"📄 旧版页面已生成: {os.path.basename(old_html)}")

    # 1. 把本期 data.json 复制到 archive/
    arch_json = os.path.join(ARCHIVE_DIR, f"{date}.json")
    with open(arch_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # 2. 渲染首页 index.html
    rc, out = build_index(data_file)
    if rc != 0:
        print(f"❌ 首页渲染失败: {out}", file=sys.stderr)
        sys.exit(1)

    # 3. 归档本期 + 重建索引
    archive(data)

    # 4. 提交并推送
    os.chdir(REPO_DIR)
    rc, out = run("git add index.html data.json archive/")
    rc, out = run(f'git commit -m "Update briefing {date}"')
    if "nothing to commit" in out:
        print("ℹ️ 无内容变更，跳过推送")
        return 0

    # 推送（带重试，处理瞬时 SSL 错误）
    for i in range(3):
        rc, out = run("git push origin main")
        if rc == 0:
            print("✅ 已推送 GitHub Pages")
            break
        print(f"⚠️ 推送失败(第{i+1}次): {out.strip()}")
        time.sleep(3)
    else:
        print("❌ 推送失败", file=sys.stderr)
        sys.exit(1)

    print(f"🌐 最新: https://hhao9817.github.io/agent-daily/")
    print(f"📚 历史: https://hhao9817.github.io/agent-daily/archive/")
    return 0


if __name__ == "__main__":
    sys.exit(main())