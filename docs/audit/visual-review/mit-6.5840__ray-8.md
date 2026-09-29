# mit-6.5840/figures/ray-8.svg

模型 claude-sonnet-4.5（本仓自绘，按 `docs/figure-spec.md` 生成）
复核对象 SHA256(前16)：`04FFE33E62F16A47`
SVG mtime：2026-09-29 21:42:22

## 版面

全图单一浅色底，顶部居中为总标题「三张 owner 表」。元素自上而下按下列顺序排布（位置用属性原值）：

- 实心或虚线方框：x=22, y=56, w=716, h=116
- 实心或虚线方框：x=22, y=76, w=222, h=54
- 实心或虚线方框：x=269, y=76, w=222, h=54
- 实心或虚线方框：x=516, y=76, w=222, h=54
- 实心或虚线方框：x=22, y=197, w=716, h=36

## 全部文字

- 三张 owner 表
- worker 1 的表
- x  B()   W1  W1,W3  W2
- worker 2 的表
- x  W1  —  W2
- worker 3 的表
- x  W1  —  W2
- 所有者那一份记引用计数（Ref）；其余 worker 只记 Owner 与 Loc
- worker 1 的表里 y 那一行的 Owner 同样是 W1；owner = (IP, port, worker id)

## 缺陷

无。`tools/svg-lint` 实测 0 error、0 warning（同日复跑 `scripts/check_figures.py --root . --strict`）。

## 判定

可用。
