# 18-ray 质量审核 · 2026-09-29 · 审校人 CourseLingo 复核流 · 作者 cs168-author（本仓第 18 讲）

## 核对基线（附录十三：先做行尾归一化 read_bytes().replace(b"\r\n", b"\n") 再算 SHA256）

- 源文件：`_fc/l-ray.txt`（课程讲义 LEC 18 的纯文本快照）
- 归一化后大小：6926 字节 ｜ 行数：223 ｜ SHA256：`024A34C98686CB20F9B67BD59F0C145980F02F984ED8EB7A9DE63C3ED9C9D419`
- 期望值（派单给出）：6926 字节 / 223 行 / `024A34C98686CB20F9B67BD59F0C145980F02F984ED8EB7A9DE63C3ED9C9D419`
- 结论：**三项全部一致**。
- 本页：`content/18-ray/index.md` ｜ 汉字 5424 ｜ 图 12 张

## 事实核对

逐条与本页对照，均可在源文件中找到出处：

| 本页说法 | 源文位置 | 结论 |
|---|---|---|
| 三个想法：futures、actors、按 ownership 分片 | `Three ideas:` 起三行 | 一致 |
| future 的三条 API（异步调用返回、可作参数传递、可强制求值） | `Futures (API table 1)` 四条 | 一致 |
| 借用例子 `f3 = Add(shared(f1), shared(f2))`、`C(shared(x))` | `Example of borrowing: fig 2 / fig 6` | 一致 |
| `@ray.remote` 与 `g.remote(10)`，四次调用并行，`ray.get` 取回 | `Ray example of remote execution with futures` | 一致 |
| Counter actor、`Counter.remote()`、`increment.remote()` 返回 future | `Ray example of actors and object refs` | 一致 |
| 中心协调者表 `(id, task, refs, worker, value)`、Get 阻塞、大值进对象存储、对象不可变 | `Sketch of simple/hypothetical implementation` 段 | 一致 |
| 引用计数例子（C 返回后不能回收 x，因为 A 还在用） | 同节 `refs for reference counting` | 一致 |
| 中心方案两个成本：一次往返、future 很多且有的只跑几毫秒 | `Implementation challenge with centralized plan` | 一致 |
| 按对象 id 分片仍要一次往返、GC 可能跨分片 | `Alternative: shard the table` | 一致 |
| 调用者拥有返回的 future；值存在跑该任务的 worker 上 | `Ray solution: shard by ownership` | 一致 |
| 三张 owner 表的内容（x 的 Ref 为 W1,W3，Loc 为 W2 等） | `Example: state when both B and C are running` 三张表 | 一致 |
| owner = (IP, port, worker id)；taskId/objectId 的构造 | `Ownership implementation` | 一致 |
| 调度循环 reserve → lease → table[t].Loc；复用已租 worker | `distributed scheduler (figure 8)` | 一致 |
| 对象存储 API Create/Get/Pin/Release、Get 阻塞、首次 Create pin、次级副本 | `Memory management (figure 9)` | 一致 |
| fate sharing 的两个例子（worker 3 失败 / worker 1、2 都失败） | `Failure recovery: fate sharing` 与 `Example:` | 一致 |
| 「谁发起重跑」的讨论题我们只讲 ownership 概念、不给答案 | 源文末尾 `Homework:` | 按课程要求处理 |

## 陌生读者测试（8 题）

1. 这一讲为什么说 MapReduce 与 Spark 不适合模型服务？—— 见「一」：它们假定启动开销可摊薄、计算无状态，而服务要低延迟且跨调用留状态。
2. future 与 RPC 的调用形状差在哪？—— 见「二」「四」：RPC 是一次调用等结果，future 是先拿凭据、需要时才求值，系统可自行决定在哪算、何时搬数据。
3. `shared(f1)` 传的是什么？—— 见「三」：传的是 future 的引用，不是值。
4. 中心协调者方案的两次往返分别发生在哪？—— 见「六」「七」：发起任务一次，取值一次。
5. 为什么按对象 id 分片不能解决问题？—— 见「七」：仍要一次往返，且 GC 可能跨分片。
6. 「调用者拥有返回的 future」和「值存在跑任务的 worker 上」是同一件事吗？—— 见「八」：不是，两者被刻意分开。
7. owner 表里的 Ref 一列有什么用？—— 见「九」：引用计数，决定对象何时可以安全删除。
8. fate sharing 解决的是什么？—— 见「十一」：所有者已经不在时，持有悬空引用的任务也随之退出，让失败可以上报。

## 附录二 / 附录十 专项

- 附录二（授权）：`course.toml` 为 `verified = false`、`redistribution = "unknown"`；本页只写原创讲解，无逐字稿、无双语对照、无 Lab 代码与作业答案。源文末尾的讨论题只取概念、不给答案。
- 附录十（术语）：本页正文标记 8 个 `[[term:...]]`（`rpc`、`mapreduce`、`future`、`actor`、`ownership`、`lineage`、`lease` 等），全部落在正文、front matter 内 0 个；`validate.py --strict` 对本页 0 警告。
- 本次为本讲新增 5 条术语（`future`、`actor`、`ownership`、`object store`、`lineage`）与 1 条论文登记（`ray`），均为**只追加**。

## 一致性 / 可读性 / 诚实性

- 一致性：三个想法在「二」提出、「四」落到代码、「八」到「十一」落到实现，术语译法全页统一（future/actor/ownership 保留英文并首次给出中文说明）。
- 可读性：11 个内容节，每节结尾有图或收束句；图后均有解读句。
- 诚实性：作业讨论题只讲概念；论文授权按 USENIX 未给条款处理，本页声明不是译文。

## 本次覆盖面（附录十二）

- 覆盖：源文件全部 223 行；本页 11 个内容节。
- 未覆盖/未做：**源页与讲义中的配图没有逐张查看**（第 18 讲的讲义本身不含图；本页 12 张图全部自绘，未参考任何原图）。
- 未做：未提交、未推送（由 Team Lead 统一提交）。

## 结论

通过。源文件哈希三项一致；事实核对全部可溯源；本页 `validate --strict` 对本页 0 警告、配图 0 error 0 warning。

---

## 陌生读者测试（8 题）· 透镜 3 —— **已执行**（2026-09-29 补记）

> ★ 这一节此前写的是「**未执行**」（或根本没有这一节），而**那是这个仓的一个人工稳态**：
> 读者测试需要站在 **depth 0** 才能派（派出去的核对者实测 `subagent` 会报
> `depth 2 exceeds maxDepth 1`）⇒ **每一份交接都写「透镜 3 待做」，而接下它的人还是做不到。**
> ⇒ **Lead 已在 depth 0 派出七位全新读者，并做了汇总。**

**汇总文件**：[`docs/audit/lens-3-reader-reports.md`](lens-3-reader-reports.md)
（含七讲的结论一览、以及那条**共同成因**的逐处对照表）

**本讲的结论**：
```
总评        ：**不能一遍读懂**
自测题      ：4 条里 2 条只能答一半
读者报的条目：19
```

**最严重的一处**：
**三处「往返次数」对不上**（第 168 行说「发起与取值各要一次往返」，而第 170/172/176/184 行说「一次」）—— 读者说那让第 8 节的对比**两边不对等**；另 `driver`/`调度器`/`对象`/`pin`/`lease` 未定义，A/B/C/x/y 首次出场就要回连，三张 ASCII 表列不对齐。

★ 而读者是**只看这一页一遍**、不读源/别的讲次/审计记录/不联网的。
⇒ 所以它量的是**「这一页能不能把一个不懂的人带到懂」** ——
而那与「事实核对（vs 源）」「逐图复核（vs 描述）」「六道（vs 规范）」**是不同的参照物**。
