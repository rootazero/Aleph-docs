# Aleph 文档校对执行计划（2026-11-24）

> 配套框架文档：[docs/ROADMAP-2026-11.md](../../ROADMAP-2026-11.md)（真值分层、三态约定、五道门、阶段路线）。
> 本文件是可执行清单：每阶段列出具体文件、具体动作、具体验证命令。

## 目标

把 Aleph-docs 从「2026-07-29 基线（Aleph 26.7.21）」推进到「Aleph 26.9.1 真实代码状态」，覆盖三条新增主线（NSH 桌面宿主、Protocol v1、能力模型与模块化），并剔除 5948 次提交累积的过时描述。产出物是文档站本身 + 两道可复用的校验脚本 + 逐页判定台账。

## 前提与约束

- 文档站仓库：`/home/zou/data/workspace/Aleph-docs`（Next 16 + Fumadocs i18n，pnpm）。
- 代码仓库（只读真值）：`/home/zou/data/workspace/Aleph`（VERSION 26.9.1，HEAD `4f966eaf6`）。
- **不改 Aleph 代码仓**，只读它取事实。
- 构建门命令：`pnpm exec next build`、`pnpm exec tsc --noEmit`、`pnpm exec eslint`。
- 依赖安装：`pnpm install --frozen-lockfile --ignore-scripts`（21s），随后 `pnpm exec fumadocs-mdx` 重新生成 `.source/`。
- 每阶段一次提交，只推文档站；不 push 到 origin（除非用户另行授权）。
- 提交信息：`docs(phase-RN): <主题>`，正文记录五门结果。

## 任务总览

| 阶段 | 任务 | 依赖 |
|---|---|---|
| R0 | 校验脚本 + 逐页基线审计 | — |
| R1 | 桌面宿主改写为 NSH（删 Tauri 文档、补 NSH） | R0 |
| R2 | Protocol v1 与传输矩阵 | R1 |
| R3 | 能力模型与模块化 | R2 |
| R4 | Panel 与插件 UI | R3 |
| R5 | 子系统补齐与过时剔除 | R4 |
| R6 | 术语表 · 导航 · changelog | R5 |
| R7 | 终验 | R6 |

---

## R0 — 校验脚本与逐页基线审计

### Task R0.1 `scripts/anchor_check.py`（锚点门 G1）

**文件**：新建 `scripts/anchor_check.py`

**做什么**：扫描 `content/docs/{zh,en}/**/*.mdx`，提取反引号包裹且以已知源码根开头的路径 token（`src/` `desktop/` `shared/` `crates/` `interfaces/` `plugins/` `scripts/` `qa/` `tests/` `docs/` `config.toml` `Cargo.toml` `Justfile`），到 Aleph 仓库（`--repo`，默认 `../Aleph`）核对存在性。路径含 `{}`/`*`/`<>` 占位或以 `/` 结尾（目录通配）时跳过并计为 `skipped`。输出 `path:line: token` 列表，退出码 1 当有未命中。

**验证**：
```bash
cd /home/zou/data/workspace/Aleph-docs
python3 scripts/anchor_check.py --repo ../Aleph | tail -20   # 期望：列出真实失效锚点
python3 scripts/anchor_check.py --repo ../Aleph > /tmp/anchors.txt; echo $?
```

### Task R0.2 `scripts/freshness_audit.py`（G2/G3/G4）

**文件**：新建 `scripts/freshness_audit.py`

**做什么**，四个子检查，可单独 `--check {facts,structure,bilingual,all}`：
- **facts**：正则黑名单（旧枚举 `CapabilityDeclaration` 的旧变体、`aleph-bridge` Swift 助手作为现行架构、`desktop/shared/src/bridge/client.rs` 之外的失效路径、由锚点门报出的路径命中）、以及站点内「Tauri v2 薄壳」类现状断言（`Tauri` 与 `薄`/`原生桌面应用`/`shell` 同句出现即报）。
- **structure**：每个 `meta.json` 的 `pages` 列出的文件都存在；每个 `mdx` 都被至少一个 `meta.json` 收录；站内相对链接 `](./x)` 与 `](../y/z)` 解析后指向存在的 mdx。
- **bilingual**：`zh` 与 `en` 的 mdx 相对路径集合完全相同；同名页面的 `##` 标题序列相同。
- 输出按检查分组，退出码非 0 即失败。

**验证**：
```bash
python3 scripts/freshness_audit.py --check all --repo ../Aleph
```

### Task R0.3 `docs/AUDIT-2026-11.md`（逐页判定基线）

**文件**：新建 `docs/AUDIT-2026-11.md`；参考既有 `docs/AUDIT.md`（2026-07-27）的判定词表（REWRITE / UPDATE / OK / NEW）。

**做什么**：为 153 个 zh 页面逐页给出判定 + 一句话理由 + 归属阶段（R1–R5）。表格列：`页面` / `判定` / `理由` / `阶段`。

**验证**：
```bash
grep -cE '^\| `[a-z0-9-]+/' docs/AUDIT-2026-11.md   # 期望 153
```

---

## R1 — 桌面宿主改写为 NSH

口径见 ROADMAP 第六节。**不保留 Tauri 主题文档**。

### Task R1.1 新建 `desktop-hosts/` 章节（zh + en）

**文件**（各 3 页 × 2 语言 = 6 个新文件）：
- `content/docs/zh/desktop-hosts/overview.mdx` + `en/…`
- `content/docs/zh/desktop-hosts/panel.mdx` + `en/…`
- `content/docs/zh/desktop-hosts/plugin-ui.mdx` + `en/…`

**内容锚点**（必须从源码抄，不得编造）：
- `desktop/nsh-shell/Cargo.toml`：`aleph-nsh-shell`，nsh 0.6.0（`nsh-core`/`nsh-base`/`nsh-engine`），feature `embedded-core`（依赖 `aleph-desktop-host` 的 `gateway-admission`）、`qa-service`。
- `desktop/nsh-shell/src/connection.rs`：`DAEMON_URL = "ws://127.0.0.1:18790"`、`build_hello_params()` 发 `system.hello`，`ProtocolVersion { major: 1, minor: 0 }`，`ClientHello { name: "aleph-nsh-desktop", platform, ui_runtime: "nsh" }`，`features = [EventReplay, Snapshot, BinaryChannel]`；重连 2s→30s 上限、10 次连续失败上限、连接超时 40s。
- `desktop/nsh-shell/src/main.rs`：CLI `--connect <origin> | --autostart-status | --desktop-ipc-status <socket>`；**不启动/停止/重配服务**；注册 `aleph` URL scheme。
- `desktop/nsh-shell/src/panel_bridge.rs` 与 `shared/protocol/src/panel_shell.rs`：Panel↔Shell 通道（`ShellRequest`/`PanelReply`/`CredentialCall`/`CredentialReply`）。
- `desktop/host/src/local_server.rs`：`ensure_ready()`、18790 端口探测、`PortOccupant{Free,DaemonReady,DaemonBooting,Foreign}`。
- `desktop/nsh-shell/src/{supervisor,autostart,credentials,ipc_status,session,platform,shell_host}.rs` 各自职责。
- Panel 挂载：`interfaces/webchat`（Rust/Leptos），`panel-modular` 为 opt-in feature，`PanelShell` 渲染点 `interfaces/webchat/src/app.rs`。

**验证**：G1–G5 全绿；页面内每条现状断言都能在 G1 报告里找到对应「命中」。

### Task R1.2 改写含 Tauri 的既有页面（zh + en）

**文件**：
- `content/docs/{zh,en}/architecture/1-2-3-4-model.mdx`：平台表（macOS/Windows/Linux → NSH 宿主）、桌面桥接表（→ 原生能力层）、R2 行（宿主改为 NSH）、仓库树 `shell/` → `nsh-shell/` + `host/`。
- `content/docs/{zh,en}/architecture/overview.mdx`：壳核分离段落、ASCII 架构图、仓库树。
- `content/docs/{zh,en}/index.mdx`：首页同段。
- `content/docs/{zh,en}/philosophy/redlines.mdx`：R1/R2 表述，删掉 Tauri 举例。
- `content/docs/{zh,en}/interfaces/webchat.mdx`：协议使用者列表。
- `content/docs/{zh,en}/development/contributing.mdx`：`desktop` crate 说明。
- `content/docs/{zh,en}/development/building.mdx`：仓库树 + **过渡期提示**（发布流水线当前仍构建 `desktop/shell`，无 NSH 发布流水线；标注「将删除」）。
- `content/docs/{zh,en}/security/overview.mdx`：「approve / reject Tauri 命令」→「审批命令」。
- `content/docs/{zh,en}/security/ipc.mdx` 与 `gateway/auth.mdx`：`tauri:` scheme 条目改为按 NSH 实际 origin 处理（NSH 走 `ws://127.0.0.1:18790` / `ws://127.0.0.1:18790/ws`），并说明该 scheme 属过渡期。

**不动的文件**：`content/docs/{zh,en}/changelog.mdx` 的历史条目保留（那是历史记录）。

### Task R1.3 桌面桥接页重写

**文件**：`content/docs/{zh,en}/architecture/desktop-bridge.mdx`

**做什么**：从「Rust 核心 spawn Swift 助手」改为「原生能力层」：`desktop/shared/src/traits/*`（`screen`/`ax`/`system`/`media`/`permission`/`automation`/`power`/`pim`）、`desktop/macos/src/*`、`desktop/linux`、`desktop/windows`；`src/builtin_tools/desktop/` 的两条输入轨道（targeted / global，`Rail` 枚举，`allow_global_pointer` 门控）；`shared/protocol/src/desktop_bridge/`（`envelope.rs` 的 JSON-RPC 2.0 `Request`/`Response`/`ErrorResponse`/`Notification`，`methods/{bridge,ax,input,media,perm,pim,screen}.rs`，`METHOD_HANDSHAKE = "bridge.handshake"`、`METHOD_PING = "bridge.ping"`、超时常量）；Swift 助手路径 `desktop/macos/bridge/`（macOS PIM 委托）。

**验证**：G1–G5 全绿。

---

## R2 — Protocol v1 与传输矩阵

**新建**：`content/docs/{zh,en}/gateway/protocol-v1.mdx`
**改写**：`content/docs/{zh,en}/gateway/protocol.mdx`、`architecture/gateway.mdx`、`api/jsonrpc.mdx`

**锚点**：`shared/protocol/src/framing.rs`（`HEADER_BYTES = 4`、`DEFAULT_MAX_PAYLOAD_BYTES = 8_388_608`、大端 u32、`encode_header`/`decode_header`/`split_frame`、`FrameError{Empty,Oversize,InvalidUtf8}`）、`shared/protocol/src/system_hello.rs`（`ProtocolVersion`、`ClientHello`、`ServerHello`、`HelloLimits`、`Feature`）、`src/gateway/handlers/system_hello.rs`、`src/gateway/server/connection/{rpc,local_ipc,web_v1}.rs`（`--desktop-ipc` Unix 只读 IPC；Web v1 原生 TLS `POST /v1/session` + `GET /v1/ws`）、`src/gateway/server/connection/rpc.rs` 共享分发、`shared/client/src/connection/requests.rs` pending calls。

蓝图 `docs/research/NSH_PROTOCOL_V1.md` 只在「规划中」小节引用。

---

## R3 — 能力模型与模块化

**新建** `content/docs/{zh,en}/capabilities/`：`capability-model.mdx`、`slots-and-replacement.mdx`、`trust-and-backends.mdx`、`hooks-and-prompts.mdx`、`plugin-package.mdx`
**改写** `content/docs/{zh,en}/concepts/capability-system.mdx`（旧 `src/extension/capability.rs` 枚举 → 保留在 `## 历史：` 小节）

**锚点**：`src/capability/`（39 文件：descriptor、grant、policy、policy_runtime、effect_claim、backend、provider_registry、special_dispatch、versioned_registry、ui_surface、zahir_facade、projection_host、census、ambient、audit、ownership、lifecycle、constraints、activation、production_init 等）、`src/scope/{authority,carried,directory,mod}.rs`、`crates/aleph-slot-api/src/`（slot、capability、descriptor、approval、cancellation、channel、concurrency、hooks、tool、webhook、embedding、search、browser/、ai*、error*、metadata、text、handler）、`src/extension/{capability,plugin_trust}.rs` + `effects/` `hooks/` `manifest/` `registry/` `runtime/` `panel_publication/` `marketplace/`。

蓝图 `Everything-externally-composable-is-a-Capability.md` 与 `aleph_modularization_plan.md` 一律标「规划中」。

---

## R4 — Panel 与插件 UI

**新建**：`content/docs/{zh,en}/desktop-hosts/panel.mdx`、`plugin-ui.mdx`（R1 只建骨架页，本阶段填满）
**锚点**：`interfaces/webchat/src/app.rs`、`interfaces/webchat/Cargo.toml` 的 `panel-modular` feature、`src/capability/ui_surface.rs`、`src/extension/panel_publication/`、`shared/protocol/src/panel_shell.rs`、ADR-003/005/009（`docs/research/NSH_ADR-001~009.md`，标「规划中」）。

---

## R5 — 子系统补齐与过时剔除

逐个判定并处理（判定基线见 `docs/AUDIT-2026-11.md`）：goal、teams、runtimes、cluster、projects、tool_output、looping、verification、export、strategy、guardrails、vision、tool_metadata、scope。规模参考（文件/行）：goal 4/5269、teams 15/7096、runtimes 11/6444、cluster 7/5700、projects 8/4309、tool_output 9/3387、looping 3/3025、verification 9/2720、export 6/1875、strategy 5/1525、guardrails 5/1357、vision 4/618、tool_metadata 4/451。

过时内容处理口径：**重写 + 把关键决策保留在 `## 历史：` 小节**。

---

## R6 — 术语表 · 导航 · changelog

- `content/docs/{zh,en}/terminology.mdx`：补 NSH、Protocol v1、Capability、Slot、Zahir 等新词。
- 全部 `meta.json`：新增 `desktop-hosts`、`capabilities` 顶层章节，挂载 `gateway/protocol-v1`。
- `content/docs/{zh,en}/changelog.mdx`：补 26.8–26.11 真实版本序列（取自 Aleph `CHANGELOG.md` 与 `docs/superpowers/runs/`）。

---

## R7 — 终验

- 新建 `docs/VERIFICATION-2026-11.md`：逐页判定表（153 zh + 153 en 全部判定完毕）、五门结果、遗留清单。
- 跑完整门：
```bash
cd /home/zou/data/workspace/Aleph-docs
python3 scripts/anchor_check.py --repo ../Aleph
python3 scripts/freshness_audit.py --check all --repo ../Aleph
pnpm exec next build && pnpm exec tsc --noEmit && pnpm exec eslint
```

---

## 执行纪律

1. 每个 subagent 拿到的文件集互不重叠；`meta.json` 只由主 agent 改。
2. subagent 输出必须自证：给出改动文件列表 + 每个现状断言的源码路径。
3. 主 agent 复核：跑五门 + 抽查每阶段 5 处锚点是否真的对应代码。
4. 阶段未过门不得进入下一阶段，也不得提交。
5. 任何一处需要编造才能自圆其说的内容 —— 删掉或标「规划中」，不猜。

---

## 阶段台账（执行记录）

### R0 — 校验脚本与逐页基线审计 ✅

产出 `scripts/anchor_check.py`（G1）、`scripts/freshness_audit.py`（G2/G3/G4）、`scripts/method_audit.py`（G1b）、
`scripts/run_gates.py`、`scripts/gate_baseline.py`、`scripts/audit_baseline.py`、`scripts/file_issues.py`、
`scripts/suggest_names.py`、`scripts/baseline.json`、`docs/AUDIT-2026-11.md`（153 zh 页逐页判定 + 9 待新建页）。

### R1 — 桌面宿主改写为 NSH ✅

- 新建 `content/docs/{zh,en}/desktop-hosts/{overview,panel,plugin-ui}.mdx`（后续 R4 补 `panel-runtime.mdx`）。
- 重写 `content/docs/{zh,en}/architecture/{desktop-bridge,overview,1-2-3-4-model}.mdx`。
- 定点修订 `index.mdx`、`philosophy/redlines.mdx`、`security/{overview,ipc}.mdx`、`gateway/auth.mdx`、
  `development/{contributing,building}.mdx`、`interfaces/webchat.mdx`。
- 口径落地：**站点不再保留 Tauri 架构描述**。终态全站只剩 9 行 Tauri 字样，
  逐行分类见 `docs/VERIFICATION-2026-11.md` 的人工结论表 —— 全部落在
  `terminology.mdx`（Legacy Shell 词条）、`development/building.mdx`（过渡期提示，含「遗留 / 将删除」豁免词）、
  `desktop-hosts/overview.mdx`（`## 历史：旧桌面壳的 daemon 托管` 小节）与 changelog 历史条目。
- 新增事实纠正：站点原写 Rust 1.95 / toolchain pin `1.96.0`，真实为根 `Cargo.toml` `rust-version = "1.99"`
  与 `rust-toolchain.toml` `channel = "1.99.1"`（`scripts/fix_msrv.py` 已修 12 个文件）。

### R2 — Protocol v1 与传输矩阵 ✅

新建 `content/docs/{zh,en}/gateway/protocol-v1.mdx`；`gateway/protocol.mdx` 改写为旧 `/ws` 入口并加
`## 历史：协议从无版本演进到 v1`；新建 `content/docs/{zh,en}/gateway/methods/chat.mdx`；
重写 `api/jsonrpc.mdx` 与 `gateway/methods/index.mdx`。
主 agent 复核通过：`DEFAULT_MAX_PAYLOAD_BYTES = 8_388_608`、`HEADER_BYTES = 4`、`negotiate_version`、
`max_inflight_requests = 128`、`incompatible protocol major version` 均有源码对应。

### R3 — 能力模型与模块化 ✅

新建 `content/docs/{zh,en}/capabilities/{capability-model,slots-and-replacement,trust-and-backends,hooks-and-prompts,plugin-package}.mdx`；
重写 `content/docs/{zh,en}/concepts/capability-system.mdx`（旧页描述的 `CapabilityDeclaration` 枚举属 `src/extension/`，已改为历史小节）。

### R4 — Panel 与插件 UI ✅

新建 `content/docs/{zh,en}/desktop-hosts/panel-runtime.mdx`；定点修订 `content/docs/{zh,en}/interfaces/webchat.mdx`。
插件 UI 现行路径核实：`src/extension/panel_publication/`（准入 → 发布仓库 → `panel_asset_route.rs` → Panel 同源加载 ES 模块）
→ `interfaces/webchat/src/panel/sdk.rs` 窄 SDK。

### R5 — 子系统补齐与过时剔除 ✅

- 锚点失效 229 条：按文件分组派 worker 修（conceptsA / conceptsB / arch / gatewayd / rest）。
  **结果：G1 锚点门失效 0**（页面 328、锚点 5690）。
- 方法幽灵 204 条 + 漏记方法 8 条：`/tmp/r5/method_resolution.md` 逐条判定，
  `scripts/make_method_briefs.py` 生成 6 组简报，wave11 六个 worker 并行修，
  wave12/13 三组（r5c-a / r5c-b / r5c-c）收尾。**结果：方法幽灵 0、漏记方法 0。**
- **审计脚本自身的三处语义修正**（都是脚本 bug，不是文档问题）：
  1. `NON_METHOD_PREFIXES` 里的 `config.` 会把真实命名空间 `config.*` 整段排除，
     导致 `config.get` / `config.schema` 等永远算「未文档化」——已移除，改用
     `CONFIG_NON_METHODS` 精确列出 `config.get_full_config` / `config.reload_with_subsystems` /
     `config.enabled` / `config.policies.capability_constraints`（Rust 函数名与配置键）。
  2. 新增 `NEGATION_MARKERS`：说明「某方法不存在 / 已废弃 / 被取代 / 是旧名」的行不再算幽灵；
     英文标记用 `historical` / `historically`，不用裸 `histor`（会误伤 `chat.history`）。
  3. 新增命名空间规则：只有「首段属于 census 命名空间」的标识符才算方法候选，
     配置键、结构体字段路径、URL、文件名一律不算；`changelog.mdx` 整体豁免（历史记录允许写已下线的方法名）。
- **新增第 4、5 处语义修正**（facts 门）：
  4. `aleph-bridge` 从过期模式里移除——Swift 助手进程是**现行**实现
     （`desktop/macos/src/pim.rs:75-78` 的 `MacOSPim { bridge: Arc<SwiftBridge>, … }`）。
  5. `HISTORY_HEADING` 放宽到 `旧` / `Legacy`，新增页面级豁免
     （页面已指向 `src/capability/` 时，谈 `CapabilityDeclaration` 是在讲「插件声明层 vs 运行时模型」的分工）
     与整页豁免 `changelog.mdx`。**结果：facts 门从 31 项降到 0 项。**
- **「裸文件名」类陈旧引用**：锚点门只认带前缀的路径，站点里 `deps_builder.rs` 这类裸文件名引用抓不到。
  已给 `anchor_check.py` 加裸 `.rs` / `.py` 文件名检查（仓库 basename 索引 + allowlist），
  并逐个核实、修掉：`architecture/{orchestrator,thinker}.mdx` 的模块清单、`concepts/agent-components.mdx`
  的 harness 安全面归属、`interfaces/telegram.mdx` 的模块表、`concepts/voice-streaming.mdx` 的
  `pty_bridge.py`、`security/exec-approval.mdx` 的 `session_memory.rs`。
  **结果：裸文件名失效 0。**
- **本阶段修掉的整节幻觉**：`architecture/routing.mdx` 第 8 节整节（VESR）与
  `architecture/resilience.mdx` 的 Trace 数据流整节（`OutcomeObserver` / `RoutingRecall` /
  `RoutingAttribution` / `RoutingExperienceStore`）——这些类型与文件在代码里**完全不存在**，
  已改写为真实实现（provider failover 链 / `TraceSink` → `GatewayTraceSink` → `task_traces`）。
- 数字纠正：`CEILING = 5055` → 真实的 `5535`（`src/harness/tests/budget.rs:795`，`scripts/fix_ceiling.py` 修 14 个文件）；
  `TokenLoopVerifier` → 真实的 `ToolLoopVerifier`；`security/exec-approval.mdx` 的 `AllowAlways` 语义
  （真实存在持久授权 `GrantScope::Always` → `~/.aleph/approval-grants.json`，由 `for_confirm_gate` 决定是否提供）。

### R6 — 术语表 · 导航 · changelog ✅

`content/docs/{zh,en}/terminology.mdx`（rest 组）、`content/docs/{zh,en}/changelog.mdx`（r6-a，zh/en 各 49 个标题）。
导航：根 `meta.json` 插入 `desktop-hosts`、`capabilities`；`gateway/meta.json` 挂 `protocol-v1`；
`desktop-hosts/meta.json` 挂 `panel-runtime`。

### R7 — 终验 ✅

- 六道门全绿：`python3 scripts/run_gates.py --repo ../Aleph --build` → G1 / G1b / G2 / G3 / G4 / G5 全 PASS。
- G5 构建门：`next build` 成功（332 个静态页，基线 310）、`tsc --noEmit` 退出 0、`eslint` 退出 0。
  **顺带修好了一个坏掉的门**：`eslint.config.mjs` 原来用 `FlatCompat` 包 `next/core-web-vitals`，
  但 `eslint-config-next@16` 只导出 flat 数组，包一层会在配置加载阶段抛
  「Converting circular structure to JSON」（`eslint-plugin-react` 的插件对象循环引用，
  schema 校验失败的报错格式化又把它 `JSON.stringify` 了一遍）。已改为直接吃 flat 数组。
- `scripts/baseline.json` 已棘轮到**全空**（anchor / bare_name / facts / method_ghost / method_missing / structure / bilingual 全为 0）。
- `docs/VERIFICATION-2026-11.md` 机器部分由 `scripts/verification_report.py` 生成，
  人工结论写在 `<!-- MANUAL:BEGIN/END -->` 区间（脚本重跑不会覆盖）。

