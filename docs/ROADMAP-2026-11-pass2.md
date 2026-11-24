# Aleph 文档对齐 Roadmap · 第二轮（2026-11）

> **一句话**：第一轮把站点从「2026-07-29 基线（Aleph 26.7.21）」推到「26.9.1 + NSH / Protocol v1 / 能力模型」；**这一轮把站点推到「2026-11-24 代码真值」**，重点是 Panel 模型迁移、Protocol v1 深化、Gateway 冷声明、跨平台桌面 IPC，以及**全站符号级腐化清理**。

配套执行清单：[docs/superpowers/plans/2026-11-24-aleph-docs-calibration-pass2.md](./superpowers/plans/2026-11-24-aleph-docs-calibration-pass2.md)

## 一、这一轮为什么必须做

第一轮（R0–R7）的锚定基线是 Aleph 提交 `4f966eaf6`（2026-11-23 18:22）。此后代码仓推进到 `7a6986bc9`（2026-11-24 16:13），`4f966eaf6..HEAD` 共 **30 个提交（27 个非 merge）、138 个文件改动**。这些提交里有四次架构级变动，站点一个字都没提：

| 提交 | 变动 | 站点现状 |
|---|---|---|
| `2f541e81a` | Panel 模型从 `interfaces/webchat/src/panel/` 搬到 `shared/ui_logic/src/panel/` | 仍把模型说成 Panel crate 的私有模块 |
| `e9162f26e` | 新增共享 TSX Panel 壳（`interfaces/panel/`，crate `aleph-panel-ui`） | 站点只承认「一个 Leptos/WASM Panel」 |
| `80435029f` / `1a848b925` | NSH 嵌入 TSX Panel 表面；Protocol v1 收敛成**一套方法集** | `gateway/protocol-v1.mdx` 仍写「尚未落地」 |
| `9976b7840` | Gateway 通道**冷声明**（配置先声明、显式 start 才激活） | `gateway/methods/channels.mdx` 无冷声明概念 |
| `5d89d7aff` | Windows 命名管道桌面 IPC | `desktop-hosts/overview.mdx` 只讲 Unix socket |
| `cd4e6f48a` | `system.hello` 增加不透明 per-user `subject` | 协议页无 `subject` |

更严重的问题不在架构主题，而在**符号层**。第一轮的门只校验「路径是否存在」，没有校验「反引号里的标识符是否还存在」。补上符号门（G1c）后扫描全站 328 页，得到 **448 条符号失效、涉及 148 个页面**：

- **406 条**所在行没有任何历史/规划中标记 —— 那是**把已经不存在的符号当作现状陈述**，例如 `permissive_default`（13 个页面在讲一个已被 fail-closed 取代的审批默认值）、`TaskGraph`（`d475c15f1` 删除了约 3.8 万行死 dispatcher 代码）、`DaemonEvent`、`WorldModel`、`QuickSetupFlow`、`LlmMatcher`。
- **41 条**带历史语义（行内含「已删除 / 已移除 / 已废弃 / no longer / renamed to」等）—— 属于历史叙述，但**没有挂到统一的 `## 历史：…` 小节**下，读者无法分辨它是现状还是遗迹。

还有一类是**改名未同步**：`MediaAttachment` → 代码里是 `MailAttachment`；`require_consent` → 代码里是 `requires_user_consent`；`enable_tool_search` → `enable_search`；`DispatcherMode` → `DispatchMode`；`AuthProfileManager` → `ProfileManager`；`ExecutionContext` → `ToolExecutionContext`。

所以这一轮的主线不是「再写几个专题页」，而是**把符号级腐化清干净，并把新架构讲准**。

## 二、真值来源分层（沿用第一轮）

| 优先级 | 来源 | 语义 |
|---|---|---|
| **T1** | Aleph 仓库 `main`（26.9.1，HEAD `7a6986bc9`）源码 | 现状唯一权威 |
| **T2** | `docs/reference/`（70 份当前层）+ `docs/README.md` | 当前架构契约 |
| **T3** | `docs/research/` 四份蓝图（含 `Everything-externally-composable-is-a-Capability.md`） | 设计目标，只能写「规划中」 |
| **T4** | 站点现状（第一轮产出） | 待校正对象 |
| **T5** | `docs/superpowers/{specs,plans,runs}/` | 时点证据，引用须带日期 |

冲突时**以代码为准**。

## 三、内容三态约定（沿用第一轮）

| 状态 | 写法 |
|---|---|
| **现状** | 直接陈述 + 真实路径锚点（路径与符号都要能在代码里 grep 到） |
| **规划中** | 块引用横幅 + 蓝图出处 + 当前实现位置 |
| **历史** | 页面内 `## 历史：<主题>` 小节 |

## 四、六道门（分级完成的判定机制）

每阶段结束必须全绿才解锁下一阶段；任一门红则该阶段**不完成**。

| 门 | 名称 | 判定 | 命令 |
|---|---|---|---|
| **G1** | 锚点门 | 页面里所有形似源码路径的引用在 Aleph 仓库真实存在 | `python3 scripts/anchor_check.py --repo ../Aleph` |
| **G1b** | 方法册门 | RPC 方法名与代码 `src/gateway/method_census.rs` 一致 | `python3 scripts/method_audit.py --repo ../Aleph` |
| **G1c** | **符号门（本轮新增）** | 反引号里的 Rust/TS 标识符在代码里真实存在；crate 名是真实 package/bin；`just <target>` 是真实 recipe | `python3 scripts/symbol_check.py --repo ../Aleph` |
| **G2** | 事实门 | 无过期断言（删除路径、旧枚举名、Tauri 独占表述）；指定页面含目标形态语义 | `python3 scripts/freshness_audit.py --repo ../Aleph` |
| **G3** | 结构门 | `meta.json` 收录完整；站内相对链接可解析 | `python3 scripts/freshness_audit.py --repo ../Aleph` |
| **G4** | 双语门 | zh/en 页面集合一致；同名页 `##` 标题骨架一致 | `python3 scripts/freshness_audit.py --repo ../Aleph` |
| **G5** | 构建门 | `next build` / `tsc --noEmit` / `eslint` 退出码全 0 | `pnpm exec next build && pnpm exec tsc --noEmit && pnpm exec eslint` |

G1c 是本轮的增量：它把「文档说的东西还存在吗」从抽查变成机器判定，并按 `scripts/baseline.json` 的 `symbol` 段棘轮 —— **基线只降不升**，每阶段修完必须 `--update-baseline` 收窄，最终目标 `symbol: []`。

## 五、阶段路线（逐级解锁）

```
S0 工具与基线 ──▶ S1 Panel 架构 ──▶ S2 Protocol v1 ──▶ S3 能力模型
                                                        │
                                                        ▼
S7 终验 ◀── S6 术语·导航·changelog ◀── S5 符号校准 ◀── S4 冷声明与桌面 IPC
```

| 阶段 | 目标 | 主要产出 | 门 |
|---|---|---|---|
| **S0** | 补齐符号门，建立新基线 | `scripts/symbol_check.py`、`scripts/symbol_triage.py`；`run_gates.py` 接入第六门；`baseline.json` 的 `symbol` 段棘轮到现存腐化 | 全门（除 G5） |
| **S1** | Panel 架构重写 | `desktop-hosts/panel-runtime.mdx` 改写为「共享 Panel 模型 + 两套渲染器」；`desktop-hosts/panel.mdx` 补 TSX 面板；`desktop-hosts/plugin-ui.mdx` 补 TSX 宿主契约 | 全门 |
| **S2** | Protocol v1 深化 | `gateway/protocol-v1.mdx` 改写为已落地（`system.hello` + `subject` + 单一方法集 + `panel.capabilities.snapshot`）；`gateway/protocol.mdx` 标注 `/ws` 兼容地位；`architecture/gateway.mdx` 同步 | 全门 |
| **S3** | 能力模型深化 | `capabilities/capability-model.mdx` 补齐 `src/capability/` 39 文件的真实挂载状态；`capabilities/plugin-package.mdx` 等对齐 `aleph-slot-api` | 全门 |
| **S4** | 冷声明与跨平台桌面 IPC | `gateway/methods/channels.mdx` 增写冷声明生命周期；`desktop-hosts/overview.mdx` 增写 Windows 命名管道与 Desktop IPC 矩阵 | 全门 |
| **S5** | **符号校准（全站）** | 448 条符号失效逐条判定：改名 → 落到代码真名；已删 → 改写为当前路径或移入 `## 历史：…`；剩余 `symbol` 基线归零 | 全门 |
| **S6** | 术语 · 导航 · changelog | `terminology.mdx` 收录本轮新术语；全部 `meta.json` 收录新增页；`changelog.mdx` 补 26.9.1→26.11 真实序列 | 全门 |
| **S7** | 终验 | `docs/VERIFICATION-2026-11-pass2.md`，逐页判定表 100% 判定 | 全门 |

每阶段一次提交，提交信息 `docs(phase-SN): <主题>`，正文列六门结果。

## 六、S5 符号校准的判定规则（唯一裁决口径）

对每条失效符号，只允许四种处置，**不得凭空发明符号**：

1. **改名同步**：代码里存在近似名 → 把文档里的旧名换成代码里的真名，并保留语义不变。
2. **路径/模块已删**：模块在代码里整体消失 → 改写该段为**当前真实路径**（如「工具聚合现在位于 `src/tools/registry.rs`」），或整段移入 `## 历史：…` 并标注删除来源提交。
3. **历史叙述**：该行讲的是旧世界 → 移入 `## 历史：<主题>` 小节，行内加「已删除 / 已移除 / renamed to」等标记，使其不再冒充现状断言。
4. **蓝图内容**：确属规划中 → 加 `> **状态：规划中**` 横幅并给出蓝图出处。

判定必须以 **Aleph 仓库 grep 结果**为依据。判定工具：`scripts/symbol_triage.py` 先用近似名把 181 个 distinct token 分成 RENAME(80) / GONE(101) 两类，给出候选，但**近似匹配只是线索，不是结论**。

## 七、执行方式

**Subagent-driven**：每阶段拆成互不重叠的文件集，分发给并行 subagent（每个 subagent 独占文件，无写冲突）；主 agent 负责门校验、事实抽查、基线棘轮与合并。

subagent 硬性要求：

1. 只写分配到的文件，不碰 `meta.json`（导航由主 agent 统一改）。
2. 每条现状断言必须带真实路径锚点；写不出锚点的断言要么删掉，要么标为「规划中」。
3. 蓝图（T3）内容一律标「规划中」并给出蓝图文件出处。
4. 不得编造 RPC 方法名、类型名、配置键、crate 名——一律从 Aleph 仓源码抄。
5. zh 与 en 由同一 subagent 一起产出，避免语义漂移。
6. 改完必须在自己负责的文件上跑 `python3 scripts/symbol_check.py --repo ../Aleph`，确认没有引入新的基线外失效。

## 八、台账

见本文件末尾「阶段状态」表。每阶段完成后更新，写明各门结果与提交哈希。

## 阶段状态

| 阶段 | 状态 | 六门结果 | 提交 |
|---|---|---|---|
| S0 | 进行中 | G1 PASS / G1b PASS / G1c PASS / G2 PASS / G3 PASS / G4 PASS / G5 未跑 | — |
| S1 | 未开始 | — | — |
| S2 | 未开始 | — | — |
| S3 | 未开始 | — | — |
| S4 | 未开始 | — | — |
| S5 | 未开始 | — | — |
| S6 | 未开始 | — | — |
| S7 | 未开始 | — | — |
