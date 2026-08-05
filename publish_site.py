#!/usr/bin/env python3
"""
发布脚本：把最新简报 data.json 渲染成 index.html 并推送到 GitHub Pages。

用法:
    publish_site.py <data.json>

前提:
    - /Users/huanghao/agent-daily 仓库已克隆并配置好 git 凭据
    - gh 已认证（用于提供 token），REST API 可用
"""
import json
import os
import subprocess
import sys
import time
from datetime import datetime

REPO_DIR = os.path.expanduser("~/agent-daily")
BUILD = os.path.join(REPO_DIR, "build_site.py")
GH = os.path.expanduser("~/.local/bin/gh")


def run(cmd, cwd=None, timeout=120):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout, cwd=cwd)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return -1, str(e)


def main():
    if len(sys.argv) < 2:
        print("用法: publish_site.py <data.json>", file=sys.stderr)
        sys.exit(2)
    data_file = os.path.abspath(sys.argv[1])
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    # 1. 渲染 index.html
    rc, out = run(f'{sys.executable} "{BUILD}" "{data_file}" --out {os.path.join(REPO_DIR, "index.html")}')
    if rc != 0:
        print(f"❌ 渲染失败: {out}", file=sys.stderr)
        sys.exit(1)

    # 2. 提交并推送
    os.chdir(REPO_DIR)
    rc, out = run("git add index.html data.json")
    rc, out = run(f'git commit -m "Update briefing {data.get("date", datetime.now().strftime("%Y-%m-%d"))}"')
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

    # 3. 返回 Pages 网址
    print(f"🌐 https://hhao9817.github.io/agent-daily/")
    return 0


if __name__ == "__main__":
    sys.exit(main())