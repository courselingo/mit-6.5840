#!/usr/bin/env python3
"""内容审计 —— 把「质量」里可机检的部分变成闸门。

与另外两道闸门的分工：
  validate.py       授权与术语（合规）
  check_style.py    文风与反 AI 味（句子层面）
  check_figures.py  单张 SVG 的房规（图本身画得对不对）
  **audit_content.py  页面结构与内容密度（该有的有没有）**  ← 本文件

本文件查的是「该画的图画了没、该讲的讲了没」这类**结构性问题**：
配图密度与分布、每个小节是否配图、句子长度、具体性、脉络完整性。

退出码：0 通过（可能带 WARN）/ 1 有 ERROR / 2 用法或 IO 错误
用法：python scripts/audit_content.py [--root .] [--strict]
      --strict 让 WARN 也算失败（CI 用）
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

CJK = re.compile(r"[\u4e00-\u9fff]")
H2 = re.compile(r"^##\s+(.+)$", re.M)
IMG = re.compile(r"!\[[^\]]*\]\((figures/[^)]+\.svg)\)")
CODE = re.compile(r"```.*?```", re.S)

# ---- 阈值（改这里就是改标准）----
MIN_FIG_PER_K = 2.0      # 每千汉字图数下限
TARGET_FIG_PER_K = 3.0   # 目标带
MAX_FIG_PER_K = 5.0      # 上限：超过就是拿图凑数
MAX_GAP_CJK = 1200       # 连续多少汉字无图算「缺口」
MAX_SENT_CJK = 120       # 单句最长汉字数
MAX_SENT_AVG = 55        # 平均句长
MIN_NUM_PER_K = 1.5      # 每千汉字具体数字/量词数
MIN_NAMED_SYSTEMS = 5    # 每页点名的系统/协议数
MIN_TERMS = 8            # [[term:]] 标记数下限
MIN_H2 = 5               # 小节数下限

SYSTEMS = [
    "GFS", "MapReduce", "Raft", "Paxos", "ZooKeeper", "Spanner", "Chubby",
    "HDFS", "Ceph", "Dynamo", "BigTable", "Kafka", "etcd", "Memcached",
    "Aurora", "Frangipani", "CRAQ", "Chain Replication", "VMware FT",
    "gRPC", "Thrift", "NFS", "AFS", "xv6", "Go", "RPC", "ZAB", "Multi-Paxos",
]


def force_utf8() -> None:
    for s in (sys.stdout, sys.stderr):
        try:
            s.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, OSError, ValueError):
            pass


def strip_fm(text: str) -> str:
    parts = text.split("+++", 2)
    return parts[2] if len(parts) == 3 else text


def sentences(body: str) -> list[str]:
    """按中文句末标点切句，忽略代码块。"""
    t = CODE.sub(" ", body)
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)
    parts = re.split(r"[。！？；\n]+", t)
    return [p.strip() for p in parts if CJK.search(p)]


def audit(path: Path, root: Path) -> tuple[list[str], list[str]]:
    """返回 (errors, warnings)。"""
    raw = path.read_text(encoding="utf-8")
    body = strip_fm(raw)
    rel = path.relative_to(root).as_posix()
    errs: list[str] = []
    warns: list[str] = []

    n_cjk = len(CJK.findall(body))
    if n_cjk < 300:
        return errs, warns

    per_k = n_cjk / 1000.0
    imgs = list(IMG.finditer(body))
    n_img = len(imgs)
    h2s = H2.findall(body)

    # ---- A. 配图密度 ----
    if n_img / per_k < MIN_FIG_PER_K:
        errs.append(
            f"[配图密度] {n_img} 幅 / {per_k:.1f}k 汉字 = 每千字 {n_img/per_k:.2f} 幅"
            f"（下限 {MIN_FIG_PER_K}，目标 {TARGET_FIG_PER_K}）⇒ 至少还需 "
            f"{int(MIN_FIG_PER_K*per_k)+1-n_img} 幅"
        )
    elif n_img / per_k < TARGET_FIG_PER_K:
        warns.append(
            f"[配图密度] 每千字 {n_img/per_k:.2f} 幅，未达目标 {TARGET_FIG_PER_K}"
        )
    if n_img / per_k > MAX_FIG_PER_K:
        warns.append(
            f"[配图密度] 每千字 {n_img/per_k:.2f} 幅，超过上限 {MAX_FIG_PER_K}"
            "（图太多会变成幻灯片，且容易凑数）"
        )

    # ---- B. 小节配图覆盖 ----
    if h2s:
        # 每个 H2 到下一个 H2 之间是否有图
        marks = [(m.start(), m.group(1)) for m in H2.finditer(body)]
        for i, (pos, title) in enumerate(marks):
            end = marks[i + 1][0] if i + 1 < len(marks) else len(body)
            seg = body[pos:end]
            if not IMG.search(seg):
                # 「读完应该能回答」「脉络回顾」「溯源」这类收尾小节不强制配图
                if re.search(r"(应该能回答|脉络回顾|小结|溯源|来源|延伸阅读)", title):
                    continue
                errs.append(f"[小节缺图] 「{title[:28]}」整节没有配图")

    # ---- C. 无图缺口 ----
    if imgs:
        prev = 0
        worst = ("", 0)
        for m in imgs:
            gap = len(CJK.findall(body[prev:m.start()]))
            if gap > worst[1]:
                seg = body[prev:m.start()]
                head = re.search(r"^##\s+(.+)$", seg, re.M)
                worst = (head.group(1) if head else "(开头)", gap)
            prev = m.end()
        tail = len(CJK.findall(body[prev:]))
        if tail > worst[1]:
            worst = ("(结尾)", tail)
        if worst[1] > MAX_GAP_CJK:
            errs.append(
                f"[无图缺口] 「{worst[0][:28]}」附近连续 {worst[1]} 汉字没有图"
                f"（上限 {MAX_GAP_CJK}）"
            )

    # ---- D. 图的上下文（引出句 + 解读句） ----
    for m in imgs:
        before = body[: m.start()].rstrip()
        after = body[m.end():].lstrip()
        before_line = before.split("\n")[-1].strip() if before else ""
        after_line = after.split("\n")[0].strip() if after else ""
        name = m.group(1).split("/")[-1]
        if len(CJK.findall(before_line)) < 6 and not before_line.startswith("|"):
            warns.append(f"[图无引出] {name} 前面没有一句正文承接")
        if len(CJK.findall(after_line)) < 6:
            warns.append(f"[图无解读] {name} 后面没有一句正文解读")

    # ---- E. 句子长度（可读性） ----
    ss = sentences(body)
    if ss:
        lens = [len(CJK.findall(s)) for s in ss]
        avg = sum(lens) / len(lens)
        mx = max(lens)
        if avg > MAX_SENT_AVG:
            warns.append(f"[句子偏长] 平均 {avg:.0f} 汉字（上限 {MAX_SENT_AVG}）")
        if mx > MAX_SENT_CJK:
            long_one = ss[lens.index(mx)]
            warns.append(f"[超长句] {mx} 汉字：「{long_one[:40]}…」")

    # ---- F. 具体性（反空泛） ----
    # 阿拉伯数字与中文数字都算 —— 只认阿拉伯数字会漏掉「三台机器」「两个副本」这类写法
    nums = re.findall(
        r"(?:\d+(?:\.\d+)?|[一二三四五六七八九十百千万几两]+)\s*"
        r"(?:%|MB|GB|KB|TB|ms|秒|分钟|小时|天|台|个|条|次|份|遍|轮|万|亿|倍|行|字节|票|台机器)",
        body,
    )
    if len(nums) / per_k < MIN_NUM_PER_K:
        warns.append(
            f"[不够具体] 具体数字 {len(nums)} 个 / {per_k:.1f}k 字"
            f"（下限 {MIN_NUM_PER_K}/千字）—— 多给数字、少下形容词"
        )
    named = sum(1 for s in SYSTEMS if s.lower() in body.lower())
    if named < MIN_NAMED_SYSTEMS:
        warns.append(f"[点名不足] 只点到 {named} 个具体系统/协议（建议 ≥{MIN_NAMED_SYSTEMS}）")

    # ---- G. 结构与术语 ----
    if len(h2s) < MIN_H2:
        warns.append(f"[结构] 只有 {len(h2s)} 个二级小节（建议 ≥{MIN_H2}）")
    terms = len(re.findall(r"\[\[term:[^\]]+\]\]", body))
    if terms < MIN_TERMS:
        warns.append(f"[术语] 只标了 {terms} 个 [[term:]]（建议 ≥{MIN_TERMS}）")

    return errs, warns


def main(argv: list[str] | None = None) -> int:
    force_utf8()
    ap = argparse.ArgumentParser(description="内容结构与密度审计")
    ap.add_argument("--root", default=".")
    ap.add_argument("--strict", action="store_true", help="WARN 也算失败")
    args = ap.parse_args(argv)

    root = Path(args.root).resolve()
    files = sorted((root / "content").rglob("index.md"))
    if not files:
        print("内容审计：content/ 下没有 index.md —— 跳过")
        return 0

    print(f"内容审计：{len(files)} 篇")
    n_err = n_warn = 0
    for f in files:
        errs, warns = audit(f, root)
        rel = f.relative_to(root).as_posix()
        n_err += len(errs)
        n_warn += len(warns)
        if errs:
            print(f"\n  ❌ {rel}")
            for e in errs:
                print(f"       {e}")
            for w in warns:
                print(f"       ⚠️  {w}")
        elif warns:
            print(f"\n  ⚠️  {rel}")
            for w in warns:
                print(f"       {w}")
        else:
            print(f"  ✅ {rel}")

    print()
    print(f"ERROR {n_err} 个，WARN {n_warn} 个")
    if n_err or (args.strict and n_warn):
        print("❌ 内容审计未通过。标准见 docs/figure-audit.md 与 docs/quality-audit.md")
        return 1
    print("✅ 内容审计通过")
    return 0


if __name__ == "__main__":
    sys.exit(main())
