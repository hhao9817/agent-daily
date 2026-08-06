# 智能对话功能（AI Chat）

给晨报网站加一个**真实 AI 智能对话**功能：访客点击左下角 💬 按钮，可以向 AI 提问（不仅能问晨报内容，还能问 AI for Business 领域问题）。

## 架构

```
浏览器 (GitHub Pages 静态站)
   │  点击 💬 打开聊天面板
   │  POST /api/chat  {messages, useBriefContext}
   ▼
Cloudflare Worker (ai-chat/worker.js)   ← 真正的"后端"
   │  校验来源 → 拉取 data.json 做 RAG 上下文 → 调用百炼
   ▼
阿里百炼 DashScope (deepseek-v4-flash-0731)
```

**为什么需要 Cloudflare Worker？**
GitHub Pages 是纯静态站，不能放 API key。Worker 是无服务器函数，把百炼 key 存在**服务端环境变量**里，浏览器永远看不到 key，安全。

## 文件
| 文件 | 作用 |
|---|---|
| `worker.js` | Cloudflare Worker 后端（代理百炼 + RAG 上下文） |
| `wrangler.toml` | Worker 配置 |
| `chat-widget.js` | 前端聊天窗口组件（注入到 template.html） |

## 启用步骤（需要你有 Cloudflare 账号）

### 1. 部署 Worker（一次性）
```bash
cd ai-chat
npm i -g wrangler
wrangler login                      # 浏览器登录 Cloudflare
wrangler secret put DASHSCOPE_API_KEY   # 粘贴你的百炼 API key（安全，不落库）
wrangler deploy
```
部署成功后会返回一个地址，例如 `https://agent-daily-chat.xxxx.workers.dev`。

### 2. 前端接入
打开 `ai-chat/chat-widget.js`，把：
```js
WORKER_URL: "REPLACE_WITH_YOUR_WORKER_URL"
```
改成你的 Worker 地址，例如：
```js
WORKER_URL: "https://agent-daily-chat.xxxx.workers.dev"
```

### 3. 注入到页面
在 `template.html` 的 `</body>` 前加一行：
```html
<script src="chat-widget.js"></script>
```
（实际部署时把 `chat-widget.js` 放到站点可访问路径，或直接内联。）

重新跑 `build_site.py` 生成页面，推送到 GitHub Pages 即可。

## 可选配置
在 `chat-widget.js` 的 `AI_CHAT_CONFIG` 里：
- `USE_BRIEF_CONTEXT`: 是否把当前晨报 data.json 作为上下文注入（默认 true，让 AI 能答晨报内容）
- `QUICK_QUESTIONS`: 预设快捷问题
- `GREETING`: 欢迎语

在 `wrangler.toml` / Worker 环境变量里：
- `MODEL`: 用的模型（默认 deepseek-v4-flash-0731）
- `BRIEF_URL`: 晨报 data.json 地址

## 安全说明
- 百炼 key 只存在 Worker 环境变量，不下发浏览器 ✓
- Worker 校验了来源 Origin，防止他人盗用 ✓
- 前端只 POST 到你的 Worker，不直接碰百炼 ✓