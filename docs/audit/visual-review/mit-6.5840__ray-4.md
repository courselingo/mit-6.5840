# mit-6.5840/figures/ray-4.svg

模型 claude-sonnet-4.5（本仓自绘，按 `docs/figure-spec.md` 生成）
复核对象 SHA256(前16)：`C77B6168D8C4DD2D`
SVG mtime：2026-09-29 21:42:22

## 版面

全图单一浅色底，顶部居中为总标题「Remote 调用扇出，actor 持有状态」。元素自上而下按下列顺序排布（位置用属性原值）：

- 实心或虚线方框：x=22, y=52, w=716, h=36
- 实心或虚线方框：x=22, y=113, w=160, h=36
- 实心或虚线方框：x=207, y=113, w=160, h=36
- 实心或虚线方框：x=392, y=113, w=160, h=36
- 实心或虚线方框：x=577, y=113, w=160, h=36
- 实心或虚线方框：x=22, y=174, w=716, h=36
- 实心或虚线方框：x=22, y=235, w=344, h=54
- 实心或虚线方框：x=394, y=235, w=344, h=54
- 连线 path：M102,93 L102,102
- 连线 path：M287,93 L287,102
- 连线 path：M472,93 L472,102
- 连线 path：M657,93 L657,102
- 连线 path：M102,154 L102,163
- 连线 path：M287,154 L287,163
- 连线 path：M472,154 L472,163
- 连线 path：M657,154 L657,163
- 连线 path：M371,262.0 L383,262.0

## 全部文字

- Remote 调用扇出，actor 持有状态
- g.remote(0..3)：四次调用立刻返回 future
- 并行任务 1
- 并行任务 2
- 并行任务 3
- 并行任务 4
- ray.get 汇总四次结果
- Counter（actor）
- self.value 留在那台机器上
- increment.remote() 返回 future
- 返回值不搬走状态
- 一次调用立刻返回 future，四次调用并行跑，最后由 ray.get 收口

## 缺陷

无。`tools/svg-lint` 实测 0 error、0 warning（同日复跑 `scripts/check_figures.py --root . --strict`）。

## 判定

可用。
