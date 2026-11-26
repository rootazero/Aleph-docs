# Aleph 文档站第四轮终验报告（2026-11）

> 本文件由 `scripts/verification_report.py` 生成**机器部分**，逐阶段结论由主 agent 撰写。
> 复核命令：`python3 scripts/run_gates.py --repo ../Aleph --build`。

## 门禁结果

| 门 | 结果 | 明细 |
|----|------|------|
| G1 锚点门 | PASS | 页面 330，锚点 6574，失效 0（路径 0，裸文件名 0；新增 0，基线旧债 0；历史免检行 2141） |
| G1b 方法册 | PASS | census methods: 396   documented dotted tokens: 467<br>ghost (documented, absent from code): 0（新增 0，基线旧债 0）<br>missing (registered, undocumented): 0（新增 0，基线旧债 0） |
| G1c 符号门 | PASS | 页面 330，失效 0（新增 0，基线旧债 0） |
| G1d 工具名门 | PASS | registered builtin tools: 209   documented tool claims: 167<br>ghost (documented, not registered): 0（新增 0，基线旧债 0）<br>missing (registered, undocumented): 0（新增 0，基线旧债 0） |
| G2 事实门 | PASS |  |
| G3 结构门 | PASS |  |
| G4 双语门 | PASS |  |
| G5 构建门 | PASS | `next build` / `tsc --noEmit` / `eslint` 退出码 0（73.4s） |

## 规模

- 页面：zh 165 页 / en 165 页
- 代码锚点：6574 个被检查，0 个失效

## 基线棘轮

`scripts/baseline.json` 各段剩余条数（全 0 表示无存量债务）：

| 段 | 条数 |
|----|------|
| `anchor` | 0 |
| `bare_name` | 0 |
| `bilingual` | 0 |
| `facts` | 0 |
| `method_ghost` | 0 |
| `method_missing` | 0 |
| `structure` | 0 |
| `symbol` | 0 |
| `tool_ghost` | 0 |
| `tool_missing` | 0 |

## 逐页判定表

| 页面 | 判定 | 依据 | 门结果 |
|------|------|------|--------|
| `content/docs/zh/api/jsonrpc.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/api/rust.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/1-2-3-4-model.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/a2a.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/acp.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/clawhub.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/cluster.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/design-patterns.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/desktop-bridge.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/dispatcher.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/executor.mdx` | 本轮改写 | S2：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/gateway.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/groupchat.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/harness.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/memory-evolution.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/memory.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/orchestrator.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/overview.mdx` | 本轮改写 | S2：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/proactive-dispatcher.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/providers.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/resilience.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/routing.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/sandbox.mdx` | 本轮改写 | S2、S3、S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/session-service.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/sessions.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/teams.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/thinker.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/tools.mdx` | 本轮改写 | S2：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/workflow.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/worldmodel.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/automation/cron-jobs.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/automation/events.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/automation/hooks.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/capabilities/capability-model.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/capabilities/hooks-and-prompts.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/capabilities/plugin-package.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/capabilities/slots-and-replacement.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/capabilities/trust-and-backends.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/changelog.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/cli/agent.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/cli/commands.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/cli/config.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/cli/gateway.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/a2a-protocol.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/acp-protocol.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/agent-components.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/agent-runtime.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/ai-providers.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/approval.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/arena.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/artifacts-deliverables.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/browser-automation.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/builtin-tools.mdx` | 本轮改写 | S1：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/bundled.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/capability-system.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/clarification.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/clawhub.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/configuration.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/core-types.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/daemon.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/discovery.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/domain-model.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/error-handling.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/event-system.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/execution-engine.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/extension-system.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/extensions-store.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/extensions.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/gateway.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/generation.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/group-chat.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/identity-context.mdx` | 本轮改写 | S2、S4：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/intent-detection.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/logging.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/looping-goal-strategy.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/markdown-utils.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/mcp-integration.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/media-processing.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/memory.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/messages.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/pii-protection.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/prompt-system.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/protocol-adapters.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/resilience.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/search.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/secret-management.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/security-primitives.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/skill-system.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/skills.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/supervisor-verification.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/task-scheduling.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/teams.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/thinker.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/tool-infrastructure.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/voice-streaming.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/wizard.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/workspaces.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/desktop-hosts/overview.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/desktop-hosts/panel-runtime.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/desktop-hosts/panel.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/desktop-hosts/plugin-ui.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/development/building.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/development/contributing.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/development/design-patterns.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/development/testing.mdx` | 本轮改写 | S4：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/auth.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/agent.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/arena.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/browser.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/channels.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/chat.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/config.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/cron.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/daemon.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/events.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/exec.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/extensions.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/graph.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/group_chat.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/heartbeat.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/identity.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/index.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/logs.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/mcp.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/memory.mdx` | 本轮改写 | S2：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/plugins.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/providers.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/pty.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/runs.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/services.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/session.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/skills.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/teams.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/tools.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/wizard.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/workspace.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/protocol-v1.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/protocol.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/getting-started/configuration.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/getting-started/deployment.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/getting-started/installation.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/getting-started/quick-start.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/getting-started/wizard.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/index.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/interfaces/discord.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/interfaces/imessage.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/interfaces/overview.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/interfaces/telegram.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/interfaces/webchat.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/philosophy/agent-thinking.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/philosophy/domain-modeling.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/philosophy/five-layers.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/philosophy/overview.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/philosophy/redlines.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/security/exec-approval.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/security/ipc.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/security/overview.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/security/pairing.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/security/sandboxing.mdx` | 本轮改写 | S2：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/terminology.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/tools/browser.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/tools/builtin.mdx` | 本轮改写 | S1、S3、S4、S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/tools/creating.mdx` | 本轮改写 | S2：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/tools/mcp.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/tools/overview.mdx` | 本轮改写 | S1：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/api/jsonrpc.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/api/rust.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/1-2-3-4-model.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/a2a.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/acp.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/clawhub.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/cluster.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/design-patterns.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/desktop-bridge.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/dispatcher.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/executor.mdx` | 本轮改写 | S2：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/gateway.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/groupchat.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/harness.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/memory-evolution.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/memory.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/orchestrator.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/overview.mdx` | 本轮改写 | S2：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/proactive-dispatcher.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/providers.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/resilience.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/routing.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/sandbox.mdx` | 本轮改写 | S2、S3、S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/session-service.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/sessions.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/teams.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/thinker.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/tools.mdx` | 本轮改写 | S2：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/workflow.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/worldmodel.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/automation/cron-jobs.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/automation/events.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/automation/hooks.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/capabilities/capability-model.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/capabilities/hooks-and-prompts.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/capabilities/plugin-package.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/capabilities/slots-and-replacement.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/capabilities/trust-and-backends.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/changelog.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/cli/agent.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/cli/commands.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/cli/config.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/cli/gateway.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/a2a-protocol.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/acp-protocol.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/agent-components.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/agent-runtime.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/ai-providers.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/approval.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/arena.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/artifacts-deliverables.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/browser-automation.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/builtin-tools.mdx` | 本轮改写 | S1：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/bundled.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/capability-system.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/clarification.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/clawhub.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/configuration.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/core-types.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/daemon.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/discovery.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/domain-model.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/error-handling.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/event-system.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/execution-engine.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/extension-system.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/extensions-store.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/extensions.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/gateway.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/generation.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/group-chat.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/identity-context.mdx` | 本轮改写 | S2、S4：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/intent-detection.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/logging.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/looping-goal-strategy.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/markdown-utils.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/mcp-integration.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/media-processing.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/memory.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/messages.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/pii-protection.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/prompt-system.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/protocol-adapters.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/resilience.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/search.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/secret-management.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/security-primitives.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/skill-system.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/skills.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/supervisor-verification.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/task-scheduling.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/teams.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/thinker.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/tool-infrastructure.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/voice-streaming.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/wizard.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/workspaces.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/desktop-hosts/overview.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/desktop-hosts/panel-runtime.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/desktop-hosts/panel.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/desktop-hosts/plugin-ui.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/development/building.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/development/contributing.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/development/design-patterns.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/development/testing.mdx` | 本轮改写 | S4：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/gateway/auth.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/agent.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/arena.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/browser.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/channels.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/chat.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/config.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/cron.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/daemon.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/events.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/exec.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/extensions.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/graph.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/group_chat.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/heartbeat.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/identity.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/index.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/logs.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/mcp.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/memory.mdx` | 本轮改写 | S2：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/plugins.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/providers.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/pty.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/runs.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/services.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/session.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/skills.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/teams.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/tools.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/wizard.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/workspace.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/protocol-v1.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/protocol.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/getting-started/configuration.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/getting-started/deployment.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/getting-started/installation.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/getting-started/quick-start.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/getting-started/wizard.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/index.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/interfaces/discord.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/interfaces/imessage.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/interfaces/overview.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/interfaces/telegram.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/interfaces/webchat.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/philosophy/agent-thinking.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/philosophy/domain-modeling.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/philosophy/five-layers.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/philosophy/overview.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/philosophy/redlines.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/security/exec-approval.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/security/ipc.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/security/overview.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/security/pairing.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/security/sandboxing.mdx` | 本轮改写 | S2：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/terminology.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/tools/browser.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/tools/builtin.mdx` | 本轮改写 | S1、S3、S4、S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/tools/creating.mdx` | 本轮改写 | S2：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/tools/mcp.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/tools/overview.mdx` | 本轮改写 | S1：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |

## 逐阶段结论

<!-- MANUAL:BEGIN -->
### 本轮范围
第四轮以 Aleph `main` `7fb540b44`（与第三轮终验时同一个 commit，代码侧未前进）为真值基线，专攻**工具面**，并新增第四道门 G1d「内置工具名普查门」。

起因是一类第三轮没能收敛的系统性偏差：文档里长期写着一个不存在的工具名 `bash_exec`，而代码注册的真名是 `bash`；一批**模块名**（`process_registry`、`command_canonicalize`、`command_ledger`、`crawl4ai`、`scratchpad_registry`、`config_guide`、`permission_tool`）被当成工具写进表格；另有一批**已注册但全站无文档**的工具（24 个）长期缺席。逐页人眼校准对这类偏差收敛很慢，所以先把它变成门禁。

起点 commit `a535ac4`（第三轮终验），终点为本轮 S7。计划见 `docs/superpowers/plans/2026-11-26-aleph-docs-calibration-pass4.md`，台账见 `docs/ROADMAP-2026-11-pass4.md`。

### 真值分层（唯一裁决口径）
沿用第三轮的 T1–T5，本轮追加一条工具面的专用层级：

6. **T0 工具真值**：内置工具的名字与描述以 `src/executor/builtin_registry/definitions.rs`（`BUILTIN_TOOL_DEFINITIONS`、`REGISTRY_ONLY_DESCRIPTIONS`）与 `src/executor/mod.rs`（`TOOLS_OUTSIDE_DEFINITIONS`、`REGISTRY_ONLY_TOOL_NAMES`、`is_builtin_tool_name`）为准，再加上按请求注入的 `get_tool_schema`（`src/tools/schema_lookup.rs:21`）与 MCP 桥接工具（`src/mcp/tool_bridge.rs`）。文档里出现的工具名必须落在这张名单上；名单之外的名字要么改，要么在代码里找到它。

### 逐阶段结论
| 阶段 | 提交 | 结论 |
|------|------|------|
| S0 门禁与基线 | `a860434`、`ecabd85` | 新增 G1d「内置工具名普查门」。代码侧不再正则扫源码树，改用代码自己的权威名单（209 个注册工具）；文档侧把「工具表首列」与 `tool_use("x")` / `allows_tool("x")` / `tool_call("x")` / `invoke_tool("x")` 调用点当作**宣称**，做双向判定：宣称但未注册 = ghost，注册但未文档 = missing。脚本 `scripts/tool_audit.py`，接入 `scripts/run_gates.py`（七道门），`scripts/baseline.json` 增 `tool_ghost` / `tool_missing` 两段。首跑：registered 209 / claims 159 / ghost 9 / missing 24。 |
| S1 工具目录校准 | `26b5852` | 重写 zh/en `tools/builtin.mdx`、`tools/overview.mdx`、`concepts/builtin-tools.mdx`：删掉 9 个幽灵名（`bash_exec`、`config_guide`、`permission_tool`、`scratchpad_registry`、`process_registry`、`command_canonicalize`、`command_ledger`、`crawl4ai`），后四个模块名改写成「这是实现模块，不是注册工具」的散文；补登记 24 个此前全站缺席的工具（工作区 / 项目 / 代理档案、运行时与外部依赖、通话生命周期、团队生命周期与协作、会话折叠还原、浏览器 companion 等）；「注册摘要」从过期的「内置工具不通过 builder 注册」改写为**四个登记面**（目录 178 项 / 仅注册表 23 项 / 目录外 `subagent` + `tool_search` / 按请求注入 `get_tool_schema`），并写明六个 MCP 桥接工具按能力门注册；装配入口更正为 `BuiltinToolRegistry::with_config()`。 |
| S2 调用面校准 | `6ce9af4` | 全站 20 处 `bash_exec` → `bash`；`tool_use("bash", {"command": …})` 的参数键改成真名 `cmd`；`architecture/tools.mdx` 参数表按 `BashExecArgs` / `CodeExecArgs` / `CodeCheckArgs` 订正（`code_check` 此前误写成 `language` / `code`）；`subagent` 标注为目录外工具；`gateway/methods/memory.mdx` 删掉不存在的 `forget`，并写清删除走 `remember` 的 Remove 操作。 |
| S3 后台作业现状 | `2a756ee` | 补齐 `bash` 的后台作业模型（zh/en `tools/builtin.mdx` 新增小节 + `architecture/sandbox.mdx` 呼应）：四个 `process_action`、8 KB 部分输出尾、60 / 170 秒等待窗口、3600 秒默认与 4 小时上限、按会话隔离（每会话 8 / 全局 32 / 登记簿 64 / 命令预览 120 字符）、owned worktree 下拒绝后台、内容门与实时尾随、登记簿纯内存而进程流水跨进程、子进程可见 `ALEPH_SESSION_ID` 与 `ALEPH_TOOL_NAME=bash`；并写清「后台只绕开 180 秒前台上限，沙箱管道不变」。 |
| S4 未登记工具落位与豁免清零 | `baa4b9e` | 补 `capability_projection_diagnostics` 的真实语义（默认关闭、需 `ALEPH_CAPABILITY_DIAGNOSTICS=1` 才投放、三项 operator 检查、七种操作）；订正 S1 一处措辞（persona 文本是 `SOUL.md`，走 `identity.set`，代码里没有 `agent_files` 工具）；豁免清单清零——`testing.mdx` 表头改成「命令 / crate」，`identity-context.mdx` 的假想工具名 `translate` 换成真有的 `code_exec`，`EXEMPT_NAMES` 改为空字典。G1d 由此从 ghost 9 / missing 24 收到 **0 / 0**。 |
| S5 未合并分支标「规划中」 | `1d7a3da` | 三个未合并分支（`shell-capability-integration` `ed049d9ac`、`shell-capability-rework` `854505aa6`、`shell-capability-stdin` `523bfe4d0`）的产出在 `architecture/sandbox.mdx` 与 `tools/builtin.mdx` 各加一个「规划中」小节：通用 stdin 续写是 no-go 且结论不撤回，受控实时 JSONL 只是待批准的设计稿；两阶段顺序与只读证据边界（Linux-only、macOS/Windows 未验、设计评审 ≠ 实现批准、独立终审未启动、分支未合并）都写在正文里。 |
| S6 术语 · 导航 · changelog | `be03568` | 术语表「工具系统」段新增 4 条（后台作业 / 进程登记簿 / 内容门 / 受控 JSONL）；已弃用表新增 `bash_exec` → `bash`（它只是模块文件名 `src/builtin_tools/bash_exec.rs`）；代码 → 文档映射新增 5 条主路径。导航无页面增删（fumadocs 目录式导航，无 `docs.json`）。changelog 页面经核对没有失效工具名，且 Aleph `main` 自上轮未前进，故不新增条目。 |
| S7 终验 | 本提交 | 本报告；七门（含 G5 构建门）全绿，基线十段全 0。 |

### 本轮查证并写进文档的关键代码事实
- **工具真名是 `bash`**：`src/builtin_tools/bash_exec.rs:376` `const NAME: &'static str = "bash";`，注册表臂在 `src/executor/builtin_registry/definitions.rs:993` `"bash" => Some(Box::new(BashExecTool::new()))`。`bash_exec` 只出现在 gateway 的测试夹具里，不是工具名。
- **`bash` 的参数**（`src/builtin_tools/bash_exec.rs:62` `BashExecArgs`）：`cmd`、`working_dir`、`timeout_seconds`（serde alias `timeout` + schemars rename `timeout` → 对模型是 `timeout`）、`allow_network`、`allow_subprocess`、`extra_writable_paths`、`background`、`process_action`、`process_id`、`justification`。
- **`code_exec` 的参数**（`src/builtin_tools/code_exec.rs:127` `CodeExecArgs`）：`language`、`code`、`working_dir`、`timeout`、`allow_network`、`allow_subprocess`、`extra_writable_paths`、`justification`（**没有** `background`）。
- **`code_check` 的参数**（`src/builtin_tools/code_check.rs:72` `CodeCheckArgs`）：`path`、`command`、`timeout_seconds`——只有 serde alias，没有 schemars rename，所以模型看到的就是 `timeout_seconds`，与前两个工具不同。
- **四个登记面**：`BUILTIN_TOOL_DEFINITIONS`（178 项，`definitions.rs:85`）、`REGISTRY_ONLY_DESCRIPTIONS`（23 项）、`TOOLS_OUTSIDE_DEFINITIONS`（`src/executor/mod.rs:30`，即 `subagent` + `tool_search`）、按请求注入的 `get_tool_schema`（`src/tools/scoped/mod.rs`）；MCP 桥接六工具在 `src/mcp/tool_bridge.rs:40-58`。
- **装配入口**是 `BuiltinToolRegistry::with_config()`（`src/executor/builtin_registry/builder/constructor/mod.rs`），不是「内置工具不通过 builder 注册」。
- **后台作业默认值**：`BACKGROUND_DEFAULT_TIMEOUT_SECS = 3600`（`bash_exec.rs:44`）、`WAIT_DEFAULT_TIMEOUT_SECS = 60`（:51）、`WAIT_MAX_TIMEOUT_SECS = 170`（:60）、`BACKGROUND_MAX_TIMEOUT_SECS = 4 * 3600`（:440）；前台上限 180 秒；后台走 `call_unclamped`（:469）但仍是同一条沙箱管道。
- **登记簿限额**（`src/builtin_tools/process_registry.rs`）：`MAX_ENTRIES = 64`（:64）、`MAX_RUNNING_PER_SESSION = 8`（:74）、`MAX_RUNNING_GLOBAL = 32`（:84）、`COMMAND_PREVIEW_MAX = 120`（:87）；状态 `Running` / `Done` / `Killed`；登记簿纯内存，跨进程流水在 `src/builtin_tools/process_journal.rs`。
- **输出闸门**是 `src/builtin_tools/partial_output.rs`，实时尾随在 `src/sandbox/live_tail.rs`——两者共同决定模型看到的输出形状。
- **owned worktree 拒绝后台**：错误文案 `bash: background commands cannot outlive an owned worktree; run in the foreground`（`bash_exec.rs:422`）。
- **通话生命周期五工具**（`src/builtin_tools/call_lifecycle.rs`）：`initiate_call`、`answer_call`、`hangup`、`cancel_output`、`call_status`；只操作自己绑定上的通话，绝不返回号码或对话文本。
- **团队生命周期**：`lifecycle_idle`、`lifecycle_request_shutdown`、`lifecycle_resolve_shutdown`（leader 侧批准或拒绝），加 `session_read`、`session_collaborate`、`team_acp_member`。
- **诊断面**：`capability_projection_diagnostics` 默认关闭（需启动时 `ALEPH_CAPABILITY_DIAGNOSTICS=1`），关闭时不投放不派发；可见时也只有同时满足 operator 角色、loopback 传输、非空连接 id 的 operator 进程能驱动。
- **工作区与项目**：`workspace_manage` 的 workspace id 就是 agent id（1:1），记录只带展示元数据，不改模型 / 工具 / 系统提示；`project_manage` 管项目房间（成员、记忆、群聊）。
- **没有 `forget` 工具**：删除走 `remember` 的 Remove 操作；按记录删除走 `memory.delete` RPC。

### 仍标「规划中」的条目
zh 74 处 / en 26 处，共 18 + 11 页。本轮新增 zh/en 各 2 页（`architecture/sandbox.mdx`、`tools/builtin.mdx`），其余沿用前轮分组：
- shell 能力重构与受控 stdin / JSONL（本轮新增，来源 `shell-capability-rework` / `shell-capability-stdin` 分支）。
- 能力模型、插件包、插槽替换、信任后端（沿用前轮）。
- Panel / 插件 UI / 桌面宿主（沿用前轮）。
- 网关协议与 v1 协议（沿用前轮）。

### 遗留债务
- G1d 的**宣称**判定只覆盖「工具表首列」与四种调用点写法；纯散文里列出的工具名不会被当成宣称。**missing** 判定用的是全站提及，覆盖面反而更宽，因此散文里的名字不会被判「缺失」也不会被判「幽灵」——若将来文档改成纯散文列工具，需要扩展宣称口径。
- 三个 shell 分支一旦合入 `main`，`tools/builtin.mdx` 与 `architecture/sandbox.mdx` 的两个「规划中」小节必须改写成现状，并重跑七门（含 G1d）。
- 代码仓 `CHANGELOG.md` 仍停在 2026-09-25、`VERSION` 仍是 `26.9.1`；站点 changelog 是文档视角的派生摘要，发版前要与上游合并去重。
- G2 / G3 / G4 通过时不打印明细（脚本只输出非零项），报告里三行留空属预期，不是漏跑。
- 本轮没有增删页面（zh 165 / en 165），路由与目录页无需同步。

### 复核方法
- 七门（含构建）：`python3 scripts/run_gates.py --repo ../Aleph --build`
- 单跑 G1d：`python3 scripts/tool_audit.py --repo ../Aleph --docs content/docs --raw`
- 重新生成本报告机器部分：`python3 scripts/verification_report.py --repo ../Aleph --out docs/VERIFICATION-2026-11-pass4.md --since a535ac4 --build`（重跑会保留 `<!-- MANUAL -->` 之间的人工结论）
- 基线棘轮：`python3 scripts/run_gates.py --repo ../Aleph --update-baseline`

<!-- MANUAL:END -->
