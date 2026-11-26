# Aleph 文档站第三轮对齐执行计划（2026-11-26）

> 对应 ROADMAP：`docs/ROADMAP-2026-11-pass3.md`
> 真值基线：Aleph `main` = `7fb540b44`（第二轮基线 `7a6986bc9`）
> 方法沿用第二轮：roadmap → phase spec（本文）→ 逐阶段过门 → 终验报告

## 阶段总览

| 阶段 | 目标 | Task |
|---|---|---|
| S0 | 门禁加固与基线盘点 | S0.1 |
| S1 | 能力模型按收敛后现状重写 | S1.1、S1.2 |
| S2 | 记忆自我进化按落地行为重写 | S2.1、S2.2 |
| S3 | 协议与方法面补齐 | S3.1、S3.2 |
| S4 | Panel 与桌面壳新模块 | S4.1、S4.2 |
| S5 | 沙箱 · 上下文压缩 · 扩展重载 | S5.1、S5.2 |
| S6 | 全站符号与锚点校准 | S6.1、S6.2 |
| S7 | 术语 · 导航 · changelog | S7.1、S7.2 |
| S8 | 终验报告 | S8.1 |

---

## S0 — 门禁加固与基线盘点

### Task S0.1 `scripts/method_audit.py` + 本轮台账

**Files:**
- Modify: `scripts/method_audit.py`
- Create: `docs/ROADMAP-2026-11-pass3.md`
- Create: `docs/superpowers/plans/2026-11-26-aleph-docs-calibration-pass3.md`

**做什么：**

1. `method_audit.py` 的 census 解析补上**常量条目**：`src/gateway/method_census.rs` 里
   `aleph_protocol::chat_transcript::CHAT_TRANSCRIPT_DETAILS_METHOD` 这类写法，旧正则只认字面量，
   于是 `chat.transcript_details` 在门眼里不存在。新增 `CENSUS_CONST_RE` 与 `protocol_constants()`，
   把 `pub const NAME: &str = "..."` 解析进方法集。修完 G1b 应报出 2 条「已注册未文档化」。
2. 盘点失效清单并存档到 `/tmp`（不入库），作为 S1–S6 的待办底账：
   - G1：30 条锚点失效，全在 `capabilities/{capability-model,hooks-and-prompts,trust-and-backends}.mdx`（zh + en）。
   - G1b：`chat.transcript_details`、`pty.history`。
   - G1c：148 条符号失效，74 个 zh 页 + 74 个 en 页对。

- [ ] **Step 1**: 改 `scripts/method_audit.py`，跑 `python3 scripts/method_audit.py --repo ../Aleph`，确认 missing 集合变成 2 条。
- [ ] **Step 2**: 跑 `anchor_check.py`、`symbol_check.py` 存档失效清单。
- [ ] **Step 3**: 写 ROADMAP 与本文。

**提交**：`docs(gates): resolve constant-registered RPC methods in the census gate`

---

## S1 — 能力模型按收敛后现状重写

> 背景：Zahir 收敛删除了 `src/capability/{activation,ambient,audit,grant,lifecycle}.rs`，
> 换成了 census 派生规则 + 版本化注册表 + 投影宿主 + 效果声明。
> 蓝图：`docs/superpowers/specs/2026-11-25-zahir-capability-convergence-design.md`（Aleph 仓），
> 回执：`docs/superpowers/runs/2026-11-25-zahir-convergence-receipt.md`（Aleph 仓）。

### Task S1.1 `capabilities/capability-model.mdx`（zh + en）

**Files:**
- Modify: `content/docs/zh/capabilities/capability-model.mdx`
- Modify: `content/docs/en/capabilities/capability-model.mdx`

**做什么：**

- 删除被删模块的现状断言：`src/capability/activation.rs`、`src/capability/lifecycle.rs`、
  `src/capability/ambient.rs`、`src/capability/audit.rs`、`src/capability/grant.rs`，
  以及符号 `LifecycleState`、`CapabilityLifecycle::transition_to`、`validate_activation`、
  `validate_runtime`、`NotInvocable`、`CapabilityActivationController`、`GrantRegistry`、`is_invocable`、`time_remaining`。
- 改写为当前结构：
  - `src/capability/mod.rs` 的 `CapabilitySlot<T>` / `MutableCapabilitySlot<T>`、`MissingSemantics`、`Outcome`（含 `install` / `decline` / `get` / `outcome`）。
  - `src/capability/census.rs` 的**派生成员规则**：句柄 iff 其所在文件自己安装它（写入式 / 首调用者胜出式），懒缓存不算成员——「派生，不是名单」。
  - `src/capability/descriptor.rs`、`ownership.rs`、`policy.rs` / `policy_runtime.rs`、`events.rs`、`ui_surface.rs`、`constraints.rs`。
  - `src/capability/projection_host.rs`、`versioned_registry.rs`、`effect_claim.rs`、`event_audience.rs`、
    `diagnostic_control.rs`、`special_dispatch.rs`、`production_init.rs`、`provider.rs` / `provider_backend.rs` / `provider_registry.rs`。
  - `src/capability/zahir_facade.rs` 的 `ResolveError::DependencyUnavailable`（依赖未就绪时报给模型，不再假装可用）。
- 被删内容按 ROADMAP 第六节处置 2/3：整体改写为当前路径，或移入 `## 历史：…` 并标注删除来源提交
  （`459c4fe96` / `8507aff30` / `4cb16e5b6`）。

- [ ] **Step 1**: 读 `src/capability/{mod,census,descriptor,ownership,policy,events,ui_surface,projection_host,versioned_registry,effect_claim,event_audience,diagnostic_control,special_dispatch,production_init,zahir_facade}.rs` 的公开面。
- [ ] **Step 2**: 逐条替换被删模块与旧符号（grep 确认 30 条锚点与 9 条符号归零）。
- [ ] **Step 3**: 改写 zh 页 + 同步 en 页（`##` 骨架一致）。
- [ ] **Step 4**: 跑 `symbol_check.py --repo ../Aleph` 与 `anchor_check.py --repo ../Aleph`，确认该页零失效。

### Task S1.2 `capabilities/{trust-and-backends,hooks-and-prompts,slots-and-replacement,plugin-package}.mdx`（zh + en）

**Files:**
- Modify: `content/docs/zh/capabilities/{trust-and-backends,hooks-and-prompts,slots-and-replacement,plugin-package}.mdx`
- Modify: `content/docs/en/capabilities/{trust-and-backends,hooks-and-prompts,slots-and-replacement,plugin-package}.mdx`

**做什么：**

- `trust-and-backends.mdx`：删 `GrantRegistry`、`LegacyCapabilityHandler`、`src/capability/grant.rs`、`src/capability/audit.rs`；
  改写为「谁授予、谁记账、谁只读」：授权来自宿主显式授予（`src/extension/capability.rs::ContextGrant` 绑定 descriptor 指纹），
  版本化注册表（`src/capability/versioned_registry.rs`）是发布原语，投影宿主（`projection_host.rs`）负责对外暴露。
- `hooks-and-prompts.mdx`：删 `src/capability/audit.rs` 锚点，改写审计相关表述为当前事件与效果声明（`events.rs` / `effect_claim.rs`）。
- `slots-and-replacement.mdx`、`plugin-package.mdx`：按 `crates/aleph-slot-api/` 与 `src/capability/` 当前符号对齐。

- [ ] **Step 1**: grep 各页失效符号，按四种处置判定。
- [ ] **Step 2**: 改写 8 个文件（4 页 × zh/en）。

**提交**：`docs(phase-S1): rewrite the capability model around the converged surface`

---

## S2 — 记忆自我进化按落地行为重写

> 蓝图：`docs/superpowers/specs/2026-11-25-memory-self-evolution-closure-design.md`（Aleph 仓），
> 计划：`docs/superpowers/plans/2026-11-25-memory-self-evolution-closure.md`，
> 终验：`docs/superpowers/runs/2026-11-25-memory-self-evolution-closure-verification.md`（均 Aleph 仓）。

### Task S2.1 `concepts/memory.mdx` + `architecture/memory.mdx`（zh + en）

**Files:**
- Modify: `content/docs/zh/{concepts,architecture}/memory.mdx`
- Modify: `content/docs/en/{concepts,architecture}/memory.mdx`

**做什么：**

- 检索重排函数改名：`cosine_rerank`、`recency_boost`、`length_normalization`、`time_decay`、`hard_min_score`
  在 `src/memory/assembler/rerank.rs` 已不是现名——按代码真名改写，并核对 `src/memory/assembler/hybrid.rs` 的融合顺序。
- 补齐落地的自进化闭环：
  - 反馈归属：召回命中记到**实际提供该笔记的语料库**，不再记到提问方语料库（`src/memory/assembler/feedback_floor.rs`、`src/memory/reflector/`）。
  - 纠正入库：`src/memory/store/markdown/raw_memory.rs` 的 append 顺序（每语料库冻结旧水位）。
  - Dream 依赖就绪：`src/memory/dreaming/stages/feedback_run.rs` / `feedback_state.rs`——缺依赖 fail-closed，不覆盖上次运行。
  - 发布—验证—退役：`src/memory/notes/indexer/distill_effect.rs`——先发布并验证后继，再退役原文。
  - 反馈批次恢复：`src/memory/store/sqlite/feedback_kv.rs`——原子游标推进。
- 被删/改名的旧行为按处置 2/3 处理。

- [ ] **Step 1**: 读 `src/memory/assembler/{rerank,hybrid,feedback_floor}.rs`、`src/memory/reflector/`、`src/memory/dreaming/stages/{feedback_run,feedback_state}.rs`、`src/memory/notes/indexer/distill_effect.rs`、`src/memory/store/sqlite/feedback_kv.rs`。
- [ ] **Step 2**: grep 5 个失效重排符号的真名。
- [ ] **Step 3**: 改写 4 个文件。

### Task S2.2 `architecture/memory-evolution.mdx` + `gateway/methods/memory.mdx`（zh + en）

**Files:**
- Modify: `content/docs/zh/architecture/memory-evolution.mdx`、`content/docs/zh/gateway/methods/memory.mdx`
- Modify: `content/docs/en/architecture/memory-evolution.mdx`、`content/docs/en/gateway/methods/memory.mdx`

**做什么：**

- `memory-evolution.mdx`：把蓝图态改成**落地态**——列出已实现的顺序契约（raw 纠正 append 序、水位冻结、后继发布—验证—退役、反馈覆盖/持久意图/回执、原子游标），并明确「没有第二策展器、没有通用日志、没有自动回滚」。
- `gateway/methods/memory.mdx`：核对 `src/gateway/handlers/memory/` 与 `src/gateway/handlers/dreaming.rs` 当前方法与投影；
  补 `src/memory/extensions/first_party.rs` 相关的工具面。

- [ ] **Step 1**: 读 `src/gateway/handlers/memory/{mod,memory_scope}.rs`、`src/gateway/handlers/dreaming.rs`。
- [ ] **Step 2**: 改写 4 个文件。

**提交**：`docs(phase-S2): document the landed memory self-evolution contracts`

---

## S3 — 协议与方法面补齐

### Task S3.1 两个新 RPC 方法入册

**Files:**
- Modify: `content/docs/zh/gateway/methods/{index,chat}.mdx`、`content/docs/zh/gateway/protocol-v1.mdx`
- Modify: `content/docs/en/gateway/methods/{index,chat}.mdx`、`content/docs/en/gateway/protocol-v1.mdx`

**做什么：**

- `chat.transcript_details`（`Class::Open`，常量 `shared/protocol/src/chat_transcript.rs::CHAT_TRANSCRIPT_DETAILS_METHOD`）：
  写清请求/响应 DTO（`ChatTranscriptDetailsRequest`、`ChatTranscriptDetails`、`ChatRunDetail`、`ChatToolDelta`、`ChatToolChange`），
  以及它在 transcript 渲染链路中的位置（`src/gateway/handlers/chat_presentation.rs`、`src/gateway/handlers/trace_replay/chat_details.rs`）。
- `pty.history`（`Class::Admin`，`src/gateway/pty/screen/history.rs`）：写清历史屏幕读取与
  `pty.attach` / `pty.input` / `pty.close` 的关系（`src/gateway/handlers/pty.rs`、`src/gateway/pty/manager.rs`）。

- [ ] **Step 1**: 读 `shared/protocol/src/chat_transcript.rs`、`src/gateway/handlers/chat_presentation.rs`、`src/gateway/pty/screen/history.rs`。
- [ ] **Step 2**: 改写 6 个文件。

### Task S3.2 记忆图协议面

**Files:**
- Modify: `content/docs/zh/gateway/methods/memory.mdx`、`content/docs/zh/gateway/protocol-v1.mdx`
- Modify: `content/docs/en/gateway/methods/memory.mdx`、`content/docs/en/gateway/protocol-v1.mdx`

**做什么：**

- 补 `shared/protocol/src/memory_graph.rs` 的三个方法与 DTO：`graph.query`（`GRAPH_QUERY_METHOD`）、`graph.search`（`GRAPH_SEARCH_METHOD`）、
  `graph.node_detail`（`GRAPH_NODE_DETAIL_METHOD`）；DTO 形如 `NoteNodeDto`、`NoteLinkDto`、`GraphQueryResponse`、`NoteDetailResponse`、`NoteAddress`。
- 核对 `src/gateway/handlers/graph/` 的实现路径。

- [ ] **Step 1**: 读 `shared/protocol/src/memory_graph.rs`、`src/gateway/handlers/graph/{mod,query}.rs`、`src/gateway/handlers/graph_types.rs`。
- [ ] **Step 2**: 改写 4 个文件。

**提交**：`docs(phase-S3): add the new transcript and history protocol surfaces`

---

## S4 — Panel 与桌面壳新模块

### Task S4.1 TSX Panel 外壳与聊天切片

**Files:**
- Modify: `content/docs/zh/desktop-hosts/{panel,panel-runtime,plugin-ui}.mdx`
- Modify: `content/docs/en/desktop-hosts/{panel,panel-runtime,plugin-ui}.mdx`

**做什么：**

- 外壳：`interfaces/panel/shell/Shell.tsx`、`Sidebar.tsx`、`CommandPalette.tsx`、`Settings.tsx`、`commands.ts`、`prefs.ts`，
  偏好模型 `shared/ui_logic/src/prefs/{appearance,commands}.rs`。
- 聊天切片：`interfaces/panel/modules/Chat.tsx` 与 `interfaces/panel/modules/chat/*`（`TranscriptList`、`ToolCard`、`Diff`、`ContextSheet`、`MessageBody`、`output.ts`），
  共享渲染逻辑 `shared/ui_logic/src/transcript/`（`chat_panel.rs`、`reducer/chat_tool.rs`、`mermaid.rs`、`context.rs`）。
- 连续性与滚动：`docs/superpowers/specs/2026-11-25-nsh-panel-r6-session-continuity-design.md`（Aleph 仓）——
  有界 scrollback（`shared/ui_logic/src/panel/projection.rs`）、会话重连保持。
- 协议：`shared/protocol/src/session_thread.rs`、`shared/protocol/src/terminal_mutation.rs`。

- [ ] **Step 1**: 读 `interfaces/panel/shell/`、`interfaces/panel/modules/chat/`、`shared/ui_logic/src/transcript/`、`shared/ui_logic/src/prefs/`。
- [ ] **Step 2**: 改写 6 个文件。

### Task S4.2 记忆星云与终端外壳

**Files:**
- Modify: `content/docs/zh/desktop-hosts/{overview,panel}.mdx`
- Modify: `content/docs/en/desktop-hosts/{overview,panel}.mdx`

**做什么：**

- Memory Nebula：`interfaces/panel/modules/MemoryNebula.tsx`、`NebulaCanvas.tsx`、`modules/nebulaViewport.ts`，
  布局与投影 `shared/ui_logic/src/nebula/{layout,vec3,fnv1a}.rs`；蓝图 `docs/superpowers/specs/2026-11-24-memory-nebula-nsh-design.md`（Aleph 仓）。
- 终端：`interfaces/webchat/tabs/terminal-ui/src/{host,session,tabs,view,recovery}.rs` 与 `shared/ui_logic/src/terminal_mutation.rs`；
  蓝图 `docs/superpowers/specs/2026-11-24-panel-terminal-rework-design.md`（Aleph 仓）。
- `desktop-hosts/overview.mdx` 的 IPC 矩阵补上本轮新增的本地目标限制。

- [ ] **Step 1**: 读 `interfaces/panel/modules/{MemoryNebula,NebulaCanvas}.tsx`、`shared/ui_logic/src/nebula/`、`interfaces/webchat/tabs/terminal-ui/src/`。
- [ ] **Step 2**: 改写 4 个文件。

**提交**：`docs(phase-S4): document the new Panel shell, nebula and transcript surfaces`

---

## S5 — 沙箱 · 上下文压缩 · 扩展重载

### Task S5.1 执行边界与上下文压缩

**Files:**
- Modify: `content/docs/zh/architecture/sandbox.mdx`、`content/docs/zh/security/sandboxing.mdx`、`content/docs/zh/concepts/execution-engine.mdx`
- Modify: `content/docs/en/architecture/sandbox.mdx`、`content/docs/en/security/sandboxing.mdx`、`content/docs/en/concepts/execution-engine.mdx`

**做什么：**

- 沙箱：owned worktree + 挂载型 OS 驱动（`src/sandbox/{worktree,driver,command,context,factory,scrub,summary}.rs`、
  `src/sandbox/platforms/linux/bwrap.rs`、`src/sandbox/workspace/mod.rs`）；蓝图 `docs/superpowers/specs/2026-11-25-sandbox-execution-boundary-design.md`（Aleph 仓）。
- 上下文压缩接线：`src/context/compact/manual.rs` 与 `src/gateway/execution_engine/` 的挂载点；
  蓝图 `docs/superpowers/specs/2026-11-25-context-compaction-wiring-design.md`（Aleph 仓）。
- 恢复记账：`docs/superpowers/specs/2026-11-25-context-recovery-accounting-design.md`（Aleph 仓）。

- [ ] **Step 1**: 读上述源文件与两份蓝图的现状段落。
- [ ] **Step 2**: 改写 6 个文件。

### Task S5.2 扩展重载预检

**Files:**
- Modify: `content/docs/zh/concepts/extensions.mdx`、`content/docs/zh/concepts/extension-system.mdx`
- Modify: `content/docs/en/concepts/extensions.mdx`、`content/docs/en/concepts/extension-system.mdx`

**做什么：**

- `src/extension/lifecycle.rs` 的重载预检：先预检新版本，再拆掉运行中的旧版本（提交 `084453b9d`）；
  对齐 `src/extension/runtime/wasm/mod.rs` 的生产接线边界。

- [ ] **Step 1**: 读 `src/extension/lifecycle.rs` 与 `src/extension/runtime/wasm/mod.rs`。
- [ ] **Step 2**: 改写 4 个文件。

**提交**：`docs(phase-S5): align sandbox, context compaction and extension reload`

---

## S6 — 全站符号与锚点校准

> 148 条符号失效（74 zh + 74 en）+ 30 条锚点失效。按 ROADMAP 第六节四种处置逐条判定。
> 主要来源：被删模块的符号（`GrantRegistry`、`LifecycleState`、`CapabilityActivationController` 等）、
> 改名后的旧名（`ContextAnchor`、`FactType`、`DeviceRole`、`DeviceType`、`EvolutionStatus`、`ExperimentId`、
> `VariantId`、`ContextId`、`TraceRole`、`RunContext`、`SmartFilter`、`ContextRuleLayer`、`SubagentOrchestrator`、
> `ToolProgressCallback`、`AudioStubProvider`、`ClaudeVisionProvider`、`SkillPrefetcher`、`pcm_input`、`cdp_port`、
> `sandbox_override`、`file_mkdir`、`file_chmod`、`memory_forget`、`llm_context`、`CapabilityConstraintContextSource`、
> `DesktopCapability`、`FlowRunTool`、`FromIterator`、`MockFoo`、重排函数 5 个等）。

### Task S6.1 概念 · 架构 · 哲学页

**Files:** `content/docs/{zh,en}/{architecture,concepts,philosophy,development,terminology}.mdx`（仅涉及失效符号的页面）

**做什么：** 逐条判定 → 改写为代码真名 / 改写为当前路径 / 移入 `## 历史：…` / 标「规划中」。

- [ ] **Step 1**: `python3 scripts/symbol_triage.py --repo ../Aleph --out /tmp/triage-pass3.json`。
- [ ] **Step 2**: 逐 token 在 Aleph 仓 `rg` 确认真名或确认已删。
- [ ] **Step 3**: 改写并同步 en 页。

### Task S6.2 剩余页面与基线归零

**Files:** 其余失效页面（`gateway/methods/browser.mdx`、`capabilities/*` 复查等）

- [ ] **Step 1**: 改写剩余页面。
- [ ] **Step 2**: 跑 `symbol_check.py --repo ../Aleph` 与 `anchor_check.py --repo ../Aleph`，确认基线外零失效。

**提交**：`docs(phase-S6): clear the symbol and anchor rot introduced by the new Aleph main`

---

## S7 — 术语 · 导航 · changelog

### Task S7.1 术语与导航

**Files:**
- Modify: `content/docs/zh/terminology.mdx`、`content/docs/en/terminology.mdx`
- Modify: `content/docs/zh/**/meta.json`、`content/docs/en/**/meta.json`

**做什么：** 收录本轮新术语（census 派生成员规则、版本化注册表、投影宿主、效果声明、事件受众、诊断控制、
聊天转录、记忆图、记忆星云、有界 scrollback、会话连续性、owned worktree、上下文压缩接线、重载预检）；
清理与旧术语冲突的条目。

- [ ] **Step 1**: 校对两份术语表。
- [ ] **Step 2**: 跑 `freshness_audit.py --check structure --docs content/docs` 确认无漏收。

### Task S7.2 changelog

**Files:**
- Modify: `content/docs/zh/changelog.mdx`、`content/docs/en/changelog.mdx`

**做什么：** 补 26.11 → 26.12 真实条目：能力模型收敛、记忆自进化闭环、聊天转录与记忆图协议、
Panel 新外壳与星云、沙箱执行边界、上下文压缩接线、扩展重载预检、终端重做。每条带日期与提交出处。

- [ ] **Step 1**: `git -C ../Aleph log --since=2026-11-24 --oneline` 抽真实条目。
- [ ] **Step 2**: 改写两份 changelog。

**提交**：`docs(phase-S7): refresh terminology, navigation and changelog`

---

## S8 — 终验

### Task S8.1 `docs/VERIFICATION-2026-11-pass3.md`

**Files:**
- Create: `docs/VERIFICATION-2026-11-pass3.md`

**做什么：** 逐页判定表（164 zh 页 + 164 en 页），列「页面 / 判定 / 依据 / 门结果」；
附六门输出（含 G5）、基线八段、仍标「规划中」的条目清单与蓝图出处。

- [ ] **Step 1**: 跑全部六门（含 `--build`）。
- [ ] **Step 2**: 生成逐页判定表。
- [ ] **Step 3**: 列出所有「规划中」条目及其蓝图出处。

**提交**：`docs(phase-S8): add the third-pass verification report`

---

## Self-Review

1. **Spec 覆盖**：ROADMAP 的 S0–S8 每阶段都有对应 Task（S0→S0.1；S1→S1.1/S1.2；S2→S2.1/S2.2；S3→S3.1/S3.2；
   S4→S4.1/S4.2；S5→S5.1/S5.2；S6→S6.1/S6.2；S7→S7.1/S7.2；S8→S8.1）——无遗漏。
2. **步骤可执行性**：每个 Task 的 Step 都指向真实文件与真实命令；S6 的失效符号清单在执行时由
   `symbol_triage.py` 生成，其余清单已在本计划中写死。
3. **接口一致性**：全篇统一用「census 派生成员规则」「版本化注册表」「投影宿主」「效果声明」「事件受众」
   「诊断控制」「聊天转录」「记忆图」「记忆星云」「有界 scrollback」「会话连续性」「owned worktree」
   「上下文压缩接线」「重载预检」这 14 个术语，zh/en 一致。
4. **Review Focus 覆盖**：①模块已删却写成现状 → S1.1 Step 2、S2.1 Step 3、S6.1；②改名误判 → S6.1 Step 2；
   ③虚构方法名 → S3 Step 1–2（常量与 DTO 一律抄源码）；④双语漂移 → 各 Task 的同步步骤；
   ⑤门禁盲区（常量方法名）→ S0.1 Step 1。
