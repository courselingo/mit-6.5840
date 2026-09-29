# mit-6.5840/figures/ray-7.svg

模型 claude-sonnet-4.5（本仓自绘，按 `docs/figure-spec.md` 生成）
复核对象 SHA256(前16)：`F608783851B6C528`
SVG mtime：2026-09-29 21:42:22

## 版面

全图单一浅色底，顶部居中为总标题「按 ownership 分片：不必联系 B」。元素自上而下按下列顺序排布（位置用属性原值）：

- 实心或虚线方框：x=22, y=56, w=344, h=54
- 实心或虚线方框：x=394, y=56, w=344, h=54
- 实心或虚线方框：x=255, y=135, w=250, h=54
- 连线 path：M371,83.0 L383,83.0

## 全部文字

- 按 ownership 分片：不必联系 B
- A（worker 1）
- 所有者在调用者这一侧
- C（worker 3）
- 借用 x，继续做引用计数
- 按 ownership 直接调，不经过 B
- B（worker 2）
- x 的值存在这里
- 所有权在调用者，值留在算它的 worker 上，两者被分开

## 缺陷

无。`tools/svg-lint` 实测 0 error、0 warning（同日复跑 `scripts/check_figures.py --root . --strict`）。

## 判定

可用。
