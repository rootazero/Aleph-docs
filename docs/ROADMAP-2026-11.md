# Aleph 文档校对 Roadmap（2026-11）

> **一句话**：把文档站从 **26.7.21 基线**推进到 **26.9.1 + 2026-07-25 以来 5948 次提交后的真实代码状态**，逐阶段解锁、逐阶段过门。

## 一、为什么需要这个 roadmap

文档站（Aleph-docs）最后一次集中校对停在 2026-07-29（基线 Aleph 26.7.21）。此后代码仓 Aleph 推进到 **26.9.1**，其中包含本轮校对的三条主线：

1. **桌面宿主换成 NSH**。`desktop/nsh-shell/`（`aleph-nsh-shell`，基于 nsh 0.6.0）成为桌面宿主主线，托管同一个 Leptos/WASM Panel；原 Tauri v2 壳（`desktop/shell/`，crate `aleph-desktop-shell`）**只是过渡期遗留，按既定路线在门禁通过后删除**。站点不再为 Tauri 保留独立文档。
2. **Protocol v1 落地**。有界帧、连接认证、`system.hello` 握手与特性协商、事件信封、Snapshot + Replay 已有真实代码（`shared/protocol/`、`src/gateway/server/connection/`）。
3. **模块化与能力模型**。新增 `src/capability/`（39 文件 / 32,704 行）、`src/scope/`、`crates/aleph-slot-api`，并以 `docs/research/` 四份蓝图定义目标形态。

站点当前对这三块几乎零覆盖：`grep -r 'NSH' content/` 命中 0，`grep -r 'system.hello' content/` 命中 0，`grep -r 'Zahir' content/` 命中 0；`concepts/capability-system.mdx` 描述的还是旧的 `src/extension/capability.rs` 声明枚举；`architecture/desktop-bridge.mdx` 还在讲「Rust 核心 spawn Swift 助手」的旧桥接模型。

## 二、真值来源分层

沿用 Aleph 代码仓 `docs/reference/EVIDENCE_LAYER.md` 的分层契约。冲突时**以代码为准**。

| 优先级 | 来源 | 语义 | 用途 |
|---|---|---|---|
| **T1** | Aleph 仓库 `main`（26.9.1）源码 | 现状唯一权威 | 所有「现状」断言必须锚定到真实路径/符号 |
| **T2** | `docs/reference/`（75 份当前层）+ `docs/README.md` | 当前架构契约 | 补全语义、术语、背景 |
| **T3** | `docs/research/` 四份蓝图 | **设计目标，非现状** | 只能写「规划中」，必须标注落地状态 |
| **T4** | 站点现状 | 2026-07 基线 | 待校正对象 |
| **T5** | `docs/superpowers/runs/` 回执 | 时点证据 | 引用须带日期与出处 |

四份蓝图：`docs/research/aleph_modularization_plan.md`（771 行）、`docs/research/Everything-externally-composable-is-a-Capability.md`（745 行）、`docs/research/NSH_ADR-001~009.md`（548 行）、`docs/research/NSH_PROTOCOL_V1.md`（921 行）。

## 三、内容状态三态约定（贯穿所有阶段）

每条陈述必须落在三态之一，避免「规划当现状」：

| 状态 | 写法 | 例子 |
|---|---|---|
| **现状** | 直接陈述 + 锚点路径 | 「`src/capability/descriptor.rs` 定义描述符结构」 |
| **规划中** | 块引用横幅 + 蓝图出处 | `> **状态：规划中** — 蓝图为 docs/research/NSH_ADR-005.md；当前实现见 src/capability/ui_surface.rs` |
| **历史** | 页面内 `## 历史：<主题>` 小节 | `## 历史：旧 Swift 助手桥接模型`（说明被替换的 spawn/stdin-stdout 协议及迁移原因） |

## 四、五道门（分级完成的判定机制）

每阶段结束必须五门全绿才解锁下一阶段；任一门红则该阶段**不完成**，在本文件台账里标记并回到该阶段。

| 门 | 名称 | 判定 | 命令 |
|---|---|---|---|
| **G1** | 锚点门 | 页面里所有 `src/` `desktop/` `shared/` `crates/` `interfaces/` `plugins/` `scripts/` `qa/` `tests/` 开头且形似路径的引用，在 Aleph 仓库真实存在 | `python3 scripts/anchor_check.py` |
| **G2** | 事实门 | 无过期断言（删除路径、旧枚举名、Tauri 独占表述）；指定页面含目标形态语义 | `python3 scripts/freshness_audit.py` |
| **G3** | 结构门 | `meta.json` 列出的页都存在；每页都被某个 `meta.json` 收录；站内相对链接可解析 | `python3 scripts/freshness_audit.py` |
| **G4** | 双语门 | zh/en 页面集合完全一致；同名页面 `##` 标题骨架一致 | `python3 scripts/freshness_audit.py` |
| **G5** | 构建门 | `next build` / `tsc --noEmit` / `eslint` 退出码全 0 | `pnpm exec next build && pnpm exec tsc --noEmit && pnpm exec eslint` |

G1 是核心：把「文档写的路径是不是真的」从人工抽查变成机器判定——旧文档腐化的主因。

## 五、阶段路线（逐级解锁）

```
R0 基线与工具 ──▶ R1 桌面宿主(NSH) ──▶ R2 Protocol v1 ──▶ R3 能力与模块化
                                                         │
                                                         ▼
R7 终验 ◀── R6 术语·导航·changelog ◀── R5 子系统补齐 ◀── R4 Panel 与插件 UI
```

| 阶段 | 目标 | 产出 | 门 |
|---|---|---|---|
| **R0** | 建立校验工具与逐页判定基线 | `scripts/anchor_check.py`、`scripts/freshness_audit.py`、`docs/AUDIT-2026-11.md` | G1 G2 G3 G4 |
| **R1** | 桌面宿主改写为 NSH | 新章节 `desktop-hosts/`（overview / panel / plugin-ui）；删除站点内 Tauri 主题内容并改写 11 处 Tauri 表述 | 全门 |
| **R2** | Protocol v1 与传输矩阵 | 新增 `gateway/protocol-v1.mdx`；改写 `gateway/protocol.mdx`、`architecture/gateway.mdx`、`api/jsonrpc.mdx` | 全门 |
| **R3** | 能力模型与模块化 | 新章节 `capabilities/`（5 页）；重写 `concepts/capability-system.mdx` | 全门 |
| **R4** | Panel 与插件 UI | `desktop-hosts/panel.mdx`、`desktop-hosts/plugin-ui.mdx` | 全门 |
| **R5** | 子系统补齐与过时剔除 | 14 个子系统逐个判定并补页/改页；过时内容重写 + 历史小节 | 全门 |
| **R6** | 术语表 · 导航 · changelog | `terminology.mdx`、全部 `meta.json`、`changelog.mdx`（26.8–26.11 真实序列） | 全门 |
| **R7** | 终验 | `docs/VERIFICATION-2026-11.md`，逐页判定表 100% 判定 | 全门 |

每阶段一次提交，提交信息 `docs(phase-RN): <主题>`，正文列五门结果。

## 六、R1 的桌面宿主口径（已按用户口径定稿）

- **目标形态是 NSH**，站点以 NSH 为主线描述桌面宿主：进程模型、Panel 挂载、Gateway 连接、凭据、生命周期、热键/通知/deep link、协议接入。
- **Tauri 壳是过渡期遗留**，站点不再保留 Tauri 主题页或 Tauri 架构描述；相关段落一律改写为 NSH。
- **例外清单（事实诚实，非 Tauri 文档）**：发布流水线当前仍构建 `desktop/shell`（Tauri），尚无 NSH 发布流水线。此事实只出现在 `development/building.mdx` 的**过渡期提示**里，并明确标注「将删除」，不构成 Tauri 架构文档。
- 历史 changelog 条目中的 Tauri 字样**保留**（那是历史记录，不是现状描述）。

## 七、执行方式

**Subagent-driven**：每阶段拆成互不重叠的文件集，分发给并行 subagent（每个 subagent 独占文件，无写冲突）；主 agent 负责门校验、事实抽查与合并。理由：153 页 × 2 语言，串行改写不现实；五道门提供机器化验收，不依赖人的细致程度。

subagent 硬性要求：

1. 只写分配到的文件，不碰 `meta.json`（导航由主 agent 统一改）。
2. 每条现状断言必须带真实路径锚点；写不出锚点的断言要么删掉，要么标为「规划中」。
3. 蓝图（T3）内容一律标「规划中」并给出蓝图文件出处。
4. 不得编造 RPC 方法名、类型名、配置键——一律从 Aleph 仓源码抄。
5. zh 与 en 由同一 subagent 一起产出，避免语义漂移。

## 八、台账

见本文件末尾「阶段状态」表。每阶段完成后更新，写明各门结果与提交哈希。
