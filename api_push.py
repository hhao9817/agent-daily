#!/usr/bin/env python3
"""通过 GitHub REST API 推送本地文件（在 github.com:443 不可达时替代 git push）。

用法: api_push.py [commit_message]
默认推送 index.html / data.json / archive/ 下所有变更文件。
"""
import base64
import json
import os
import subprocess
import sys

REPO_DIR = os.path.expanduser("~/agent-daily")
REPO = "hhao9817/agent-daily"
API = "https://api.github.com"


def token():
    out = subprocess.run(["gh", "auth", "token"], capture_output=True, text=True)
    return (out.stdout or "").strip()


def req(method, path, payload=None, tok=None):
    import urllib.request
    url = API + path
    data = json.dumps(payload).encode() if payload is not None else None
    r = urllib.request.Request(url, data=data, method=method)
    r.add_header("Authorization", f"Bearer {tok}")
    r.add_header("Accept", "application/vnd.github+json")
    if data:
        r.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(r, timeout=60) as resp:
        body = resp.read().decode()
    return json.loads(body) if body.strip() else {}


def collect():
    files = ["index.html", "data.json", "briefing_evolution.md",
             "publish_site.py", "build_site.py", "api_push.py"]
    aport = os.path.join(REPO_DIR, "archive")
    for name in sorted(os.listdir(aport)):
        if name.endswith((".html", ".json")):
            files.append(f"archive/{name}")
    return files


def git_sha(path):
    return subprocess.run(["git", "hash-object", path], cwd=REPO_DIR,
                          capture_output=True, text=True).stdout.strip()


def main():
    msg = sys.argv[1] if len(sys.argv) > 1 else "Update briefing"
    tok = token()
    head = req("GET", f"/repos/{REPO}/git/ref/heads/main", tok=tok)["object"]["sha"]
    base_tree = req("GET", f"/repos/{REPO}/git/commits/{head}", tok=tok)["tree"]["sha"]
    remote = {e["path"]: e["sha"] for e in
              req("GET", f"/repos/{REPO}/git/trees/{base_tree}?recursive=1", tok=tok)["tree"]
              if e["type"] == "blob"}

    tree = []
    for rel in collect():
        p = os.path.join(REPO_DIR, rel)
        if not os.path.isfile(p):
            continue
        sha = git_sha(rel)
        if remote.get(rel) == sha:
            continue
        content = base64.b64encode(open(p, "rb").read()).decode()
        blob = req("POST", f"/repos/{REPO}/git/blobs",
                   {"content": content, "encoding": "base64"}, tok=tok)
        tree.append({"path": rel, "mode": "100644", "type": "blob", "sha": blob["sha"]})
        print(f"  ↑ {rel}", flush=True)

    if not tree:
        print("ℹ️ 远端内容已一致，无需推送")
        return

    new_tree = req("POST", f"/repos/{REPO}/git/trees",
                   {"base_tree": base_tree, "tree": tree}, tok=tok)
    commit = req("POST", f"/repos/{REPO}/git/commits",
                 {"message": msg, "tree": new_tree["sha"], "parents": [head]}, tok=tok)
    req("PATCH", f"/repos/{REPO}/git/refs/heads/main",
        {"sha": commit["sha"], "force": True}, tok=tok)
    print(f"✅ API 推送完成 {commit['sha'][:7]} ({len(tree)} 个文件)")


if __name__ == "__main__":
    main()