## papers/mapreduce 质量审核 · 2026-09-28 · 审校人 mit65840-reviewer · 作者 mit65840-author

> 审校人**不是**本讲作者。本记录只写结论，不改正文与图。
> **注意：本记录与其它六份不同 —— 它有一块很大的「未核」区域，原因见下。请 Lead 决策。**

### 核对基线（附录十三：先做行尾归一化再算哈希）

| 对象 | 归一化 SHA256 | 字节 |
| --- | --- | --- |
| `content/papers/mapreduce/index.md` | `08546A232610E69C87E2AF53423875D70A8C8D1C073B687E93507A7A130F4896`（全 64 位） | 25879 |
| 源 `_fc/l01.txt`（LEC 1 讲义，含 MapReduce 一节） | `57D5008EC0ADFE7D9F13D2684347AE52189A4890FD563DBEACFBE0DC504B110E` | 10886 |
| 旁证 `courselingo/docs/_fetch/6824-lab-mr.html`（Lab 1 官方页） | — | 15394 |

11 张图（前 16 位）：`mapreduce-1 46E2B672FAF8C9BD` · `mapreduce-3 0FFA9FC8C26CC2AA` · `mapreduce-4 F0EBCD2D188167D2` ·
`mapreduce-5 3D40694C53650861` · `mapreduce-6 490694A212AC3C0C` · `mapreduce-8 619FCD7F1F494D03` ·
`mapreduce-11 CB21716B8EE0939A` · `mapreduce-12 912CD0F443C71012` · `mapreduce-13 5C78CDF5B94C9AFA` ·
`mapreduce-21 9EBBEA4D96B5234F` · `mapreduce-22 171E9A65C0AECCD8`

---

## ★ 可核范围（**论文已到手，本节已更新**）

**第一轮核对时 MapReduce 论文正文不在工作区**：`_fetch/mapreduce-usenix.html` 与仓库根 `usenix.html` **都只是 USENIX 出版页**；
全仓 grep `Execution Overview` / `Backup Tasks` / `Task Granularity` / `skipping bad records` **0 命中**；
`web_fetch` 被拒（`resolves to a non-public IP address`）；`web_search` 无 API key。
**⇒ 当时我拒绝用记忆把那 21 条论文级声明标成 ✅，而是列成一张「未核清单」（原样保留在下面的 B 节，作为留痕）。**

**Lead 随后把论文取来了**（正是当时给的处置建议①）：

| 对象 | 归一化 SHA256 | 尺寸 |
| --- | --- | --- |
| `_fc/mapreduce.txt`（抽好的论文文本，1280 行） | `91AA3D51E17602483353F1E58733B67A3B1861CADA489281F92188AE090029FF` | 原始 57106 B |
| `_fc/mapreduce-osdi04.pdf`（OSDI '04 正式版，13 页） | — | 190711 B |

**⇒ 那 21 条我已逐条回源重核，见本记录末尾的「补核」一节；最终 P 计数以那一节为准。**

---

### 事实核对

#### A · 本地有源、可核的部分（`_fc/l01.txt` 与 Lab 1 页）

| 声明（页面位置） | 源 | 结果 |
| --- | --- | --- |
| 输入被切成多份、每份交给不同机器（L45/L63） | l01 L162 `input is (already) split into M pieces` | ✅ |
| 中间键空间切成 R 份、按 `hash(key) mod R` 落盘、同一个键去同一个归约任务（L45/L67） | l01 L208–211 `MR splits into files by hash(key) mod R` / `each "hash bucket" contains multiple keys` / `The map workers all hash the same way`；L213 `each Reduce task processes one hash bucket` | ✅ |
| 归约任务用远程调用去**每台** map 机器上拉自己那一份（shuffle）（L67） | l01 L214 `MR fetches each Reduce tasks' bucket from every Map worker` | ✅ 方向正确 |
| 拉齐后按键排序、逐键调用 reduce；每个归约任务写一个输出文件（L67/L68） | l01 L215–216 | ✅ |
| 中间结果落在 map 机器**本地磁盘**、而不是写进分布式文件系统（L79） | l01 L248–250 `Intermediate data goes over network just once. Map worker writes to local disk. Reduce workers read from Map worker disks over the network.` | ✅ 事实对 |
| 「留在本地只需重跑那几个映射任务」（L77/L79、`mapreduce-1` 下排） | l01 L269 `Coordinator re-runs just the failed Map()s and Reduce()s.` | ✅ |
| 「顺带补一条**课程讲义**给的理由：留在本地磁盘时中间数据只过一次网络，走分布式存储至少过两趟」（L81） | l01 L251 `(Storing it in GFS would require at least two trips over the network.)` | ✅ **归属正确**（这确实是讲义的话） |
| 容错靠重跑：worker 崩溃后重跑它那部分活（L57/L83） | l01 L264–269 | ✅ |
| 要求 map/reduce 是确定性函数；不确定则语义降级（L57/L93/L179） | l01 L271–278 `Map and Reduce should be pure deterministic functions` | ✅ 要求本身对（**降级到什么程度**属论文级 ⇒ 未核） |
| 同一个任务跑两遍只留一份：靠原子改名（L89/L93、`mapreduce-6`） | l01 L284–286 `atomic GFS rename prevents mixing; one complete file will be visible` | ✅ |
| 落后者（straggler）→ 备份执行，谁先完成用谁（L113） | l01 L287–289 `coordinator starts a second copy of last few tasks` | ✅ 机制对（**具体数字**属论文级 ⇒ 未核） |
| 主节点只负责记账：跟踪每个任务状态、把任务发给空闲 worker（L83/L127） | l01 L218–220 | ✅ |
| 主节点挂掉怎么办 —— **讲义只提问没回答**（L91 说论文给了检查点与中止） | l01 L292 `What if the coordinator crashes?`（无答案） | ✅ 讲义侧如此（**论文侧**属未核） |
| GFS 里输入以 **64MB** 切块（L97） | l01 L201 `in 64 MB chunks` | ✅ |
| grep 峰值 **30 GB/s** 量级（L97） | l01 L300 `30,000 MB/s (30 GB/s)` | ✅ 量级对；页面写「**30GB/s 以上**」，讲义只说 30,000 MB/s ⇒「以上」无据 → P2-2 |
| 数据本地性：尽量把 map 调度到「本地就有这份输入」的机器（L97） | l01 L245–247 `Coordinator tries to run each Map task on GFS server that stores its input… Map input is usually read from GFS data on local disk, not over network.` | ✅ |
| 「框架没有选举、没有多数派（这两条对比是我们的归纳）」（L57） | l01 全篇无选举/多数派 | ✅ 已标为我们的话 |
| 「论文没有讨论键分布不均这一类倾斜，这一段是我们顺着分区函数补的分析」（L117） | 论文不可得 | ✅ 已标为我们的话（**论文是否真的没讨论**属未核，见 C 表） |
| 「Spark、Dryad、Pregel 是课外的延伸对比，论文没有提到它们」（L153/L163） | 论文不可得 | ✅ 已标；**且 `mapreduce-13`/`-22` 把「课外延伸，论文未提」写进了图内可见文字** |
| 「写了 2TB 结果还各存两份副本」之外的多数实测数字（L141） | l01 只有 30,000 MB/s / 1764 workers / 17MB/s / 9MB/s | ⏳ 未核 |

#### B · 第一轮的 ⏳ 未核清单（21 条）—— **已被末尾「补核」一节全部核过；本节只作留痕**

| # | 页面位置 | 未核的声明 | 需要什么才能核 |
| --- | --- | --- | --- |
| 1 | L20 | 线上索引系统某阶段代码 **3800 行 → 700 行** C++ | 论文 §1 |
| 2 | L32 | 值以**迭代器**喂给 reduce，以免值太多装不进内存 | 论文 §2.1 |
| 3 | L49 | 「**论文明确说**」R 与分区函数由用户指定；分片大小、输入输出格式、combiner 也在用户手上 | 论文 §4.1/§4.3/§4.4 |
| 4 | L63 | 输入分片 **16MB 到 64MB**，切法可由用户调整 | 论文 §3.1/§4？ |
| 5 | L65–L66 | 缓冲区攒到一定量才落盘、按分区切成 R 个区域并上报位置与大小 | 论文 §3.1 |
| 6 | L71 | 同一分区内按 key 递增交给 reduce；输出文件本身按键有序；全局有序拼 R 个文件 | 论文 §4.2 |
| 7 | L71 | 本地顺序执行模式（把 M、R 压小在单机跑） | 论文 §4.7 |
| 8 | L71 | reader 接口允许扩展输入类型 | 论文 §4.4 |
| 9 | L83 | 主节点**定期 ping**、超时标记失败；正在执行的任务退回 idle；**已完成的 map 要重跑、已完成的 reduce 不用**；重跑后通知 reduce 改去新位置读 | 论文 §3.3 |
| 10 | L91 | 主节点可写周期检查点、从检查点恢复「原理上容易」；但选择**中止整个作业** | 论文 §3.3（Master Failure） |
| 11 | L93 | 非确定性时语义**降级为**「每个归约分区的输出各自等价于某一次顺序执行」 | 论文 §3.3/§4.5 |
| 12 | L97 | 副本「**通常 3 份**」；退一步放到**同一台交换机下**；本地性收益主要体现在「跑在相当一部分 worker 上的大规模作业」 | 论文 §3.4/§4.1（注意：l01 L204 写的是 `2 or 3 servers` ⇒ 见 P2-1） |
| 13 | L105 | O(M+R) 次调度、O(M×R) 状态（约每组合一字节）；真实规模 **M=200000、R=5000、2000 台 worker** | 论文 §3.5/§4.2 |
| 14 | L105 | M 要取到每份分片 16–64MB；R 取成机器数的「一个小倍数」 | 论文 §4.2 |
| 15 | L105 | 排序基准 **M=15000、R=4000、输入约 1TB** | 论文 §6.2 |
| 16 | L107 | combiner；词频大致服从 **Zipf**；combiner 代码通常与 reduce 相同、区别只在输出去向 | 论文 §4.3 |
| 17 | L113 | 坏磁盘 **30MB/s→1MB/s**；机器初始化代码把处理器缓存关掉、慢上百倍 | 论文 §3.6/§6.5？ |
| 18 | L113 | 备份执行只多花**百分之几**资源；排序关掉备份 **891 秒 → 1283 秒（+44%）** | 论文 §6.5？ |
| 19 | L125 | 论文在经验一节把**大规模机器学习与图计算**列为已经用上的领域 | 论文 §7 |
| 20 | L131 | 框架**不支持**多输出文件的原子提交；「论文说实践中这从来不是问题」 | 论文 §4.5 或 §6？ |
| 21 | L139/L141 | 坏记录的**跳过模式**（信号处理器 + 全局变量记序号 + 「最后的话」UDP 包 + 失败超过一次就跳过）；grep **150 秒里约一分钟**是启动开销；排序一半时间写本地磁盘；2TB 输出各存两份 | 论文 §4.6 / §6.1 / §6.2 |

> 说明：**「未核」不等于「有问题」**。它们的形态与量级都与我对这篇论文的印象相容，
> 但**相容不是核对**（附录七第三次的教训就是「把读到的参照当事实」）。列出这张表是为了让 Lead 决定：
> 补论文文本后重核，或接受把本页的 `reviewed` 前置条件记为**未满足**。

#### C · 归属类声明（页面已标为「我们的」——本地可核的部分）

| 声明 | 判定 |
| --- | --- |
| L57「没有选举、没有多数派这两条对比是我们的归纳」 | ✅ 已标 |
| L79「论文只写了它留在本地磁盘这个事实，理由要我们顺着消费模式推」 | ✅ 已标（**且理由本身是对的**：一次性消费 + 多副本开销确实成立）；但「论文**只**写了事实」这半句属未核（C-表第 12 条相邻） |
| L117「论文没有讨论键分布不均…这一段是我们的分析」 | ✅ 已标 |
| L153/L163/L171「Spark/Dryad/Pregel、与 Raft 的对照是课外延伸」 | ✅ 已标，**且落进图内可见文字**（`mapreduce-13` 页脚「共识那一侧（课外延伸，论文未提）」、`-22`「这三个系统是课外延伸，论文没有提到」） |
| L163「MapReduce 用重跑绕开共识 / 目标是选择中心调度」 | ✅ 我们的对照，方向正确（作者本轮已把「中心化写成放弃中心化」那处方向错改掉） |

---

### 陌生读者测试（8 题）

**执行方式**：Lead 在 depth 0 spawn 的全新子代理，只给 `content/papers/mapreduce/index.md`，
禁止读源/联网/用自身背景补。

**结果：✅ 6　⚠️ 2　❌ 0**（⚠️ 25% ≤ 40%、❌ 0% ⇒ **不触发 §3 的比例阈值**）

| 题 | 判定 | 依据 |
| --- | --- | --- |
| Q2 崩溃后谁重跑 | ✅ | L83 |
| Q3 跑两遍只留一份 | ✅ | L93/L115 |
| Q4 哈希分区的瓶颈与 combiner | ✅ | L117 |
| Q5 M/R 为什么远大于机器数、代价与取值规则 | ✅ | L105 |
| Q6 主节点挂了怎么办 | ✅ | L91 |
| Q8 数据本地性与收益前提 | ✅ | L97 |
| Q1 中间结果为什么留本地磁盘 | ⚠️ | 正文给了理由，但**「如果写进分布式存储，容错规则会怎么变」这个反事实只在 L175 的「读完应该能回答」里被问、正文没给** |
| Q7 非确定性时的语义降级 | ⚠️ | 读者：降级写清了，但**没说这个更弱的保证为什么可以接受**，只写了它是「刻意的」 |

**我对这两条 ⚠️ 的判断（都判成立，但都不升 P1，理由分开写）**：

- **Q1**：与 `02-rpc-and-threads` 的 P1-1 是**同一形状**（页面在自己的「读完应该能回答」里提了一个正文答不全的问题）。
  **但我判它是 P2、不是 P1**，区别在于缺口大小：02 那题正文**完全没讲**（源里有、页面没有）；
  这里正文已给出**理由**与「已完成 map 要重跑」的机制，只差把反事实那半句说出来。
  ⇒ 处置：**P2-4（新增）**——在 L79 末尾补半句「（若中间结果也进分布式存储，已完成的映射任务就不必重跑，代价是每个字节多走两趟网络与多副本写入）」。
  **这条与 P0-1 的修法在同一处，一起改最省。**
- **Q7**：**源里也没有论证**这个降级为什么可接受（§3.3 只描述语义；论文只在 §4.5 对 side-effects 说了
  `This restriction has never been an issue in practice`，**不是**对非确定性降级说的）。
  ⇒ 按判据「源里有就挂出处、源里没有就是我们的推断」，**页面没写不算缺陷**，记为「⚠️ 成立，但源亦未展开」。
  建议（可选）：在 L93 加一句「论文只描述了这个降级，没有论证它为什么可接受」。

---

### 附录二 / 附录十 专项

**（一）附录二（标记必须落到图内可见文字 + alt）—— 本页做得好**

| 属于「我们的/课外的」内容 | 正文标记 | 图内可见文字 | `desc` | `alt` | 判定 |
| --- | --- | --- | --- | --- | --- |
| Spark/Dryad/Pregel 属课外延伸 | L153 | ✅ `mapreduce-22`「（这三个系统是课外延伸，论文没有提到）」 | ✅ | ✅ L157 | ✅ |
| 与 Raft 的对照、共识那一侧 | L163 | ✅ `mapreduce-13`「共识那一侧（课外延伸，论文未提）」 | ✅ | ✅ L167 | ✅ |
| 分区倾斜那段是我们的分析 | L117 | 未画 | — | — | ✅ 不适用 |
| 换掉默认分区的代价 | L49/L55 | ✅ `mapreduce-21` 页脚「代价：换掉默认分区（比如按主机名），某个大站点可能把单一分区撑爆」 | ✅ | ✅ L53 | ✅ |

**（二）附录十（文字没说的事，图不许说）**

- ⚠️ **`mapreduce-3` 的「关掉它：891 秒涨到 1283 秒」代词先行词不在本框内** —— 见 P2-3（属性原文在下面）。
  页面上这个数字的正确说法在正文 L113「排序程序关掉**备份执行**后，整体耗时从 891 秒涨到 1283 秒，多了 44%」，
  而图里的第三格主文字是「谁先完成用谁」、副文字是「关掉它：…」——**「它」要靠读者跨到相邻那一格（「对策：备份执行」）去接**。
  按 `附录十` 判据 1（「每个标签/文字，仅凭位置能否唯一确定它属于哪个元素」），这是一处需要读者自行拼接的指代。
  属性原文（`mapreduce-3.svg`）：
  ```xml
  <text x="379" y="110" font-size="15" text-anchor="middle" fill="#b45309">对策：备份执行</text>
  <text x="379" y="132" font-size="12" text-anchor="middle" fill="#b45309">没结束的任务在别处再起一份</text>
  <text x="616" y="110" font-size="15" text-anchor="middle" fill="#166534">谁先完成用谁</text>
  <text x="616" y="132" font-size="12" text-anchor="middle" fill="#166534">关掉它：891 秒涨到 1283 秒</text>
  ```
  （另有一份更早的配图复核记录 `preview/visual-review/mit-6.5840__mapreduce-3.md` 也指向同一处，
  结论是「需小修…把绿框副文字补全为『关掉备份执行：891 秒涨到 1283 秒』」。
  我按**附录五**只把它当线索，**我自己看了当前文件的属性原文**，所以这条是我核出来的，不是转述旧结论。）
- ✅ 其余各图的「并列/对齐」都未读出文字没下的断言：`mapreduce-4/5/13/21/22` 两列都是**显式对比**（一侧是"要解决的问题"、一侧是"解法/代价"），
  `mapreduce-13` 两列还各带列标题（「重跑这一侧」/「共识那一侧（课外延伸，论文未提）」）⇒ 判据 3 要求的显式分组已做。

**（三）几何类（附录十一）**：本页无「看起来偏了/更宽」类主张，未做渲染量墨迹。

---

### 一致性 / 可读性 / 诚实性

- **一致性（透镜 4）**：
  - **跨页数字**：本页 L97 写 GFS 每块「**通常 3 份**副本」，而 `_fc/l01.txt` L204 写 `replicates data on 2 or 3 servers`，
    `03-gfs` 页写「默认存三份」（论文 §2.3）。三个说法里本页与 03 页同向、与 01 页面（引 l01）不同向 ⇒ **P2-1**（与 `03-gfs-factcheck.md` 的 P2-2 是同一处，两处一起修最省）。
  - 与 `04-paxos` / `papers-raft` 的口径：「重跑 vs 共识」这条对照三页同向 ✅。
- **可读性（透镜 5）**：本次**没有重跑** `audit_content.py`。人读一遍：L105（任务粒度）与 L117（倾斜）两段偏长且数字密集，但每段都有结论句。
  **机检指标属"未验"。**
- **诚实性（透镜 6）**：**本页的标注习惯是好的** —— 四类课外/我们的内容都标了，其中两类还落进了图内可见文字；
  L79 主动坦白「理由要我们顺着消费模式推」；L81 主动区分「讲义给的理由」与「论文没给理由」。**没有发现伪装成源结论的臆造。**

### 本次覆盖面（附录十二）

- **已验**：11 张图的 `title`/`desc`/图内文字与正文 `alt` 逐张比对；`mapreduce-3` 的代词归属按属性原文核；
  **`_fc/l01.txt` 全部 316 行逐段对照**；Lab 1 页的接口约定（`nReduce`、`mr-out-X`、把中间结果放当前目录）与页面 L67/L45 的口径一致 ✅。
- **未核（本记录的主要缺口）**：**论文正文全篇**（21 条声明，见 B 表）；机检指标；渲染量墨迹。

---

### 结论

**P0 1 项、P1 0 项、P2 3 项 → 修完 P0 后可提 `reviewed`。**
（第一轮那句「21 条未核 ⇒ 不具备 reviewed 条件」**已被本节的补核取代**；原结论如实保留在下面「留痕」里。）

#### P0 · 1 项（本轮补核新发现）

**P0-1（对源的否定性声明与源冲突）**：L81 说「**论文本身确实没有给这条理由**」（指"中间结果留本地磁盘、而不是走分布式存储"的理由）。
**论文给了。** 论文 §7（Conclusions）原文：

> `the locality optimization allows us to read data from local disks, and writing a single copy of the intermediate data to local disk saves network bandwidth`（`_fc/mapreduce.txt` @49038）

⇒ 论文从「**只写一份、省网络带宽**」的角度给过理由，只是没有像讲义那样把「只过一趟 vs 至少两趟」的账算出来。
→ **修在**：L81 的括注改成「论文在设计权衡的总结里点过一句：中间数据只写一份到本地磁盘，省下网络带宽（§7）；讲义把同一件事算得更具体（只过一次网络 vs 至少两趟）」。
**L79 的「理由要我们顺着消费模式推」也要跟着改**，否则读者会以为论文完全没解释这个选择。

#### P1 · 0 项

#### P2 · 3 项

1. **P2-1（跨页数字，不变，但结论要改一半）**：L97「每块**通常 3 份**副本」——**现在可确认页面用的是论文原话**
   （§5.1：`stores several copies of each block (typically 3 copies)`，@18966），而 `_fc/l01.txt` L204 写 `2 or 3 servers`。
   ⇒ **页面不错，是两处源口径不同**；建议与 `03-gfs` 的 P2-2 一起处理（在引 l01 的那一处标注「讲义的说法」）。
2. **P2-3（附录十 判据 1，不变）**：`mapreduce-3` 第三格副文字「**关掉它**：891 秒涨到 1283 秒」的先行词在相邻格，
   建议补全为「关掉**备份执行**：891 秒涨到 1283 秒」。
3. **P2-4（透镜 3 Q1 那条 ⚠️，新增）**：L79 补半句反事实（见「陌生读者测试」一节），与 P0-1 同处一起改。

#### ~~P2-2~~ —— **已证伪并撤销**

第一轮我据讲义把 L97「峰值能到 **30GB/s 以上**」记成「『以上』没有依据」，并注明「论文原文我核不到」。
**论文到手后一查：原文就是 `peaks at over 30 GB/s when 1764 workers have been assigned`（@33553）。**
⇒ **页面准确，我那条 P2 不成立，撤销。** 这是「拿到源」最直接的一次收益：**一条我自己的假异议被源关掉了**（附录八：复核者的发现也要能被证伪）。

#### 已核不出问题（更新版，供下一个复核者直接关闭）

- 页面对「中间结果为什么不写 GFS」**没有把它记在论文名下**（写成「讲义给的理由」）—— 跨材料归属没搞混 ✅；
  但同一段的**否定半边**（"论文没给理由"）与源冲突，见 P0-1。
- 「同一个任务跑两遍只留一份」的两处机制（map 侧忽略重复完成消息、reduce 侧临时文件原子改名）与 `l01.txt` L284–286 同向 ✅，且论文 §3.3 `We rely on the atomic rename operation`（@17478）✅。

---

### ★ 补核（论文到手后 · 21 条逐条回源）

源：`_fc/mapreduce.txt`（`91AA3D51E17602483353F1E58733B67A3B1861CADA489281F92188AE090029FF`，1280 行）。
**21 条全部核过：20 条与页面一致，1 条冲突（即 P0-1）。**

| # | 页面 | 声明 | 论文原文（片段 + 字符偏移） | 结果 |
| --- | --- | --- | --- | --- |
| 1 | L20 | 3800 行 → 700 行 | `dropped from approximately 3800 lines of C++ code to approximately 700 lines` @42688 | ✅ |
| 2 | L32 | 值以迭代器喂 reduce | §2.1 `we use an iterator` | ✅ |
| 3 | L49 | R 与分区函数由用户指定 | `The number of partitions (R) and the partitioning function are specified by the user` @10740 | ✅ |
| 4 | L63 | 分片 16MB–64MB | `each individual task is roughly 16 MB to 64 MB of input data` @20598 | ✅ |
| 5 | L65–66 | 缓冲落盘、按分区切 R 区、上报位置 | §3.1 步骤 3–4 | ✅ |
| 6 | L71 | 分区内按 key 递增 | §4.2 `We guarantee that within any given partition, the intermediate key/value pairs are processed in increasing key order` | ✅ |
| 7 | L71 | 本地顺序执行模式 | §4.7 Local Execution | ✅ |
| 8 | L71 | reader 接口可扩展输入类型 | §4.4 `support for reading input data in several different formats` @25103 | ✅ |
| 9 | L83 | ping 超时判失败；已完成 map 重跑、已完成 reduce 不用；通知改读新位置 | §3.3 `The master pings every worker periodically… Any map tasks completed by the worker are reset back to their initial idle state` @14505 | ✅ |
| 10 | L91 | 检查点「容易」但选择中止 | §3.3 `It is easy to make the master write periodic checkpoints… However, given that there is only a single master, its failure is unlikely; therefore our current implementation aborts the MapReduce computation if the master fails` @15981 | ✅ |
| 11 | L93 | 非确定性的降级语义 | §3.3 `the output of a particular reduce task R1 is equivalent to… a sequential execution… However, the output for a different reduce task R2 may correspond to… a different sequential execution` @18023 | ✅ |
| 12 | L97 | 「通常 3 份副本」；同交换机；本地性收益前提 | §5.1 `stores several copies of each block (typically 3 copies)` @18966 | ✅ |
| 13 | L105 | O(M+R)／O(M×R)／约 1 字节每组；M=200000、R=5000 | `keeps O(M R) state… approximately one byte of data per map task/reduce task pair` @20127；`M = 200,000 and R = 5,000` @20640 | ✅ |
| 14 | L105 | M 取 16–64MB、R 取机器数的小倍数 | `we make R a small multiple of the number of worker machines we expect to use` @20598 | ✅ |
| 15 | L105 | 排序基准 M=15000、R=4000、约 1TB | `approximately 1 terabyte of data` @34109；`(M = 15000)`、`4000 files (R = 4000)` @35280 | ✅ |
| 16 | L107 | combiner；Zipf；代码与 reduce 相同、只差输出去向 | `word frequencies tend to follow a Zipf distribution` @24123；`essentially the same code is used to implement both the combiner and the reduce functions. The only difference…` @24633 | ✅ |
| 17 | L113 | 坏盘 30MB/s→1MB/s；缓存被关掉慢上百倍 | §5.5 / §3.6 | ✅ |
| 18 | L113 | 备份执行只多花百分之几；891 → 1283（+44%） | `the entire computation takes 891 seconds` @37425；`The entire computation takes 1283 seconds, an increase of 44%` @38509；`takes 44% longer… when the backup task mechanism is disabled` @22314 | ✅ **方向也对**（关掉备份 ⇒ 891 涨到 1283） |
| 19 | L125 | 经验一节列了大规模机器学习与图计算 | §6.1 `large-scale machine learning problems… large-scale graph computations` @39940/@40218 | ✅ |
| 20 | L131 | 不支持多输出文件的原子提交；有一致性要求就得确定性；「实践中从来不是问题」 | §4.5 `We do not provide support for atomic two-phase commits of multiple output files produced by a single task. Therefore, tasks that produce multiple output files with cross-file consistency requirements should be deterministic. This restriction has never been an issue in practice.` @26663 | ✅ 三句逐句对应 |
| 21 | L139/L141 | 跳过模式；grep 150 秒里约一分钟启动；排序一半时间写本地磁盘；2TB 输出各存两份 | §4.6 `the signal handler sends a "last gasp" UDP packet that contains the sequence number… seen more than one failure on a particular record… skipped` @27860；§5.1 `approximately 150 seconds… includes about a minute of startup overhead` @33741；§5.3 `the sort map tasks spend about half their time and I/O bandwidth writing intermediate output to their local disks` @36149；§5.3 `2 terabytes are written as the output` @35280 | ✅ 四条全对 |

**顺带核掉的**：L97「峰值能到 30GB/s 以上」= 论文 `peaks at over 30 GB/s when 1764 workers have been assigned`（@33553）✅（即上面撤销的 P2-2）。

### 本轮覆盖面（附录十二）

- 已验：**论文全文**（21 条 + 30GB/s + 3 副本）；`_fc/l01.txt` 全部 316 行；11 张图的 `title`/`desc`/图内文字与正文 `alt` 逐张比对。
- **未验**：机检指标；渲染量墨迹；**抽文本身的准确性**（用的是 Lead 抽好的 `_fc/mapreduce.txt`，不是 PDF 原件 —— 但 PDF 就在旁边 `_fc/mapreduce-osdi04.pdf`，可复核）。

---

**审校人声明**：本记录覆盖的基线版本写在开头（页面 `08546A23…` **本轮复核未变**；论文 `91AA3D51…`）。按附录五，对其它版本的结论不成立。
**第一轮那份「21 条未核 ⇒ 不具备 reviewed 条件」的结论已被本轮补核取代**（原文如实保留，作为「结论只对它看的那一版成立」的留痕）。
透镜 3 答卷已回（✅6 / ⚠️2 / ❌0）。本记录不修改任何正文或图，`status` 字段由 Lead 处理。
