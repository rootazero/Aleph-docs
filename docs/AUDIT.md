# Aleph 文档校对审计报告

> **生成时间**：2026-07-27
> **校对范围**：Aleph 最近 3 个月的提交（5989 次 / 3690 行 CHANGELOG / 1040 次 docs 改动）
> **校对基线**：Aleph v26.7.21（CHANGELOG 截至 [26.7.21]）
> **结论**：现有 324 个文档文件大量落后，需按下列清单分批重写

## 一、现状摘要

| 维度 | 数据 |
|---|---|
| 现有 docs 文件 | 324（zh/en 各一份） |
| Aleph 实际 RPC 方法 | ~265 个（去重后） |
| docs 中网关方法页 | 28 个（缺 ~30+ 个主题） |
| 新增未文档化模块 | 14 个（loop_graph、looping、goal、artifacts、export、hub、projects、runtimes、strategy、verification、vision、tool_metadata、tool_output、guardrails、voice） |
| 主要未写入特性 | chat/work/code mode、loop-graph 治理层、TLS SAN 自发现、Panel TOFU、Panel 内存 Vault、Teams Kanban、Cluster 生命周期 SSOT、session_compact 工具、MoA 审计、loop pause/resume |

## 二、章节级审计

| 章节 | 文件数 | 严重度 | 主要问题 |
|---|---|---|---|
| getting-started | 6 | 中 | CLI 命令、配置 schema、wizard 流程未跟进新特性 |
| philosophy | 5 | 中 | 五层模型自描述基本对，但 redlines 与 AGENTS.md 偏差较大 |
| concepts | 51 | 高 | 大量引用旧路径 / 旧类型；新特性未覆盖 |
| architecture | 24 | 高 | harness.mdx 仍标 `agent_loop` 旧路径；loop_graph 完全缺失 |
| gateway + methods | 30+ | 高 | methods 文件仅 28 个，缺 acp / agents / artifacts / channels / cluster / config / discord / dreaming / embedding_providers / environments / extensions / fetch_config / fs / gateway_* / generation_providers / group_chat / hooks / identity / insights / mcp_config / memory_config / projects / providers / rerank_config / route_config / routing_rules / runtimes / search_config / secret_approvals / secret_migration / secrets / security_config / session.* / subagent / teams.* / tools.* / trace.* / voice / workspace.* 等大类 |
| interfaces | 5 | 高 | iMessage 新增未文档；Telegram/Discord 大改未跟进 |
| tools | 5 | 中 | 缺 round-3 MCP/plugin/skill LLM-read hardening；cat-steer verbs 等 |
| security | 5 | 高 | TLS / TOFU / 证书信任 / pairing 修复未写入 |
| automation | 3 | 中 | hooks 注入上下文限额 / 同意 / 库存未写 |
| cli | 5 | 中 | cargo install 命令、CLI 命令随版本调整未跟进 |
| development | 4 | 中 | 提及旧 build 命令；增量构建、Tauri 升级未跟进 |
| api | 2 | 低 | 较稳定，但需追加新导出符号 |
| terminology | 1 | 低 | 增量追加新术语即可 |
| changelog | 1 | 高 | 当前未与 Aleph CHANGELOG 对齐（甚至内容是空白模板） |

## 三、文件级审计清单

> **标记说明**：
> - 🔴 **REWRITE** — 结构性过时，需按 26.7.21 重写
> - 🟡 **UPDATE** — 内容基本可用，需补齐新特性/路径/术语
> - 🟢 **OK** — 变动不大，必要时小幅校对
> - ➕ **NEW** — 缺失或必须新增的文件（仅在不改结构的前提下补齐）

### 3.1 顶层 / 导航

| 文件 | 状态 | 关键问题 |
|---|---|---|
| `content/docs/zh/index.mdx` | 🔴 REWRITE | 架构图仍是旧五层；缺 loop_graph / TLS / Panel 内存等亮点；卡片列表未跟进新章节 |
| `content/docs/zh/terminology.mdx` | 🟡 UPDATE | 缺 `chat/work/code mode`、`loop_graph`、`governance_metrics`、`TOFU` 等术语 |
| `content/docs/zh/changelog.mdx` | 🔴 REWRITE | 内容几乎是占位，需从 Aleph CHANGELOG 26.7.x 系列摘要 |
| `content/docs/zh/meta.json` | 🟡 UPDATE | 顺序与新结构基本一致，但需校验 |
| `content/docs/en/**` | 全部同步 | en 在 zh 改完后同步 |

### 3.2 getting-started（6 文件）

| 文件 | 状态 | 关键问题 |
|---|---|---|
| `installation.mdx` | 🟡 UPDATE | 安装命令、磁盘要求、Rust toolchain 1.95 未提 |
| `quick-start.mdx` | 🟡 UPDATE | `aleph chat` / `aleph wizard` 命令已演进 |
| `wizard.mdx` | 🔴 REWRITE | 向导新增 chat/work/code mode 选择 / TLS / TOFU 步骤 |
| `deployment.mdx` | 🟡 UPDATE | 部署/容器化建议未跟进新拓扑 |
| `configuration.mdx` | 🔴 REWRITE | 配置 schema 大变；新增 session mode、policy、approval、TLS 等节 |
| `meta.json` | 🟢 OK | |

### 3.3 philosophy（5 文件）

| 文件 | 状态 | 关键问题 |
|---|---|---|
| `overview.mdx` | 🟡 UPDATE | 体系表述基本可保留；需引用 CHANGELOG 新增的"第三双生子"等概念 |
| `five-layers.mdx` | 🟢 OK | 抽象层描述尚可，仅需小补 |
| `domain-model.mdx` | 🟡 UPDATE | 域类型大幅扩展 |
| `agent-thinking.mdx` | 🟡 UPDATE | Think→Act 循环已重构 |
| `redlines.mdx` | 🔴 REWRITE | R1-R10 等硬性约束大幅更新 |

### 3.4 concepts（51 文件）

按主题分 4 子批：

**子批 A — 基础内核（13 文件）**

| 文件 | 状态 | 关键问题 |
|---|---|---|
| `identity-context.mdx` | 🟡 UPDATE | 委托角色链、生命周期在链内、签名者所有权未写 |
| `core-types.mdx` | 🟡 UPDATE | 引入 SessionEvent / TurnId / LoopState / GoalStore 等新类型 |
| `domain-model.mdx` | 🟡 UPDATE | 与 architecture/domain-model 对齐 |
| `messages.mdx` | 🔴 REWRITE | UnifiedMessage / ProviderDelta 取代旧消息结构 |
| `event-system.mdx` | 🟡 UPDATE | SessionEvent 体系大改；broadcast RecvError::Lagged 已修 |
| `intent-detection.mdx` | 🟡 UPDATE | 跟随 routing/intent 重构 |
| `configuration.mdx` | 🔴 REWRITE | schema 大变 |
| `logging.mdx` | 🟡 UPDATE | 日志轮转 / ALEPH-BOOT marker 未提 |
| `error-handling.mdx` | 🟡 UPDATE | 网关错误链已 single-source |
| `workspaces.mdx` | 🟡 UPDATE | workspace RPC 新增 archive 等 |
| `daemon.mdx` | 🟡 UPDATE | day-boundary rotation / 睡眠抑制剂修复未提 |
| `discovery.mdx` | 🟡 UPDATE | 改为按需 MCP 检索 |
| `wizard.mdx` | 🔴 REWRITE | 同 getting-started/wizard |

**子批 B — Agent / Skill / Extension（13 文件）**

| 文件 | 状态 | 关键问题 |
|---|---|---|
| `agent-runtime.mdx` | 🟡 UPDATE | 状态机 / 子代理未提 mid-turn interruptible |
| `agent-components.mdx` | 🟡 UPDATE | 同上 |
| `prompt-system.mdx` | 🔴 REWRITE | layers 大改（28 个 layers vs 旧 6 层）；prompt 极简化未提 |
| `skills.mdx` / `skill-system.mdx` | 🟡 UPDATE | 触发词增强、Markdown skill 作者指南未提 |
| `extensions.mdx` / `extension-system.mdx` / `extensions-store.mdx` | 🟡 UPDATE | 插件 + 技能统一机制未提 |
| `builtin-tools.mdx` | 🟡 UPDATE | 工具集已随版本变更 |
| `tool-infrastructure.mdx` | 🟡 UPDATE | 资源并发声明、parallel partition |
| `protocol-adapters.mdx` | 🟡 UPDATE | Telegram/Discord 适配层大量删除 |
| `mcp-integration.mdx` | 🟡 UPDATE | resources/subscribe 已删；最长前缀匹配 |
| `capability-system.mdx` | 🟡 UPDATE | 能力账本 / runtime install ledger |
| `browser-automation.mdx` | 🟡 UPDATE | canvas inspector 撤除 |

**子批 C — 系统级（13 文件）**

| 文件 | 状态 | 关键问题 |
|---|---|---|
| `a2a-protocol.mdx` | 🟡 UPDATE | 子代理授权恢复 |
| `acp-protocol.mdx` | 🟡 UPDATE | presets/test/update |
| `clawhub.mdx` | 🟡 UPDATE | browse/detail/install/search |
| `task-scheduling.mdx` | 🟡 UPDATE | cron stubs→real、heartbeat stubs→real |
| `generation.mdx` | 🟡 UPDATE | provider failover 重构；pricing 单源 |
| `media-processing.mdx` | 🟢 OK | 较稳定 |
| `search.mdx` | 🟡 UPDATE | memory retrieve_with_trace、graph search 改 |
| `resilience.mdx` | 🟡 UPDATE | Guardian judge payload 隐藏密钥、probe 拒绝危险工具 |
| `arena.mdx` | 🟡 UPDATE | 已重构多次 |
| `group-chat.mdx` | 🟡 UPDATE | Kanban 重构、成员工具面 |
| `teams.mdx` | 🟡 UPDATE | Team 节点融合 graph、多模板 |
| `execution-engine.mdx` | 🟡 UPDATE | 缺截图/录制/输入修复 |
| `ai-providers.mdx` | 🟡 UPDATE | failover 重构；删除 ~2000 行不可达代码 |

**子批 D — 安全/工具辅助（12 文件）**

| 文件 | 状态 | 关键问题 |
|---|---|---|
| `approval.mdx` | 🔴 REWRITE | 默认 fail-closed；guardian judge |
| `security-primitives.mdx` | 🟡 UPDATE | pairing store 单源 |
| `pii-protection.mdx` | 🟡 UPDATE | review 修复 |
| `secret-management.mdx` | 🟡 UPDATE | secret_approvals / migration |
| `supervisor-verification.mdx` | 🟡 UPDATE | 取消 DiminishingReturnsDetector 硬停 |
| `markdown-utils.mdx` | 🟢 OK | 较稳定 |
| `bundled.mdx` | 🟡 UPDATE | bundled.sync RPC 新增；symlink 拒收 |
| `gateway.mdx` | 🟡 UPDATE | 错误链 single-source、WS 任务泄漏修复 |
| `thinker.mdx` | 🔴 REWRITE | 与 architecture/thinker 重复；layers 列表过时 |
| `memory.mdx` | 🟡 UPDATE | self-evolution discipline (SkillOpt)、记忆压缩 |
| `clarification.mdx` | 🟡 UPDATE | clarification.resolve/pending |
| `intent-detection.mdx` | 🟡 UPDATE | 见子批 A |

### 3.5 architecture（24 文件）

| 文件 | 状态 | 关键问题 |
|---|---|---|
| `overview.mdx` | 🔴 REWRITE | 五层图已不准；缺 loop_graph / looping / goal / hub |
| `gateway.mdx` | 🟡 UPDATE | TLS / TOFU / pairing 修复 |
| `orchestrator.mdx` | 🟡 UPDATE | 与新 harness 边界 |
| `harness.mdx` | 🔴 REWRITE | 仍标 agent_loop 旧路径；think/act/guardrails 新文件结构 |
| `thinker.mdx` | 🔴 REWRITE | 与 concepts/thinker 重复；layers 列表过时 |
| `dispatcher.mdx` | 🟡 UPDATE | dispatcher 改造 |
| `executor.mdx` | 🟡 UPDATE | 并行调度 / 资源声明 |
| `memory.mdx` | 🟡 UPDATE | self-evolution |
| `sandbox.mdx` | 🟡 UPDATE | 多模隔离 |
| `session-service.mdx` | 🟡 UPDATE | presence / 模板环境排序 |
| `providers.mdx` | 🟡 UPDATE | failover 重构 |
| `memory-evolution.mdx` | 🟡 UPDATE | dreaming |
| `desktop-bridge.mdx` | 🟡 UPDATE | macOS 屏幕录制 / AX 解析 |
| `cluster.mdx` | 🔴 REWRITE | 生命周期 SSOT、归一化 CJK、enroll/deregister |
| `a2a.mdx` | 🟡 UPDATE | 子代理授权恢复 |
| `acp.mdx` | 🟡 UPDATE | presets |
| `clawhub.mdx` | 🟡 UPDATE | browse/detail/install/search |
| `groupchat.mdx` | 🟡 UPDATE | 团队表面重写 |
| `teams.mdx` | 🔴 REWRITE | Team 节点 / Kanban / 模板工具面 |
| `workflow.mdx` | 🟡 UPDATE | interop bare-scan |
| `worldmodel.mdx` | 🟡 UPDATE | 与 graph_topology 关系 |
| `proactive-dispatcher.mdx` | 🟡 UPDATE | cron/heartbeat stubs→real |
| `design-patterns.mdx` | 🟡 UPDATE | 增补 R1-R10 实战 |
| ➕ `loop-graph.mdx` | ➕ NEW | 治理拓扑层（26.7.21 新增） |
| ➕ `looping.mdx` | ➕ NEW | loop 暂停/恢复 |
| ➕ `goal.mdx` | ➕ NEW | 目标子系统 |
| ➕ `artifacts.mdx` | ➕ NEW | 工件存储 / 交付物 |
| ➕ `verification.mdx` | ➕ NEW | 验证器 / verifier |
| ➕ `vision.mdx` | ➕ NEW | 视觉子系统 |

> 注：架构章节保留原结构，因此新文件**暂不新增**（用户偏好"保留结构"），新主题作为现有 thinker / memory / execution-engine 的延伸章节描述。

### 3.6 gateway + methods

`protocol.mdx` 与 `auth.mdx`：

| 文件 | 状态 | 关键问题 |
|---|---|---|
| `gateway/protocol.mdx` | 🔴 REWRITE | 引入 TLS 子协议、原子 regen marker、TOFU handshake |
| `gateway/auth.mdx` | 🔴 REWRITE | 新增设备 ticket、Token rotate、TOFU 流程 |

`gateway/methods/` — 现 28 个文件 vs 实际 265 个 RPC 方法：

| 现有 docs 文件 | 状态 | 涉及实际方法 |
|---|---|---|
| `agent.mdx` | 🟡 UPDATE | agent.run/status/cancel/list |
| `arena.mdx` | 🟡 UPDATE | dreaming/insights 相关 |
| `browser.mdx` | 🟡 UPDATE | 浏览器配置 |
| `channels.mdx` | 🟡 UPDATE | channel.* + channels.* + channels.set_agent + channel.pairing.* |
| `config.mdx` | 🔴 REWRITE | config.*（schema/get/path/patch/reload/validate/error/reloaded） |
| `cron.mdx` | 🟡 UPDATE | cron.*（stubs→real） |
| `daemon.mdx` | 🟡 UPDATE | daemon.* + 路径 |
| `events.mdx` | 🟡 UPDATE | gateway.events + SessionEvent |
| `exec.mdx` | 🟡 UPDATE | tools.invoke/cancel_call/in_flight/catalog/effective |
| `extensions.mdx` | 🟡 UPDATE | extensions.* + plugins.* + plugin.* |
| `graph.mdx` | 🟡 UPDATE | graph.* |
| `group_chat.mdx` | 🟡 UPDATE | group_chat.* |
| `heartbeat.mdx` | 🟡 UPDATE | heartbeat.* |
| `identity.mdx` | 🟡 UPDATE | identity.* + agents.* 部分 |
| `index.mdx` | 🟡 UPDATE | 完整 RPC 表 |
| `logs.mdx` | 🟡 UPDATE | logs.* |
| `mcp.mdx` | 🟡 UPDATE | mcp.* + mcp_config.* |
| `memory.mdx` | 🟡 UPDATE | memory.* |
| `plugins.mdx` | 🟡 UPDATE | plugins.* + plugin.* |
| `providers.mdx` | 🟡 UPDATE | providers.* + embedding_providers.* + generation_providers.* |
| `runs.mdx` | 🟡 UPDATE | trace.* |
| `services.mdx` | 🟡 UPDATE | services.* |
| `session.mdx` | 🟡 UPDATE | session.* + sessions.* |
| `skills.mdx` | 🟡 UPDATE | skills.* + bundled.sync |
| `teams.mdx` | 🟡 UPDATE | teams.* + agents.teams |
| `wizard.mdx` | 🟡 UPDATE | wizard 相关 |
| `workspace.mdx` | 🟡 UPDATE | workspace.* + projects.* |
| `meta.json` | 🟡 UPDATE | 增加新文件 |

**需新增的 RPC 方法分组**（可合并到现有文件）：

- ➕ `acp.mdx` — acp.*（create/delete/get/list/presets/presets_meta/set_enabled/test/update + sessions_*）
- ➕ `agents.mdx` — agents.*（含 files.*/tools_schema/teams/bindings）+ agents.set_default + 归档旧 `agent.mdx` 部分
- ➕ `artifacts.mdx` — artifacts.list + session.export_html
- ➕ `behavior-config.mdx`（可并入 config.mdx）
- ➕ `channels.mdx`（已有但要扩充 channel.*/channels.*/pairing.*/discord.*）
- ➕ `cluster.mdx` — cluster.deregister/enroll/environments_list
- ➕ `config-providers.mdx` — providers.* / generation_providers.* / embedding_providers.*（或并入 providers.mdx）
- ➕ `discord.mdx` — discord.*（并入 channels.mdx）
- ➕ `embedding-providers.mdx`（并入 providers.mdx）
- ➕ `environments.mdx` — environments.list
- ➕ `fetch-config.mdx`（并入 config.mdx）
- ➕ `fs.mdx` — fs.* + environments.list
- ➕ `gateway-tokens.mdx` — gateway.ticket.* + gateway.token.* + gateway.devices.* + gateway.credentials + gateway.identity.* + gateway.metrics.*
- ➕ `generation-providers.mdx`（并入 providers.mdx）
- ➕ `goals.mdx` — looping/goal 相关（仍在 gateway 路由上）
- ➕ `hooks.mdx` — hooks.*
- ➕ `insights.mdx` — insights.tools + dreaming.*（部分并入 arena）
- ➕ `mcp-config.mdx` — mcp_config.*
- ➕ `memory-config.mdx`（并入 memory.mdx）
- ➕ `projects.mdx` — projects.*
- ➕ `pty.mdx` — pty.*
- ➕ `routing.mdx` — routing_rules.* + route_config.* + channels.set_agent（部分并入 channels.mdx）
- ➕ `runtimes.mdx` — runtimes.*
- ➕ `search-config.mdx`（并入 config.mdx）
- ➕ `secrets.mdx` — secrets.* + secret_approvals + secret_migration
- ➕ `security-config.mdx`（并入 config.mdx）
- ➕ `subagent.mdx` — subagent.tree
- ➕ `teams.mdx`（已有但要扩 teams.* + agents.teams）
- ➕ `tools.mdx`（已有但要扩 tools.*）
- ➕ `trace.mdx`（与现有 runs.mdx 合并）
- ➕ `voice.mdx` — voice.*
- ➕ `workspace.mdx`（已有但要扩 workspace.* + projects.*）

> 实际新增时，**优先合并到现有文件**，避免文件爆炸。仅在主题自成体系时新建：
> - `gateway-tokens.mdx`（设备 / 凭据 / 票 / 令牌独立体系）
> - `secrets.mdx`（机密管理独立）
> - `voice.mdx`（语音自成体系）
> - 其余合并到对应主题文件

### 3.7 interfaces / tools / security / automation / cli

| 文件 | 状态 | 关键问题 |
|---|---|---|
| `interfaces/overview.mdx` | 🔴 REWRITE | 缺 iMessage；Telegram/Discord 大改 |
| `interfaces/webchat.mdx` | 🟡 UPDATE | Webchat/serve_webchat |
| `interfaces/telegram.mdx` | 🔴 REWRITE | 删除 ~2.6k LOC，统一到路由器 |
| `interfaces/discord.mdx` | 🔴 REWRITE | 平行层删除 |
| `interfaces/imessage.mdx` | 🟡 UPDATE | 新增；channel 入口已加 |
| `tools/overview.mdx` | 🟡 UPDATE | 工具分类调整 |
| `tools/builtin.mdx` | 🟡 UPDATE | builtin_tools 模块重组 |
| `tools/mcp.mdx` | 🟡 UPDATE | longest-prefix / cat-steer |
| `tools/browser.mdx` | 🟡 UPDATE | canvas inspector 撤除 |
| `tools/creating.mdx` | 🟡 UPDATE | 文档较稳定，但需更新路径 |
| `security/overview.mdx` | 🔴 REWRITE | TLS / TOFU / 失败关闭 / 签名链 |
| `security/pairing.mdx` | 🔴 REWRITE | 单源路由器 |
| `security/sandboxing.mdx` | 🟡 UPDATE | macOS 屏幕录制修复 |
| `security/exec-approval.mdx` | 🔴 REWRITE | approval policy 改进 |
| `security/ipc.mdx` | 🟡 UPDATE | WS 任务泄漏修复 |
| `automation/events.mdx` | 🟡 UPDATE | SessionEvent 体系 |
| `automation/hooks.mdx` | 🔴 REWRITE | 注入限额 / 同意 / 库存 |
| `automation/cron-jobs.mdx` | 🟡 UPDATE | stubs→real |
| `cli/commands.mdx` | 🔴 REWRITE | 命令随 wizard 重写变化 |
| `cli/agent.mdx` | 🟡 UPDATE | aleph chat / mode 选项 |
| `cli/config.mdx` | 🟡 UPDATE | 配置命令 |
| `cli/gateway.mdx` | 🟡 UPDATE | 子命令变化 |

### 3.8 development / api

| 文件 | 状态 | 关键问题 |
|---|---|---|
| `development/building.mdx` | 🟡 UPDATE | Rust 1.95、增量构建 |
| `development/testing.mdx` | 🟡 UPDATE | proptest 工具、fixtures |
| `development/contributing.mdx` | 🟡 UPDATE | R1-R10 已升级 |
| `development/design-patterns.mdx` | 🟡 UPDATE | 与 architecture/design-patterns 同步 |
| `api/rust.mdx` | 🟡 UPDATE | 增量更新导出符号 |
| `api/jsonrpc.mdx` | 🟡 UPDATE | 引用 gateway/methods |

### 3.9 en/** 镜像

所有 zh 文件改动后，en 文件需同步（保留结构）。

## 四、未列入审计的元数据/导航

- `content/docs/zh/{concepts,architecture,getting-started,philosophy,gateway/methods,interfaces,tools,security,automation,cli,development,api}/meta.json` — 校对路径与现有顺序一致即可
- `content/docs/{zh,en}/meta.json` — 校对路径
- `content/docs/zh/{getting-started,philosophy,concepts,architecture,gateway,interfaces,tools,security,automation,cli,development,api}/index.mdx` — 部分章节缺 index.mdx，按需补

## 五、推荐执行顺序

1. **Batch 1** — 顶层：meta.json × 12 + index.mdx + terminology.mdx + changelog.mdx
2. **Batch 2** — 入门/理念：getting-started × 6 + philosophy × 5
3. **Batch 3A-3D** — 概念 51 文件按子批
4. **Batch 4A-4C** — 架构 24 文件按主题
5. **Batch 5** — 网关 protocol/auth + methods（含新增 5-8 个文件）
6. **Batch 6** — interfaces/tools/security/automation/cli
7. **Batch 7** — development + api
8. **Batch 8** — en 同步 + lint/typecheck/build

## 六、风险与提示

- **不破坏站外链接**：保留原文件名；新增章节并入现有同名文件
- **每次批量结束提交前**，先做 grep 校验确保旧链接不悬空
- en/zh 双语内容尽量保持一致，zh 先行，en 跟进
- 不写虚构事实；优先引用 Aleph 源码符号、CHANGELOG、docs/reference/*.md