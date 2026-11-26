# Aleph 文档对齐 Roadmap · 第四轮（2026-11）
> 第三轮（pass3）把站点对齐到 Aleph `main` 的 `7fb540b44`，终验报告 `docs/VERIFICATION-2026-11-pass3.md`。
> Aleph `main` 自此后**未前进**（`origin/main` == `7fb540b44`），所以第四轮不是追新代码，而是补上前三轮
> 门禁**看不见**的那一类差距：站点宣称的内置工具名，与代码真实注册的工具名之间的错位。
## 一、这一轮为什么必须做
前三轮的门禁覆盖了**路径**（G1 锚点）、**RPC 方法名**（G1b 方法册）、**代码符号**（G1c 符号）、
**事实断言**（G2）、**结构与双语**（G3/G4）。四轮下来基线八段全 0，站点在「提到某个东西」这件事上
没有硬伤。但有一类差距一直没有被任何一道门覆盖：

> **工具名**。站点写 `bash_exec`，代码注册的是 `bash`；站点把 `process_registry`、`command_ledger`、
> `crawl4ai` 这些**模块名**当成内置工具列进目录；站点漏掉 `get_tool_schema`、`tool_search`、
> `workspace_manage` 等真实注册的工具。

这类错误不会让任何既有门变红，因为路径锚点门只认「`src/…` 形状」的引用，符号门只认**反引号里的
Rust/TS 标识符**（`bash_exec` 是 snake_case 字符串，不是符号），事实门管的是断言句式。结果是：
站点目录页把工具名写错、把模块名当工具、把真实工具漏掉，而六道门全绿——**绿色的门不等于正确的站点**。

第四轮因此做两件事：**补第七道门（G1d 内置工具名普查门）**，把这类差距变成可回归的判定；
然后**按门的结果把内容修平**。

第四轮还额外处理一类前三轮没有明确口径的差距：**未合并分支的能力**。Aleph 仓库当前有三个未合并分支
（`shell-capability-integration` `ed049d9ac`、`shell-capability-rework` `854505aa6`、
`shell-capability-stdin` `523bfe4d0`），它们各自带设计文档与部分实现，但**都不在 `main` 上**。
站点必须把它们写成「规划中 + 蓝图出处」，而不是现状——这正是第三轮 ROADMAP 第二节「冲突时以代码为准」
在分支场景下的落地。

### 第一轮盘点（G1d 首跑）的事实
> 下表是 **S0 首跑快照**，用于说明门禁的起点；最终数字见第七节。

| 指标 | 数值 | 说明 |
|---|---|---|
| 代码侧注册工具 | **209** | 见下「普查口径」 |
| 站点宣称工具名 | 159 | 目录表首列 + `tool_use("x")` / `allows_tool("x")` 调用点 |
| **幽灵名**（文档写了、代码没有） | **9** | `bash_exec`、`command_canonicalize`、`command_ledger`、`config_guide`、`crawl4ai`、`forget`、`permission_tool`、`process_registry`、`scratchpad_registry` |
| **未登记工具**（代码有、文档没有） | **24** | 见 S4 |
| 豁免 | 6 | dev-dependency crate（`criterion` 等）+ 示例假想名 `translate` |

### 普查口径（读代码自己的名单，不做正则扫树）
G1d 的代码侧来自 Aleph 自己承认的权威名单，而不是「扫一遍源码抓 `const NAME`」：

| 来源 | 位置 | 贡献 |
|---|---|---|
| 工具目录 | `src/executor/builtin_registry/definitions.rs` `BUILTIN_TOOL_DEFINITIONS` | 178 个无条件工具 |
| 注册表外工具描述 | 同文件 `REGISTRY_ONLY_DESCRIPTIONS` | 23 个 |
| 名字白名单 | `src/executor/mod.rs` `REGISTRY_ONLY_TOOL_NAMES` | 23 个 |
| 目录外工具 | `src/executor/mod.rs` `TOOLS_OUTSIDE_DEFINITIONS` | `subagent`、`tool_search` |
| MCP 桥接 | `src/mcp/tool_bridge.rs` | 6 个 `mcp_*` |
| 按请求注入 | `src/agents/subagent_tool/mod.rs`、`src/tools/{tool_search,schema_lookup}.rs` | `subagent`、`tool_search`、`get_tool_schema` |
| 条件注册点 | `src/executor/builtin_registry/builder/*.rs` `reg(tools, "x", …)` | 83 个（已被上表覆盖） |

先前的正则扫树版本会把 `#[cfg(test)]` 标在函数上的地方当成模块起点，删掉后面整段生产代码
（`src/builtin_tools/memory_search.rs:236` 会吃掉第 272 行的 `const NAME`），也会把测试夹具里的
假工具名混进普查。改读权威名单后两个问题都不存在了。

## 二、真值来源分层（沿用前三轮）
| 优先级 | 来源 | 语义 |
|---|---|---|
| **T1** | Aleph 仓库 `main`（HEAD `7fb540b44`）源码 | 现状唯一权威 |
| **T2** | `docs/reference/`（`FEATURE_LOCATOR`、`PROCESS_MANAGEMENT`、`SANDBOX`、`TOOL_SYSTEM`） | 当前架构契约 |
| **T3** | `docs/research/` 蓝图、设计稿 | 设计目标，只能写「规划中」 |
| **T4** | 站点现状（前三轮产出） | 待校正对象 |
| **T5** | `docs/superpowers/{specs,plans,runs}/` | 时点证据，引用须带日期 |
冲突时**以代码为准**。**未合并分支不属于任何一层现状**——它只能以「规划中 + 蓝图出处」出现。

## 三、内容三态约定（沿用前三轮）
| 状态 | 写法 |
|---|---|
| **现状** | 直接陈述 + 真实路径锚点（路径与符号都要能在代码里 grep 到） |
| **规划中** | 块引用横幅 + 蓝图出处 + 当前实现位置 |
| **历史** | 页面内 `## 历史：<主题>` 小节 |
工具名写错属于「现状写错」，必须改写；已删除的模块不得留在现状段落里。

## 四、七道门（分级完成的判定机制）
每阶段结束必须全绿才解锁下一阶段；任一门红则该阶段**不完成**。

| 门 | 名称 | 判定 | 命令 |
|---|---|---|---|
| **G1** | 锚点门 | 页面里所有形似源码路径的引用在 Aleph 仓库真实存在 | `python3 scripts/anchor_check.py --repo ../Aleph` |
| **G1b** | 方法册门 | RPC 方法名与代码 `src/gateway/method_census.rs` 一致 | `python3 scripts/method_audit.py --repo ../Aleph` |
| **G1c** | 符号门 | 反引号里的 Rust/TS 标识符在代码里真实存在 | `python3 scripts/symbol_check.py --repo ../Aleph` |
| **G1d** | **工具名门（新增）** | 站点宣称的内置工具名必须真实注册；代码注册的工具必须被站点覆盖（或被显式豁免） | `python3 scripts/tool_audit.py --repo ../Aleph` |
| **G2** | 事实门 | 无过期断言；指定页面含目标形态语义 | `python3 scripts/freshness_audit.py --check facts --docs content/docs` |
| **G3** | 结构门 | `meta.json` 收录完整；站内相对链接可解析 | `python3 scripts/freshness_audit.py --check structure --docs content/docs` |
| **G4** | 双语门 | zh/en 页面集合一致；同名页 `##` 标题骨架一致 | `python3 scripts/freshness_audit.py --check bilingual --docs content/docs` |
| **G5** | 构建门 | `next build` / `tsc --noEmit` / `eslint` 退出码全 0 | `pnpm exec next build && pnpm exec tsc --noEmit && pnpm exec eslint` |

### G1d 的判定细则
- **文档侧「宣称」**：①表头命中「工具 / 工具名 / 内置工具 / tool / tool name / builtin tool(s)」的表格**首列**
  反引号 token；②`tool_use("x")` / `allows_tool("x")` / `tool_call("x")` / `invoke_tool("x")` 调用点。
- **文档侧「覆盖」**：反引号提及**或**正文整词出现（排除 `changelog.mdx`，它记录的是过去版本说过的话）。
- **幽灵名** = 宣称 ∉ 注册；**未登记** = 注册 ∉ 覆盖。
- **豁免**：`scripts/tool_audit.py` 的 `EXEMPT_NAMES`，每条都要写明理由（dev-dependency crate、示例假想名、
  内部诊断工具）。
- **棘轮**：`scripts/baseline.json` 新增 `tool_ghost` / `tool_missing` 两段。只棘轮**已知旧债**，
  阶段中途引入的新失效立即让 G1d 变红；修完一条就棘轮降一条。

## 五、阶段路线（逐级解锁）
```
S0 门禁与基线 ─▶ S1 工具目录校准 ─▶ S2 调用面校准 ─▶ S3 后台作业现状
                                                        │
                                                        ▼
S7 终验 ◀── S6 术语·导航·changelog ◀── S5 规划中区块 ◀── S4 未登记工具落位
```
| 阶段 | 目标 | 主要产出 |
|---|---|---|
| **S0** | 门禁加固与基线盘点 | `scripts/tool_audit.py`、接入 `run_gates.py`、`baseline.json` 两段、本 ROADMAP 与执行计划 |
| **S1** | 内置工具目录校准 | `tools/builtin.mdx`、`tools/overview.mdx`、`concepts/builtin-tools.mdx`（zh + en） |
| **S2** | 工具调用面校准 | `architecture/{tools,executor,sandbox,overview}.mdx`、`security/sandboxing.mdx`、`concepts/identity-context.mdx`、`tools/creating.mdx`（zh + en） |
| **S3** | 后台作业与执行现状 | `tools/builtin.mdx`、`architecture/sandbox.mdx`、`architecture/executor.mdx`（zh + en） |
| **S4** | 未登记工具逐个落位或豁免 | 24 个工具对应的页面（zh + en）+ `EXEMPT_NAMES` 理由 |
| **S5** | 未合并分支能力标「规划中」 | shell rework / stdin-EOF / JSONL 蓝图出处横幅 |
| **S6** | 术语 · 导航 · changelog | `terminology.mdx`、`changelog.mdx`、`meta.json` |
| **S7** | 终验报告 | `docs/VERIFICATION-2026-11-pass4.md` |

## 六、范围边界（本轮明确不做）
- **不**改动 Aleph 代码仓任何文件；本轮只读 `../Aleph`，所有产出落在文档站仓库。
- **不**合并、不推送三个未合并分支；`main` 仍是唯一现状基线。
- **不**为「让门变绿」而放宽门：G1d 的判定口径写在脚本与本文件里，改口径要改这两处并说明理由。
- **不**把内部诊断工具包装成用户能力：确认属于内部观测面的工具走 `EXEMPT_NAMES` 豁免并写明理由，
  而不是硬塞进目录页。
## 七、完成状态（2026-11-26 收口）
起点 `a535ac4`（第三轮终验），终点为本轮 S7。

| 阶段 | 提交 | 状态 |
|---|---|---|
| S0 门禁与基线 | `a860434`、`ecabd85` | 完成 |
| S1 工具目录校准 | `26b5852` | 完成 |
| S2 调用面校准 | `6ce9af4` | 完成 |
| S3 后台作业现状 | `2a756ee` | 完成 |
| S4 未登记工具落位与豁免清零 | `baa4b9e` | 完成 |
| S5 未合并分支标「规划中」 | `1d7a3da` | 完成 |
| S6 术语 · 导航 · changelog | `be03568` | 完成 |
| S7 终验报告 | `docs/VERIFICATION-2026-11-pass4.md` | 完成 |

收口时的 G1d 数字：注册 209 / 宣称 167 / **幽灵 0** / **未登记 0** / **豁免 0**。

豁免归零的做法是**改文档而不是放宽门**：`testing.mdx` 的表头由「工具」改成「命令 / crate」，
`identity-context.mdx` 的示例假想名 `translate` 换成真实存在的 `code_exec`，
`EXEMPT_NAMES` 随后清空。`capability_projection_diagnostics` 没有走豁免——它是真实注册的工具，
按内部诊断面的真实语义写进目录页。

