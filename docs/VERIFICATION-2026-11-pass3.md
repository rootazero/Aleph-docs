# Aleph 文档站第三轮终验报告（2026-11）

> 本文件由 `scripts/verification_report.py` 生成**机器部分**，逐阶段结论由主 agent 撰写。
> 复核命令：`python3 scripts/run_gates.py --repo ../Aleph --build`。

## 门禁结果

| 门 | 结果 | 明细 |
|----|------|------|
| G1 锚点门 | PASS | 页面 330，锚点 6523，失效 0（路径 0，裸文件名 0；新增 0，基线旧债 0；历史免检行 2049） |
| G1b 方法册 | PASS | census methods: 396   documented dotted tokens: 467<br>ghost (documented, absent from code): 0（新增 0，基线旧债 0）<br>missing (registered, undocumented): 0（新增 0，基线旧债 0） |
| G1c 符号门 | PASS | 页面 330，失效 0（新增 0，基线旧债 0） |
| G2 事实门 | PASS |  |
| G3 结构门 | PASS |  |
| G4 双语门 | PASS |  |
| G5 构建门 | PASS | `next build` / `tsc --noEmit` / `eslint` 退出码 0（56.2s） |

## 规模

- 页面：zh 165 页 / en 165 页
- 代码锚点：6523 个被检查，0 个失效

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

## 逐页判定表

| 页面 | 判定 | 依据 | 门结果 |
|------|------|------|--------|
| `content/docs/zh/api/jsonrpc.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/api/rust.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/1-2-3-4-model.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/a2a.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/acp.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/clawhub.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/cluster.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/design-patterns.mdx` | 本轮改写 | S5、S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/desktop-bridge.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/dispatcher.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/executor.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/gateway.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/groupchat.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/harness.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/memory-evolution.mdx` | 本轮改写 | S2：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/memory.mdx` | 本轮改写 | S2、S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/orchestrator.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/overview.mdx` | 本轮改写 | S6、S7：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/proactive-dispatcher.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/providers.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/resilience.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/routing.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/sandbox.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/session-service.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/sessions.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/teams.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/thinker.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/tools.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/workflow.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/worldmodel.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/automation/cron-jobs.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/automation/events.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/automation/hooks.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/capabilities/capability-model.mdx` | 本轮改写 | S1：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/capabilities/hooks-and-prompts.mdx` | 本轮改写 | S1：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/capabilities/plugin-package.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/capabilities/slots-and-replacement.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/capabilities/trust-and-backends.mdx` | 本轮改写 | S1：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/changelog.mdx` | 本轮改写 | S7：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/cli/agent.mdx` | 本轮改写 | S7：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/cli/commands.mdx` | 本轮改写 | S7：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/cli/config.mdx` | 本轮改写 | S7：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/cli/gateway.mdx` | 本轮改写 | S7：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/a2a-protocol.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/acp-protocol.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/agent-components.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/agent-runtime.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/ai-providers.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/approval.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/arena.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/artifacts-deliverables.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/browser-automation.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/builtin-tools.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/bundled.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/capability-system.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/clarification.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/clawhub.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/configuration.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/core-types.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/daemon.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/discovery.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/domain-model.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/error-handling.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/event-system.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/execution-engine.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/extension-system.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/extensions-store.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/extensions.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/gateway.mdx` | 本轮改写 | S7：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/generation.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/group-chat.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/identity-context.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/intent-detection.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/logging.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/looping-goal-strategy.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/markdown-utils.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/mcp-integration.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/media-processing.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/memory.mdx` | 本轮改写 | S2、S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/messages.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/pii-protection.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/prompt-system.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
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
| `content/docs/zh/concepts/voice-streaming.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/wizard.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/workspaces.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/desktop-hosts/overview.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/desktop-hosts/panel-runtime.mdx` | 本轮改写 | S4：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/desktop-hosts/panel.mdx` | 本轮改写 | S4：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/desktop-hosts/plugin-ui.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/development/building.mdx` | 本轮改写 | S7：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/development/contributing.mdx` | 本轮改写 | S6、S7：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/development/design-patterns.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/development/testing.mdx` | 本轮改写 | S7：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/auth.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/agent.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/arena.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/browser.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/channels.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/chat.mdx` | 本轮改写 | S3：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
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
| `content/docs/zh/gateway/methods/index.mdx` | 本轮改写 | S3：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/logs.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/mcp.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/memory.mdx` | 本轮改写 | S2：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/plugins.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/providers.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/pty.mdx` | 本轮改写 | S3：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/runs.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/services.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/session.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/skills.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/teams.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/tools.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/wizard.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/workspace.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/protocol-v1.mdx` | 本轮改写 | S3：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/protocol.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/getting-started/configuration.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/getting-started/deployment.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/getting-started/installation.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/getting-started/quick-start.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/getting-started/wizard.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/index.mdx` | 本轮改写 | S7：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/interfaces/discord.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/interfaces/imessage.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/interfaces/overview.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/interfaces/telegram.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/interfaces/webchat.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/philosophy/agent-thinking.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/philosophy/domain-modeling.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/philosophy/five-layers.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/philosophy/overview.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/philosophy/redlines.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/security/exec-approval.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/security/ipc.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/security/overview.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/security/pairing.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/security/sandboxing.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/terminology.mdx` | 本轮改写 | S6、S7：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/tools/browser.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/tools/builtin.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/tools/creating.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/tools/mcp.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/tools/overview.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/api/jsonrpc.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/api/rust.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/1-2-3-4-model.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/a2a.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/acp.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/clawhub.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/cluster.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/design-patterns.mdx` | 本轮改写 | S5、S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/desktop-bridge.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/dispatcher.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/executor.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/gateway.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/groupchat.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/harness.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/memory-evolution.mdx` | 本轮改写 | S2：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/memory.mdx` | 本轮改写 | S2、S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/orchestrator.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/overview.mdx` | 本轮改写 | S6、S7：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/proactive-dispatcher.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/providers.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/resilience.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/routing.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/sandbox.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/session-service.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/sessions.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/teams.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/thinker.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/tools.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/workflow.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/worldmodel.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/automation/cron-jobs.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/automation/events.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/automation/hooks.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/capabilities/capability-model.mdx` | 本轮改写 | S1：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/capabilities/hooks-and-prompts.mdx` | 本轮改写 | S1：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/capabilities/plugin-package.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/capabilities/slots-and-replacement.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/capabilities/trust-and-backends.mdx` | 本轮改写 | S1：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/changelog.mdx` | 本轮改写 | S7：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/cli/agent.mdx` | 本轮改写 | S7：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/cli/commands.mdx` | 本轮改写 | S7：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/cli/config.mdx` | 本轮改写 | S7：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/cli/gateway.mdx` | 本轮改写 | S7：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/a2a-protocol.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/acp-protocol.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/agent-components.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/agent-runtime.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/ai-providers.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/approval.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/arena.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/artifacts-deliverables.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/browser-automation.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/builtin-tools.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/bundled.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/capability-system.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/clarification.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/clawhub.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/configuration.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/core-types.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/daemon.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/discovery.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/domain-model.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/error-handling.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/event-system.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/execution-engine.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/extension-system.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/extensions-store.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/extensions.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/gateway.mdx` | 本轮改写 | S7：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/generation.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/group-chat.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/identity-context.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/intent-detection.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/logging.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/looping-goal-strategy.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/markdown-utils.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/mcp-integration.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/media-processing.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/memory.mdx` | 本轮改写 | S2、S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/messages.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/pii-protection.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/prompt-system.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
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
| `content/docs/en/concepts/voice-streaming.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/wizard.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/workspaces.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/desktop-hosts/overview.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/desktop-hosts/panel-runtime.mdx` | 本轮改写 | S4：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/desktop-hosts/panel.mdx` | 本轮改写 | S4：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/desktop-hosts/plugin-ui.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/development/building.mdx` | 本轮改写 | S7：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/development/contributing.mdx` | 本轮改写 | S6、S7：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/development/design-patterns.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/development/testing.mdx` | 本轮改写 | S7：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/gateway/auth.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/agent.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/arena.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/browser.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/channels.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/chat.mdx` | 本轮改写 | S3：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
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
| `content/docs/en/gateway/methods/index.mdx` | 本轮改写 | S3：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/logs.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/mcp.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/memory.mdx` | 本轮改写 | S2：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/plugins.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/providers.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/pty.mdx` | 本轮改写 | S3：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/runs.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/services.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/session.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/skills.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/teams.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/tools.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/wizard.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/workspace.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/protocol-v1.mdx` | 本轮改写 | S3：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/gateway/protocol.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/getting-started/configuration.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/getting-started/deployment.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/getting-started/installation.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/getting-started/quick-start.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/getting-started/wizard.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/index.mdx` | 本轮改写 | S7：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/interfaces/discord.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/interfaces/imessage.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/interfaces/overview.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/interfaces/telegram.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/interfaces/webchat.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/philosophy/agent-thinking.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/philosophy/domain-modeling.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/philosophy/five-layers.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/philosophy/overview.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/philosophy/redlines.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/security/exec-approval.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/security/ipc.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/security/overview.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/security/pairing.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/security/sandboxing.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/terminology.mdx` | 本轮改写 | S6、S7：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/tools/browser.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/tools/builtin.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/tools/creating.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/tools/mcp.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/tools/overview.mdx` | 沿用前轮 | 前轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |

## 逐阶段结论

<!-- MANUAL:BEGIN -->
### 本轮范围

第三轮对齐 Aleph `main` 上 2026-11-24 → 2026-11-26 的三批变更：**能力模型收敛**（生命周期状态机、审计收集器、授予注册表、遗留处理器表拆除）、**记忆自我进化闭环收口**、**聊天转录与记忆图协议**、**Panel 双渲染器外壳与只读星云**、**沙箱自有工作树**、**上下文压缩折返接线**、**扩展重载预检**、**终端 scrollback 重做**。起点 commit `52a8d7f`（第二轮终验），终点为本轮 S8。计划见 `docs/superpowers/plans/2026-11-26-aleph-docs-calibration-pass3.md`，台账见 `docs/ROADMAP-2026-11-pass3.md`。

### 真值分层（唯一裁决口径）

1. **T1 代码**：`../Aleph` 的源码为准。
2. **T2 代码仓 `docs/reference/`**：现状描述的二手依据。
3. **T3 代码仓 `docs/research/` 蓝图**：只作「规划中」内容，并在正文加 `> **状态：规划中**` 横幅 + 蓝图出处。
4. **T4 站点现状**：旧页面里与 T1 冲突的断言一律改写，不保留「曾经如此」的现状措辞。
5. **T5 证据层**（`docs/superpowers/`、`docs/reports/` 等）：只作历史记录，不作现状引用。

已从代码删除的模块与类型，写入「历史 / 已弃用」小节并标明删除提交，不做「现状直述」。

### 逐阶段结论

| 阶段 | 提交 | 结论 |
|------|------|------|
| S0 门禁加固与基线盘点 | `c1b03b1`、`0009a62`、`822d7d3` | census 识别常量注册的方法（`chat.transcript_details`、`pty.history`）；锚点门与符号门对历史小节、已删除行整行免检，避免把「写明已删除」误判为失效。 |
| S1 能力模型重写 | `0af0854` | 按 `src/capability/` 收敛后的真身重写：删除生命周期状态机后，改以解析结果（`ResolveError` / `ProviderState`）与投影宿主（`ProjectionHost`）承担能力语义。 |
| S2 记忆自我进化重写 | `10a1153` | 按 `src/memory/dreaming/`、`src/memory/store/raw_memory.rs` 的真实落地行为重写：缺依赖先行上报、反馈批次先校验再推进游标、继任笔记先发布验证再退役原文。 |
| S3 协议与方法面补齐 | `69f142f` | 补齐 `chat.transcript_details` 与 `pty.*` 方法面，两条「已注册未文档化」清零。 |
| S4 Panel 与桌面壳 | `86e99bb` | 共享 UI 逻辑层（`shared/ui_logic/src/panel/`）与双渲染器、`live_events` 推送、v1 方法集按真身重写。 |
| S5 沙箱 · 压缩 · 扩展重载 | `04b57c7` | 自有工作树（`src/sandbox/worktree.rs`）、折返接线（`src/context/compact/folds.rs`）、重载预检（`src/extension/lifecycle.rs`）按真身校准。 |
| S6 全站符号与锚点校准 | `b243341` | 125 条旧符号全部处置完毕（改名同步 / 改写当前路径 / 移入历史 / 标「规划中」），符号棘轮从 125 回到 0。 |
| S7 术语 · 导航 · changelog | `2f17883` | 术语表收录 14 个新术语并清理与代码脱节的旧条目；changelog 补 2026-11-24 / 11-25 / 11-26 三轮条目；总览与 CLI 页的 RPC 计数改用 census 真值（396）。 |
| S8 终验 | 本提交 | 本报告；七门（含 G5 构建门）全绿，基线八段全 0。 |

### 本轮查证并写进文档的关键代码事实

1. **顶部切换器是 8 项，`Extensions` 不在其中**：`interfaces/webchat/src/components/nav_menu.rs:21` 的 `ALL_MODES: [PanelMode; 8] = [Chat, Dashboard, Memory, Agents, Teams, Projects, Terminal, Settings]`，同处注释写明扩展入口在 Chat 侧栏的 advanced-features 区；`interfaces/webchat/src/components/settings_sidebar.rs:180-224` 的 `SETTINGS_GROUPS` 把 MCP / Plugins / Skills / ACP 归入 Extensions 组，Browser / Policies / Security / Execution / Workspaces 归入 Advanced 组。
2. **Panel 四个运行时符号分属两层**：`TabRegistry` 与 `PanelProjection` 在 `shared/ui_logic/src/panel/`，`PanelLoader` 与 `PanelSdk` 在 `interfaces/webchat/src/panel/`。
3. **Dispatcher / Hydration 已无模块**：现役是 `src/tools/registry.rs` 的 `ToolHandlerRegistry`（描述符派生，模型可见的 `ToolDefinition` 是投影而非第二真身）与 `src/tools/tool_search.rs:208` 的 `tool_search`（自足 BM25，不耦合记忆 FTS5 索引）。
4. **Capability Ledger 是状态账本**：`src/runtimes/ledger.rs` 只跟踪能力状态（Missing / Bootstrapping / Ready / Stale），不下载也不安装；它与安装前披露（`src/hub/trust.rs` 的 `DisclosurePayload`）不是一回事。
5. **ClawHub 与守护进程子系统已从代码消失**：`git grep -il clawhub` 只命中 `interfaces/webchat/src/components/settings_sidebar.rs` 的回归测试与 `src/hub/trust.rs:135` 的注释；WorldModel 与 Proactive Dispatcher 随 `32a6157f1` 删除，现为 `src/loop_graph/` 与 `src/tasks/cron/`、`src/tasks/heartbeat/`。
6. **RPC 计数以 census 为准**：`src/gateway/method_census.rs` 登记 396 个方法；`artifacts.*` 2 个（`list` / `read_text`）、`voice.*` 8 个，`hub.*` / `strategy.*` / `goals.*` 在 census 中零命中，因此不作为分类写入站点。
7. **记忆图与星云是两层**：`shared/protocol/src/memory_graph.rs` 定义 `graph.query` / `graph.search` / `graph.node_detail` 读契约（节点身份即笔记路径）；`shared/ui_logic/src/nebula/` 的 `NebulaIndex` 与 `ForceLayout` 是纯索引与布局，两套渲染器共用。
8. **记忆自进化的三条新契约**：缺依赖先上报（`src/capability/provider.rs` 的 `ProviderState` 进入 `ResolveError::DependencyUnavailable`）、反馈批次先校验再推进游标（`src/memory/store/raw_memory.rs` 的 `CorrectionStatusCursor`）、继任笔记先发布并验证再退役原文（`src/memory/notes/indexer/distill_effect.rs`）。
9. **扩展重载先预检后拆旧版**：`src/extension/lifecycle.rs:371` 的 `preflight_reload` 只编译新版本，失败以 `PrepareError::Defect` 拒绝，不动正在运行的版本。
10. **子代理强制自有工作树**：`src/sandbox/worktree.rs` 的 `WorktreeHandle::create` 在 `$TMPDIR/aleph-subagent-<label>-<uuid>/` 建 detached HEAD 工作树，随句柄释放而清理。
11. **折返接线只有一处真身**：`src/context/compact/folds.rs` 的 `FoldRecord` / `route_fold_recovery` / `derive_fold_id` 是纯派生视图，回本记账在 `src/context/compact/fold_ledger.rs` 的 `FoldVerdict` / `Payback`。
12. **终端 scrollback 有界且按投影顺序**：`src/gateway/session_manager/ops/crud.rs:589` 的 `read_scrollback_locked` 按 `before_row` 分页取回，网格真身在 `src/gateway/pty/screen/history.rs`。

### 仍标「规划中」的条目（zh 68 处 / en 24 处，13 + 9 页）

按蓝图出处归组（蓝图文件均已核对存在于 `../Aleph`）：

| 蓝图出处 | 涉及页面 |
|----------|----------|
| `docs/research/aleph_modularization_plan.md` | `capabilities/{hooks-and-prompts,plugin-package,slots-and-replacement,trust-and-backends}.mdx`、`concepts/capability-system.mdx` |
| `docs/research/Everything-externally-composable-is-a-Capability.md` | `capabilities/{capability-model,trust-and-backends}.mdx`、`concepts/capability-system.mdx` |
| `docs/research/NSH_PROTOCOL_V1.md` | `architecture/gateway.mdx`、`gateway/protocol-v1.mdx`、`gateway/methods/events.mdx`、`desktop-hosts/overview.mdx` |
| `docs/research/NSH_ADR-001~009.md` | `desktop-hosts/plugin-ui.mdx`（ADR-005 受限 TSX 插件视图、ADR-009 动态 UI 分发） |
| `docs/superpowers/specs/2026-11-22-nsh-panel-modular-refactor-design.md` | `desktop-hosts/panel.mdx` |
| `docs/superpowers/specs/2026-11-23-nsh-panel-s2-customizable-shell-design.md` | `desktop-hosts/panel-runtime.mdx` |
| `docs/superpowers/specs/2026-11-25-zahir-capability-convergence-design.md` | `capabilities/capability-model.mdx` |
| `docs/superpowers/plans/2026-11-22-nsh-panel-migration-roadmap.md` | `desktop-hosts/overview.mdx` |

### 遗留债务

- 代码仓 `CHANGELOG.md` 停在 2026-09-25、`VERSION` 仍为 `26.9.1`；本轮 changelog 的 2026-11-24 → 2026-11-26 条目由 **git 历史派生**，发版前需与上游 changelog 合并去重。
- S7 提交顺带收口了前两轮遗留的「~265 个 RPC 方法」计数陈旧问题（CLI 与网关页共 18 页），改用 census 真值 396。
- 逐页判定表是**站点级门禁结果**按「本轮改写 / 沿用前轮」标注依据，不是逐页人工复核记录；符号类事实的复核入口是 G1c 的逐页 token 判定（`scripts/symbol_report.py`）。
- 未覆盖：真实浏览器里 Panel 外壳与星云的交互、发布制品的端到端安装、`docs/research/` 蓝图在代码仓以外的分发形态。

### 复核方法

```bash
python3 scripts/run_gates.py --repo ../Aleph --build          # 七门（含 G5 构建门）
python3 scripts/symbol_check.py --repo ../Aleph                # 新增失效即失败
python3 scripts/verification_report.py --repo ../Aleph \
  --since 52a8d7f --build \
  --out docs/VERIFICATION-2026-11-pass3.md \
  --title "Aleph 文档站第三轮终验报告（2026-11）"                # 重跑保留人工部分
```
<!-- MANUAL:END -->
