/* ============================================================
 * agent-daily 智能对话前端组件
 * 用法：把下面这段 <script> 和 <link>/<style> 放进 template.html。
 * 启用前必须先部署好 ai-chat/worker.js（Cloudflare Worker），
 * 然后把 WORKER_URL 改成你的 worker 地址。
 * ============================================================ */

const AI_CHAT_CONFIG = {
  // 后端 Worker 地址 — 部署后改成你的，例如 https://agent-daily-chat.xxx.workers.dev
  WORKER_URL: "REPLACE_WITH_YOUR_WORKER_URL",
  // 是否把当前晨报 data.json 作为上下文注入（让 AI 能答晨报内容）
  USE_BRIEF_CONTEXT: true,
  // 欢迎语
  GREETING: "👋 你好！我是晨报智能助手，可以回答你关于本日晨报内容、以及 AI for Business（业务知识库 / 业务语义理解 / 业务系统精确查询分析）领域的问题。有什么想问的？",
  // 预设快捷问题
  QUICK_QUESTIONS: [
    "这期有哪些 text-to-SQL 相关的条目？",
    "总结一下今天最有价值的 3 条",
    "语义层和知识图谱怎么选？",
    "什么是 AI for Business？",
  ],
};

(function () {
  // 未配置则不初始化（避免报错）
  if (!AI_CHAT_CONFIG.WORKER_URL || AI_CHAT_CONFIG.WORKER_URL.startsWith("REPLACE")) return;

  // 注入样式
  var style = document.createElement("style");
  style.textContent = chatCSS();
  document.head.appendChild(style);

  // 注入 DOM
  var root = document.createElement("div");
  root.innerHTML = chatHTML();
  document.body.appendChild(root);

  var chatBtn = document.getElementById("ai-chat-fab");
  var panel = document.getElementById("ai-chat-panel");
  var messages = document.getElementById("ai-chat-messages");
  var input = document.getElementById("ai-chat-input");
  var sendBtn = document.getElementById("ai-chat-send");
  var open = false;

  chatBtn.addEventListener("click", function () {
    open = !open;
    panel.classList.toggle("show", open);
    chatBtn.classList.toggle("active", open);
    if (open && messages.children.length <= 1) {
      addMsg("assistant", AI_CHAT_CONFIG.GREETING);
      renderQuick();
    }
    if (open) input.focus();
  });

  function send() {
    var text = input.value.trim();
    if (!text) return;
    addMsg("user", text);
    input.value = "";
    addTyping();
    callAI(text);
  }

  sendBtn.addEventListener("click", send);
  input.addEventListener("keydown", function (e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      send();
    }
  });

  function renderQuick() {
    var box = document.querySelector("#ai-chat-quick");
    if (!box) return;
    AI_CHAT_CONFIG.QUICK_QUESTIONS.forEach(function (q) {
      var b = document.createElement("button");
      b.className = "ai-chat-quick-btn";
      b.textContent = q;
      b.addEventListener("click", function () {
        addMsg("user", q);
        addTyping();
        callAI(q);
      });
      box.appendChild(b);
    });
  }

  function addMsg(role, text) {
    var typing = document.querySelector(".ai-chat-typing");
    if (typing) typing.remove();
    var wrap = document.createElement("div");
    wrap.className = "ai-chat-msg " + role;
    var bubble = document.createElement("div");
    bubble.className = "ai-chat-bubble";
    bubble.textContent = text;
    wrap.appendChild(bubble);
    messages.appendChild(wrap);
    messages.scrollTop = messages.scrollHeight;
  }

  function addTyping() {
    var wrap = document.createElement("div");
    wrap.className = "ai-chat-msg assistant ai-chat-typing";
    var bubble = document.createElement("div");
    bubble.className = "ai-chat-bubble";
    bubble.textContent = "思考中…";
    wrap.appendChild(bubble);
    messages.appendChild(wrap);
    messages.scrollTop = messages.scrollHeight;
  }

  async function callAI(userText) {
    try {
      var resp = await fetch(AI_CHAT_CONFIG.WORKER_URL + "/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          messages: [{ role: "user", content: userText }],
          useBriefContext: AI_CHAT_CONFIG.USE_BRIEF_CONTEXT,
        }),
      });
      var data = await resp.json();
      if (!resp.ok) throw new Error(data.error || "请求失败");
      addMsg("assistant", data.reply || "（无回复）");
    } catch (err) {
      addMsg("assistant", "⚠️ 出错了：" + err.message + "\n\n（请确认 Worker 已部署并配置 WORKER_URL）");
    }
  }

  function chatHTML() {
    return `
      <button id="ai-chat-fab" title="晨报智能助手">💬<span class="ai-chat-fab-dot"></span></button>
      <div id="ai-chat-panel">
        <div class="ai-chat-head">
          <div class="ai-chat-head-title">🤖 晨报智能助手</div>
          <button id="ai-chat-close" title="关闭">×</button>
        </div>
        <div id="ai-chat-messages"></div>
        <div id="ai-chat-quick" class="ai-chat-quick"></div>
        <div class="ai-chat-input-row">
          <textarea id="ai-chat-input" rows="1" placeholder="输入你的问题… (Enter 发送)"></textarea>
          <button id="ai-chat-send">➤</button>
        </div>
        <div class="ai-chat-foot">由 Hermes Agent 驱动 · 内容仅供参考</div>
      </div>
    `;
  }

  function chatCSS() {
    return `
      #ai-chat-fab {
        position: fixed; bottom: 24px; left: 24px; width: 56px; height: 56px; border-radius: 50%;
        background: linear-gradient(135deg, #2563eb, #059669); border: none; color: #fff;
        font-size: 24px; cursor: pointer; box-shadow: 0 6px 20px rgba(37,99,235,.4);
        z-index: 9500; transition: transform .15s;
      }
      #ai-chat-fab:hover { transform: scale(1.1); }
      #ai-chat-panel {
        position: fixed; bottom: 92px; left: 24px; width: 360px; max-width: calc(100vw - 40px);
        height: 520px; max-height: calc(100vh - 120px);
        background: #fff; border: 1px solid #d6dde8; border-radius: 16px;
        box-shadow: 0 20px 60px rgba(15,23,42,.2); z-index: 9500;
        display: none; flex-direction: column; overflow: hidden;
      }
      #ai-chat-panel.show { display: flex; }
      .ai-chat-head {
        display: flex; justify-content: space-between; align-items: center;
        padding: 12px 16px; background: linear-gradient(135deg, #2563eb, #059669); color: #fff;
      }
      .ai-chat-head-title { font-weight: 600; }
      #ai-chat-close { background: none; border: none; color: #fff; font-size: 22px; cursor: pointer; line-height: 1; }
      #ai-chat-messages { flex: 1; overflow-y: auto; padding: 14px; display: flex; flex-direction: column; gap: 10px; }
      .ai-chat-msg { display: flex; }
      .ai-chat-msg.user { justify-content: flex-end; }
      .ai-chat-bubble {
        max-width: 82%; padding: 9px 13px; border-radius: 12px; font-size: .9em; line-height: 1.55;
        white-space: pre-wrap; word-break: break-word;
      }
      .ai-chat-msg.assistant .ai-chat-bubble { background: #f1f5f9; color: #111827; border-top-left-radius: 4px; }
      .ai-chat-msg.user .ai-chat-bubble { background: #2563eb; color: #fff; border-top-right-radius: 4px; }
      .ai-chat-quick { padding: 0 14px 6px; display: flex; flex-wrap: wrap; gap: 6px; }
      .ai-chat-quick-btn {
        background: #dbeafe; color: #2563eb; border: 1px solid #bfdbfe; border-radius: 20px;
        padding: 4px 11px; font-size: .78em; cursor: pointer; transition: all .15s;
      }
      .ai-chat-quick-btn:hover { background: #2563eb; color: #fff; }
      .ai-chat-input-row { display: flex; gap: 8px; padding: 10px 12px; border-top: 1px solid #e5e7eb; }
      #ai-chat-input {
        flex: 1; border: 1px solid #d6dde8; border-radius: 10px; padding: 9px 12px;
        font-size: .9em; resize: none; outline: none; font-family: inherit; line-height: 1.4;
      }
      #ai-chat-input:focus { border-color: #2563eb; }
      #ai-chat-send {
        width: 40px; height: 40px; border: none; border-radius: 10px; background: #2563eb; color: #fff;
        font-size: 16px; cursor: pointer; flex-shrink: 0;
      }
      #ai-chat-send:hover { opacity: .9; }
      .ai-chat-foot { text-align: center; color: #9aa0b0; font-size: .72em; padding: 6px; }
      @media (max-width: 480px) { #ai-chat-panel { left: 12px; right: 12px; width: auto; } }
    `;
  }
})();