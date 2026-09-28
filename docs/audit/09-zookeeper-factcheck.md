## 09-zookeeper 质量审核 · 2026-09-28 · 审校人 mit65840-reviewer · 作者 mit65840-author

> 审校人**不是**本讲作者。本记录只写结论，不改正文与图。
> **版本提示**：我开工时这一页**仍在被作者改动**（最后写入 2026-09-28 23:28:53，比作者的轮次记录 `author-round-notes.md` 新 38 分钟）。
> 本记录只对下面这个哈希的版本成立（附录五）。
> **另**：`zookeeper-5.svg` 在本轮被改过（最后写入 23:24:19）。我**核的是改后版本**，并把现值记进下表 ——
> 我第一遍取的哈希（`A715557B…`）已过期，**不要再用它**（这正是附录五说的情况：结论要绑在它看的那一版上）。

### 核对基线（附录十三：先做行尾归一化再算哈希）

| 对象 | 归一化 SHA256 | 字节 |
| --- | --- | --- |
| `content/09-zookeeper/index.md` | `FFB0AD539C7CC3CB933145BD0920FD83888AFBDE15E7C19E315644B9D2CA9C7E`（全 64 位） | 29023 |
| 源 `_fc/l-zookeeper.txt`（287 行讲义） | `405DE0B1739DBB67E433649BD3764C9342706E6447D36F6E6E3AA4623F2A60FE` | 11686 |
| 源 `_fc/zookeeper.txt`（ATC'10 论文全文，1473 行） | `C05E436DB2E66DF531878B971565A205E2F8805DEA96AF5D66E16D967B4090F0` | 72264 |

14 张图（前 16 位）：`zookeeper-1 4205184F5F51C762` · `-2 54B6C84BD2B492FE` · `-3 F687F87D2E483B23` · `-4 7B9C4DA12ED137D6` ·
`-5 1CD568D94818DDC4`（本轮被改过，见上面的版本提示；第一遍的 `A715557B…` 已过期） · `-6 9C74DAED2F94CA38` · `-7 91DAFF3A1EB09FB5` · `-9 41FD2F464BB1DA99` · `-12 517ED5D0E8D7D78D` ·
`-13 A28CCF1B9164880B` · `-15 7FFC20EED93E49BD` · `-16 A755C0FC963C7353` · `-18 E47FCEFD422C4107` · `-20 2FC9A6D004365DBE`

---

### 事实核对

「讲义」= `l-zookeeper.txt`（行号照抄）；「论文」= `_fc/zookeeper.txt`（**行号照抄 + 原文片段**）。两篇源都完整核过。

| 声明（页面位置） | 源 | 结果 |
| --- | --- | --- |
| 论文出处：Hunt/Konar/Junqueira/Reed，ATC 2010（L13） | 讲义 L3–5 | ✅ |
| 两个角度：更简单的地基 + Raft 类复制的工程样例（L36） | 讲义 L7–11 | ✅ |
| etcd 受了它的影响（L36） | 讲义 L11 | ✅ |
| 「Raft 复制的是计算，不是状态」；应用要把每个变化变成日志、commit 后再执行（L26） | 讲义 L17–23 | ✅ 逐句对应 |
| 只复制存储：无副本的进程把状态写进容错存储，崩了换机重读（L44） | 讲义 L25–35 | ✅ |
| 云上临时申请替代机器很容易（L46） | 讲义 L52–53 | ✅ |
| 难点清单：检测已死／选出唯一新主／从半途更新恢复／老主还活着；**加上性能**（L46） | 讲义 L55–61（**恰 5 条**，含 performance） | ✅ 数目与内容都对 |
| 「写本机磁盘」这一档是我们补的（L42/L52） | 讲义无此档 | ✅ 已标（且写进 `zookeeper-5` 的 `desc`） |
| 内部：leader + followers、写走多数派、接近 primary-backup + 全序日志（**这个类比是我们加的**）（L58） | 讲义 L64–71 | ✅ 机制有源、类比已标 |
| wait-free＝服务端不替任何人排队、等待在客户端（L65/L186） | 论文 @609 `the wait-free aspects of shared registers with an event-driven mechanism` | ✅ 说明与论文一致 |
| create 排他：并发创建只有一个成功（L85） | 讲义 L88、L100、L120–122 | ✅ |
| setData 带版本号＝比较并交换；**版本号 −1 等于关闭检查**（L86） | 论文 @15852 `If the version number is−1, it does not perform version checking`；讲义 L92–94 | ✅ **逐字对应**（论文 API 侧确认） |
| 单 znode 原子、跨 znode 不是事务（L87） | 论文 @62304 `ordering enables functionality similar to mini-transactions`；讲义 L146–147 | ✅ |
| ephemeral 绑会话、超时后服务端删掉全部临时节点（L95） | 讲义 L102、L136–139；论文（会话/临时节点） | ✅ |
| sequential：服务端追加单调递增序号（L95） | 讲义 L83、L103 | ✅ |
| ZAB 原子广播 + 全序；顺序不同终值不同（L101/L105） | 讲义 L64–70；论文 §4.2 Atomic Broadcast | ✅ |
| 写路径五步：发给所连服务器 → 转 leader → 定位置并分配 zxid → 副本按序执行 → 多数派确认才回复（L109–L115） | 讲义 L68–70、L194–197 | ✅ 顺序与主体都对 |
| 写是线性化的；每个写要一次多数派确认（L117） | 讲义 L70 | ✅ |
| **只有写**是 A-线性的；读在本地副本完成 ⇒ 可能陈旧（L119/L121） | 论文 @17004 `Because only update requests are A-linearizable, ZooKeeper processes read requests locally at each replica`；讲义 L71 | ✅ **逐字对应** |
| A-linearizability 与 Herlihy 原定义的差别（客户端可同时有多个未完成操作）（L119） | 论文 @16460 全段（`we call it A-linearizability… In the original definition… a client is only able to have one outstanding operation at a time… In ours, we allow…`） | ✅ **逐字对应** |
| 逐客户端两条保证：读得见自己的写、位置不倒退（L119/L198） | 讲义 L218–225（`client FIFO order`） | ✅ |
| 锁：临时顺序节点 + 只监视前一个（L125/L131） | 论文 @25818–@27033（`it suffers from the herd effect… by only watching the znode that precedes the client's znode, we avoid the herd effect`） | ✅ |
| 被叫醒后必须重新检查自己是否持锁（L135） | 论文 @27033 `Once the znode being watched by the client goes away, the client must check if it now holds the lock` | ✅ **逐字对应**（页面还补了"论文伪代码就是跳回开头"） |
| ZK 刻意不在服务端实现原语；"协调内核"；"ZooKeeper 不是一个锁服务"（L139） | 论文 @2971 `a coordination kernel that enables new primitives without requiring changes to the service core`；论文 @58890 `ZooKeeper is not a lock service… there are no lock operations in its API` | ✅ 后两句逐字对应（引号那句见 P2-2） |
| 成员表：/workers 下临时节点、子节点列表＝活着的成员（L141/L145） | 论文 @24596（`obtain group information by simply listing the children of zg… set the watch flag to true`） | ✅ |
| **临时节点不能有子节点**（L141） | 论文 @9742 `all znodes, except for ephemeral znodes, can have children` | ✅ **逐字对应** |
| 崩在半途：没有跨 znode 事务；三种绕法（单 znode／ready 闸门／新集合＋指针），都以一次提交写收尾（L151） | 讲义 L144–161 | ✅ 逐段对应 |
| 会话判死时原子做两件事：删临时节点 + 拒绝该会话的请求（L157） | 讲义 L136–140、L170–173 | ✅ |
| **删临时节点本身是一次 A-线性的写操作，讲义专门标注**（L162） | 讲义 L141 `(ephemeral deletions are A-linearizable ZK ops)` | ✅ **逐字对应，归属也对** |
| fencing：对已判死的客户端也拒绝（**这个词与含义出自讲义**）（L166） | 讲义 L177–178 | ✅ 讲义明写 `"Fencing" is a term for ignoring requests from a client declared dead` |
| fencing token 那种形式是我们的补白（两个源里没有 token）（L166、`zookeeper-18`） | 两源检索无 `token` | ✅ 已标（**且写进图内可见文字与 desc**） |
| 故障检测可能判错，但所有人服从；「认同同一个判断」比「判得对」更重要（L174） | 讲义 L180–187 | ✅ 逐句对应 |
| watch 一次性、触发即失效（L188） | 论文 @10924 `Watches are one-time triggers associated with a session; they are unregistered once triggered or the session closes` | ✅ **逐字对应** |
| 三个坑：通知不保证次数/时机；收到后要重读；读-注册-再检查写成循环（L196/L197） | 论文 @11151（`/foo` 被改两次只收到一次通知）；讲义 L218–225 | ✅ |
| **通知的排序保证：先看到通知事件，再看到新状态**（L202） | 论文 L387–390 `is solved by the ordering guarantee for the notifications: if a client is watching for a change, the client will see the notification event before it sees the new state of the system after the change is made` | ✅ **逐字对应** |
| 会话/连接丢失也会送进监视点回调，所以通知可能被延迟（L202） | 论文 @11173 `Session events, such as connection loss events, are also sent to watch callbacks so that clients know that watch events may be delayed` | ✅ |
| 性能按读与通知优化：散连多台、读在本地、监视点就地记、异步批量、数据全在内存（L204–L209） | 讲义 L189–206、L227–229；论文 @62304 `keeps its state fully replicated and in memory for high performance` | ✅ |
| 写要落盘、定期快照、快照用「模糊」技术（L209） | 讲义 L230–235；论文 §4.3（fuzzy snapshot 的 /foo /goo 例子 @40910） | ✅ |
| 数字：整体几万次/秒；单客户端每次等确认约 **1.3ms**、**约 776 次/秒**；约 2000 是 Table 2 十 worker 档；leader 故障停顿几秒；follower 故障只吞吐下滑；纯写按 1000 字节算（L217） | 讲义 L240、L246、L250–L255、L261–L262 | ✅ **逐个对应**（含「776」与「2000」的区分） |
| 「讲义里能找到的是这几条，我按能找到的数目写，没有按『三条』凑」（L217） | 讲义 L242–245（4 条现象）+ L252–253 | ✅ **诚实** |
| 读可能陈旧；可接受/不可接受的情形（L221） | 讲义 L208–216 | ✅ 逐条对应 |
| sync 用来把客户端追到最新；**这一讲笔记没展开它**（L221、`zookeeper-20`） | 论文 L404–413 `issuing a write before re-reading… sync request: when followed by a read, constitutes a slow read. sync causes a server to apply all pending write requests before processing the read` | ✅ 归属对（笔记确实没展开）；措辞见 P2-3 |
| 数据必须装内存，所以不能放大文件（L229） | 讲义 L228–229 | ✅ |
| 多数派不在就不能写、选不出 leader（L237） | 论文 L415–417 `if a majority of ZooKeeper servers are active and communicating the service will be available`；讲义 L209 | ✅ |
| 设计缺口：读不是线性的、会话粗糙、或许按 znode 做 lease、很难分片、多 znode 事务（L239） | 讲义 L270–277 | ✅ 五条逐一对应 |
| 会话超时取长取短的两头代价；笔记没给答案（L241） | 讲义无 | ✅ 如实标注（`zookeeper-15` 里标了「我们加的」） |
| 版本号 vs zxid 不要混：一个是「这条路径这份数据改过几次」，一个是「集群第几个事务」（L255） | 论文/讲义分别定义 | ✅ 这是作者本轮修掉的混用，现版清楚 |
| 下一步是分布式事务/2PC/Spanner（L259） | 讲义 L279–281 | ✅ |

**事实核对小结**：**与源冲突 0 条**。**讲义与论文两个源我分别核过，行号与原文片段都粘在上面。**
作者轮次记录里记的「8 处漏讲」我现在**逐条都在页面上找到了**（watch 排序保证 L202、刻意不做锁原语 L139、临时节点不能有子节点 L141、
follower 可能延迟读 L213、临时节点删除是 A-线性操作 L162、写日志为崩溃/断电不丢已提交更新 L209、被唤醒后重新 getChildren L135、fuzzy snapshot L209）✅。

---

### 陌生读者测试（8 题）

**执行方式**：Lead 在 depth 0 spawn 全新子代理，只给 `content/09-zookeeper/index.md`（禁止读源/联网/用自身背景补）。

**⏳ 答卷状态**：**尚未发出**（我这一轮先把事实层做完；题目已备好，见下）。**这是本记录唯一的缺口**，
按 §3，本页**现在还不能算过了透镜 3**。题目（8 题）：
① 为什么直接拿 Raft 写应用很别扭、ZK 换来的是什么；② 为什么「写本机磁盘」不行、「只复制存储」还缺什么；
③ 写为什么必须排成全序、一次写怎么走完；④ 读为什么可能是旧的、ZK 对读给的**逐客户端**保证是什么、A-linearizability 与教科书线性一致差在哪；
⑤ 用临时顺序节点做锁为什么要「只监视前一个」（惊群）；⑥ 会话判死时为什么要**原子地**做两件事、第二件事挡住的是什么；
⑦ watch 为什么要重读、为什么「先通知后新状态」这条保证是重读能成立的前提；⑧ 跨多个 znode 的更新为什么不是事务、三种绕法的共同点是什么。

---

### 附录二 / 附录十 专项

**（一）附录二（标记必须落到图内可见文字 + alt）—— 本页达标**

| 属于我们的内容 | 正文本标 | 图内可见文字 | `desc` | `alt` | 判定 |
| --- | --- | --- | --- | --- | --- |
| fencing token 那一层是我们的补白 | L166 | ✅ `zookeeper-18`「一个单调递增的编号（**我们补的**）」 | ✅ 整句说明 | ✅ L180 | ✅ |
| 「会话超时取长这一段谁来服务」是我们的判断 | L241 | ✅ `zookeeper-15`「这段谁来服务没答案（**我们加的**）」 | ✅ | ✅ L245 | ✅ |
| 「写本机磁盘」这一档是我们补的对照 | L42 | ✅ `zookeeper-5` 的 `desc` 明写 | ✅ | ✅ L52 | ✅ |
| primary-backup 类比、读得见自己的写是**无条件**的 | L58/L215 | ✅ `zookeeper-13`「无条件：跟不上就延迟这次读」 | ✅ | ✅ L213 | ✅ |

**（二）附录十 —— 本项目历史上点名的三处缺陷，**这一版全部已闭合**（我按属性原文逐条核过）**

1. **`zookeeper-5` 的列对齐**（`附录十` 里"上排四格方案／下排四格难点被读成一一对应"那一例）：现版上排是**三格**（`x=134 / 380 / 626`），
   下排四个难点改成 **2×2** 块（`x=388.5 / 617.5`，两行 `y=220 / 282`），并加了说明「下面这四件事，任何一条写错方案就失效」。
   ⇒ **不再构成一一对应的暗示**，且用文字把归属说清了 ✅。
2. **`zookeeper-1` 的正文/图口径相反**（正文说普通与临时互斥、图上只写"可叠加"）：现版最后一行
   `T17 "普通与临时互斥；临时 + 顺序 = 会排队的成员"` ⇒ **图与正文口径一致** ✅（属性原文：
   `<text x="567" y="347" font-size="12" text-anchor="middle" fill="#166534">普通与临时互斥；临时 + 顺序 = 会排队的成员</text>`）。
3. **`zookeeper-13` 的「并列断言因果」**（原来"同一台读完 → 看得见自己的写"与"换台读 → 可能旧"并列，读者会把前者归因给"同一台"）：
   现版 `T06/T07` 写「读得见自己的写 / **无条件**：跟不上就延迟这次读」、`T08/T09` 写「落后的副本仍可能旧 / 但换台读位置也不倒退」，
   与讲义 L220–223（`a client read sees all of its own previous writes… so follower may have to delay a read` / `even if client switches ZK followers!`）同向 ✅。

**（三）几何类（附录十一）**：本页无「看起来偏了/更宽」类主张；上面三条结论我都附了属性原文，未做渲染量墨迹。

---

### 一致性 / 可读性 / 诚实性

- **一致性（透镜 4）**：与 `03-gfs`（checksum 校验的读）、`04-paxos`/`papers-raft`（多数派、leader、日志全序）的口径一致 ✅；
  本页内部「版本号 vs zxid」已明确拆开（L255）✅；`zookeeper-13` 与 L215 的「无条件」表述一致 ✅。
- **可读性（透镜 5）**：本次**没有重跑** `audit_content.py`。人读一遍：L217（性能那一大段）最长、数字最密，
  但它自己写了「我按能找到的数目写，没有按『三条』凑」，读者知道自己在读什么。**机检指标属"未验"。**
- **诚实性（透镜 6）**：**做得好**：L42/L166/L241 三处主动标明是我们补的，其中两处还落进了图；
  L217 拒绝为凑数而编；L221/L241 主动写「笔记没有展开」「笔记没有给答案」；L162 把「讲义专门标注了这一点」的归属说清。

### 本次覆盖面（附录十二）

- 已验：讲义 **287 行**与论文 **1473 行**两个源分别逐段对照（行号 + 原文片段都粘贴在本记录里）；
  14 张图的 `title`/`desc`/图内文字与正文 `alt` 逐张比对；`zookeeper-5/-1/-13` 三处历史缺陷按属性原文核闭合。
- **未验**：① 机检指标；② 渲染量墨迹；③ **透镜 3（答卷未发出）**。

---

### 结论

**P0 0 项、P1 0 项、P2 3 项 → 事实层已清；但按 §3 / §9，本页在「陌生读者测试」回执之前不应提 `reviewed`。**

#### P0 · 0 项　　P1 · 0 项

#### P2 · 3 项（都属"归属措辞"，不阻塞）

1. **P2-1**：L81 把「ACL、时间戳、子节点列表」一起说成「**论文把这些一起算作 znode 的元数据**」。
   我在这份论文抽文里**没有定位到这句归总**（只找到：`setDataTXN` 带 updated timestamps @37482、Figure 7 提到 `ACL checks` @51794、`getChildren` 返回子节点名 @14590）。
   这些字段确实存在（ZooKeeper 的 `Stat` 结构就含它们，讲义 L283 引的就是官方 API 文档），所以**内容不错、归属待定**。
   → 建议改成「API 的 `Stat` 结构里有这些字段」，或补出处。
2. **P2-2**：L139 用引号写了「**放弃了在服务端实现具体原语**」。论文原话是
   `a coordination kernel that enables new primitives without requiring changes to the service core`（@2971），
   我**没能定位到与引号内文字一致的原句**。→ 建议把引号改成意译，或把出处贴到句尾（同段的「不是一个锁服务」是逐字可核的 ✅）。
3. **P2-3**：L221 把 `sync` 说成「把客户端**追到 leader 的最新状态**」；论文的措辞是
   `sync causes a server to apply all pending write requests before processing the read`（L411–413，服务器是**客户端所连的那台**，论文同时称它"一次慢读"）。
   效果上等价，但主体不同。→ 建议改成「让所连服务器把它之前挂起的写都应用完」（顺带把论文那句「一次慢读」写进正文，`zookeeper-20` 的 `desc` 已经写了 ✅）。

#### 已核不出问题（记录在案，供下一个复核者直接关闭）

- **作者轮次记录里的「8 处漏讲」在这一版全部落地**（逐条列在事实表里），其中包括最容易漏的两条：
  「临时节点不能有子节点」（论文 @9742 逐字可核）与「通知的排序保证：先看到通知、再看到新状态」（论文 L387–390 逐字可核）。
- **两处曾被点名的问题已修**：`fencing token` 现在明确标为我们的补白（图内 + `desc` + 正文三处），
  znode 版本号与 zxid 现在明确拆开（L255）。
- `zookeeper-5` / `zookeeper-1` / `zookeeper-13` 三处历史配图缺陷**已闭合**（属性原文见上）。

---

**审校人声明**：本记录只覆盖开头那个哈希的版本。按附录五，对其它版本的结论不成立 ——
**尤其因为这一页在我开工时仍在被编辑**（最后一次写入 23:28:53）：若作者此后又改动本页，
**本记录的行号与结论必须重核**，至少重跑一遍陌生读者测试。
本记录不修改任何正文或图，`status` 字段由 Lead 处理。
