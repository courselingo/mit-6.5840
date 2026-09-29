# mit-6.5840/figures/ray-12.svg

模型 claude-sonnet-4.5（本仓自绘，按 `docs/figure-spec.md` 生成）
复核对象 SHA256(前16)：`784AE0708003F441`
SVG mtime：2026-09-29 21:42:22

## 版面

全图单一浅色底，顶部居中为总标题「driver 侧与 worker 侧各发生什么」。元素自上而下按下列顺序排布（位置用属性原值）：

- 实心或虚线方框：x=22, y=56, w=344, h=96
- 实心或虚线方框：x=38, y=86, w=312, h=54
- 实心或虚线方框：x=394, y=56, w=344, h=96
- 实心或虚线方框：x=410, y=86, w=312, h=54
- 实心或虚线方框：x=22, y=177, w=716, h=36
- 连线 path：M371,113.0 L383,113.0

## 全部文字

- driver 侧与 worker 侧各发生什么
- driver（用户代码）
- @ray.remote 声明函数或类
- g.remote(i) 立刻拿到 future
- worker（真正执行）
- 执行函数体，算出结果值
- 值留在算它的那台机器上
- ray.get(future) 把 driver 阻塞到值可用；取回来的是值，不是状态
- future 是两侧之间唯一的凭据，值在哪、谁在等它由 ownership 记录

## 缺陷

无。`tools/svg-lint` 实测 0 error、0 warning（同日复跑 `scripts/check_figures.py --root . --strict`）。

## 判定

可用。
