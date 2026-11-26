# Aleph 文档站第四轮对齐执行计划（2026-11-26）
> 对应 ROADMAP：`docs/ROADMAP-2026-11-pass4.md`
> 真值基线：Aleph `main` = `7fb540b44`（与第三轮同一 HEAD；`origin/main` == `7fb540b44`）
> 方法沿用前三轮：roadmap → phase spec（本文）→ 逐阶段过门 → 终验报告
## 阶段总览
| 阶段 | 目标 | Task |
|---|---|---|
| S0 | 门禁加固与基线盘点 | S0.1、S0.2 |
| S1 | 内置工具目录校准 | S1.1、S1.2 |
| S2 | 工具调用面校准 | S2.1、S2.2 |
| S3 | 后台作业与执行现状补齐 | S3.1 |
| S4 | 未登记工具逐个落位或豁免 | S4.1 |
| S5 | 未合并分支能力标「规划中」 | S5.1 |
| S6 | 术语 · 导航 · changelog | S6.1 |
| S7 | 终验报告 | S7.1 |
---
## S0 — 门禁加固与基线盘点
### Task S0.1 `scripts/tool_audit.py`（G1d 工具名普查门）
**Files:**
- Create: `scripts/tool_audit.py`
**做什么：**
1. 代码侧普查读 Aleph 自己的权威名单，不做正则扫树：
   - `src/executor/builtin_registry/definitions.rs`：`BUILTIN_TOOL_DEFINITIONS`（`name: "x"`）、
     `REGISTRY_ONLY_DESCRIPTIONS`（`("x", …)`）、`BRIDGE_TOOL_DESCRIPTIONS` / `INJECTED_TOOL_DESCRIPTIONS`
     （`crate::…::CONST` 引用，用 `_resolve_const()` 解析出字符串值）；
   - `src/executor/mod.rs`：`REGISTRY_ONLY_TOOL_NAMES`、`TOOLS_OUTSIDE_DEFINITIONS`；
   - `src/executor/builtin_registry/builder/*.rs`：`reg(tools, "x", …)` 条件注册点；
   - `src/tools/tool_search.rs`、`src/tools/schema_lookup.rs`：`const NAME`（按请求注入的两个工具）。
2. 文档侧两套判定：
   - **宣称**（会判幽灵）：表头命中「工具 / tool / builtin tool(s)」的表格**首列**反引号 token，
     外加 `tool_use("x")` / `allows_tool("x")` / `tool_call("x")` / `invoke_tool("x")` 调用点；
   - **覆盖**（会判未登记）：反引号提及**或**正文整词出现，排除 `changelog.mdx`。
3. `EXEMPT_NAMES` 豁免清单，每条写明理由（dev-dependency crate、示例假想名、内部诊断工具）。
4. 与 G1b 同款 CLI：`--repo/--docs/--baseline/--files/--files-from/--raw/--json/--update-baseline`，
   基线段名 `tool_ghost` / `tool_missing`，复用 `scripts/gate_baseline.py`。
- [x] **Step 1**: 写脚本，跑 `python3 scripts/tool_audit.py --repo ../Aleph --docs content/docs --raw`。
- [x] **Step 2**: 核对 census 数量与名单（应为 209 / 幽灵 9 / 未登记 24 / 豁免 6）。
- [x] **Step 3**: 用 `--json` 导出完整清单存档到 `/tmp`（不入库），作为 S1–S4 的底账。
**提交**：`docs(gates): add the builtin tool name census gate`

### Task S0.2 接入总门 + 基线棘轮 + 本轮台账
**Files:**
- Modify: `scripts/run_gates.py`（G1c 之后加 `G1d 工具名门`）
- Modify: `scripts/baseline.json`（新增 `tool_ghost`、`tool_missing` 两段）
- Create: `docs/ROADMAP-2026-11-pass4.md`
- Create: `docs/superpowers/plans/2026-11-26-aleph-docs-calibration-pass4.md`
**做什么：**
1. `run_gates.py` 标题从「六道门」改为「七道门」，检查表加一行 G1d。
2. `baseline.json` 两段先写当前实测集合（幽灵 9 + 未登记 24），让门在修复过程中保持绿；
   **只棘轮已知旧债**，任何新幽灵立即让门变红。
3. 写本 ROADMAP 与执行计划。
- [x] **Step 1**: 改 `run_gates.py` 与 `baseline.json`，跑 `python3 scripts/run_gates.py --repo ../Aleph`，
      确认七门全绿（G5 不带 `--build` 时不跑）。
- [x] **Step 2**: 写 ROADMAP 与本文。
**提交**：`docs(gates): wire the tool name gate into the gate runner and baseline`
---
## S1 — 内置工具目录校准
> 背景：G1d 幽灵名全部落在工具目录页与调用面页。目录页把**模块名**当工具列出来
> （`process_registry` → `src/builtin_tools/process_registry.rs`），又把真实工具名写错
> （`bash_exec` → 代码里是 `bash`），还漏掉一批真实注册的工具。
### Task S1.1 `tools/builtin.mdx`（zh + en）
**Files:**
- Modify: `content/docs/zh/tools/builtin.mdx`
- Modify: `content/docs/en/tools/builtin.mdx`
**做什么：**
1. 删掉「模块名当工具」的行：`process_registry`、`command_canonicalize`、`command_ledger`、
   `crawl4ai`、`scratchpad_registry`；它们是模块/后端，不是注册的工具。
2. `config_audit` / `config_guide` / `read_config_guide` 一行收敛为 `config_audit` 与
   `read_config_guide`（真实注册的是这两个）。
3. `permission_tool` 一行删除（与 `permission` 重复，真名是 `permission`）。
4. 正文里 `code_exec` 与 `bash_exec` 接收 `code` / `command` 的说法改为
   `code_exec` 接收 `language` / `code`、`bash` 接收 `cmd`。
5. 「注册摘要」一节「内置工具不通过 builder 注册」是过期断言：`src/executor/builtin_registry/builder/`
   就是装配路径（`BuiltinToolRegistry::with_config()` → `builder/constructor/mod.rs`），改写成现状。
6. 目录补齐属于目录本身的真实工具（按 S4 的归类结果落位）：`workspace_manage`、`project_manage`、
   `runtime_manage`、`context_plugin`、`tool_usage`、`agent_update`、`agent_unbind`、
   `hub_catalog_search`、`browser_companion`、`session_decompress` 等。
- [x] **Step 1**: 按 1–5 改 zh/en 两页，保持标题骨架一致（G4 要求）。
- [x] **Step 2**: 跑 `python3 scripts/tool_audit.py --repo ../Aleph --docs content/docs --raw`，
      幽灵名应从 9 降到 0（`forget` 在 S2 修，`bash_exec` 的架构页调用点在 S2 修——本阶段先保证
      目录页不再宣称幽灵名）。
- [x] **Step 3**: 跑 `python3 scripts/run_gates.py --repo ../Aleph`。
**提交**：`docs(phase-S1): calibrate the builtin tool catalogue`

### Task S1.2 `tools/overview.mdx` + `concepts/builtin-tools.mdx`（zh + en）
**Files:**
- Modify: `content/docs/zh/tools/overview.mdx`
- Modify: `content/docs/en/tools/overview.mdx`
- Modify: `content/docs/zh/concepts/builtin-tools.mdx`
- Modify: `content/docs/en/concepts/builtin-tools.mdx`
**做什么：**
1. `tools/overview.mdx` 的「内置」一行里 `bash_exec` 改为 `bash`。
2. `concepts/builtin-tools.mdx` 复核「什么算内置工具」的定义，与代码的目录/注册表外/按请求注入
   三层结构对齐（`subagent`、`tool_search`、`get_tool_schema` 属于后两层）。
- [x] **Step 1**: 改 zh/en 四页。
- [x] **Step 2**: 跑 G1d 与全门。
**提交**：`docs(phase-S1): align the builtin tool concept pages`
---
## S2 — 工具调用面校准
### Task S2.1 调用点与参数表（zh + en）
**Files:**
- Modify: `content/docs/zh/architecture/tools.mdx`
- Modify: `content/docs/en/architecture/tools.mdx`
- Modify: `content/docs/zh/concepts/identity-context.mdx`
- Modify: `content/docs/en/concepts/identity-context.mdx`
- Modify: `content/docs/zh/tools/creating.mdx`
- Modify: `content/docs/en/tools/creating.mdx`
**做什么：**
1. `tool_use("bash_exec", {"command": "ls -la"})` → `tool_use("bash", {"cmd": "ls -la"})`
   （真参数字段是 `cmd`，不是 `command`）。
2. `allows_tool("bash_exec")` → `allows_tool("bash")`。
3. `tools/creating.mdx` 的 snake_case 示例 `bash_exec` → `bash`。
4. `architecture/tools.mdx` 的 `bash` / `code_exec` 参数表补齐并改名：
   - `bash`：`cmd`、`working_dir`、`timeout`、`allow_network`、`allow_subprocess`、
     `extra_writable_paths`、`background`、`process_action`、`process_id`、`justification`；
   - `code_exec`：`language`、`code`、`working_dir`、`timeout`、`allow_network`、
     `allow_subprocess`、`extra_writable_paths`、`justification`。
   线上字段名是 `timeout`（schemars rename），serde 仍接受 `timeout_seconds`。
5. `architecture/tools.mdx` 的 `subagent` 行核对：`subagent` 是真实工具（目录外注册，
   `src/agents/subagent_tool/mod.rs` 的 `SUBAGENT_TOOL_NAME`），描述「不在定义目录里」成立，保留并补出处。
- [x] **Step 1**: 改 zh/en 六页。
- [x] **Step 2**: 跑 `python3 scripts/tool_audit.py --repo ../Aleph --docs content/docs --raw`，
      幽灵名应降到 0。
- [x] **Step 3**: 跑全门。
**提交**：`docs(phase-S2): calibrate tool call sites and argument tables`

### Task S2.2 沙箱与执行架构页（zh + en）
**Files:**
- Modify: `content/docs/zh/architecture/{executor,sandbox,overview}.mdx`
- Modify: `content/docs/en/architecture/{executor,sandbox,overview}.mdx`
- Modify: `content/docs/zh/security/sandboxing.mdx`
- Modify: `content/docs/en/security/sandboxing.mdx`
**做什么：**
1. exec 类工具列表里的 `bash_exec` → `bash`（共 5 处/页对）。
2. 复核「exec 类工具通过沙箱层路由」的表述与代码一致：`bash` 与 `code_exec` 共用
   `Arc<dyn Sandbox>`，经 `SandboxCommand` 过接缝，driver 为 `OsSandboxDriver`。
3. `gateway/methods/memory.mdx` 的记忆工具表里的 `forget` 删除（代码里没有这个工具；删除事实走
   `remember` 的 Remove 操作），zh/en 同步。
- [x] **Step 1**: 改 zh/en 八页 + `gateway/methods/memory.mdx` 两页。
- [x] **Step 2**: 跑 G1d（幽灵应为 0）与全门。
**提交**：`docs(phase-S2): align sandbox and executor pages with the registered tool names`
---
## S3 — 后台作业与执行现状补齐
> 背景：`bash` 工具在 `main` 上已经有完整的后台作业面（`background: true` + `process_action`），
> 站点一个字都没写。模型每轮都在用这个面，读者却看不到它的边界。
### Task S3.1 `tools/builtin.mdx` + `architecture/sandbox.mdx`（zh + en）
**Files:**
- Modify: `content/docs/zh/tools/builtin.mdx`
- Modify: `content/docs/en/tools/builtin.mdx`
- Modify: `content/docs/zh/architecture/sandbox.mdx`
- Modify: `content/docs/en/architecture/sandbox.mdx`
**做什么：**
1. 在 `tools/builtin.mdx` 的「代码执行」小节补「后台作业」子节，事实全部来自
   `src/builtin_tools/bash_exec.rs` 与 `src/builtin_tools/process_registry.rs`：
   - `background: true` 立即返回 `process_id`，逃出 180 秒前台上限；
   - 后台默认 1 小时（`BACKGROUND_DEFAULT_TIMEOUT_SECS` = 3600），可调；
   - `process_action`：`poll`（运行中给 8 KB `partial_stdout`/`partial_stderr` 尾，完成后给完整
     `{exit_code, stdout, stderr}`）、`wait`（默认 60 秒窗口，上限 170 秒 `WAIT_MAX_TIMEOUT_SECS`）、
     `kill`、`list`；
   - 配额：每会话最多 8 个运行中（`MAX_RUNNING_PER_SESSION`）、全局 32（`MAX_RUNNING_GLOBAL`）、
     注册表 64 条（`MAX_ENTRIES`）；命令预览 120 字符（`COMMAND_PREVIEW_MAX`）；
   - 输出经 `src/builtin_tools/partial_output.rs` 脱敏，`src/builtin_tools/process_journal.rs` 记流水，
     `src/sandbox/live_tail.rs` 负责实时尾随；
   - 子进程环境变量 `ALEPH_SESSION_ID`、`ALEPH_TOOL_NAME=bash`。
2. `architecture/sandbox.mdx` 补一句：后台作业同样走沙箱接缝，后台只是不阻塞调用方。
- [x] **Step 1**: 改 zh/en 四页，事实逐条对源码。
- [x] **Step 2**: 跑全门 + `scripts/anchor_check.py` 复核新增路径锚点。
**提交**：`docs(phase-S3): document the background job surface of the bash tool`
---
## S4 — 未登记工具逐个落位或豁免
> 背景：G1d 报出 24 个「代码注册、站点没写」的工具。本阶段逐个定性：对外能力写进对应页，
> 内部观测面走豁免并写明理由。
### Task S4.1 24 个工具的定性、落位与豁免
**Files:**
- Modify: `content/docs/**`（按域落到具体页，zh + en）
- Modify: `scripts/tool_audit.py`（`EXEMPT_NAMES` + 理由）
**做什么：**
1. 逐个读代码定性（工具名 → 源码文件 → 语义）：
   - **协作 / team**：`session_read`、`session_collaborate`、`team_acp_member`、
     `lifecycle_idle`、`lifecycle_request_shutdown`、`lifecycle_resolve_shutdown`
     → `architecture/teams.mdx`；
   - **语音 / 通话**：`initiate_call`、`answer_call`、`call_status`、`hangup`
     → `tools/builtin.mdx` 的通信分组或既有语音页；
   - **运行时控制**：`memory_runtime_start`、`memory_runtime_stop`、`runtime_manage`
     → `architecture/memory.mdx` / `tools/builtin.mdx`；
   - **工作区 / 项目**：`workspace_manage`、`project_manage` → `tools/builtin.mdx`；
   - **agent 管理**：`agent_update`、`agent_unbind` → `tools/builtin.mdx`；
   - **浏览器**：`browser_companion` → `tools/browser.mdx`；
   - **hub**：`hub_catalog_search` → `tools/builtin.mdx` 或既有 hub 页；
   - **上下文插件**：`context_plugin` → `tools/builtin.mdx`；
   - **元 / 观测**：`tool_usage`、`cancel_output`、`get_tool_schema`、`tool_search`、
     `capability_projection_diagnostics` → 按「对外 / 内部」定性：
     对外能力写进 `tools/builtin.mdx`；纯内部诊断走 `EXEMPT_NAMES` 并在脚本里写明理由。
2. 每个落位都要 zh/en 同批改，保持标题骨架一致。
3. 收尾时 `python3 scripts/tool_audit.py --repo ../Aleph --docs content/docs --raw` 的未登记数降到 0
   （豁免项除外），棘轮 `tool_missing` 段。
- [x] **Step 1**: 逐个定性，产出「工具 → 落位页 / 豁免」对照表。
- [x] **Step 2**: 改页面（zh + en）。
- [x] **Step 3**: 跑 G1d 与全门，棘轮基线。
**提交**：`docs(phase-S4): place or exempt every registered builtin tool`
---
## S5 — 未合并分支能力标「规划中」
> 背景：`shell-capability-integration` `ed049d9ac`、`shell-capability-rework` `854505aa6`、
> `shell-capability-stdin` `523bfe4d0` 三个分支都**不在 `main`**。站点必须写「规划中 + 蓝图出处」，
> 不能写成现状。
### Task S5.1 shell 能力分支的现状 / 规划中切分
**Files:**
- Modify: `content/docs/zh/architecture/sandbox.mdx`
- Modify: `content/docs/en/architecture/sandbox.mdx`
- Modify: `content/docs/zh/security/sandboxing.mdx`
- Modify: `content/docs/en/security/sandboxing.mdx`
- Modify: `content/docs/zh/tools/builtin.mdx`
- Modify: `content/docs/en/tools/builtin.mdx`
**做什么：**
1. 三条未合并能力各写一个「规划中」横幅，并给出蓝图出处（带日期）：
   - **受监督的可恢复作业**（`shell-capability-rework`：`src/sandbox/shell_lifecycle.rs`、
     有界 stdin / 输出 drain / 子进程回收）→ 蓝图 `docs/superpowers/specs/2026-11-26-shell-capability-*.md`
     与回执 `docs/superpowers/runs/2026-11-26-shell-capability-rework-verification.md`；
   - **通用 stdin / EOF 准入**：该分支的结论是 **NO-GO**（最宽松策略仍有 16 条无条件文本阻断），
     写成「已评估、未采纳」并给证据位置；
   - **受控实时 JSONL stdin**：设计稿 `docs/superpowers/specs/2026-11-26-shell-capability-jsonl-design.md`，
     尚未实现。
2. 横幅里点明这些能力**不在 `main`**（`main` == `7fb540b44`），当前 `bash` 工具的现状仍以 S3 写的为准。
- [x] **Step 1**: 改 zh/en 六页。
- [x] **Step 2**: 跑全门（注意 G1/G1c 的免检规则：横幅行需带完成态/规划态标记）。
**提交**：`docs(phase-S5): mark unmerged shell capability work as planned`
---
## S6 — 术语 · 导航 · changelog
### Task S6.1 术语表、导航与 changelog
**Files:**
- Modify: `content/docs/zh/terminology.mdx`
- Modify: `content/docs/en/terminology.mdx`
- Modify: `content/docs/zh/changelog.mdx`
- Modify: `content/docs/en/changelog.mdx`
- Modify: `content/docs/meta.json`（若导航需要补条目）
**做什么：**
1. 术语表收录本轮新术语：内置工具名普查门（G1d）、工具目录 vs 注册表外 vs 按请求注入三层、
   后台作业（`background` / `process_action`）、目录外工具（`subagent` / `tool_search` /
   `get_tool_schema`）。
2. changelog 补 2026-11 第四轮条目（zh + en），带真实提交号。
3. 复核 `meta.json` 收录完整（G3 结构门会兜底，但导航顺序按逻辑微调）。
- [x] **Step 1**: 改四页 + 必要时 `meta.json`。
- [x] **Step 2**: 跑全门（含 `--build`）。
**提交**：`docs(phase-S6): refresh terminology navigation and changelog`
---
## S7 — 终验
### Task S7.1 `docs/VERIFICATION-2026-11-pass4.md`
**Files:**
- Create: `docs/VERIFICATION-2026-11-pass4.md`
- Modify: `scripts/verification_report.py`（按提交信息 `docs(phase-SN)` 推导阶段归属；`--build` 自动跑 G5）
**做什么：**
1. 逐页判定表（zh/en 各页一列：页面 / 判定 / 依据 / 门结果）。
2. 附七门输出（含 G5）、基线九段、仍未文档化的工具清单（应为 0 或只剩显式豁免项）、
   仍标「规划中」的条目清单及其蓝图出处。
3. 报告脚本沿用第三轮做法：判定词用「沿用前轮」，阶段归属从提交信息推导。
- [x] **Step 1**: 跑全部七门（含 `--build`）。
- [x] **Step 2**: 生成逐页判定表。
- [x] **Step 3**: 列出所有「规划中」条目及其蓝图出处、所有豁免工具及理由。
**提交**：`docs(phase-S7): add the fourth-pass verification report`
---
## Self-Review
1. **Spec 覆盖**：ROADMAP 的 S0–S7 每阶段都有对应 Task（S0→S0.1/S0.2；S1→S1.1/S1.2；S2→S2.1/S2.2；
   S3→S3.1；S4→S4.1；S5→S5.1；S6→S6.1；S7→S7.1）——无遗漏。
2. **步骤可执行性**：每个 Task 的 Step 都指向真实文件与真实命令；S4 的 24 个工具清单来自 G1d 首跑，
   在执行时用 `--json` 重新导出核对，不依赖记忆。
3. **接口一致性**：全篇统一用「工具目录 / 注册表外 / 按请求注入」「幽灵名」「未登记工具」
   「后台作业」「规划中」这些术语，zh/en 一致。
4. **Review Focus 覆盖**：①工具名写错 → S1.1 Step 2、S2.1 Step 2；②模块名当工具 → S1.1 Step 1；
   ③参数名写错（`command` vs `cmd`）→ S2.1 Step 4；④未合并分支被写成现状 → S5.1；
   ⑤门禁盲区（工具名从不被任何门检查）→ S0.1；⑥豁免滥用 → S4.1 要求逐条写理由。
5. **不做的事**：不改 Aleph 代码仓；不合并未合并分支；不放宽门禁口径。
