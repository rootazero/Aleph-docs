"""锚点门与符号门共用的免检规则。

两条门都面对同一个问题：文档会提到一些「已经不在代码树里」的东西——
历史小节里的旧模块、正在被收敛掉的模块、只存在于 git 历史里的类型。
这些引用是文档有意保留的记录，不是现状腐化，但只要规则不显式，
就会把门刷红，久而久之门就没人信了。

免检有两类：

1. **小节级**：落在「历史 / 规划中」这类小节里的引用一律免检。
   小节按标题正则识别，中英文必须对称（英文页用 "History:" / "Planned:"）。
2. **行级**：同一行显式说明该引用已被删除或已下线时，这一行免检。
   这样「挂载状态表」这类必须列出已删除模块的表格可以继续写事实，
   而不用把整张表搬进历史小节。

行级规则用词要窄：只认「确凿表示这个东西已经不在了」的说法，
不认泛泛的「移除」「删除」等动词，避免把真实的路径腐化一起放过去。
"""

from __future__ import annotations

import re

# 小节级免检：历史（描述当时）与规划中（描述将来）都不要求当下存在。
# 中英文必须对称：英文页用 "History:" / "Planned:" / "Deprecated ..."，
# 只豁免中文会让英文侧的同一段历史叙述被误判成现状腐化。
EXEMPT_HEADING_RE = re.compile(
    r"历史|规划中|已废弃|历史记录"
    r"|Historical|History|Superseded|Deprecated|Planned|Planning|Retracted|Removed"
)

# 行级免检：明确说「这个引用已经不在代码树里」的措辞。
# 中文用「已删除 / 已移除 / 已下线 / 不再存在」这类完成态；
# 英文用 removed / deleted 的过去式与被动式——这些词本身就表示「已被拿走」，
# 而运行时的动作要用现在式（removes / deletes），不会被误判。
REMOVED_MARKER_RE = re.compile(
    r"已删除|已移除|已被删除|已下线|已不存在|不再存在|删除了|删除于|收敛中删除"
    r"|\bremoved\b|\bdeleted\b|\bno\s+longer\s+exists\b",
    re.IGNORECASE,
)


def is_removed_line(line: str) -> bool:
    """这一行是否显式声明了「被引用的东西已经不在了」。"""
    return bool(REMOVED_MARKER_RE.search(line))


def exempt_lines(text: str) -> list[bool]:
    """逐行标记该行是否免检：小节级历史/规划中，或行级已删除声明。"""
    exempt: list[bool] = []
    exempt_level: int | None = None
    for line in text.splitlines():
        heading = re.match(r"^(#+)\s", line)
        if heading:
            level = len(heading.group(1))
            if exempt_level is not None and level <= exempt_level:
                exempt_level = None
            if exempt_level is None and EXEMPT_HEADING_RE.search(line):
                exempt_level = level
            exempt.append(False)
            continue
        exempt.append(exempt_level is not None or is_removed_line(line))
    return exempt
