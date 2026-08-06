/**
 * agent-daily 智能对话后端 (Cloudflare Worker)
 *
 * 作用：作为前端与阿里百炼(DashScope)之间的安全代理。
 *  - 百炼 API key 只存在 Worker 的环境变量里，绝不下发到浏览器。
 *  - 前端只调用本 Worker 的 /api/chat。
 *  - 可选：把晨报 data.json 作为 RAG 上下文注入，让 AI 能回答"这期晨报有什么"。
 *
 * 部署（需要 Cloudflare 账号）：
 *   cd ai-chat
 *   npm i -g wrangler
 *   wrangler login
 *   wrangler secret put DASHSCOPE_API_KEY     # 粘贴你的百炼 key
 *   wrangler secret put DASHSCOPE_BASE_URL    # 可选，默认兼容模式
 *   wrangler deploy
 * 部署后把返回的 https://xxx.workers.dev 地址填到前端配置里。
 */

// 跨域白名单 — 只允许你的站点调用
const ALLOWED_ORIGINS = [
  "https://hhao9817.github.io",
  "http://localhost:8787",
  "http://localhost:8000",
  "null", // file:// 打开时 origin 为 null
];

const DEFAULT_BASE_URL =
  "https://dashscope.aliyuncs.com/compatible-mode/v1";

// 系统提示 —— 让 AI 知道自己是晨报助手，可结合 RAG 上下文
const SYSTEM_PROMPT = `你是「AI for Business 每日晨报」网站的智能助手。
你的任务：回答访客关于晨报内容、以及 AI for Business（业务知识库 / 业务语义理解 / 业务系统精确查询分析）领域的问题。
回答要求：
- 简洁、准确、专业，用中文（术语保留英文）。
- 如果访客问的是晨报里已有的条目，优先引用晨报内容的摘要。
- 如果问题超出晨报范围，用你的通用知识回答，但不要编造晨报里有而实际没有的内容。
- 如果引用了具体条目，说明其来源类型（论文/GitHub/业界动态/技术博客）。`;

export default {
  async fetch(request, env) {
    // 1. CORS 预检
    if (request.method === "OPTIONS") {
      return new Response(null, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Methods": "POST, OPTIONS",
          "Access-Control-Allow-Headers": "Content-Type",
          "Access-Control-Max-Age": "86400",
        },
      });
    }

    // 2. 只接受 POST /api/chat
    if (request.method !== "POST" || !new URL(request.url).pathname.startsWith("/api/chat")) {
      return json({ error: "Not found" }, 404);
    }

    // 3. 校验来源（可选，防止他人盗用你的 worker）
    const origin = request.headers.get("Origin") || "null";
    if (!ALLOWED_ORIGINS.includes(origin)) {
      return json({ error: "Origin not allowed" }, 403);
    }

    // 4. 读取 body
    let body;
    try {
      body = await request.json();
    } catch {
      return json({ error: "Invalid JSON body" }, 400);
    }
    const { messages = [], useBriefContext = true } = body;

    const apiKey = env.DASHSCOPE_API_KEY;
    if (!apiKey) {
      return json({ error: "Server not configured (missing DASHSCOPE_API_KEY)" }, 500);
    }
    const baseUrl = env.DASHSCOPE_BASE_URL || DEFAULT_BASE_URL;
    const model = env.MODEL || "deepseek-v4-flash-0731";

    // 5. 组装调用消息：系统提示 + (可选)RAG 上下文 + 用户/对话历史
    const fullMessages = [{ role: "system", content: SYSTEM_PROMPT }];

    if (useBriefContext) {
      try {
        const brief = await fetchBrief(env);
        if (brief) {
          fullMessages.push({
            role: "system",
            content:
              "以下是当前晨报的内容摘要（JSON），回答晨报相关问题时可参考：\n```json\n" +
              brief.slice(0, 8000) +
              "\n```",
          });
        }
      } catch (e) {
        // 上下文获取失败不阻塞对话
        console.error("brief fetch failed", e);
      }
    }

    // 限制历史长度，防止 token 爆炸
    const recent = Array.isArray(messages) ? messages.slice(-12) : [];
    fullMessages.push(...recent);

    // 6. 调用百炼
    const dashResp = await fetch(`${baseUrl}/chat/completions`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${apiKey}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        model,
        messages: fullMessages,
        max_tokens: 1200,
        temperature: 0.4,
      }),
    });

    const dashJson = await dashResp.json().catch(() => ({}));
    if (!dashResp.ok) {
      return json({ error: "Upstream error", detail: dashJson }, dashResp.status);
    }

    const content =
      dashJson?.choices?.[0]?.message?.content ||
      dashJson?.choices?.[0]?.message?.reasoning_content ||
      "（无回复）";

    return json({
      reply: content,
      model,
      usage: dashJson?.usage || null,
    });
  },
};

// 从 GitHub 拉取最新晨报 data.json 作为 RAG 上下文
async function fetchBrief(env) {
  const url =
    env.BRIEF_URL ||
    "https://raw.githubusercontent.com/hhao9817/agent-daily/main/data.json";
  const resp = await fetch(url, {
    headers: { "User-Agent": "agent-daily-worker" },
  });
  if (!resp.ok) return null;
  const text = await resp.text();
  // 简化：只保留 date + 每条 title/summary/insight，控制体积
  try {
    const d = JSON.parse(text);
    const item = (it) =>
      `- [${it.tag}] ${it.title} | ${it.summary || ""}`;
    const items = (d.items || []).map(item).join("\n");
    return JSON.stringify({ date: d.date, banner: d.banner, items });
  } catch {
    return text.slice(0, 8000);
  }
}

function json(obj, status = 200) {
  return new Response(JSON.stringify(obj), {
    status,
    headers: {
      "Content-Type": "application/json; charset=utf-8",
      "Access-Control-Allow-Origin": "*",
    },
  });
}