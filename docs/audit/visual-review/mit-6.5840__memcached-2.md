# mit-6.5840/figures/mc-2.svg

> **作者自查**：本页 11 张图均由本讲作者自绘（源笔记里没有任何图片文件），
> 因此这份记录是**作者对自绘图的几何核对**，**不是**独立第二人复核。
> 页面正文本次**未做任何修改**。

## 版面

- viewBox `0 0 760 342`
- 标题（`<title>`）：大图景：一个 region 里有三样东西，而每个 region 都是完整副本
- 边距：左 25px ／ 右 25px ／ 上 24px ／ 下 24px（窗口 20–25px）
- 框 8 个；文字节点 17 个；画布 760×342

逐元素（框，属性值）：

- `<rect x="25" y="72" width="220" height="45" rx="6"/>`
- `<rect x="270" y="72" width="220" height="45" rx="6"/>`
- `<rect x="515" y="72" width="220" height="45" rx="6"/>`
- `<rect x="25" y="145" width="710" height="27" rx="6"/>`
- `<rect x="25" y="200" width="710" height="30" rx="6"/>`
- `<rect x="25" y="258" width="220" height="60" rx="6"/>`
- `<rect x="270" y="258" width="220" height="60" rx="6"/>`
- `<rect x="515" y="258" width="220" height="60" rx="6"/>`

逐元素（文字，属性值）：

- `<text x="380" y="38" font-size="16">大图景：一个 region 里有三样东西，而每个 region 都是完整副本</text>`
- `<text x="135" y="90.5" font-size="10">数据新鲜不新鲜并不关键</text>`
- `<text x="135" y="105.5" font-size="10">人对轻微的陈旧是容忍的</text>`
- `<text x="380" y="90.5" font-size="10">读多写少</text>`
- `<text x="380" y="105.5" font-size="10">这对缓存有利</text>`
- `<text x="625" y="90.5" font-size="10">但局部性很差</text>`
- `<text x="625" y="105.5" font-size="10">这对缓存不利</text>`
- `<text x="380" y="161.65" font-size="9">负载极高：每秒数十亿次存储操作。对比：一台 MySQL 约十万次简单查询每秒，一台 memcached 约一百万次 get 或 put 每秒</text>`
- `<text x="380" y="218.5" font-size="10">每个 region 里有三样东西：分片存在 MySQL 上的真数据（有 ACID 但慢）</text>`
- `<text x="135" y="276.5" font-size="10">一层 memcached</text>`
- `<text x="135" y="291.5" font-size="10">数据在内存里，快</text>`
- `<text x="135" y="306.5" font-size="10">但容量有限</text>`
- `<text x="380" y="284" font-size="10">无状态的 web 服务器</text>`
- `<text x="380" y="299" font-size="10">它是 memcached 与数据库的客户端</text>`
- `<text x="625" y="276.5" font-size="10">副本关系</text>`
- `<text x="625" y="291.5" font-size="10">每个 region 都是完整副本</text>`
- `<text x="625" y="306.5" font-size="10">西岸是主，其余走异步日志复制</text>`

## 全部文字

```
大图景：一个 region 里有三样东西，而每个 region 都是完整副本
数据新鲜不新鲜并不关键
人对轻微的陈旧是容忍的
读多写少
这对缓存有利
但局部性很差
这对缓存不利
负载极高：每秒数十亿次存储操作。对比：一台 MySQL 约十万次简单查询每秒，一台 memcached 约一百万次 get 或 put 每秒
每个 region 里有三样东西：分片存在 MySQL 上的真数据（有 ACID 但慢）
一层 memcached
数据在内存里，快
但容量有限
无状态的 web 服务器
它是 memcached 与数据库的客户端
副本关系
每个 region 都是完整副本
西岸是主，其余走异步日志复制
```

## 缺陷

- **行内对齐**：框(270,258) 高 60 比按其自身行数算出的 45 高，因为同一行内所有框按**本行最大行数**对齐（生成脚本 `row()` 的设计），**不是缺陷**。

## 判定

**可用**（作者自查；`check_figures --strict` 对本图 0 error 0 warning；上面唯一的「框高」条目是行内对齐的设计，不是缺陷）。
