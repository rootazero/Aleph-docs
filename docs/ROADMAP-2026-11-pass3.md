# Aleph 文档对齐 Roadmap · 第三轮（2026-11）

> 第二轮（pass2）把站点对齐到 Aleph `main` 的 `7a6986bc9`。此后 Aleph 连续推进 221 个提交，代码面变化 309 个文件（+25664 / −10978）。本轮继续用同一套「roadmap → phase spec → 逐阶段过门 → 终验报告」的方法，把站点推到 `7fb540b44`。

## 一、这一轮为什么必须做

Aleph 仓库自第二轮基线以来的变化不是「改了实现细节」，而是**模块级的增删**：

| 变化类型 | 事实 | 对文档站的直接影响 |
|---|---|---|
| 模块整体删除 | `src/capability/{activation,ambient,audit,grant,lifecycle}.rs` 被删 | `capabilities/*` 页里的 5 个路径锚点当场失效（30 条锚点失效全部集中在这几页） |
| 能力面新增 | `src/capability/` 新增 `census.rs`、`versioned_registry.rs`、`projection_host.rs`、`effect_claim.rs`、`event_audience.rs`、`diagnostic_control.rs`、`special_dispatch.rs`、`production_init.rs` | 能力模型页停在旧结构，讲的还是被删掉的那套激活/授权状态机 |
| 协议面新增 | `shared/protocol/src/chat_transcript.rs`、`shared/protocol/src/memory_graph.rs`；`shared/ui_logic/src/{nebula,prefs,transcript}` 与 `terminal_mutation.rs` | 协议页、Panel 页没有任何一处提到这些新面 |
| RPC 面新增 | `chat.transcript_details`（Open）、`pty.history`（Admin） | G1b 判「已注册未文档化」 |
| 记忆自进化 | `src/memory/` 落地产出归属、依赖就绪、发布—验证—退役顺序、反馈批次恢复 | `concepts/memory`、`architecture/memory`、`architecture/memory-evolution` 讲的是修复前的旧行为 |
| 面板新外壳 | `interfaces/panel/modules/{Chat,MemoryNebula,NebulaCanvas}.tsx`、`interfaces/panel/shell/{CommandPalette,Settings,Sidebar}.tsx` | `desktop-hosts/*` 停在第一轮写的 Leptos 侧与早期 TSX 宿主契约 |
| 执行边界 | `src/sandbox/` 改为 owned worktree + 挂载型 OS 驱动；`src/context/compact/manual.rs` 接线；`src/extension/lifecycle.rs` 增加重载预检 | 沙箱页、上下文页、扩展页与现状不符 |

第二轮结束时基线八段全 0，`scripts/baseline.json` 里没有一格存量债务。本轮的新失效全部是新增的。

**棘轮口径**：S1 先修能力面（把 `capabilities/*` 的 30 条锚点失效与相关符号失效修到 0）；剩下 125 条符号失效散在 74 个 zh/en 页对上（`development/design-patterns`、`architecture/*`、`philosophy/*` 等），不在任一单阶段的范围内，全部归到 S6。S4 结束时把这 125 条棘轮进 `scripts/baseline.json` 的 `symbol` 段作为**已知旧债**——这样中途阶段一旦引入新失效，G1c 仍会立即变红——S6 清零后再棘轮回 0。其余七段（anchor、bare_name、bilingual、facts、method_ghost、method_missing、structure）全程保持 0，不棘轮。

门禁现状（`python3 scripts/run_gates.py --repo ../Aleph`）：

| 门 | 现状 | 说明 |
|---|---|---|
| G1 锚点门 | **FAIL（30）** | 全部落在 `capabilities/{capability-model,hooks-and-prompts,trust-and-backends}.mdx`（zh + en） |
| G1b 方法册 | **FAIL（2）** | `chat.transcript_details`、`pty.history` 已注册但无页面提及 |
| G1c 符号门 | **FAIL（148）** | 74 个 zh 页 + 74 个 en 页对，含被删模块的符号（`GrantRegistry`、`LifecycleState`、`CapabilityActivationController`）与改名后的旧名（`ContextAnchor`、`FactType`、`cosine_rerank` 等） |
| G2 事实门 | PASS | — |
| G3 结构门 | PASS | — |
| G4 双语门 | PASS | — |
| G5 构建门 | 未跑 | 每阶段收尾时跑 |

## 二、真值来源分层（沿用第一轮）

| 优先级 | 来源 | 语义 |
|---|---|---|
| **T1** | Aleph 仓库 `main`（HEAD `7fb540b44`）源码 | 现状唯一权威 |
| **T2** | `docs/reference/`（50 份本轮有更新）+ `docs/README.md` | 当前架构契约 |
| **T3** | `docs/research/` 蓝图 | 设计目标，只能写「规划中」 |
| **T4** | 站点现状（第一轮 + 第二轮产出） | 待校正对象 |
| **T5** | `docs/superpowers/{specs,plans,runs}/`（本轮新增 13 组） | 时点证据，引用须带日期 |

冲突时**以代码为准**。T5 只说明「当时打算怎么做」；落地与否以 T1 判定。

## 三、内容三态约定（沿用第一轮）

| 状态 | 写法 |
|---|---|
| **现状** | 直接陈述 + 真实路径锚点（路径与符号都要能在代码里 grep 到） |
| **规划中** | 块引用横幅 + 蓝图出处 + 当前实现位置 |
| **历史** | 页面内 `## 历史：<主题>` 小节 |

被删除的模块一律**不得**留在现状段落里。要么改写为当前真实路径，要么移入 `## 历史：…` 并写明删除来源提交（`459c4fe96` 删 lifecycle/activation 状态机、`8507aff30` 删 audit collector 与 grant registry、`4cb16e5b6` 删 legacy handler registry）。

## 四、六道门（分级完成的判定机制）

每阶段结束必须全绿才解锁下一阶段；任一门红则该阶段**不完成**。

| 门 | 名称 | 判定 | 命令 |
|---|---|---|---|
| **G1** | 锚点门 | 页面里所有形似源码路径的引用在 Aleph 仓库真实存在 | `python3 scripts/anchor_check.py --repo ../Aleph` |
| **G1b** | 方法册门 | RPC 方法名与代码 `src/gateway/method_census.rs` 一致 | `python3 scripts/method_audit.py --repo ../Aleph` |
| **G1c** | 符号门 | 反引号里的 Rust/TS 标识符在代码里真实存在；crate 名是真实 package/bin；`just <target>` 是真实 recipe | `python3 scripts/symbol_check.py --repo ../Aleph` |
| **G2** | 事实门 | 无过期断言（删除路径、旧枚举名、Tauri 独占表述）；指定页面含目标形态语义 | `python3 scripts/freshness_audit.py --check facts --docs content/docs` |
| **G3** | 结构门 | `meta.json` 收录完整；站内相对链接可解析 | `python3 scripts/freshness_audit.py --check structure --docs content/docs` |
| **G4** | 双语门 | zh/en 页面集合一致；同名页 `##` 标题骨架一致 | `python3 scripts/freshness_audit.py --check bilingual --docs content/docs` |
| **G5** | 构建门 | `next build` / `tsc --noEmit` / `eslint` 退出码全 0 | `pnpm exec next build && pnpm exec tsc --noEmit && pnpm exec eslint` |

### 本轮的工具加固（G1b 常量方法名 / G1·G1c 行级免检）

第二轮的 `method_audit.py` 只认 census 里的**字面量**方法名。协议 crate 把方法名收进常量后，census 里写成 `aleph_protocol::chat_transcript::CHAT_TRANSCRIPT_DETAILS_METHOD`，字面量正则匹配不到——这类方法在门眼里凭空消失，`chat.transcript_details` 因此直到本轮才发现没被文档覆盖。

本轮把 census 的常量条目解析进方法集（`scripts/method_audit.py`：`CENSUS_CONST_RE` + `protocol_constants()`），修完基线保持 0，新出现的未文档化方法立即让 G1b 变红。

第二轮的 `anchor_check.py` 与 `symbol_check.py` 只按**小节**豁免历史 / 规划中段落，行级引用一律判失效。文档却必须能记录「这个模块已经不在代码树里」——挂载状态表必须列出已删除的模块，历史说明必须点名旧文件。本轮把两门的免检规则抽到共享模块 `scripts/gate_exempt.py`，并加了一条**行级**免检：同一行显式声明「该引用已被删除 / 已下线」时该行免检（中文用「已删除 / 已移除 / 已下线 / 不再存在」这类完成态，英文用 removed / deleted 的过去式）。新增失效仍会立刻让门变红。

## 五、阶段路线（逐级解锁）

```
S0 工具与基线 ─▶ S1 能力模型 ─▶ S2 记忆自进化 ─▶ S3 协议与方法面
                                                        │
                                                        ▼
S8 终验 ◀── S7 术语·导航·changelog ◀── S6 全站符号校准 ◀── S5 沙箱·上下文·扩展
                                                        │
                                        S4 Panel 与桌面壳 ◀┘
```

| 阶段 | 目标 | 主要产出 | 门 |
|---|---|---|---|
| **S0** | 门禁加固 + 基线盘点 | `scripts/method_audit.py` 解析常量方法名；本 ROADMAP 与 phase spec；失效清单快照 | G1–G4 |
| **S1** | 能力模型按收敛后现状重写 | `capabilities/{capability-model,trust-and-backends,hooks-and-prompts,slots-and-replacement,plugin-package}.mdx`（zh + en） | 全门 |
| **S2** | 记忆自我进化按落地行为重写 | `concepts/memory.mdx`、`architecture/{memory,memory-evolution}.mdx`、`gateway/methods/memory.mdx`（zh + en） | 全门 |
| **S3** | 协议与方法面补齐 | `gateway/protocol-v1.mdx`、`gateway/methods/{index,chat,memory}.mdx`（zh + en）；补 `chat.transcript_details`、`pty.history` | 全门 |
| **S4** | Panel 与桌面壳新模块 | `desktop-hosts/{panel,panel-runtime,plugin-ui,overview}.mdx`（zh + en） | 全门 |
| **S5** | 沙箱 · 上下文压缩 · 扩展重载 | `architecture/sandbox.mdx`、`security/sandboxing.mdx`、`concepts/{execution-engine,extensions}.mdx`（zh + en） | 全门 |
| **S6** | 全站符号与锚点校准 | 74 个 zh + 74 个 en 页对的失效符号、30 条失效锚点逐条判定 | 全门 |
| **S7** | 术语 · 导航 · changelog | `terminology.mdx` 收录本轮新术语；`meta.json` 收录新页；`changelog.mdx` 补 26.11 → 26.12 真实条目 | 全门 |
| **S8** | 终验 | `docs/VERIFICATION-2026-11-pass3.md` | 全门 |

每阶段一次提交，提交信息 `docs(phase-SN): <主题>`，正文列六门结果。

## 六、失效符号与锚点的判定规则（唯一裁决口径）

对每条失效符号，只允许四种处置，**不得凭空发明符号**：

1. **改名同步**：代码里存在近似名 → 把文档里的旧名换成代码里的真名，语义不变。
2. **路径/模块已删**：模块在代码里整体消失 → 改写该段为**当前真实路径**，或整段移入 `## 历史：…` 并标注删除来源提交。
3. **历史叙述**：该行讲的是旧世界 → 移入 `## 历史：<主题>` 小节，行内加「已删除 / 已移除 / renamed to」标记。
4. **蓝图内容**：确属规划中 → 加 `> **状态：规划中**` 横幅并给出蓝图文件出处。

判定必须以 **Aleph 仓库 grep 结果**为依据。`scripts/symbol_triage.py` 的近似匹配只是线索，不是结论。

## 七、执行方式

**阶段内单写者**：每个 Task 的文件集互不重叠；zh 与 en 由同一次改写一起产出，避免语义漂移。导航（`meta.json`）由主流程统一改。

硬性要求：

1. 每条现状断言必须带真实路径锚点；写不出锚点的断言要么删掉，要么标为「规划中」。
2. 蓝图（T3）内容一律标「规划中」并给出蓝图文件出处。
3. 不得编造 RPC 方法名、类型名、配置键、crate 名——一律从 Aleph 仓源码抄。
4. 改完必须在自己负责的文件上跑 `symbol_check.py` 与 `anchor_check.py`，确认没有引入新的基线外失效。
5. 每阶段收尾跑六门（末阶段加 G5）。

## 八、台账

见本文件末尾「阶段状态」表。每阶段完成后更新，写明各门结果与提交哈希。

## 阶段状态

| 阶段 | 状态 | 六门结果 | 提交 |
|---|---|---|---|
| S0 | 完成 | G1b 加固后判定「已注册未文档化」2 条（`chat.transcript_details`、`pty.history`）；G1 30 条锚点失效、G1c 148 条符号失效待修。G1 失效在本阶段后由 S1 修到 0 | `c1b03b1`、`0009a62`、`822d7d3` |
| S1 | 完成 | G1 锚点 0（新增 0）；G2 / G3 / G4 各 0；G5 `next build` / `tsc --noEmit` / `eslint` 退出码 0。G1b 剩 2 条（S3 范围）、G1c 剩 125 条（S6 范围），本阶段未新增 | `0af0854`（正文含 `822d7d3`） |
| S2 | 完成 | G1 锚点 0（新增 0）；G2 / G3 / G4 各 0；G5 `next build` / `tsc --noEmit` / `eslint` 退出码 0。G1b 剩 2 条（S3 范围）、G1c 剩 125 条（均为既有存量，本阶段新增 0） | `10a1153` |
| S3 | 完成 | G1 锚点 0（新增 0，页面 330、锚点 6340）；G1b census 396 方法、ghost 0、missing 0；G2 / G3 / G4 各 0；G5 `next build`（334 静态页）/ `tsc --noEmit` / `eslint` 退出码 0。G1c 剩 125 条（S6 范围），本阶段新增 0 | `69f142f` |
| S4 | 完成 | G1 锚点 0（新增 0，页面 330、锚点 6402）；G1b ghost 0、missing 0；G2 / G3 / G4 各 0；G5 `next build`（334 静态页）/ `tsc --noEmit` / `eslint` 退出码 0。G1c 125 条在本阶段棘轮为基线旧债（S6 范围），本阶段新增 0 | `86e99bb` |
| S5 | 完成 | G1 锚点 0（新增 0，页面 330、锚点 6408）；G1b census 396 方法、ghost 0、missing 0；G2 / G3 / G4 各 0；G5 `next build`（334 静态页）/ `tsc --noEmit` / `eslint` 退出码 0。G1c 125 条均为既有旧债，本阶段新增 0 | 待提交（`docs(phase-S5): …`） |
