# Aleph 文档站终验报告（2026-11）

> 本文件由 `scripts/verification_report.py` 生成**机器部分**，逐阶段结论由主 agent 撰写。
> 复核命令：`python3 scripts/run_gates.py --repo ../Aleph --build`。

## 门禁结果

| 门 | 结果 | 明细 |
|----|------|------|
| G1 锚点门 | PASS | 页面 328，锚点 5690，失效 0（路径 0，裸文件名 0；新增 0，基线旧债 0） |
| G1b 方法册 | PASS | census methods: 394   documented dotted tokens: 464<br>ghost (documented, absent from code): 0（新增 0，基线旧债 0）<br>missing (registered, undocumented): 0（新增 0，基线旧债 0） |
| G2 事实门 | PASS |  |
| G3 结构门 | PASS |  |
| G4 双语门 | PASS |  |

## 规模

- 页面：zh 164 页 / en 164 页
- 代码锚点：5690 个被检查，0 个失效

## 逐阶段结论

<!-- MANUAL:BEGIN -->
### 口径决定：桌面宿主不是双轨

2026-11-24 明确：**NSH 是桌面端的目标形态，Tauri 壳只是过渡期遗留、最终会删除**。
因此本站的处理是**提前删除 Tauri 架构描述、补齐 NSH 文档**，而不是两边并排描述。

全站 `Tauri` 字样只剩 **9 行**，每一行都落在允许的例外里：

| 位置 | 行数 | 性质 |
|------|------|------|
| `terminology.mdx` | 2 | `Legacy Shell`（旧桌面壳）词条，注明「过渡期遗留 / 最终会删除」 |
| `development/building.mdx` | 2 | 过渡期提示：当前发布流水线仍构建遗留旧壳、NSH 尚无自己的发布流水线，并写明旧壳**将删除** |
| `desktop-hosts/overview.mdx` | 2 | `## 历史：旧桌面壳的 daemon 托管` 小节，描述旧壳的 daemon supervisor 设计 |
| `changelog.mdx` | 3 | 历史条目（Panel TOFU 信任存储、Updater 签名密钥轮换），不改写历史 |

代码侧的依据：`docs/superpowers/prompts/2026-11-15-phase8-nsh-main-restart.md:47` 写明「完全替换方向已确定，不走 Tauri 混合兜底」，
同时要求 Phase4 parity 完成 + 两周双运行之前不得删除 Tauri/WebChat/workspace members——这解释了为什么**代码里旧壳还在、文档里已经不写它了**。

### 真值分层

本轮校对沿用 Aleph 的三层文档契约（`docs/reference/EVIDENCE_LAYER.md`）：

- **T1 代码**：`/home/zou/data/workspace/Aleph` 的源码，是唯一事实来源。
- **T2 当前层**：`Aleph/docs/reference/`（75 份）+ `docs/README.md`（文档地图）。
- **T3 证据层**：`docs/research/` 四份蓝图（modularization plan、Everything-externally-composable-is-a-Capability、NSH ADR-001~009、NSH_PROTOCOL_V1）——**规划目标，不是现状**。
- **T5 回执**：`docs/superpowers/runs/` 下带日期的验证回执。

站点页面据此分三种写法：

1. **现状**：直接陈述，带 `src/`、`desktop/`、`shared/`、`crates/`、`interfaces/` 下的真实路径锚点。
2. **规划中**：`> **状态：规划中**` 横幅 + 蓝图出处（文件名 + 章节）。
3. **历史**：`## 历史：<主题>` 小节，保留当年的结论并标明它已被什么取代。

### 逐阶段结论

| 阶段 | 结论 | 依据 |
|------|------|------|
| R0 校验脚本与基线审计 | 完成 | `scripts/` 下门禁脚本 + `docs/AUDIT-2026-11.md`（153 zh 页逐页判定 + 9 待新建页） |
| R1 桌面宿主改写为 NSH | 完成 | 新建 `desktop-hosts/`（overview / panel / plugin-ui / panel-runtime）；重写 `architecture/{desktop-bridge,overview,1-2-3-4-model}`；Tauri 架构描述清零（见上表） |
| R2 Protocol v1 与传输矩阵 | 完成 | 新建 `gateway/protocol-v1.mdx`；`gateway/protocol.mdx` 改为旧 `/ws` 入口并加历史小节；新建 `gateway/methods/chat.mdx` |
| R3 能力模型与模块化 | 完成 | 新建 `capabilities/` 五页；`concepts/capability-system.mdx` 改为「三层含义」并把 `CapabilityDeclaration` 收进历史小节 |
| R4 Panel 与插件 UI | 完成 | 新建 `desktop-hosts/panel-runtime.mdx`；`interfaces/webchat.mdx` 定点修订；插件 UI 现行路径核实到 `src/extension/panel_publication/` → `panel_asset_route.rs` → `interfaces/webchat/src/panel/sdk.rs` |
| R5 子系统补齐与过时剔除 | 完成 | 失效代码锚点 0、方法幽灵 0、漏记方法 0、裸文件名引用 0、facts 断言 0；Rust 版本与 `CEILING` 数字纠正 |
| R6 术语表 · 导航 · changelog | 完成 | `terminology.mdx` 新增「桌面宿主与 Panel」「能力模型与插槽」两节与协议词条；根 `meta.json` 挂 `desktop-hosts`、`capabilities` |
| R7 终验 | 完成 | 本文件；六道门（含构建门）全绿，`scripts/baseline.json` 棘轮至全空 |

### 本轮修掉的真实过时项

| 过时表述 | 事实 | 依据 |
|----------|------|------|
| Rust 1.95 / `rust-toolchain.toml` pin `1.96.0` | `rust-version = "1.99"`；toolchain channel `1.99.1` | Aleph 根 `Cargo.toml`、`rust-toolchain.toml` |
| 「桌面壳（Tauri v2）」是桌面端 | NSH 是目标形态，旧壳将删除 | 见上节 |
| `CapabilityDeclaration` 是能力模型 | 它是旧扩展模型的静态声明；运行时模型在 `src/capability/` | `src/extension/capability.rs` vs `src/capability/` |
| `desktop/nsh-shell/src/connection.rs` 描述现行 NSH 连接 | 该文件未在 `main.rs` 的 `mod` 声明里，不在当前编译产物 | `desktop/nsh-shell/src/main.rs`、`Cargo.toml` |
| 桌面桥接是「aleph-server 与 Swift 助手之间的独立 stdio 进程」 | 桌面能力层是**进程内**的：`alephcore` 直接依赖 `aleph-desktop` / `-macos` / `-linux` / `-windows`；Swift 助手只服务 macOS PIM 一类能力 | 根 `Cargo.toml`、`desktop/shared/src/`、`desktop/macos/src/pim.rs:75-78` |
| `architecture/routing.mdx` 第 8 节整节「Provider Failover 与 VESR」 | `routing/recall.rs` / `experience_store.rs` / `observer.rs` 与 `RoutingRecall` / `RoutingAttribution` / `OutcomeObserver` / `ProviderAvailability` / `task_emb` **在代码里全部不存在** | `src/routing/` 实有 6 个模块；真实 failover 在 `src/providers/failover/` + `src/orchestrator/deps_builder/provider_chain.rs` |
| `architecture/resilience.mdx` 的 Trace 数据流指向 VESR 读写端 | 真实链路是 `TraceSink::on_trace` → `GatewayTraceSink` → `TracePersistence::record` → `task_traces` 表 | `src/harness/trace_sink.rs`、`src/gateway/execution_engine/{trace_sink_adapter,callback}.rs`、`src/resilience/database/traces.rs:133` |
| `security/exec-approval.mdx` 写「没有持久 allowlist，AllowAlways 按钮永远不渲染」 | 持久授权**存在**：`GrantScope::Always` 落到 `~/.aleph/approval-grants.json`；`for_confirm_gate` 只在 operator 层级且非硬底线时才提供该档位，回答时由 `clamp_decision` 收窄 | `src/sandbox/exec_approval/grants.rs`、`src/exec/allowed_decisions.rs`、`src/exec/manager.rs:1333` |
| `CEILING = 5055` | `const CEILING: usize = 5535;` | `src/harness/tests/budget.rs:795` |
| `TokenLoopVerifier` | 真实类型是 `ToolLoopVerifier` | `src/verification/tool_loop_verifier.rs` |
| 模块清单里的裸文件名（`deps_builder.rs`、`flow_run_tool.rs`、`prompt_builder.rs`、`session_memory.rs`、`sticker.rs`、`pty_bridge.py` …） | 对应真实路径或该文件已删除 | 逐个 `find` 核实（`scripts/anchor_check.py` 已加入裸文件名检查） |

### 遗留债务

- **未挂载的能力模块**：`src/capability/` 里若干模块写好且测过，但没挂到生产路径（2026-11-20 severed-wire 审计）。站点已按「挂载状态」逐项标注，不当作运行时行为。
- **NSH 的发布流水线**：还没有自己的 release 流水线、updater、deeplink 注册、macOS 菜单、服务控制；切换由 Phase 11 门禁决定。
- **工具自身的已知盲区**：`anchor_check.py` 只能校验路径与裸文件名，无法判断「路径存在但语义说错」；这类问题只能靠人工复核，所以 R1–R5 的每批 worker 产出都要求附「断言 → 证据路径」对照表。

### 复核方法

```bash
cd /home/zou/data/workspace/Aleph-docs
python3 scripts/run_gates.py --repo ../Aleph --build   # 六道门（含构建）
python3 scripts/verification_report.py --repo ../Aleph # 重新生成本文件的机器部分
```

抽查任一页面时，取页面里的反引号路径，在 `/home/zou/data/workspace/Aleph` 下 `ls` 一下；
取页面里的 `a.b` 方法名，`grep` 一下 `src/gateway/method_census.rs` 与源码字面量。
<!-- MANUAL:END -->
