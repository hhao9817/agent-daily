# 晨报改进档案（Morning Briefing Evolution Log）

本文件是"每日晨报"任务的进化回路。晨报任务每次运行前读取本文件，
根据历史反馈调整内容；用户的新反馈由白天会话追加到此文件。

## 晨报定位
- 用户：data Agent 开发者 / 团队技术架构师，正在做"AI for 业务"
  （从 AI for 研发转型，研发知识库已建成）。
- 核心约束：不直连数据库，通过高业务含义的 API 查数（部分为上百字段宽表 API）。
- 三大方向：①业务知识库构建 ②业务语义理解（API/宽表字段语义）③业务系统精确查询分析。

## 已应用的改进（按时间倒序）

### 2026-08-06
- 选题从"数据分析 Agent / 业务 Agent"聚焦到"AI for Business / 业务知识库"。
- 纳入关键约束：不直连数据库、通过业务含义 API 查数、上百字段宽表 API。
- 语义层/指标平台 vs 企业知识图谱两条路线都要研究，需先看对比。
- 每条内容增加"深度详情"：为什么值得关注 / 核心机制 / 深度解读 / 落地建议 / 局限与风险 + 架构示意图。
- 网站改为两级结构：列表页 + 点击弹详情（含 SVG 流程图，图文并茂）。

## 待应用的反馈（由白天会话追加，处理后移入上方"已应用"）
- （暂无）

## 2026-08-11 运行记录（本次）
- arXiv API（export.arxiv.org）持续不稳定：search_arxiv.py socket.timeout；API query 端点先 301→https 再返回"Rate exceeded."（14 字节）。改用 RSS feed 成功：cs.DB 12 篇（lastBuildDate 2026-08-10 04:00，skipDays 含 Saturday/Sunday 但周一已恢复）、cs.CL 119 篇、cs.AI 295 篇。按 abs 页 curl 摘要成功（-L + User-Agent）。
- Semantic Scholar 仍间歇 429 限流，成功核实：MIRA(2608.06950)=0/infl0、CWS(2608.07214)=0/infl0、SemBaker(2608.06677)=0/infl0、FHS(2608.06614)=0/infl0（均 2026-08-06/07 新文，符合预期）；FinRank(2608.07400)、Crystallization(2608.07213)、LVLM Confidence(2608.06532) 因限流未核实，标注"信息待核实"。
- GitHub API 经已认证 gh CLI（hhao9817）工作正常：发现 Apache Ossie（apache/ossie，1817⭐，incubating，厂商中立语义模型交换规范，dbt Labs/Snowflake/Salesforce/BlackRock/RelationalAI 联合推进，最近提交 2026-07-31 GSF 双向转换器/SUM_BOOLEAN 修复/Java 21）、OpenMetadata 2.0.0-RC1（2026-07-30 发布，8/10 持续高频提交：Ontology Explorer RDF 知识图谱 + ContextCenter 版本化上下文 + AI Mode + Data Marketplace + Glossary 治理迁移，从数据目录向 AI 原生平台跃迁）、Cube v1.7.18 后 8/10 新增两个 tesseract 引擎修复（FILTER_PARAMS segment 谓词下推 PR#11517 + 多阶段 out-of-grain 维度读取报错 PR#11514，均 Claude Opus 5 协作）。dbt-labs/metricflow pushed 2026-08-10（本周活跃）。
- blogwatcher 工作正常（7 源，20 条）。TDS《Building an Agent-Ready Data Warehouse》（2026-08-10，Shafeeq Ur Rahaman）正文经 curl 抓取核实：提出 Decision Contract 概念（批准源+最小时间窗+指标定义+时效上限+完整性校验+允许/禁止执行边界，比 Data Contract 多一维"决策适合度"），论点"可查询≠Agent 就绪，正确 SQL 可能推错行动"。dbt Summit 2026 预告（getdbt.com）正文抓取核实：四大支柱 + 标志性 session"The semantic layer is dead. Long live the semantic layer!"（语义层是 AI 策略最承重的一块）+ Apache Ossie session + dbt MCP Server + dbt Wizard 三模式 + dbt State 30% 计算节省。OpenAI 博客 Cloudflare 挑战无法抓取。
- 本次精选 9 条情报（与历次不重复，避开了 MERIT/NeSy-RAG/Schema-Guided/Beyond Top-K/Tytan/Agentic Nesting/Bitter Lesson/BEGIN AI TRANSACTION/LinkAlign/ReFoRCE/Executable Schema Contracts/TableZoomer/ADORE/On Benchmarking/OADD/AttnLink/DataClawEval/ACE-GraphRAG/DataSpace/BAP-SQL/CASE/DBLifeBench/SERL-SQL/Evidence-Grounded KG/ISEE/Metadata Reasoner/HyperAgent/GPTKB2.0/MCTS-Report/EvolveNet/GDPevo/Stateful Governance/SkillTrace/SocratiCode 等已用条目），覆盖三来源：学术 5 篇（MIRA 证据验证记忆复用/CWS 因果数据管理生态/SemBaker 语义算子编译/FHS 因子化假设检索/FinRank 金融溯源基准）+ 博客 2 篇（TDS Decision Contract/dbt Summit 2026 语义层承重墙）+ GitHub 2 条（Apache Ossie 厂商中立语义规范/OpenMetadata 2.0 RC1 Ontology Explorer+AI Mode）+ product 1 条（三层分工研判合并到 groups.product，共 9 条 items）。
- 关键发现：本次 9 条串成"让 AI 真正懂业务、精确查数、可信行动"完整三层链路——语义层（Apache Ossie 厂商中立规范 + Cube v1.7.18 + dbt Summit 承重墙定位）管指标一致 → 知识图谱（OpenMetadata 2.0 Ontology Explorer）管实体关系 → 因果层（CWS）管决策依据 → 上下文层（TDS Decision Contract + ContextCenter）管治理边界 → 编译层（SemBaker）管执行效率 → 检索层（FHS 因子化 + FinRank 溯源）管证据可信。最核心战略研判：用户"语义层 vs 知识图谱"二元选择正被"语义层+知识图谱+因果层"三层分工取代。Apache Ossie 是本周最具战略价值的开源发现——厂商中立语义模型交换规范，解决跨工具语义碎片化，是用户避免厂商锁定的关键基础设施。TDS Decision Contract 是本周最贴合用户场景的博客——"可查询≠Agent 就绪"，提出 Decision Contract 概念填补 Data Contract 与 Agent 行动间治理空白。CWS 是本周最具架构视野的论文——为 Agentic AI 建因果层，从相关关系到处方决策。MIRA 与昨日 MERIT 形成"记忆复用"主题两种实现——MERIT 双极性 vs MIRA 证据门控。FHS 与昨日 Beyond Top-K 形成主题呼应——表格密集数据 chunk+embed 结构性失效需因子化假设。
- 发布成功：index.html 已含 2026-08-11 全部 9 条（grep 核实 MIRA/CWS/SemBaker/FHS/FinRank/Apache Ossie/OpenMetadata 2.0/三层分工 均存在），publish_site.py 输出"✅ 已推送 GitHub Pages"，归档索引更新至 13 期。

## 2026-08-10 运行记录（本次）
- arXiv API（export.arxiv.org API 端点）可用：通过 id_list 批量查询获取论文摘要（Atom XML 解析），search_arxiv.py 关键词检索仍混杂（默认 relevance 排序混入数学/物理）。cs.DB RSS feed 周末为空（lastBuildDate 2026-08-09 04:00，skipDays 含 Saturday/Sunday，items=0），改用 API query cat:cs.DB OR cs.CL sortBy=submittedDate 获取最新 30 篇。
- Semantic Scholar 仍间歇 429 限流，间隔 10-15s 重试后成功核实：NeSy-RAG(2608.06292)=0/infl0、MERIT(2608.05906)=0/infl0、Schema-Guided IE(2608.06167)=0/infl0、Beyond Top-K(2608.06305)=0/infl0（均 2026-08-06 新文，符合预期）；Compliance-First Agentic Platforms(2608.06112) 因限流未核实。
- GitHub API 经已认证 gh CLI（hhao9817）工作正常：发现 Cube v1.7.18 今日发布（2026-08-09T18:27:56Z，client-core cubeSql/cubeSqlStream timezone 选项 PR #11507，比档案 v1.7.17 更新）；SocratiCode v1.11.0（3,237⭐，2026-08-05 push，TypeScript/MCP，DB/API/infra knowledge 标注，61% token 减少/84% 调用减少/37x 更快，AGPL-3.0）均经 gh API 核实。GitHub REST search API 未限流。
- blogwatcher 工作正常（7 源，20 条），TDS 两篇正文经 curl 抓取核实：Loading Data（2026-08-09，Ibrahim Salami，source vs model + 测试断言 + lineage graph，论点"数据加载≠数据可用"）、Structured Output（2026-08-09，Shuai Guo，Pydantic schema + Ollama format + Gemma 4 本地生成，论点"schema 约束本地 LLM 输出为可解析对象"）。
- 本次精选 8 条情报（与历次不重复，避开了 Tytan/Agentic Nesting/Bitter Lesson/BEGIN AI TRANSACTION/LinkAlign/ReFoRCE/Executable Schema Contracts/TableZoomer/ADORE/On Benchmarking/OADD/AttnLink/DataClawEval/ACE-GraphRAG/DataSpace/BAP-SQL/CASE/DBLifeBench/SERL-SQL/Evidence-Grounded KG/ISEE/Metadata Reasoner/HyperAgent/GPTKB2.0/MCTS-Report/EvolveNet/GDPevo/Stateful Governance/SkillTrace 等已用条目），覆盖三来源：学术 4 篇（MERIT 双极性记忆修复 Text-to-SQL/NeSy-RAG 神经符号可归因 QA/Schema-Guided IE schema 先行抽取/Beyond Top-K 表格密集文档 top-k 失效）+ 博客 2 篇（TDS Loading Data 语义层立项论据/TDS Structured Output schema 约束本地 LLM）+ GitHub 2 条（Cube v1.7.18 timezone 支持/SocratiCode 知识图谱+MCP）+ product 1 条（双路线态势研判合并到 groups.product，共 8 条 items）。
- 关键发现：本次 8 条串成"让 AI 在业务系统精确查数、可信解释、可控输出"三条主线——Schema-Guided（schema 先行建术语表）→ MERIT（带记忆的可信查询修复，Spider 66.34%→69.79%）→ NeSy-RAG（查询结果可归因验证 + 知识缺口检测）→ Beyond Top-K（宽表/表格密集文档禁用 chunk+embed，走 Agent 化操作）→ TDS Loading Data（语义层是可用性根基）→ TDS Structured Output（schema 约束输出为可解析对象）→ Cube v1.7.18（语义层工业迭代，业务规则集中封装）→ SocratiCode（知识图谱+MCP 在关系推理场景补足）。Beyond Top-K 是本次最贴合用户宽表 API 场景的论文——量化证明了"chunk+embed 在表格密集数据上结构性失效"，为用户选择查询范式提供硬数据。NeSy-RAG 的知识缺口检测与 MERIT 的双极性记忆是本周最值得落地的两个机制——前者避免信息不足时幻觉补全，后者让查询经验可积累复用。
- 发布成功：index.html 已含 2026-08-10 全部 8 条（grep 核实 MERIT/NeSy-RAG/Beyond Top-K/SocratiCode/v1.7.18/Schema-Guided 均存在），GitHub Pages CDN 缓存导致即时 fetch 仍显示旧版（已知局限）。

## 2026-08-09 运行记录（本次）
- arXiv API（export.arxiv.org）持续不稳定：search_arxiv.py 多关键词检索再次 SSLEOFError/socket.timeout；arXiv RSS feed 周末为空（cs.DB lastBuildDate 2026-08-08 04:00，skipDays 含 Saturday/Sunday，items=0）；改用 Semantic Scholar paper search API（限流中但部分成功）+ arxiv.org abs 页直接 curl 摘要（HTTP 重定向到 HTTPS 但 -L + User-Agent 头可工作）。Semantic Scholar 间歇 429，成功核实 LinkAlign(2503.18596)=31/infl4、ReFoRCE(2502.00675)=31/infl8、Executable Schema Contracts(2606.05415)=0、ADORE(2601.18267)=0、Agentic Nesting(2608.05159)=0、Project2Task(2608.05225)=0、SearchAuditor(2608.05212)=0、TASER(2508.13404)=0；TableZoomer(2509.01312)、KG-RAG Agentic Crawling(2604.14220)、Plugging Schema Graph(2506.04427) 因限流未核实，标注"信息待核实"。
- GitHub API REST 层 403 rate limit，但已认证 gh CLI（hhao9817）工作正常：cube-js/cube v1.7.17（2026-08-07 今日发布，releases API 核实；仓库描述"open-source semantic layer for AI, BI and embedded analytics"，topics 含 agentic-analytics/agents/ai，20,575⭐，2026-08-08 push）、isaacwasserman/mcp_cube_server（15⭐，2026-07-21，read_data/describe_data 工具核实）、Canner/WrenAI 0.29.2（2026-08-05，PR#2043 get knowledge from ibis + #2076 Databricks + #2079 LLMProvider 重构）、open-metadata/OpenMetadata 1.13.3（2026-07-31，data contract 治理 + Snowflake 外键修复 #30473）、OpenSPG v0.8（2025-06，近一年无新发布）、vanna-ai/vanna v2.0.2（2026-02-02）、chat2db/Chat2DB v5.3.3（2026-08-06）均核实。
- blogwatcher 工作正常（7 源，2299 篇），其中 Data Engineering Weekly《On Benchmarking》（2026-08-06，Ananth Packkildurai）正文经 curl 抓取核实（active vs passive benchmarking 三要素：决策/工作负载/系统边界）。TDS 两篇（Before Q K V / Streamlit LangGraph）标题可取但正文 JS 渲染拿不到 body，仅取标题+URL。
- 本次精选 8 条情报（与历次不重复，避开了 Tytan/Agentic Nesting/Bitter Lesson/BEGIN AI TRANSACTION/OADD/AttnLink/DataClawEval/ACE-GraphRAG/DataSpace/BAP-SQL/CASE/DBLifeBench/ISEE/Metadata Reasoner/HyperAgent/GPTKB2.0/MCTS-Report/EvolveNet/GDPevo 等已用条目），覆盖三来源且形成完整闭环：学术 5 篇（LinkAlign 千字段 schema linking/Executable Schema Contracts closed-world 自动 schema 发现/TableZoomer query-aware 列子表/ReFoRCE Spider 2.0 登顶 1000+列/ADORE Memory Bank 可信编排）+ 博客 1 篇（Data Engineering Weekly On Benchmarking 主动基准测试方法论）+ GitHub 1 条（Cube v1.7.17 + mcp_cube_server 语义层原生面向 AI Agent）+ product 1 条（WrenAI 0.29.2 ibis + OpenMetadata 1.13.3 data contract 双栈）。
- 关键发现：本次 8 条串成"让 AI 在业务系统精确查数并可信执行"完整链路——LinkAlign（千字段选对表列，31引用）→ Executable Schema Contracts（自动发现可执行 schema 契约，closed-world 防幻觉）→ TableZoomer（按查询动态裁剪字段子集降 token）→ ReFoRCE（不信任单次生成，consensus+self-refine+column exploration，31引用8 influential）→ ADORE（orchestrator+Memory Bank 把查询升级为可审计调查）→ On Benchmarking（吞吐量不是架构决策，Agent 评估方法论）→ Cube v1.7.17+mcp_cube_server（语义层原生面向 AI Agent，MCP 标准化调用）→ WrenAI+OpenMetadata（语义层扩源 + 目录契约双供给）。LinkAlign、ReFoRCE、Executable Schema Contracts 是本周最贴合用户宽表 API 场景的三篇：分别解决"上千字段选列""schema 自动发现标注""企业级查询可信执行"。ReFoRCE 的 column exploration 与 mcp_cube_server 的 describe_data 工具思想交叉验证——Agent 应有"先探查后查询"的主动 schema understanding 能力。
- 发布成功：commit 27edef9 已推送，本地 index.html 含 2026-08-09 全部 8 条，GitHub Pages CDN 缓存导致即时 fetch 仍显示旧版（已知局限）。

## 2026-08-08 运行记录（本次）
- arXiv API（export.arxiv.org）全程不稳定：search_arxiv.py 多关键词检索持续 SSLEOFError/socket.timeout；改用 RSS feed（cs.DB 18 篇/cs.CL 154 篇/cs.AI 307 篇）+ 按 abs ID curl 单篇摘要页（HTTP，非 HTTPS，避开 SSL EOF）。Semantic Scholar 仍间歇 429 限流，成功核实 Tytan(2608.06331)=0、Agentic Nesting(2608.05159)=0、SkillTrace(2608.05204)=0 引用数（均 2026 新文）；Bitter Lesson of Tool Calling(2608.06370)、BEGIN AI TRANSACTION(2608.05412)、Screenshots or Tools(2608.03327) 因限流未核实，标注"信息待复核"。
- GitHub API 检索顺利：Cube v1.7.17（2026-08-07 今日发布，releases API 核实 lastRefreshTime pushdown 修复 #11394）、OpenMetadata 1.13.3（2026-07-31，releases API 核实 data contract/Snowflake 外键修复）、OtterMind/Chat2DB v5.3.3（2026-08-06，从原 chat2db 仓库迁移核实）、OpenSPG v0.8（2025-06，last push 2025-07-05，近一年无新发布核实）、LeanRAG（AAAI 2026，257⭐核实）、RAGFlow 87k⭐ 均核实。
- dbt 博客源工作正常，抓取到高相关文章正文：《Data platforms were built to store. Intelligence platforms are built to reason.》（phData 客座，核心论点"可靠性在知识层而非智能层建立"）。
- 本次精选 8 条情报（与历次不重复），覆盖三来源且形成完整闭环：学术 4 篇（Tytan 语义层自动构建/Agentic Nesting 遗留系统嵌套 Agent 化/Bitter Lesson of Tool Calling PYC vs JSON/BEGIN AI TRANSACTION 语义隔离级别）+ dbt 博客 1 篇（知识层是被低估的可靠性根基）+ GitHub 2 条（Cube v1.7.17 语义层今日发布/OpenMetadata 1.13.3 上下文层卡位）+ product 1 条（双路线对照：语义层工业活跃 vs 知识图谱开源放缓）。
- 关键发现：本次 8 条串成"让 AI 真正懂业务数据并精确执行"完整链路——Tytan（自动化语义层，100% 覆盖）→ Agentic Nesting（遗留业务 API 系统封装为嵌套 Agent）→ Bitter Lesson of Tool Calling（PYC 代码式调用优于 JSON，为 API 精准调用选型供据）→ BEGIN AI TRANSACTION（多步 Agent 的语义一致性契约，业务可信度事务化）→ dbt 知识层论（可靠性在知识层，立项论据）→ Cube v1.7.17（语义层工业周级迭代，lastRefreshTime 可信修复）→ OpenMetadata（数据目录向 AI 上下文层演进，data contract 治理）→ 双路线对照（语义层短期占优，知识图谱开源放缓）。Tytan 与 Agentic Nesting 是本周最贴合用户场景的两篇：前者解决"语义层怎么自动建"，后者解决"业务 API 系统怎么当 Agent 调"。GitHub Pages CDN 缓存导致即时 fetch 显示旧版，本地 index.html 已含 2026-08-08 全部 8 条，commit ce2b4eb 已推送。

## 2026-08-07 运行记录（本次）
- arXiv API（export.arxiv.org）恢复可用，多关键词检索（semantic layer/text-to-SQL/business knowledge graph/API understanding/function calling/table QA/schema linking/GraphRAG/metadata reasoning）成功。Semantic Scholar 仍间歇 429 限流，成功核实 AttnLink(2608.00693)=0、OADD(2608.04536)=0 引用数（均 2026 新文）；ACE-GraphRAG(2608.01269)、DataClawEval(2607.28033) 因限流未核实，标注"信息待复核"。
- GitHub API 先成功后限流：OpenSPG 2.1k⭐（Java/蚂蚁SPG/KAG框架，topics 核实）、WrenAI v0.29.2（2026-08-05，releases API 核实 PR#2043 get knowledge from ibis +Databricks）、Chat2DB 27.7k⭐、vanna 23.8k⭐ 均核实；SuperSonic/LeanRAG 后续因限流未能取最新 release（SuperSonic 最新 release 仍为 v0.9.8/2024-11）。
- dbt 博客源工作正常，抓取到 1 篇高相关文章正文：From Analytics Engineer To Context Engineer（Gong 通话案例：5万token→几百token，成本降98%，直连MCP是捷径陷阱）。
- 本次精选 6 条情报（与历次不重复），覆盖三来源且恰好对应技术栈串联：学术 3 篇（OADD 运营化数据发现/AttnLink 注意力schema linking/DataClawEval 数据工程Agent基准）+ dbt 博客 1 篇（Context Engineer context engineering）+ GitHub 2 条（OpenSPG/KAG 知识图谱路线 vs WrenAI v0.29.2 语义层路线，恰好构成用户双路线对照）+ product 1 条（双路线对比点评，合并到groups.product）。
- 关键发现：本次 6 条串联成"让 AI 真正读懂业务数据"完整链路——OADD（定义宽表字段语义理解的新范式，直击用户上百字段场景）→ AttnLink（用注意力毫秒级筛字段，为 API 调用填参提效）→ DataClawEval（分引擎确定性沙箱评分，业务可信度验证范式）→ ACE-GraphRAG（知识图谱路线的推理时上下文策略层）→ dbt Context Engineer（语义层路线行业级方法论背书，token降98%）→ OpenSPG vs WrenAI（双路线开源落地对照）。OADD 是本周最贴合用户场景的论文，首次形式化"运营化感知数据发现"。

## 2026-08-06 第二次运行记录
- 本次因 arXiv API 与 Semantic Scholar API 持续限流（Rate exceeded / 429），改用 arXiv RSS feed（cs.CL/cs.DB/cs.AI）作为学术来源，筛选出 6 篇高相关新论文（DataSpace、BAP-SQL、CASE、SERL-SQL、DBLifeBench、Evidence-Grounded KG）。
- 成功核实的 Semantic Scholar 引用数：BAP-SQL=0、SERL-SQL=0（均为 2026 新论文，符合预期）。其余 3 篇因限流未能核实，已在 detail.caveats 标注"链接待复核"。
- GitHub 检索顺利：WrenAI v0.29.2（ibis 知识源）、Cube v1.7.16、graphrag 35.3k⭐、LightRAG 38.5k⭐ 均核实。
- 本次精选 6 条情报，覆盖：学术 4 篇（DataSpace/BAP-SQL/CASE/DBLifeBench）+ GitHub 开源 2 条（WrenAI vs Cube 语义层对比、graphrag vs LightRAG 知识图谱对比），恰好对应用户"语义层 vs 企业知识图谱"双路线需求。

## 2026-08-06 第三次运行记录（本次）
- arXiv API 仍 429，继续用 RSS feed（cs.DB 14 篇/cs.AI 416 篇）作为学术源。Semantic Scholar 限流中，成功核实 ISEE=0、BAP-SQL=0、Stateful Governance=0（均 2026 新论文，符合预期）；Metadata Reasoner/HyperAgent/GPTKB2.0 因限流未能核实，已标注"信息待复核"。
- GitHub 检索顺利：RAGFlow 86.9k⭐、mem0 62.6k⭐、private-gpt 57.4k⭐、Cube 20.5k⭐、WrenAI 17.0k⭐ 均核实。WrenAI v0.29.2（2026-08-05 发布）"get knowledge from ibis"经 releases API 核实（PR #2043）。
- dbt 博客源工作正常，抓取到 3 篇高相关文章正文：语义债危机 / 数据平台→智能平台 / AI 数据管道（含 2026 State of Analytics Engineering 数据：72% 团队用 AI 写代码但仅 24% 用 AI 管管道）。
- 为与第二次运行不重复，本次精选 6 条全新情报，覆盖三来源：学术 4 篇（ISEE 字段语义富集/Metadata Reasoner 元数据推理/HyperAgent 工具超图规划/GPTKB2.0 知识库消歧）+ dbt 博客 1 篇（语义债危机）+ GitHub 1 篇（WrenAI v0.29.2 深读）。
- 关键发现：本次 6 条恰好串成完整技术栈——ISEE（字段语义富集）→ Metadata Reasoner（数据源/API 选择）→ HyperAgent（API 调用链规划）三篇层层递进，从"字段懂业务"到"选对 API"到"串对 API"；GPTKB2.0 与 WrenAI 分别代表知识图谱/语义层双路线最新进展；dbt 语义债文章为全套提供商业立项论据。

## 2026-08-06 第四次运行记录（本次）
- arXiv API 恢复可用，多关键词检索（semantic layer/text-to-SQL/enterprise RAG/metadata schema/agent harness）成功。Semantic Scholar 仍 429 限流，所有 6 篇引用数未核实，均标注"信息待复核"。
- 本次精选 6 条情报，覆盖三来源且与二/三次运行不重复：学术 4 篇（GDPevo 企业业务自进化基准/DBLifeBench 数据库全生命周期+Progressive-Text2SQL/MCTS-Report 表→多模态报告+SQL 回验/EvolveNet 联邦式 harness 进化）+ dbt 博客 1 篇（dbt Core v2.0 Fusion 引擎+Fivetran 合并=为可信 AI Agent 打造数据基础设施）+ GitHub 1 篇（SQLBot v1.10.0 RAG 问数+MCP 接入+安全加固）。
- GitHub 检索顺利：Chat2DB 27.7k⭐、Cube 20.6k⭐、WrenAI 17.0k⭐、jimureport 8.2k⭐、SQLBot 6.6k⭐、SuperSonic 5.0k⭐、Awesome-Text2SQL 3.7k⭐ 均核实。SQLBot v1.10.0（2026-07-16）经 releases API 核实，含 SQL 注入/提示注入修复 + MCP 支持。GitHub API 后续因速率限制未能取 WrenAI/SuperSonic 最新 release。
- dbt 博客源工作正常，抓取 2 篇正文：Fivetran+dbt 合并完成（2026-06-01）、Snowflake Summit（dbt Core v2.0/Fusion Rust 重写/10x 解析）。
- 关键发现：本次 6 条串联成"业务 Agent 从评估到落地"完整链路——GDPevo（怎么评估业务 Agent 自进化）→ DBLifeBench（怎么评估全栈 DB 智能，警示专精模型灾难性遗忘）→ MCTS-Report（怎么生成可信业务报告，SQL 回验数值）→ EvolveNet（多业务线怎么联邦进化而不碰数据合规）→ dbt v2.0+Fivetran（数据基础设施怎么为 Agent 就绪）→ SQLBot（开源 ChatBI 怎么接 MCP 成为 Agent 可调用的数据技能）。dbt 合并+v2.0 是本日最强商业信号，为用户"语义层路线"提供行业级背书。