# Aleph 文档站第二轮终验报告（2026-11）

> 本文件由 `scripts/verification_report.py` 生成**机器部分**，逐阶段结论由主 agent 撰写。
> 复核命令：`python3 scripts/run_gates.py --repo ../Aleph --build`。

## 门禁结果

| 门 | 结果 | 明细 |
|----|------|------|
| G1 锚点门 | PASS | 页面 328，锚点 6786，失效 0（路径 0，裸文件名 0；新增 0，基线旧债 0） |
| G1b 方法册 | PASS | census methods: 394   documented dotted tokens: 464<br>ghost (documented, absent from code): 0（新增 0，基线旧债 0）<br>missing (registered, undocumented): 0（新增 0，基线旧债 0） |
| G1c 符号门 | PASS | 页面 328，失效 0（新增 0，基线旧债 0） |
| G2 事实门 | PASS |  |
| G3 结构门 | PASS |  |
| G4 双语门 | PASS |  |

## 规模

- 页面：zh 164 页 / en 164 页
- 代码锚点：6786 个被检查，0 个失效

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
| `content/docs/zh/api/jsonrpc.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/api/rust.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/1-2-3-4-model.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/a2a.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/acp.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/clawhub.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/cluster.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/design-patterns.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/desktop-bridge.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/dispatcher.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/executor.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/gateway.mdx` | 本轮改写 | S2：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/groupchat.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/harness.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/memory-evolution.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/memory.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/orchestrator.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/overview.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/proactive-dispatcher.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/providers.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/resilience.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/routing.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/sandbox.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/session-service.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/sessions.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/teams.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/thinker.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/tools.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/workflow.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/architecture/worldmodel.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/automation/cron-jobs.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/automation/events.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/automation/hooks.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/capabilities/capability-model.mdx` | 本轮改写 | S3：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/capabilities/hooks-and-prompts.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/capabilities/plugin-package.mdx` | 本轮改写 | S3：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/capabilities/slots-and-replacement.mdx` | 本轮改写 | S3：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/capabilities/trust-and-backends.mdx` | 本轮改写 | S3：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/changelog.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/cli/agent.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/cli/commands.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/cli/config.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/cli/gateway.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/a2a-protocol.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/acp-protocol.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/agent-components.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/agent-runtime.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/ai-providers.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/approval.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/arena.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/artifacts-deliverables.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/browser-automation.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/builtin-tools.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/bundled.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/capability-system.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/clarification.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/clawhub.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/configuration.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/core-types.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/daemon.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/discovery.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/domain-model.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/error-handling.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/event-system.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/execution-engine.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/extension-system.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/extensions-store.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/extensions.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/gateway.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/generation.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/group-chat.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/identity-context.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/intent-detection.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/logging.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/looping-goal-strategy.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/markdown-utils.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/mcp-integration.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/media-processing.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/memory.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/messages.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/pii-protection.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/prompt-system.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/protocol-adapters.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/resilience.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/search.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/secret-management.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/security-primitives.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/skill-system.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/skills.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/supervisor-verification.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/task-scheduling.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/teams.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/thinker.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/tool-infrastructure.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/voice-streaming.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/wizard.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/concepts/workspaces.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/desktop-hosts/overview.mdx` | 本轮改写 | S4：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/desktop-hosts/panel-runtime.mdx` | 本轮改写 | S1：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/desktop-hosts/panel.mdx` | 本轮改写 | S1：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/desktop-hosts/plugin-ui.mdx` | 本轮改写 | S1：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/development/building.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/development/contributing.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/development/design-patterns.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/development/testing.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/auth.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/agent.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/arena.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/browser.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/channels.mdx` | 本轮改写 | S4：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/chat.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/config.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/cron.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/daemon.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/events.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/exec.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/extensions.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/graph.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/group_chat.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/heartbeat.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/identity.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/index.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/logs.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/mcp.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/memory.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/plugins.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/providers.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/runs.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/services.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/session.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/skills.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/teams.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/tools.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/wizard.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/methods/workspace.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/protocol-v1.mdx` | 本轮改写 | S2：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/gateway/protocol.mdx` | 本轮改写 | S2：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/getting-started/configuration.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/getting-started/deployment.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/getting-started/installation.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/getting-started/quick-start.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/getting-started/wizard.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/index.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/interfaces/discord.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/interfaces/imessage.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/interfaces/overview.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/interfaces/telegram.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/interfaces/webchat.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/philosophy/agent-thinking.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/philosophy/domain-modeling.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/philosophy/five-layers.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/philosophy/overview.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/philosophy/redlines.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/security/exec-approval.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/security/ipc.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/security/overview.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/security/pairing.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/security/sandboxing.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/terminology.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/tools/browser.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/tools/builtin.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/zh/tools/creating.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/tools/mcp.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/zh/tools/overview.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/api/jsonrpc.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/api/rust.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/1-2-3-4-model.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/a2a.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/acp.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/clawhub.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/cluster.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/design-patterns.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/desktop-bridge.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/dispatcher.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/executor.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/gateway.mdx` | 本轮改写 | S2：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/groupchat.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/harness.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/memory-evolution.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/memory.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/orchestrator.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/overview.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/proactive-dispatcher.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/providers.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/resilience.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/routing.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/sandbox.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/session-service.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/sessions.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/teams.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/thinker.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/tools.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/architecture/workflow.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/architecture/worldmodel.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/automation/cron-jobs.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/automation/events.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/automation/hooks.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/capabilities/capability-model.mdx` | 本轮改写 | S3：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/capabilities/hooks-and-prompts.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/capabilities/plugin-package.mdx` | 本轮改写 | S3：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/capabilities/slots-and-replacement.mdx` | 本轮改写 | S3：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/capabilities/trust-and-backends.mdx` | 本轮改写 | S3：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/changelog.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/cli/agent.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/cli/commands.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/cli/config.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/cli/gateway.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/a2a-protocol.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/acp-protocol.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/agent-components.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/agent-runtime.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/ai-providers.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/approval.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/arena.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/artifacts-deliverables.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/browser-automation.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/builtin-tools.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/bundled.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/capability-system.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/clarification.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/clawhub.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/configuration.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/core-types.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/daemon.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/discovery.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/domain-model.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/error-handling.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/event-system.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/execution-engine.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/extension-system.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/extensions-store.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/extensions.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/gateway.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/generation.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/group-chat.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/identity-context.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/intent-detection.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/logging.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/looping-goal-strategy.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/markdown-utils.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/mcp-integration.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/media-processing.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/memory.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/messages.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/pii-protection.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/prompt-system.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/protocol-adapters.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/resilience.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/search.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/secret-management.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/security-primitives.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/skill-system.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/skills.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/supervisor-verification.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/task-scheduling.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/teams.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/thinker.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/tool-infrastructure.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/voice-streaming.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/concepts/wizard.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/concepts/workspaces.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/desktop-hosts/overview.mdx` | 本轮改写 | S4：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/desktop-hosts/panel-runtime.mdx` | 本轮改写 | S1：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/desktop-hosts/panel.mdx` | 本轮改写 | S1：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/desktop-hosts/plugin-ui.mdx` | 本轮改写 | S1：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/development/building.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/development/contributing.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/development/design-patterns.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/development/testing.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/gateway/auth.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/agent.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/arena.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/browser.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/channels.mdx` | 本轮改写 | S4：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/chat.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/config.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/cron.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/daemon.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/events.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/exec.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/extensions.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/graph.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/group_chat.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/heartbeat.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/identity.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/index.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/logs.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/mcp.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/memory.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/plugins.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/providers.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/runs.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/services.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/session.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/skills.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/teams.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/tools.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/wizard.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/methods/workspace.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/gateway/protocol-v1.mdx` | 本轮改写 | S2：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/gateway/protocol.mdx` | 本轮改写 | S2：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/getting-started/configuration.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/getting-started/deployment.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/getting-started/installation.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/getting-started/quick-start.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/getting-started/wizard.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/index.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/interfaces/discord.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/interfaces/imessage.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/interfaces/overview.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/interfaces/telegram.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/interfaces/webchat.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/philosophy/agent-thinking.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/philosophy/domain-modeling.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/philosophy/five-layers.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/philosophy/overview.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/philosophy/redlines.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/security/exec-approval.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/security/ipc.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/security/overview.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/security/pairing.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/security/sandboxing.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/terminology.mdx` | 本轮改写 | S6：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/tools/browser.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/tools/builtin.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |
| `content/docs/en/tools/creating.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/tools/mcp.mdx` | 本轮改写 | S5：改写后符号 / 锚点 / 方法册零失效 | G1–G4 通过 |
| `content/docs/en/tools/overview.mdx` | 沿用首轮 | 首轮已校准，本轮未改动，站内复查零失效 | G1–G4 通过 |

## 逐阶段结论

<!-- MANUAL:BEGIN -->
### 本轮范围

第二轮对齐针对 2026-09 至 2026-11 的重构：Panel 的**模型与渲染器拆分**、**Protocol v1 落地**、**Capability 系统 Phase 6–9**、**频道冷声明与跨平台桌面 IPC**。起点 commit `e47beb2`（第一轮终验），终点为本轮 S7。计划与台账见 `docs/ROADMAP-2026-11-pass2.md` 与 `docs/superpowers/plans/2026-11-24-aleph-docs-calibration-pass2.md`。

### 真值分层（唯一裁决口径）

1. **T1 代码**：`../Aleph` 的源码为准。
2. **T2 代码仓 `docs/reference/`**：现状描述的二手依据。
3. **T3 代码仓 `docs/research/` 蓝图**：只作「规划中」内容，并在正文加 `> **状态：规划中**` 横幅 + 蓝图出处。
4. **T4 站点现状**：旧页面里与 T1 冲突的断言一律改写，不保留「曾经如此」的现状措辞。
5. **T5 证据层**（`docs/superpowers/`、`docs/reports/` 等）：只作历史记录，不作现状引用。

已从代码删除的模块与类型，写入 `## 历史：…`（英文页 `## History:`）小节，保留结论并标明删除提交，不做「现状直述」。

### 逐阶段结论

| 阶段 | 提交 | 结论 |
|------|------|------|
| S0 工具与基线 | `e079c42` | 新增第六门 G1c 符号门（`scripts/symbol_check.py`、`symbol_triage.py`），`run_gates.py` 接入；基线 `symbol` 段当时棘轮到 389 条。 |
| S1 Panel 架构 | `91b2689` | 三页改写为「共享模型 + 两套渲染器」：模型层 `shared/ui_logic/src/panel/`（含 `layout.rs` 的 `PanelLayout` / `LayoutSlot`），渲染器层 `interfaces/webchat/`（Leptos WASM）与 `interfaces/panel/`（TSX）；布局只存稳定 `PanelTabKey` 与纯数据，快照不再提供的 tab 渲染为永不执行的占位。 |
| S2 Protocol v1 | `df9baf3` | v1 改写为**已落地**：单一方法集 `health` / `sessions.list` / `panel.capabilities.snapshot`（`src/gateway/server/connection/mod.rs` 的 `V1_METHODS`），`system.hello` 的 per-user `subject` 为不透明值（`shared/protocol/src/system_hello.rs`），Web v1 入口在 TLS 路由下挂 `/v1/panel/`（`src/gateway/server/connection/web_v1.rs`）；`/ws` 保留为历史兼容入口。 |
| S3 能力模型 | `5e704da` | 四页按 `src/capability/` 与 `crates/aleph-slot-api/` 的真实符号校准，并复核「已挂生产路径 / 写好了没挂」的清单。 |
| S4 冷声明与桌面 IPC | `f074ebb` | 补冷声明生命周期（boot 不水合、不构造 adapter；`channel.create` 先落盘再返回 `disabled`；`channel.start` 先发布策略再启动 adapter；无热更新）与跨平台桌面 IPC 矩阵（Unix socket；Windows 命名管道的 endpoint 校验、账户绑定、服务端 PID 校验）。 |
| 门禁加固 | `8a0aad1` | 符号门历史小节免检扩到英文标题；crate 字样须紧邻 token 才判失败；新增 `scripts/symbol_report.py`。基线棘轮收口。 |
| S5 符号校准 | `04272f7` | 448 条失效符号逐条判定，基线 `symbol` 段 389 → 0。 |
| S6 术语·导航·changelog | `6fa5f1f` | 术语表收录本轮新术语；`index.mdx` 架构图重画；`meta.json` 页面顺序重排；changelog 补 2026-09-26 → 2026-11-24 共 11 条。 |
| S7 终验 | 本提交 | 本报告；七门（含 G5 构建门）全绿，基线八段全 0。 |

### S5 的处置分布

失效符号轨迹：**448 → 413 → 338 → 216 → 48 → 36 → 18 → 0**。四种处置：

- **改名同步**——落到代码里的真名。例：`process_with_tools` → `AiProvider::process`；`McpToolBridge` → `spawn_tool_bridge`；`McpCommand` 的变体按真实枚举重写；`ThinkerConfig` → `PromptConfig` / `HarnessDeps`；`ContextCompressor` → `ContextCompactor`。
- **路径已删 → 改写为当前路径**——`canvas_io` → `json_canvas_io`（删除提交 `191ec4ae6`）、`components` → `canvas`（`682e49adc`）、`loop_graph` / `tasks::cron` / `tasks::heartbeat` / `group_chat` / `hub` 等按现存模块名改写。
- **移入「历史」小节**——`AuthProfileManager`（`c4bbccdc6`）、`LoggingCallback` / `CollectingCallback` / `NoOpLoopCallback`（`ffc458100`）、`Thinker` / OTAF（`c3e550d8c`）。
- **标「规划中」**——只对代码仓 `docs/research/` 里的蓝图生效。

### 本轮查证并写进文档的关键代码事实

1. **频道配置是 map，不是数组表**：`src/config/structs.rs` 的 `channels: HashMap<String, Value>`，TOML 形态为 `[channels.<id>]`；代码仓 `qa/README.md` 明写数组表写法会导致启动失败（`invalid type: sequence, expected a map`）。
2. **凭据只进保险库**：`channel:{id}:{field}` 形式的键只覆盖**顶层**字段；嵌套凭据在冷创建时报 `Channel contains a credential this vault layout cannot store`；`src/gateway/handlers/secret_migration.rs` 的 `migrate_channels` 在加载时把顶层凭证搬进 vault。
3. **频道段不做 `${VAR}` 展开**：只有 gateway 段（`src/gateway/config.rs`）与 MCP 段（`src/mcp/manager/config.rs`）支持环境变量展开。
4. **审批默认策略可枚举**：浏览器的 19 个 `ActionType` 各自有默认决策，`safe_fetch` + `SsrfPolicy` 是网络工具的默认闸门。

### 仍标「规划中」的条目（站内 79 处）

按蓝图出处归组：

| 蓝图出处 | 涉及页面 |
|----------|----------|
| `docs/research/NSH_PROTOCOL_V1.md` | `gateway/protocol-v1.mdx`、`architecture/gateway.mdx`、`gateway/methods/events.mdx` |
| `docs/research/aleph_modularization_plan.md` | `capabilities/{capability-model,hooks-and-prompts,plugin-package,slots-and-replacement,trust-and-backends}.mdx`、`concepts/capability-system.mdx` |
| `docs/research/Everything-externally-composable-is-a-Capability.md` | `capabilities/capability-model.mdx` |
| `docs/superpowers/specs/2026-11-22-nsh-panel-modular-refactor-design.md`、`2026-11-23-nsh-panel-s2-customizable-shell-design.md` | `desktop-hosts/{panel,panel-runtime,plugin-ui}.mdx` |

### 遗留债务

- 代码仓 `CHANGELOG.md` 停在 2026-09-25，`VERSION` 仍为 `26.9.1`；本轮 changelog 的 2026-09-26 → 2026-11-24 条目由 **git 历史派生**，发版前需与上游 changelog 合并去重。
- 全站 `Tauri` 字样 9 行，全部落在第一轮已确认的例外里（遗留旧壳的过渡期说明与历史条目），本轮未新增。
- 逐页判定表是**站点级门禁结果**按「本轮改写 / 沿用首轮」标注依据，不是逐页人工复核记录；符号类事实的复核入口是 G1c 的逐页 token 判定（`scripts/symbol_report.py`）。

### 复核方法

```bash
python3 scripts/run_gates.py --repo ../Aleph --build          # 七门（含 G5 构建门）
python3 scripts/symbol_check.py --repo ../Aleph                # 新增失效即失败
python3 scripts/symbol_triage.py --repo ../Aleph --out /tmp/triage.json
python3 scripts/verification_report.py --repo ../Aleph \
  --out docs/VERIFICATION-2026-11-pass2.md --since e47beb2 \
  --title "Aleph 文档站第二轮终验报告（2026-11）"                # 重跑保留人工部分
```

<!-- MANUAL:END -->
