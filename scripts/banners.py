#!/usr/bin/env python3
"""页面顶部的授权提示条。

为什么单独一个模块：这些文字会出现在每一个页面上，措辞必须只有一处真相。
renderer 换了，提示条不能跟着丢 —— 读者有权在正文之前就知道授权状态。
"""
from __future__ import annotations

COURSE_UNVERIFIED = """!!! warning "本课程授权状态：未核实"
    课程**主页**标注 CC BY 3.0 US，但该徽章**只出现在主页**；本课程实际依据的
    笔记文件（`notes/l01.txt` 等）本身**没有许可声明**，覆盖范围未获确认。

    因此本站**只发布 CourseLingo 自己的原创讲解** —— 讲概念、不转载原文，
    也不提供逐字稿与双语原文对照。Lab 代码与作业答案课程明确要求不得公开，永久排除。
"""

COURSE_FORBIDDEN = """!!! danger "本课程授权明确不允许传播"
    按内容策略，本站不发布该课程的任何材料或其衍生内容。
"""

PAPER_NO_TRANSLATION = """!!! note "授权：未核实，或条款未明确允许全文翻译"
    本篇是 CourseLingo 自己撰写的**导读**，不含原论文段落，也不是逐句对照。
    论文的权利归出版方所有，我们只提供链接与自己的解读。
"""


def course_banner(license_: dict) -> str:
    """按课程授权状态给出提示条；状态正常时返回空串。"""
    if str(license_.get("redistribution")) == "forbidden":
        return COURSE_FORBIDDEN
    if license_.get("verified") is not True:
        return COURSE_UNVERIFIED
    return ""


def paper_banner(lic: dict | None) -> str:
    """论文页提示条：未取得翻译许可时说明这是导读。"""
    if not lic:
        return PAPER_NO_TRANSLATION
    if lic.get("verified") is True and lic.get("allows_translation") is True:
        return ""
    return PAPER_NO_TRANSLATION
