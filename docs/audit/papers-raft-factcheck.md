## papers/raft 质量审核 · 2026-09-28 · 审校人 mit65840-reviewer · 作者 mit65840-author

> 审校人**不是**本讲作者。本记录只写结论，不改正文与图。

### 核对基线（附录十三：先做行尾归一化再算哈希）

| 对象 | 归一化 SHA256 | 字节 |
| --- | --- | --- |
| `content/papers/raft/index.md` | `B375F38FE785F38F14F25F6C51496E9B9B58BF04D044D434F79FEBCAFE0A7487`（全 64 位） | 29073 |
| 论文（**扩展版**，页面 L11 明说课程用的就是扩展版） | `2E1DFE10C8CBF03EE536F933B108C19FFD655B21AA3D2DEF0BA258C6B0642EC4` | 原始 94099 / 归一化 92229 |
| 讲义 LEC 6（RSM and Raft (1)） | `8BC18871653E77CFC84E76A470946890ACFFEA8040D84DC5D1E163AE1A54BEF8` | 8935 |
| 讲义 LEC 7（Raft (2)） | `7CE04209E2215957AF34137DC2D5FC507781A74F4EA44E2B89C428CBF52E3566` | 15520 |

> **可核范围**：论文正文与两份讲义都在工作区（我读的是 PDF 抽文 `_tmp` 文本，逐条引原文片段；
> 抽文有 `ﬁ` 连字与 `T ak` 这类缺陷，不影响数字与句意）。页面标题写明用的是**扩展版**，我核的也是扩展版，**版本一致**。

11 张图（前 16 位）：`raft-1 1FC3DED3B2ED4672` · `raft-2 474C27FC9ED507FB` · `raft-4 16562D37A573F7F1` ·
`raft-5 79028ADCBB2D30A9` · `raft-6 CA467702D63C40FE` · `raft-7 746757FC823E089B` · `raft-8 1C1C0D44AAA41298` ·
`raft-12 F84E1406C6E60157` · `raft-13 07D11674BABA380D` · `raft-14 033CF76605AA5229` · `raft-15 7A1B580EDDE637DE`

---

### 事实核对

「论文」引原文片段（扩展版）。**本页含大量数字，我逐个回源核过，全部一致。**

| 声明（页面位置） | 源 | 结果 |
| --- | --- | --- |
| Paxos 缺口一：单值内核「两个阶段没有直观解释、也无法独立理解」（L26） | 论文 §1：`Single-decree Paxos is dense and subtle: it is divided into two stages that do not have simple intuitive explanations and cannot be understood independently` | ✅ 逐字对应 |
| Paxos 缺口二：没有公认的多决策版本，各系统各自演化（L26） | §1：`there is no widely agreed-upon algorithm for multi-Paxos… several attempts… these differ from each other and from Lamport's sketches` | ✅ |
| 「最后变成『以一份没被证明过的协议为基础』」（L26） | §1 引 **Chubby 实现者的话**：`the final system will be based on an unproven protocol` | ✅ 内容对；**这是论文引用的他人原话**，页面未点明"引语"→ P2-1 |
| 「Paxos 的描述与真实系统的需求之间存在明显的鸿沟」（L26） | 同一处引语：`There are significant gaps between the description of the Paxos algorithm and the needs of a real-world system` | ✅ |
| 两个可操作手法：问题分解 + 状态空间缩减（L34） | §1（`decomposition` / `state space reduction`） | ✅ |
| 用户研究：斯坦福 + 伯克利两门课、**43 名学生**（L36） | §6.2：`an Advanced… course at Stanford University and a Distributed Computing course at U.C. Berkeley`；`A user study with 43 students` | ✅ **两所学校与人数都对** |
| Raft 平均 **25.7** 分（满分 60）、Paxos **20.8** 分、**33** 人在 Raft 上更高（L36） | §6.2：`the mean Raft score was 25.7 and the mean Paxos score was 20.8`；`33 of these students were able to answer questions about Raft better` | ✅ 三个数字全对 |
| 两条对 Paxos 有利的保留：**15 人**此前接触过 Paxos、Paxos 录像长 **14%**（L38） | §6.2：`15 of the 43 participants reported having some prior experience with Paxos, and the Paxos video is 14% longer` | ✅ |
| 配对 t 检验：95% 置信区间下界「Raft 至少高 **2.5** 分」（L38） | §6.2：`with 95% confidence, the true distribution of Raft scores has a mean at least 2.5 points larger` | ✅ |
| 回归摊平后预测差距 **12.5** 分，比实测 **4.9** 分更大，且作者给出解释（L38） | §6.2：`The model predicts that the choice of quiz produces a 12.5-point difference in favor of Raft. This is significantly higher than the observed difference of 4.9 points, because many of the actual students had prior Paxos experience` | ✅ 数字与解释都对 |
| 「先做 Paxos 题再做 Raft 题的人，在 Raft 那道题上低 **6.3** 分」，且作者不知道为什么（L38） | §6.2：`the model also predicts scores 6.3 points lower on Raft for people that have already taken the Paxos quiz; although we don't know why` | ✅ **方向正确**（低的是"先做 Paxos"那组在 Raft 卷上的分） |
| 拆成三块：领导者选举 / 日志复制 / 安全性（L46） | §1 与 §5–§7 | ✅ |
| 强领导者：日志只从领导者单向流出（L54） | 摘要：`Strong leader: Raft uses a stronger form of leadership… log entries only flow from the leader to other servers` | ✅ |
| 「Raft 只保证**每个任期**最多一个领导者（论文专门限定在给定任期上）」（L54/L74） | Figure 3 `Election Safety: at most one leader can be elected in a given term. §5.2` | ✅ 措辞与论文一致 |
| 任期充当逻辑时钟、识别过期领导者、不依赖物理时钟（L74） | §5.1：`Terms act as a logical clock… they allow servers to detect obsolete information such as stale leaders` | ✅ |
| 三种状态、五节点容忍两台（L66） | §5.1 | ✅ |
| 三个时间尺度：广播时间 ≪ 选举超时 ≪ 单机 MTBF（L76） | §5.6 timing requirements | ✅ |
| 选举超时随机化；作者原本设计过**排位规则**、每次修补又冒新角落情况、最后判定随机重试更好懂（L62/L76） | §9（原文：`Initially we planned to use a ranking system… after each adjustment new corner cases appeared. Eventually we concluded that the randomized retry approach is more obvious and understandable`） | ✅ **逐句对应**（这条是很多人会漏的细节） |
| 提交：多数派复制**且**条目属于当前任期；旧条目可能被覆盖（L78/L86/L92） | §5.3 + §5.4.2（Figure 8 的四步场景） | ✅ 方向与限定都对 |
| 领导者把最高已提交位置带在后续请求（含心跳）里（L78） | §5.3 | ✅ |
| 日志匹配靠一致性检查归纳维持；拒绝则退一格；新领导者不需要专门修复流程（L88） | §5.3 | ✅ |
| 选举限制：比较方式＝先看最后条目任期、任期相同则更长者更新（L90） | §5.4.1 原文 | ✅ |
| 「若允许领导者改写自己的日志，就必须把缺失的已提交条目传送给新领导者，那正是其他算法…的复杂度」；与 Viewstamped Replication 的区别（L90） | §5.4：`In some consensus algorithms, such as Viewstamped Replication, a leader can be elected even if it doesn't initially contain all of the committed entries. These algorithms contain additional mechanisms to identify the missing entries and transmit them to the new leader` | ✅ **连"哪一类算法"都点名正确** |
| 领导者可安全断定更老条目已提交的一些情形，论文为简单没这么做（L92） | §5.4.2 讨论段 | ✅ |
| 提交点"找一致点"朴素实现一次退一格很浪费、真实系统按任期跳着退（L102） | §5.3（含按任期的优化） | ✅ |
| 成员变更：不存在同时切换；必须联合共识；投票与提交要两套配置各自多数派；三处细节（非投票成员／提交后退位／压住被移出节点的拉票）（L104） | §6（含 `joint consensus`、non-voting、step down、ignore RequestVote within minimum election timeout） | ✅ 五条全对 |
| 快照：写状态整体 + 最后包含位置、丢弃之前日志；每个跟随者各自做快照更高效；落后太多由领导者分块传（L112） | §7 + 讲义 LEC 7（`every server snapshots (not just the leader)` / `InstallSnapshot`） | ✅ 论文与讲义分别核过 |
| 「状态机的确定性…这一段是我们的补充，论文只把它当作既成前提」（L112） | 论文只假设确定性状态机 | ✅ 已标（且落进 `raft-13` 图内可见文字） |
| 快照两个性能问题：建议写时复制、写盘与正常写入争抢带宽（L114） | §7（`copy-on-write`、`fork on Linux`） | ✅ |
| 「讲义说得更直接：对一个大的数据库来说这个做法不太好…把整个数据库造出来再写进磁盘」（L114） | 讲义 LEC 7：`Raft's snapshot scheme is reasonable if the state is small; for a big DB… not so good; slow to create and write entire DB to disk` | ✅ 归属正确（这是**讲义**的话，页面标的就是讲义） |
| 「最少消息数（领导者到半个集群一次往返）」（L122/L140） | §8/§9：`Raft achieves this using the minimal number of messages (a single round-trip from the leader to half the cluster)` | ✅ **逐字对应**；批处理与流水线也在同一段 |
| 换主停机：5ms 随机化下中位 **287ms**；选举超时压到 **12–24ms** 可降到 **35ms**（L122） | §9.6：`just 5ms of randomness… a median downtime of 287ms`；`With an election timeout of 12–24ms, it takes only 35ms` | ✅ 三个数字全对 |
| 陈旧读的来源是「已经下台却没察觉的旧领导者」（L124） | §8：`the risk of returning stale data, since the leader responding to the request might have been superseded by a newer leader of which it is unaware` | ✅ **方向正确**（这是本页历史上改过一次的方向错误，现版对） |
| 客户端请求都发领导者、跟随者拒绝并告知最新领导者地址（L66/L124） | §8：`the follower will reject the client's request and supply information about the most recent leader it has heard from` | ✅ |
| 线性一致读两条路：读也走日志 / 带时限的租约（L124） | §8：`the leader… exchange heartbeat messages with a majority… before responding to read-only requests. Alternatively… a form of lease` | ✅ |
| 租约会**让安全性重新依赖时间**（假定时钟偏移有界）（L126） | §8：`this would rely on timing for safety (it assumes bounded clock skew)` | ✅ 逐字对应 |
| 「恰好一次」要调用方给唯一序号 + 状态机去重（L128） | §8 | ✅ |
| 实现约 **2000** 行 C++；约 **25** 个第三方实现（L140） | §9：`roughly 2000 lines of C++ code`；`about 25 independent third-party open source implementations` | ✅（页面写"二十多个"＝约 25 ✅） |
| TLA+ 规格里有一部分不变式**未被机械化检查**（L142） | §9.6：`this proof relies on invariants that have not been mechanically checked` | ✅ |
| CockroachDB 是讲义给的旁证（L150） | 讲义 LEC 7：`Raft is used in CockroadDB, a sharded distributed database`（讲义拼写如此） | ✅ 归属正确 |
| 成员变更的后续简化（一次只加减一台＝联合共识特例）出自 Ongaro 学位论文（L150） | 论文正文无 | ✅ 已标出处是学位论文，不是这篇 |
| 「只读索引一类优化是我们补的」（L150）；「跨分片事务论文没有讨论」（L136/L150） | 论文无 | ✅ 已标 |
| 「与 Paxos 故障模型相同」「论文没有并排比较」（L52/L62/L166） | 论文未并排比较 | ✅ 三处都标了；**且 `raft-6` 把它写进了图内可见文字** |

**事实核对小结**：与源**冲突 0 条**；数字 **全部**一致（我逐个回源）；源未提及但已正确标为我们的 4 处。

---

### 陌生读者测试（8 题）

**执行方式**：Lead 在 depth 0 spawn 的全新子代理，只给 `content/papers/raft/index.md`，禁止读源/联网/用自身背景补；
自证「我本轮读过的文件：content\papers\raft\index.md」。

**结果：✅ 7 　⚠️ 1 　❌ 0**（⚠️ 12.5% ≤ 40%，❌ 0% ⇒ **不触发 §3 的比例阈值**）

- ⚠️ **Q1「Raft 为什么只保证每个任期最多一个领导者，而不是全局最多一个」** —— 读者写：
  > 「后半两问（任期的逻辑时钟作用、不依赖物理时钟的原因）有原句，但『**为什么不要求全局最多一个领导者**』页面只说了限定在给定任期，**没有给出理由**。」
  **我判这条成立**（页面 L54 给了"果"、L74 给了机制，但没给"为什么全局那条断言不了"）。
  **它不构成 P1**（比例未触发），处理为 **P2-2**；但**修法必须有源**（Lead 特别提醒不要自编因果）——
  论文里现成的依据是 §5.1 的一句：`Different servers may observe the transitions between terms at different times, and in some situations a server may not observe an election or even entire terms`
  以及 §5.2 的机制句 `Each server will vote for at most one candidate in a given term… The majority rule ensures that at most one candidate can win the election for a particular term`。

---

### 附录二 / 附录十 专项

**（一）附录二（标记必须落到图内可见文字 + alt）—— 本页做得好**

| 属于"我们的"内容 | 正文标记 | 图内可见文字 | `desc` | `alt` | 判定 |
| --- | --- | --- | --- | --- | --- |
| 「故障模型与 Paxos 相同」是我们的归纳 | L52/L62/L166 | ✅ `raft-6` 页脚「（与 Paxos 相同这一步是我们的归纳，论文未并排比较）」 | ✅ | ✅ L50 | ✅ |
| 状态机确定性那一层是我们的补充 | L112 | ✅ `raft-13` 面板「（下排是我们的补充）」 | ✅ | ✅ L118 | ✅ |
| 分片、只读索引、跨分片事务是后续工作/我们的补充 | L136/L150 | ✅ `raft-14` 下排「把键空间切成许多复制组…」 | ✅ | ✅ L134/L146 | ✅ |

**（二）附录十（文字没说的事，图不许说）**

- ✅ `raft-1` 的三个时间尺度用**三个并列框**表达"依次放大"，图内文字各自写明「（最短）／（居中）／（最长）」⇒ 归属与序关系都由文字说出，不是靠排版暗示 ✅。
- ✅ `raft-6` 的三块并列是论文自己的分解，不是排版额外断言的关系 ✅。
- ✅ `raft-8` 三排分别讲三件事，各有行标题（前缀检查／多数派相交／旧任期陷阱），未暗示跨排的一一对应 ✅。
- ✅ `raft-15` 的「放弃／做到／接受」用**列标题**写明（"放弃少数派一侧的可用性" / "写延迟做到下界" / "接受单集群的写吞吐上限"），不是靠颜色暗示 ✅。

**（三）几何类（附录十一）**：本页无"看起来偏了/更宽"类主张，未做渲染量墨迹。

---

### 一致性 / 可读性 / 诚实性

- **一致性（透镜 4）**：
  - 与 `04-paxos` 的口径：两页都写「Paxos 那类对称内核只适合单个决定、真实系统要一串决定」✅ 同向；
    04 讲 L200 的「ZAB 与 Raft 都不是 Paxos 的直接实例」与本页 L166「两者面对同样的故障模型、回答同一个问题，区别在入口」✅ 不冲突。
  - 与 `03-gfs`：L122「只有多数派可达才能推进」与 03 的多数派口径一致 ✅。
  - 本页内部：L140「写延迟这条它没有放弃，反而做到了下界」与 `raft-15` 图内「写延迟做到下界」✅ 一致（这是本页历史上改过的方向错误，现版已同向）。
- **可读性（透镜 5）**：本次**没有重跑** `audit_content.py`。人读一遍：L26、L62、L92、L104 四段很长（尤其 L104 的成员变更五件事挤在一段），
  但每段都有明确的问题句开头，读得下去。**机检指标属"未验"。**
- **诚实性（透镜 6）**：**做得很好**：L52/L112/L136/L142/L150 五处主动标注归属与未展开处，
  L150 甚至写明「至于它是否推动了社区跟进，论文没有说，我们也不下这个结论」。**唯一未标的**是 L26 的引语性质（P2-1）。

### 本次覆盖面（附录十二）

- 已验：全部具体数字（43/33/25.7/20.8/15/14%/2.5/12.5/4.9/6.3/287/35/12–24/2000/25）；
  论文 §1/§5.1/§5.2/§5.3/§5.4.1/§5.4.2/§6/§7/§8/§9 的对应原文片段逐条粘贴核对；两份讲义（LEC 6/7）分别核了快照与 CockroachDB 两处归属；
  11 张图的 `title`/`desc`/图内文字与正文 `alt` 逐张比对。
- **未验**：① 机检指标；② 渲染量墨迹；③ 论文抽文本身的准确性（我用的是工作区已有的 PDF 抽文，不是 PDF 原件）。

---

### 结论

**P0 0 项、P1 0 项、P2 3 项 → 修完 P2 的建议项后即可提 `reviewed`（本讲无必修项）。**

#### P0 · 0 项　　P1 · 0 项

#### P2 · 3 项（记录在案，不阻塞）

1. **P2-1**：L26 的「以一份没被证明过的协议为基础」是**论文引用的 Chubby 实现者原话**（论文 §1 明写 `The following comment from the Chubby implementers is typical`），
   页面没点明这是引语。建议加「论文引用 Chubby 实现者的话」。
2. **P2-2（透镜 3 的那条 ⚠️）**：L54/L74 给了"每个任期最多一个领导者"与任期的机制，但没给"为什么不能断言全局最多一个"。
   **修法（必须有源，别自编）**：用论文 §5.1 原句补一句——
   「不同节点可能在不同时刻才观察到任期切换，有些节点甚至整段任期都没观察到（论文 §5.1），
   所以能断言的是『**给定任期**最多一个』：它由『每台机器在同一任期内只投一票』＋多数派共同推出（§5.2）。」
3. **P2-3**：持久化（`currentTerm` / `votedFor` 必须先落盘再应答）只在末段 L168 一带而过，正文没讲它为什么是安全性的前提。
   这是 Lab 3B 的常见坑。建议在"任期与逻辑时钟"一节补一句（论文 §5.2／§5.4 有据）。

#### 已核不出问题（记录在案，供下一个复核者直接关闭）

- **本页所有数字都与论文一致**，包括最容易被记错的 25.7/20.8/33/15/14%/2.5/12.5/4.9/6.3（用户研究那一组）与 287/35/12–24（换主停机那一组）。
  尤其 **6.3 的方向**（"先做 Paxos 题"的人在 Raft 卷上更低）与论文一致。
- L90 把「允许领导者改写日志 ⇒ 必须传送缺失条目」归给「Viewstamped Replication 一类算法」，与论文 §5.4 点名的算法**完全一致**。
- L114 的「讲义说得更直接…」归属正确（那句话确实在 LEC 7 讲义里，不在论文里）——**跨材料的归属没有搞混**。
- `raft-6` 是三页里**唯一把"我们的归纳"写进图内可见文字的图**，可作为 `01-introduction` P1-4 的样板。

---

**审校人声明**：本记录只覆盖上表列出的基线版本。按附录五，对其它版本的结论不成立。
透镜 3 答卷已回：✅7 / ⚠️1 / ❌0。本记录不修改任何正文或图，`status` 字段由 Lead 处理。
