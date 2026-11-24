# Aleph 文档对齐执行计划 · 第二轮（2026-11-24）

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 把 Aleph-docs 从「第一轮校准后的 26.9.1 早期状态」推进到「2026-11-24 代码真值（HEAD `7a6986bc9`）」，覆盖 Panel 模型迁移、Protocol v1 深化、Gateway 冷声明、跨平台桌面 IPC，并**清零全站 448 条符号级失效**。

**Architecture:** 沿用第一轮的「真值分层 + 三态约定 + 六门」框架。文档正文由并行 subagent 按互斥文件集改写，主 agent 负责门校验、基线棘轮与合并。机器判定优先于人工抽查：新增的符号门（G1c）把「反引号里的标识符是否还存在」变成可棘轮的自动检查。

**Tech Stack:** Next.js 16 + Fumadocs（i18n，zh/en）+ TypeScript + Tailwind；校验脚本为纯 Python 3（`scripts/`）；真值来源为 Aleph Rust 仓库 `/home/zou/data/workspace/Aleph`。

**Spec:** [docs/ROADMAP-2026-11-pass2.md](../../ROADMAP-2026-11-pass2.md)（真值分层、三态约定、六门、阶段路线、符号校准判定规则）。配套：[docs/ROADMAP-2026-11.md](../../ROADMAP-2026-11.md)（第一轮）、[docs/VERIFICATION-2026-11.md](../../VERIFICATION-2026-11.md)（第一轮终验）。

## Global Constraints

- 文档站仓库：`/home/zou/data/workspace/Aleph-docs`。代码仓库（**只读真值**）：`/home/zou/data/workspace/Aleph`，VERSION 26.9.1，HEAD `7a6986bc9`。
- **不改 Aleph 代码仓**，只读它取事实。
- **不得编造**：RPC 方法名、Rust/TS 类型名、配置键、crate 名、`just` recipe、文件路径——一律从 Aleph 仓源码抄，抄不到就删掉该断言。
- **现状断言必须带锚点**：路径 + 符号双锚（`src/capability/descriptor.rs` 的 `CapabilityDescriptor`）。只有路径锚点、符号写不出来的段落，改写或删除。
- **蓝图内容一律标「规划中」**：T3 来源是 `docs/research/` 四份蓝图（含 `Everything-externally-composable-is-a-Capability.md`），必须带 `> **状态：规划中**` 横幅 + 蓝图出处。
- **历史内容不删**：移入页面内 `## 历史：<主题>` 小节，行内加「已删除 / 已移除 / 已废弃 / renamed to」等标记。
- 构建门命令：`pnpm exec next build`、`pnpm exec tsc --noEmit`、`pnpm exec eslint`。
- 每阶段一次提交，提交信息 `docs(phase-SN): <主题>`，正文记录六门结果。**不 push**（除非用户另行授权）。
- zh 与 en 由同一 subagent 一起产出；每个 subagent 独占文件集，**不碰 `meta.json`**。
- 基线棘轮只降不升：每阶段结束跑 `python3 scripts/symbol_check.py --repo ../Aleph --update-baseline`，并把被修复的条目数写进提交信息。

## Review Focus

这一轮最容易翻车的五个点，按可能性排序：

1. **把改名当成删除** —— `MediaAttachment`/`MailAttachment`、`require_consent`/`requires_user_consent`、`enable_tool_search`/`enable_search` 这类只差一个词的，误判成「模块已删」会让页面丢掉真实存在的能力。判定前必须先在代码仓 grep 近似名。
2. **把已删模块写成现状** —— `TaskGraph`、`DaemonEvent`、`WorldModel`、`QuickSetupFlow`、`permissive_default` 在代码里 grep 全无，但文档仍在描述它们。正确处置是改写为当前路径（`src/tools/registry.rs`、`src/loop_graph/`、`src/tasks/cron/`）或移入历史小节，而不是留一句「已不存在」的现状句。
3. **虚构 crate 名 / just recipe** —— `aleph-server` 是 **bin** 不是 package；`aleph-panel-ui` 是新 package；`just panel-tsx-bundle` 是新 recipe。写错会让 G1c 门在下一阶段红。
4. **双语漂移** —— zh 改了 en 没改（或只改 zh 的标题骨架），G4 门会红；更糟的是两边语义不同但门只查标题。
5. **引入了新的符号失效** —— 改写时顺手写了个看起来合理的类型名。这类是 G1c 门的「基线外新失效」，必须在 subagent 交付前自查。

---

## S0 — 工具与基线

### Task S0.1 `scripts/symbol_check.py`（符号门 G1c）

**Files:**
- Create: `scripts/symbol_check.py`
- Create: `scripts/symbol_triage.py`
- Modify: `scripts/run_gates.py`
- Modify: `scripts/baseline.json`

**Interfaces:**
- Consumes: `--repo <path>`（默认 `../Aleph`）、`--update-baseline`、`--json`。
- Produces: 退出码 1 = 存在基线外新失效；`scripts/baseline.json` 的 `symbol` 段（棘轮键：`页面: 符号不存在: token`）。

**做什么**：从 Aleph 仓 `git ls-files --recurse-submodules` 收集源码标识符全集（后缀 `rs|ts|tsx|js|mjs|py|swift|sh|toml|json|yml|yaml` 或 `justfile`），扫描站点反引号内的候选 token，判定其是否存在。候选规则：含 `::`、以 `()` 结尾、小写下划线且长度 > 4、或 CamelCase。`## 历史/规划中/已废弃/Deprecated/Planned` 小节内的行免检。crate 形状 `aleph-*` 须命中 Cargo.toml 的 `[package]` 或 `[[bin]]` name。`just <target>` 须命中 justfile recipe。

- [ ] **Step 1**: 实现 `known_symbols()` / `known_crates()` / `known_just_targets()` 三个采集函数。
- [ ] **Step 2**: 实现候选 token 抽取与四类免检（历史小节、通用词 allowlist、双下划线、非代码 token）。
- [ ] **Step 3**: 实现 crate / just 检查，避免 `aleph-server`（bin）这类误报。
- [ ] **Step 4**: 接入 `gate_baseline.py` 的 `load_baseline` / `split_violations` / `update_section`，段名 `symbol`。
- [ ] **Step 5**: 实现 `scripts/symbol_triage.py`（`difflib.get_close_matches(cutoff=0.82`）把失效 token 分 RENAME / GONE，输出 JSON。
- [ ] **Step 6**: `scripts/run_gates.py` 增加第六门 G1c。
- [ ] **Step 7**: 跑 `--update-baseline` 建立 `symbol` 段基线（现存 448 条）。
- [ ] **Step 8**: 验证 `python3 scripts/run_gates.py --repo ../Aleph` 六门全绿。

### Task S0.2 修复 Panel 模型迁移遗留的失效锚点

**Files:**
- Modify: `content/docs/zh/desktop-hosts/panel-runtime.mdx`
- Modify: `content/docs/en/desktop-hosts/panel-runtime.mdx`

**做什么**：提交 `2f541e81a` 把 Panel 模型四件（discovery / projection / registry / source）从 `interfaces/webchat/src/panel/` 搬到 `shared/ui_logic/src/panel/`。站点两页共 20 条路径锚点失效。

- [ ] **Step 1**: 把 `interfaces/webchat/src/panel/{discovery,projection,registry,source}.rs` 全部改为 `shared/ui_logic/src/panel/<同名>.rs`。
- [ ] **Step 2**: 验证 `python3 scripts/anchor_check.py --repo ../Aleph` → 失效 0。

**提交**：`docs(phase-S0): add the symbol gate and ratchet the second-pass baseline`

---

## S1 — Panel 架构重写

> 本阶段回答「Panel 到底是什么」。第一轮把 Panel 写成「`interfaces/webchat/` 里的 Leptos 单页应用」，而代码现在把**模型**和**渲染器**拆开了：`shared/ui_logic/src/panel/` 是与运行时无关的模型（只依赖 `aleph_protocol`），`interfaces/panel/` 是新的 TSX 渲染器，`interfaces/webchat/` 仍是 Leptos 渲染器。两者读同一份模型实现。

### Task S1.1 `desktop-hosts/panel-runtime.mdx`（zh + en）

**Files:**
- Modify: `content/docs/zh/desktop-hosts/panel-runtime.mdx`
- Modify: `content/docs/en/desktop-hosts/panel-runtime.mdx`

**做什么**：按当前代码重写页面骨架：
- 模型层：`shared/ui_logic/src/panel/` 的 `registry.rs`（`TabRegistry`、`BUILTIN_NAMESPACE = "aleph"`）、`projection.rs`（`PanelProjection`、`PanelRoute`）、`discovery.rs`（`PanelDiscoveryState`、`PanelDiscoveryStatus`、`SnapshotUpdate`）、`source.rs`、**新增** `layout.rs`（`PanelLayout`、`LayoutSlot`、`LayoutRepair`、`RestoredLayout`、`LAYOUT_VERSION = 1`、`layout_storage_key`）。
- 渲染器层：`interfaces/webchat/`（Leptos，`aleph-panel`）与 `interfaces/panel/`（TSX，`aleph-panel-ui`，`nsh.json` 的 id `com.aleph.panel`，host 能力 `aleph.rpc` / `aleph.pair` / `aleph.connect` / `aleph.connection`）。
- 布局持久化语义：布局只存稳定 `PanelTabKey` 与纯数据，不存描述符/条目/权限；恢复时快照不再提供的 tab 渲染为占位且**永不执行**（`LayoutSlot::Unavailable`）。
- 协议：`shared/protocol/src/panel.rs` 的 `PANEL_UI_API_MAJOR = 1`、`panel.capabilities.snapshot`、`panel.project.select`、`x-aleph-panel-project-generation`、`PANEL_HOST_UNAVAILABLE = -32090`。

- [ ] **Step 1**: 读 `shared/ui_logic/src/panel/{mod,registry,projection,discovery,source,layout}.rs` 全文，确认每个符号名与语义。
- [ ] **Step 2**: 读 `interfaces/panel/{nsh.json,src/lib.rs,web/host.js}`，确认 TSX 侧宿主契约与内置 tab（overview / sessions / capabilities）。
- [ ] **Step 3**: 重写 zh 页，保持 `##` 骨架。
- [ ] **Step 4**: 同步重写 en 页，骨架逐节对应。
- [ ] **Step 5**: 自查 `python3 scripts/symbol_check.py --repo ../Aleph` 与 `anchor_check.py` 无新增。

### Task S1.2 `desktop-hosts/panel.mdx`（zh + en）

**Files:**
- Modify: `content/docs/zh/desktop-hosts/panel.mdx`
- Modify: `content/docs/en/desktop-hosts/panel.mdx`

**做什么**：现有页面只讲 Leptos Panel 的 `just wasm` → `rust_embed` 刷新链。需补：
- 两套渲染器的存在与选择：Leptos WASM（`interfaces/webchat/`，`just wasm` / `just check-dist`）与 TSX（`interfaces/panel/`，`just panel-tsx-bundle` / `just panel-tsx-test` / `just panel-tsx-web`）。
- NSH 嵌入面：`desktop/nsh-shell/src/panel_surface.rs`（原生组件 `aleph/panel-surface`，bundle 经 `include_str!` 编入壳内，`desktop/nsh-shell/src/panel_host.rs` 提供 `aleph.rpc` 等四个宿主函数）、`desktop/nsh-shell/build.rs` 在 `tsx-panel` feature 下缺 bundle 即编译失败。
- 保持 Leptos 刷新链（`rust_embed` 嵌入目录由 `src/gateway/control_plane/assets.rs` 的 `folder` 指定）作为「仍存在的另一条链」，明确两者关系。

- [ ] **Step 1**: 读 `desktop/nsh-shell/src/{panel_surface,panel_host}.rs`、`desktop/nsh-shell/build.rs`、`desktop/nsh-shell/Cargo.toml` 的 `tsx-panel` feature。
- [ ] **Step 2**: 读 Aleph 仓 justfile 的 `panel-tsx-*` 与 `wasm` recipe，确认 recipe 名与依赖。
- [ ] **Step 3**: 重写 zh 页 + 同步 en 页。

### Task S1.3 `desktop-hosts/plugin-ui.mdx`（zh + en）

**Files:**
- Modify: `content/docs/zh/desktop-hosts/plugin-ui.mdx`
- Modify: `content/docs/en/desktop-hosts/plugin-ui.mdx`

**做什么**：现有页面写「插件 Panel 标签页」只走 Leptos 侧（`interfaces/webchat/src/panel/`，feature `panel-modular`）。需补 TSX 宿主契约一侧：`interfaces/panel/web/host.js`（浏览器适配：`/v1/ws` 帧、id 关联、`system.hello`、连接事件）与 `desktop/nsh-shell/src/panel_host.rs`（桌面侧：Desktop IPC 由操作系统认证，故 `aleph.pair` 直接返回错误；非本地目标报 `unavailable`）。

- [ ] **Step 1**: 读 `interfaces/panel/web/host.js` 与 `desktop/nsh-shell/src/panel_host.rs` 的函数契约。
- [ ] **Step 2**: 改写 zh 页 + 同步 en 页，明确「一个 SDK 面、两个宿主适配器」。

**提交**：`docs(phase-S1): rewrite the Panel architecture around the shared model`

---

## S2 — Protocol v1 深化

### Task S2.1 `gateway/protocol-v1.mdx`（zh + en）

**Files:**
- Modify: `content/docs/zh/gateway/protocol-v1.mdx`
- Modify: `content/docs/en/gateway/protocol-v1.mdx`

**做什么**：当前页面写「v1 尚未落地」且说 NSH 仍走旧 `/ws`——**已过时**。需改写为现状：
- 单一方法集：`src/gateway/server/connection/mod.rs:103` 的 `V1_METHODS`（`health`、`sessions.list`、`aleph_protocol::panel::PANEL_UI_CAPABILITY_SNAPSHOT_METHOD`）与 `v1_mounted()`（原先两处各写一份，现已合并）。
- `system.hello` 的 `subject`：`shared/protocol/src/system_hello.rs` 的 `HelloResult.subject: Option<String>`——**不透明 per-user 值**，供 Panel 布局作客户端存储键，**不是身份**；旧 `/ws` 或无 key 时缺省。
- `shared/protocol/src/panel.rs` 的面板方法常量与 `PanelUiCapabilitySnapshot`。
- Web v1 入口在 TLS 路由下挂 `/v1/panel/` 静态 web 包（`src/gateway/server/connection/web_v1.rs:122`）。
- 保留「蓝图 vs 现状」的边界：`docs/research/NSH_PROTOCOL_V1.md` 里未落地的部分仍标「规划中」。

- [ ] **Step 1**: 读 `shared/protocol/src/system_hello.rs`、`shared/protocol/src/panel.rs`、`src/gateway/server/connection/{mod,web_v1}.rs`。
- [ ] **Step 2**: 重写 zh 页 + 同步 en 页。

### Task S2.2 `gateway/protocol.mdx` + `architecture/gateway.mdx`（zh + en）

**Files:**
- Modify: `content/docs/zh/gateway/protocol.mdx`、`content/docs/zh/architecture/gateway.mdx`
- Modify: `content/docs/en/gateway/protocol.mdx`、`content/docs/en/architecture/gateway.mdx`

**做什么**：`/ws` 页保持「历史兼容入口」定位，但补上它与 v1 的关系现状（v1 已落地，Desktop IPC 与 Web v1 是新客户端接入面）。`architecture/gateway.mdx` 同步 v1 入口矩阵。

- [ ] **Step 1**: 核对 `src/gateway/server/mod.rs` 的路由挂载与 `src/gateway/server/connection/upgrade.rs`。
- [ ] **Step 2**: 改写四个文件。

**提交**：`docs(phase-S2): document the shipped Protocol v1 surface`

---

## S3 — 能力模型深化

### Task S3.1 `capabilities/capability-model.mdx`（zh + en）

**Files:**
- Modify: `content/docs/zh/capabilities/capability-model.mdx`
- Modify: `content/docs/en/capabilities/capability-model.mdx`

**做什么**：页面已有骨架（描述符 / 所有权 / 可见性 / 策略 / 后端解析），需按 `src/capability/` 39 文件的真实状态校准：
- 描述符 `src/capability/descriptor.rs`、所有权 `src/capability/ownership.rs`、可见性 `src/capability/ownership.rs` + `src/scope/`（`authority.rs` / `carried.rs` / `directory.rs`）、事件 `src/capability/events.rs`（`CapabilityEvent` / `CapabilityEventType`）、策略 `src/capability/policy.rs` + `policy_runtime.rs`、后端 `src/capability/{backend,provider_backend,provider_registry}.rs`、生命周期 `src/capability/lifecycle.rs`、UI 表面 `src/capability/ui_surface.rs`、facade `src/capability/zahir_facade.rs`。
- 契约 crate `crates/aleph-slot-api/`（41 文件）：`capability.rs`、`descriptor.rs`、`handler.rs`、`hooks.rs`、`approval.rs`、`ai*.rs`、`search.rs`、`embedding.rs`、`channel.rs`、`concurrency.rs`、`cancellation.rs`、`error.rs`、`metadata.rs`。
- 挂载状态：哪些模块已挂生产路径、哪些只是「写好了测了没挂」（页面已有 Callout，需按代码复核）。

- [ ] **Step 1**: 读 `src/capability/` 各关键文件与 `crates/aleph-slot-api/src/lib.rs`。
- [ ] **Step 2**: 校准挂载状态清单，每条带文件锚点。
- [ ] **Step 3**: 改写 zh 页 + 同步 en 页。

### Task S3.2 `capabilities/plugin-package.mdx` / `trust-and-backends.mdx` / `slots-and-replacement.mdx`（zh + en）

**Files:**
- Modify: `content/docs/zh/capabilities/{plugin-package,trust-and-backends,slots-and-replacement}.mdx`
- Modify: `content/docs/en/capabilities/{plugin-package,trust-and-backends,slots-and-replacement}.mdx`

**做什么**：对齐 `src/capability/` 与 `crates/aleph-slot-api` 的真实符号；`slots-and-replacement` 当前有 2 条符号失效，一并按 S5 规则处置。

- [ ] **Step 1**: grep 各页失效符号，判定改名 / 已删 / 历史三种处置。
- [ ] **Step 2**: 改写 6 个文件。

**提交**：`docs(phase-S3): align the capability model pages with src/capability`

---

## S4 — 冷声明与跨平台桌面 IPC

### Task S4.1 `gateway/methods/channels.mdx`（zh + en）

**Files:**
- Modify: `content/docs/zh/gateway/methods/channels.mdx`
- Modify: `content/docs/en/gateway/methods/channels.mdx`

**做什么**：增写 Gateway 通道**冷声明**生命周期（对齐 `docs/reference/GATEWAY.md` 的「Cold declarations / 冷声明」小节）：
- `enabled = false` 留在 Config；boot **不做** vault 水合、**不构造** adapter。
- `channel.create` 先保存再返回 `disabled`；配置落盘后才把**本次明确提供**的受支持凭据一次写入 vault（不支持的嵌套凭据 / vault 失败 → 报错，**不回退明文**）。
- `channels.list` / `channels.status` 显示冷声明，且**不声明运行能力**。
- `channel.start` 校验最新配置与策略、要求工厂返回同一 ID、先发布策略再启动 adapter、**不改写磁盘 enabled**。
- send / stop 仍需运行实例；delete 可删冷声明；**不提供热更新**。

- [ ] **Step 1**: 读 `docs/reference/GATEWAY.md` 的冷声明小节与 `src/gateway/handlers/channels*.rs`。
- [ ] **Step 2**: 增写 zh 页 + 同步 en 页，标出「规划中 vs 现状」的边界。

### Task S4.2 `desktop-hosts/overview.mdx`（zh + en）

**Files:**
- Modify: `content/docs/zh/desktop-hosts/overview.mdx`
- Modify: `content/docs/en/desktop-hosts/overview.mdx`

**做什么**：增写跨平台桌面 IPC 矩阵：
- Unix：`shared/client/src/local_ipc/` 的 socket 路径与权限。
- Windows：`shared/client/src/local_ipc/windows.rs`（`validate_endpoint` 要求 `\\.\pipe\` 前缀、`PipeAccount::current` / `PipeAccount::create`、服务端 PID 校验）、`src/gateway/server/connection/local_ipc/windows.rs`（`NamedPipeServer` + 账户绑定）、`desktop/nsh-shell/src/ipc_status.rs`。
- NSH 通过 Desktop IPC 连本地 Gateway；TSX Panel 的桌面侧只支持本地目标，非本地报 `unavailable`（`desktop/nsh-shell/src/panel_host.rs`）。

- [ ] **Step 1**: 读 `shared/client/src/local_ipc/windows.rs` 与 `src/gateway/server/connection/local_ipc/windows.rs`。
- [ ] **Step 2**: 改写 zh 页 + 同步 en 页。

**提交**：`docs(phase-S4): document cold declarations and cross-platform desktop IPC`

---

## S5 — 符号校准（全站）

> 本阶段把 `scripts/baseline.json` 的 `symbol` 段从 389 条降到 **0**。判定规则见 [ROADMAP 第六节](../ROADMAP-2026-11-pass2.md#六s5-符号校准的判定规则唯一裁决口径)。

### Task S5.1 分包改写（按 section 切分，互斥文件集）

**Files:** 按下表分配，每包由一个 subagent 负责 zh + en 同名页对。

| 包 | 页面（zh + en 同名） | 主要失效符号 | 判定重心 |
|---|---|---|---|
| **S5-A** | `concepts/thinker.mdx`、`concepts/core-types.mdx`、`concepts/intent-detection.mdx`、`concepts/looping-goal-strategy.mdx` | `ThinkerConfig`、`ThinkerContext`、`LlmMatcher`、`TodoView`、`ScratchpadLayer`、`PromptBudget`、`transient_recall` | 对齐 `src/thinker/layers/` 39 个真实 layer 与 `src/thinker/context.rs` 的 `EnvironmentContract` / `VoiceContext` / `TurnEnvelope` / `ResolvedContext` / `ContextAggregator` |
| **S5-B** | `concepts/messages.mdx`、`concepts/search.mdx`、`concepts/wizard.mdx`、`concepts/memory.mdx`、`concepts/event-system.mdx`、`concepts/prompt-system.mdx` | `CuratedHotMemory`、`SearchProviderType`、`QuickSetupFlow`、`ProviderSetupFlow`、`usage_mode`、`risk_class` | 对齐 `src/wizard/`、`src/memory/`、`src/event/`（`EventType` 现仅 10 个 Team/SubAgent/Process 变体） |
| **S5-C** | `architecture/worldmodel.mdx`、`architecture/proactive-dispatcher.mdx`、`architecture/dispatcher.mdx`、`architecture/groupchat.mdx`、`architecture/clawhub.mdx`、`architecture/memory.mdx`、`architecture/session-service.mdx`、`architecture/routing.mdx`、`architecture/resilience.mdx`、`architecture/teams.mdx`、`architecture/tools.mdx`、`architecture/executor.mdx`、`architecture/thinker.mdx`、`architecture/a2a.mdx`、`architecture/acp.mdx`、`architecture/cluster.mdx`、`architecture/design-patterns.mdx`、`architecture/providers.mdx`、`architecture/harness.mdx`、`architecture/sessions.mdx`、`architecture/desktop-bridge.mdx` | `WorldModel`、`TaskGraph`、`DaemonEvent`、`GroupChatCommandParser`、`SlotResolver`、`release_instance_lock` | 删除的模块改写为当前路径：`src/loop_graph/`、`src/tools/registry.rs`、`src/tasks/cron/` + `src/tasks/heartbeat/`、`src/group_chat/`、`src/hub/` |
| **S5-D** | `automation/events.mdx`、`automation/cron-jobs.mdx`、`automation/hooks.mdx`、`api/rust.mdx`、`philosophy/domain-modeling.mdx`、`philosophy/redlines.mdx`、`cli/{agent,commands,config,gateway}.mdx`、`tools/{browser,creating,mcp}.mdx`、`development/{design-patterns,testing}.mdx`、`development/building.mdx`、`development/contributing.mdx`、`security/pairing.mdx`、`interfaces/{discord,imessage,webchat}.mdx` | `ConfigReloaded`、`SessionCreated`、`ToolCallFailed`、`CapturedContext`、`AuthProfileManager`、`LoggingCallback`、`process_with_tools` | `automation/events.mdx` 的事件表整体对齐 `shared/protocol/src/events.rs` 的 `StreamEvent` 与 `src/capability/events.rs` |
| **S5-E** | `terminology.mdx`、`changelog.mdx`、`gateway/methods/{arena,channels,config,extensions,memory,providers}.mdx`、`concepts/{a2a-protocol,agent-runtime,approval,arena,browser-automation,bundled,capability-system,clarification,clawhub,discovery,domain-model,error-handling,markdown-utils,media-processing,supervisor-verification,task-scheduling}.mdx` | 零散改名与 crate 名 | 与 S1–S4 已改页面保持术语一致；`terminology.mdx` 收录本轮新术语 |

- [ ] **Step 1**: 每个包先跑 `python3 scripts/symbol_triage.py --repo ../Aleph --out /tmp/triage-<包>.json` 拿到 RENAME / GONE 候选。
- [ ] **Step 2**: 对每个失效 token，在 Aleph 仓 `rg` 一次确认真名或确认已删。**近似匹配只是线索**。
- [ ] **Step 3**: 按 ROADMAP 第六节的四种处置改写页面（改名同步 / 路径已删 → 改写当前路径 / 移入 `## 历史：…` / 标规划中）。
- [ ] **Step 4**: 同步改写 en 页，保持 `##` 骨架一致。
- [ ] **Step 5**: 每个包交付前跑 `python3 scripts/symbol_check.py --repo ../Aleph` 与 `anchor_check.py`，确认该包页面无基线外新失效。
- [ ] **Step 6**: 主 agent 合并后跑 `python3 scripts/symbol_check.py --repo ../Aleph --update-baseline`，把 `symbol` 段收到剩余量。

### Task S5.2 术语与页面一致性收尾

**Files:**
- Modify: `content/docs/zh/terminology.mdx`、`content/docs/en/terminology.mdx`

**做什么**：确认本轮新术语（Panel 模型 / TSX Panel / Desktop IPC / 冷声明 / `subject` / `PanelTabKey` / `LayoutSlot`）在术语表里有定义，且旧术语（`TabRegistry` 旧位置、`PanelShell`）不残留矛盾条目。

- [ ] **Step 1**: 校对两份术语表。
- [ ] **Step 2**: 确认 `symbol` 基线为 0（或仅剩明确豁免项）。

**提交**：`docs(phase-S5): clear the site-wide symbol rot`

---

## S6 — 术语 · 导航 · changelog

### Task S6.1 `meta.json` 收录

**Files:**
- Modify: `content/docs/zh/**/meta.json`、`content/docs/en/**/meta.json`

**做什么**：确认本轮新增/改写的页面都在某个 `meta.json` 的 `pages` 里，且顺序合理。

- [ ] **Step 1**: 跑 `python3 scripts/freshness_audit.py --check structure --repo ../Aleph` 确认无漏收。

### Task S6.2 `changelog.mdx`

**Files:**
- Modify: `content/docs/zh/changelog.mdx`
- Modify: `content/docs/en/changelog.mdx`

**做什么**：补 26.9.1 → 26.11 的真实条目（Panel 模型迁移、TSX Panel、Protocol v1 单一方法集、冷声明、Windows IPC），每条带日期与提交/文档出处。

- [ ] **Step 1**: 从 `git -C ../Aleph log --since=2026-09-24 --oneline` 抽取真实条目。
- [ ] **Step 2**: 改写两份 changelog。

**提交**：`docs(phase-S6): refresh navigation, terminology and changelog`

---

## S7 — 终验

### Task S7.1 `docs/VERIFICATION-2026-11-pass2.md`

**Files:**
- Create: `docs/VERIFICATION-2026-11-pass2.md`

**做什么**：逐页判定表（164 zh 页 + 164 en 页），列「页面 / 判定 / 依据 / 门结果」；附六门输出、符号基线归零证据、仍标「规划中」的条目清单。

- [ ] **Step 1**: 跑全部六门（含 `--build`）。
- [ ] **Step 2**: 生成逐页判定表。
- [ ] **Step 3**: 列出所有「规划中」条目及其蓝图出处。

**提交**：`docs(phase-S7): add the second-pass verification report`

---

## Self-Review

1. **Spec 覆盖**：ROADMAP 的 S0–S7 每阶段是否都有对应 Task？（S0→Task S0.1/S0.2；S1→S1.1–S1.3；S2→S2.1/S2.2；S3→S3.1/S3.2；S4→S4.1/S4.2；S5→S5.1/S5.2；S6→S6.1/S6.2；S7→S7.1）—— 已覆盖，无遗漏阶段。
2. **步骤可执行性**：每个 Task 的 Step 是否都指向真实的文件、真实的代码路径、真实的命令？—— 是；唯一需要执行时补充的是 S5 各包的具体失效符号清单（由 `symbol_triage.py` 在执行时生成）。
3. **接口一致性**：各 Task 之间是否共享了同一个符号命名与路径事实？（Panel 模型路径 `shared/ui_logic/src/panel/`、协议常量 `shared/protocol/src/panel.rs`、能力目录 `src/capability/`、IPC 路径 `shared/client/src/local_ipc/windows.rs` —— 全文一致。）
4. **Review Focus 覆盖**：五个高风险点分别落在哪个 Task 的哪个 Step？—— ①改名误判→S5.1 Step 2；②已删模块写成现状→S5.1 Step 3；③虚构 crate/recipe→S5.1 Step 5 + S1.2 Step 2；④双语漂移→S5.1 Step 4 + S1 各 Step；⑤新引入符号失效→S5.1 Step 5。
5. **比例**：代码/工具占比低（仅 S0），文档内容占比高（S1–S7），符合本轮性质——这是一次文档对齐轮次，工具只有一个新脚本。
