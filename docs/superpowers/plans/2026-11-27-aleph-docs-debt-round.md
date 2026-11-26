# Aleph 文档站第四轮遗留债务收口执行计划（2026-11-27）
> 对应 ROADMAP：`docs/ROADMAP-2026-11-pass4.md` 第八章
> 真值基线：Aleph `main` = `7fb540b44`（与第四轮同一 HEAD；`origin/main` == `7fb540b44`）
> 起点：`c302c34`（第四轮终验报告），本轮只处理第四轮列出的三条遗留
## 阶段总览
| 阶段 | 目标 | Task |
|---|---|---|
| D0 | 债务一：G1d 宣称口径扩到散文 | D0.1 |
| D1 | 债务二：「规划中」小节的可回归判定（G1e） | D1.1、D1.2 |
| D2 | 债务三：更新日志对账（G1f） | D2.1、D2.2 |
| D3 | 收口：报告、构建门、推送 | D3.1 |
---
## D0 — 债务一：G1d 宣称口径扩到散文
### Task D0.1 散文级宣称判定
**Files:**
- Modify: `scripts/tool_audit.py`
- Modify: `content/docs/zh|concepts/acp-protocol.mdx`（`acp_member` → `team_acp_member`）
**做什么：**
1. 原 G1d 只把「工具表首列」与四种调用点当宣称，纯散文里列出的工具名既不判幽灵也不判未登记。
2. 新增散文宣称层：工具词与名字贴在一起的写法（「工具 `x`」/「`x` 是内置工具」/「the `x` tool」）算宣称。
3. 散文口径必须有排除项，否则误报淹没门禁：
   - 否定句（「不是 `browser` 工具」不算宣称）；
   - 历史语境（「以前叫 `x`」不算宣称）；
   - 量词修饰（「每个 `x` 工具由…」不算宣称，the/a/an 不算量词）；
   - 动作/字段语境（「`x` 动作」「`x` 参数」不算宣称）；
   - 复合词（`per-tool` 之类不算）；
   - 同句已点名工具后的并列（「`x` 与 `y` 工具」里的 `y` 视为 `x` 的动作）。
4. 否定与历史的作用域必须细到**列表项**粒度：同一 bullet 列表里别的条目含「不是」不能连坐。
5. 判定范围与表格口径一致：中文正则用 `(?![A-Za-z])` 而不是 `\b`（Python 的 `\b` 在 CJK 上不成立）。
- [x] **Step 1**: 写散文宣称层，跑 `--raw` 看误报集。
- [x] **Step 2**: 修误报：否定/历史作用域改列表项粒度；量词正则允许 token 前是反引号。
- [x] **Step 3**: 修文档真实缺陷：`acp-protocol.mdx` 的 `acp_member` → `team_acp_member`（zh/en）。
- [x] **Step 4**: 跑全门，确认幽灵 0 / 未登记 0。
**提交**：`docs(gates): extend the tool name gate to prose claims`

## D1 — 债务二：「规划中」小节的可回归判定
### Task D1.1 `scripts/planned_status_audit.py`（G1e 规划中状态门）
**Files:**
- Create: `scripts/planned_status_audit.py`
**做什么：**
1. 范围：所有标题含「规划中 / Planned」的 `##`–`####` 小节（zh 11 + en 11 = 22 节）。
2. 判定：
   - **状态标记语言**：中文页必须写「状态：规划中」，英文页必须写 `Status: planned`；引用分支或提交的小节必须带本语言标记；
   - **提交**：引用的 commit 必须存在；已是 `main` 祖先且不在历史语境里 → 小节失效；
   - **分支**：引用的分支已是 `main` 祖先 → 失效；
   - **路径**：小节提到的路径由该分支引入且现已存在于 `main` → 失效（能抓 squash 合入）。
3. 误报防护：分支引用必须代码仓真实存在（`git rev-parse --verify refs/heads/<token>`）才算，否则
   `tsx-panel` 这类词会被当分支；commit 需 8–40 位十六进制，7 位短 SHA 不算。
- [x] **Step 1**: 写脚本，跑 `--raw` 看首轮结果。
- [x] **Step 2**: 用 `/tmp/g1e-fixture` 合成仓验证四种情形（未合并 / 分支合并 / squash 合入 / commit 已合入）。
- [x] **Step 3**: 修文档真实缺陷：英文页里的中文状态标记。
**提交**：`docs(gates): add the planned section status gate`

### Task D1.2 接入总门 + 基线棘轮
**Files:**
- Modify: `scripts/run_gates.py`（加 `G1e 规划中门`）
- Modify: `scripts/baseline.json`（新增 `planned_stale` 段）
- Modify: `scripts/verification_report.py`（门表加 G1e 行）
- [x] **Step 1**: 接线，跑全门。
**提交**：`docs(gates): wire the planned section gate into the gate runner`

## D2 — 债务三：更新日志对账
### Task D2.1 `scripts/changelog_audit.py`（G1f 对账门）
**Files:**
- Create: `scripts/changelog_audit.py`
**做什么：**
1. 上游版本集来自代码仓 `CHANGELOG.md` 的 `## [26.9.1]` 段落，滚动条目来自 `## 2026-09-25`；
   站点版本/日期集来自 `content/docs/{zh,en}/changelog.mdx` 的 `## 26.9.1` / `## 2026-11-26` 标题。
2. 判定：
   - 站点版本 ⊆ 上游版本（防编造）；
   - 覆盖边界 = 站点最旧版本条目，其后每个上游版本必须在站点（防上游发版站点不更新）；
   - 上游 `VERSION` 文件值必须在站点有条目；
   - zh/en 版本集与日期集一致；单页不得重复版本；
   - frontmatter 的「截至 / through」必须等于页面最新日期条目；
   - 上游最新滚动条目不得晚于站点最新。
3. 不改代码仓的 `CHANGELOG.md`，也不 bump `VERSION`：发版属代码仓发布流程，门禁在发版瞬间强制站点补条目。
- [x] **Step 1**: 写脚本，跑 `--raw` 看首轮结果。
- [x] **Step 2**: 用 `/tmp/g1f-fixture` 合成仓验证（一致 / 上游发版 / 站点编造版本 + 中英不一致）。
- [x] **Step 3**: 修文档真实缺陷：站点覆盖边界表述改准（从 26.6.29 起）。
**提交**：`docs(gates): add the changelog reconciliation gate`

### Task D2.2 接入总门 + 基线棘轮
**Files:**
- Modify: `scripts/run_gates.py`（加 `G1f 对账门`）
- Modify: `scripts/baseline.json`（新增 `changelog_drift` 段）
- Modify: `scripts/verification_report.py`（门表加 G1f 行）
- [x] **Step 1**: 接线，跑全门。
**提交**：`docs(gates): wire the changelog gate into the gate runner`

## D3 — 收口
### Task D3.1 报告、构建门与推送
**Files:**
- Modify: `docs/ROADMAP-2026-11-pass4.md`（第八章）
- Modify: `docs/VERIFICATION-2026-11-pass4.md`（门表补 G1e/G1f；遗留一节改写）
- Create: `docs/superpowers/plans/2026-11-27-aleph-docs-debt-round.md`（本文）
- [x] **Step 1**: ROADMAP 补第八章。
- [x] **Step 2**: 跑 `python3 scripts/verification_report.py --repo ../Aleph --out docs/VERIFICATION-2026-11-pass4.md --since a535ac4 --build`，人工段保留。
- [x] **Step 3**: 跑九门（含 G5 构建门）。
- [x] **Step 4**: 提交并推送 `origin/main`。
**提交**：`docs(debts): close the three pass-4 leftovers with two new gates`
