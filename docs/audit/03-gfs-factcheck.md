## 03-gfs 质量审核 · 2026-09-28 · 审校人 mit65840-reviewer · 作者 mit65840-author

> 审校人**不是**本讲作者。本记录只写结论，不改正文与图。

### 核对基线（附录十三：先做行尾归一化 `read_bytes().replace(b"\r\n", b"\n")` 再算 SHA256）

| 对象 | 归一化 SHA256 | 字节 |
| --- | --- | --- |
| `content/03-gfs/index.md` | `4D9E46EB16D1603C31E3E43A6BB7F6C585C0ADC56EEB727A6192CFA86FF09961`（全 64 位） | 40298 |
| 源 `_fc/l-gfs.txt`（351 行讲义） | `9D0B8DCF7320D37C7013EEE5264BDA1AAA28D735149EFC5D304D496105FEE2AF`（全 64 位） | 14912 |
| 旁证 GFS 论文全文（我对论文逐条核时用的文本） | `0D645F6017A75B03EDE41A34F0FB4881E17DDF4D18873E2F1DB37E5BEBCC5F7A` | 原始 93373 / 归一化 91504 |

> **论文文本的来源与效力，先如实交代**：`_fc/` 里没有论文正文，我用的是工作区里已有的一份 PDF 抽文
> `_chk/gfs.txt`（1870 行，带 PAGE 分隔与少量 PDF 抽字瑕疵，例如 `T ak Leung`、`notiﬁed`）。
> 它**不是**我生成的，我只核对了内容与论文 §编号自洽（见下表 §6.2.3/6.2.4 一栏）。凡我据它下的判断，
> 本记录都写出**§编号 + 原文片段**，可被独立复核；若它本身有错，错会体现在"论文说"那一列，请以 PDF 为准。

19 张图（哈希取前 16 位，沿用本项目 `check_reviewed.py` 的惯例）：
`gfs-1 585C600B03EE753F` · `gfs-2 251D81D19EB8DEEC` · `gfs-4 9C86982BC81C4558` · `gfs-5 5B6C815613FB18BF` ·
`gfs-6 0C07439F5EDD59E5` · `gfs-7 C8DBF70DD3CCD3C5` · `gfs-8 FA7B0D48AA2FF7B1` · `gfs-10 98EDDC4FA9894B14` ·
`gfs-12 F2F0E993AD9F2EAE` · `gfs-14 01B84E8285709214` · `gfs-15 2469B6049A8B24B3` · `gfs-16 17EFCE35724A62AB` ·
`gfs-17 7F4AE9E506362B53` · `gfs-22 5B54803CBC92BC20` · `gfs-27 A9D0F57A8234F3A5` · `gfs-28 CD7F99A571650E31` ·
`gfs-29 4485CEEFDF1B788C` · `gfs-30 FBCFEB3237B89103` · `gfs-31 18F2E1FA0B865918`

---

### 事实核对

「讲义」= `_fc/l-gfs.txt`（行号照抄）；「论文」= 'The Google File System'（引 §号 + 原文片段）。
**凡页面自己指出「这是我们的补充/推断」的地方，我把它当归属来核（是否有据、标记是否落地）。**

| 声明（页面位置） | 源 | 结果 |
| --- | --- | --- |
| 「几百 TB」数据／几百客户端（L23、L25） | 论文摘要：`provides hundreds of terabytes of storage across thousands of disks on over a thousand machines, and it is concurrently accessed by hundreds of clients` | ✅ 数字对；把「集群容量」说成「数据量」见 P2-1 |
| 论文第二章列了**六条**设计假设（L37） | 论文 §2.1 恰为 **6 条** bullet（原文逐一核对：故障常态／少数大文件／两种读／追加为主／并发追加与原子性／带宽优先于延迟） | ✅ 数目与内容全对 |
| 「文件数量不算多…预期几百万个文件，单个通常 100MB 以上，多 GB 是常态」（L41） | 论文 §2.1 `a few million files, each typically 100 MB or larger. Multi-GB files are the common case` | ✅ |
| 「大流式读几百 KB，1MB 以上更常见；小随机读几 KB；应用会批量化排序」（L42） | 论文 §2.1（逐句对应，含 `batch and sort their small reads`） | ✅ |
| 「写主要是追加…任意位置的小写要支持但不高效」（L43） | 论文 §2.1 | ✅ |
| 「同一个文件被多个客户端并发追加（队列/多路归并），原子性与最小同步开销」（L44） | 论文 §2.1 | ✅ |
| 「持续高吞吐比低延迟重要」（L45） | 论文 §2.1 第 6 条 | ✅ |
| 64MB 块、块句柄是"主节点在创建时分配的、**不可变的**、全局唯一 64 位"（L57） | 论文 §2.3 `identified by an immutable and globally unique 64 bit chunk handle assigned by the master at the time of chunk creation` | ✅ 连"不可变的"都是论文原词 |
| 默认三副本；用户可对不同命名空间区域指定副本级别（L57） | 论文 §2.3 `By default, we store three replicas, though users can designate different replication levels for different regions of the file namespace` | ✅ |
| 三类元数据；前两类落操作日志、改动可见前先刷本地与远程磁盘、配周期性检查点（L65） | 论文 §2.6.3；§5.1.3 `A mutation to the state is considered committed only after its log record has been flushed to disk locally and on all master replicas` | ✅ |
| 第三类（块位置）刻意不持久化，启动时与块服务器加入时直接问它（L65/L67） | 论文 §2.6.2 + 讲义 L248–249 | ✅ 两个源同向 |
| 每块元数据不到 64 字节（L75） | 论文 §2.6.1 `maintains less than 64 bytes of metadata for each 64 MB chunk` | ✅ |
| 全内存 ⇒ 主节点快 + 有余力后台扫描（GC／再复制／迁移）（L75） | 论文 §2.6.1 `master operations are fast… periodically scan through its entire state in the background` + §4.4 | ✅ |
| 客户端问多个块，主节点顺带返回后面几块的位置（L77） | 论文 §2.3 | ✅ |
| 客户端缓存键是"文件名 + 块下标"（L77） | 论文 §2.3 `caches this information using the file name and chunk index as the key` | ✅ |
| 「把一个多 TB 工作集的块位置全部缓存下来」（L97） | 论文 §2.5 `comfortably cache all the chunk location information for a multi-TB working set` | ✅ |
| 「主节点分布化＝掉进 consensus 问题，这条论文没有比较」（L81） | 论文无 | ✅ 已标为我们的推断 |
| HDFS（NameNode/DataNode）与 Ceph（CRUSH、MON、MDS）对比（L83） | 源无 | ✅ 已标为我们的补充；两处外部描述我也复核过，无误 |
| 1GB／64MB＝16 次、1GB／4KB≈26 万次（L87–L91） | 论文只给 64MB；四则运算 | ✅ 已标「4KB 那一栏是我们为对比加的假设」 |
| 「论文只说比典型文件系统的块大得多，没有给出倍数」（L93） | 论文 §2.1 `chosen 64 MB, which is much larger than typical file system block sizes`；全文搜 `4 KB`/`4KB` 无块大小对比 | ✅ 这是对**否定性**声明做的检索核对 |
| 「副本按需增长、延迟分配，内部碎片并不存在；论文特意点出」（L93） | 论文 §2.1 `extended only as needed. Lazy space allocation avoids wasting space due to internal fragmentation` | ✅ |
| 块大三好处（交互次数／网络开销／元数据小）（L97–L99） | 论文 §2.5 三条 `First/Second/Third` | ✅ 三条逐一对应 |
| 热点事故：单块可执行文件被上百台同时启动、压垮少数块服务器、两条修法（L109） | 论文 §2.5 `an executable was written to GFS as a single-chunk file and then started on hundreds of machines at the same time… We fixed this problem by storing such executables with a higher replication factor and by making the batch-queue system stagger application start times` | ✅ |
| 「论文在这一节只记下热点这一条代价」（L111） | 论文 §2.5 的 disadvantages 段只列 hotspot（`a large chunk size, even with lazy space allocation, has its disadvantages` 后只讲 hot spot） | ✅ |
| 「另外两条代价（尾部延迟、调度粒度）是我们补的」（L111/L113/L115/L117、L296） | 论文无 | ✅ **且已落进图内可见文字**："另外两条代价不在磁盘上（**这两条是我们的补充**）"（`gfs-8` 面板标题） |
| 副本产生的三种原因（创建／再复制／再均衡）（L121） | 论文 §4.3 | ✅ |
| 放置时挑机器的三条考虑（低于平均使用率／限制最近创建的块数／跨机架分散）（L121） | 论文 §4.3 | ✅ |
| 再复制触发原因四条；「不会一发现就动手」（L125） | 论文 §4.3 | ✅ |
| 80GB 磁盘按 10MB/s 铺满要"一两个小时"（L127） | 讲义 L202 `80 GB disk, 10 MB/s network -> an hour or two for full copy` | ✅ 与讲义同（80GB/10MB/s≈2.2h） |
| 再复制优先级：丢两个副本的更急；挡住客户端读写的排前面；存活文件的块排在已删除文件前（L127） | 论文 §4.3 `we prefer to first re-replicate chunks for live files as opposed to chunks that belong to recently deleted files. Finally… we boost the priority of any chunk that is blocking client progress` | ✅ 三条全对（我按"优先级"逐条搜到原文） |
| 失效检测：讲义是"定期 ping、超时就认为挂了（讲义 195 行）"；论文是 heartbeat（L135） | 讲义 L194–196；论文 §2.7.1 `identifies failed chunkservers by regular handshakes` | ✅ **两个源分别标注、且都对** |
| 判定后的三个动作（移出副本列表／记缺失走等待再排队／告诉主副本新次副本列表）（L135） | 讲义 L196–198 | ✅ |
| 它持有的租约不会立刻另发，要等旧租约到期（L135） | 讲义 L213–215；论文 §3.1 `can safely grant a new lease to another replica after the old lease expires` | ✅ 两源同向 |
| 版本号：授租约时加一、通知最新副本、写进持久状态、在通知客户端之前完成（L137） | 论文 §4.5 `Whenever the master grants a new lease… increases the chunk version number and informs the up-to-date replicas. The master and these replicas all record the new version number in their persistent state. This occurs before any client is notified` | ✅ 逐句对应 |
| 联系不上的副本不被推进；重启自报时被认出；GC 清掉、之前当它不存在（不派修改、不告诉客户端）（L137） | 论文 §4.5；§2.7.1 `Stale replicas will never be involved in a mutation or given to clients asking the master for chunk locations` | ✅ |
| 「报上来的版本号比记录的大 ⇒ 认为当初授租约那一步是自己失败，以较大的为准」（L137） | 论文 §4.5 `the master assumes that it failed when granting the lease and so takes the higher version to be up-to-date` | ✅ |
| 校验和：每块切 64KB 小块、每小块 32 位、与用户数据分开存放（内存 + 随日志持久化）（L141） | 论文 §5.2 `A chunk is broken up into 64 KB blocks. Each has a corresponding 32 bit checksum. Like other metadata, checksums are kept in memory and stored persistently with logging, separate from user data` | ✅ 逐句对应 |
| 读时先验证；不匹配就报错并上报主节点、请求方改读别的副本、主节点克隆修回、最后让报错的机器删掉坏副本（L141） | 论文 §5.2 | ✅ |
| 「多数读至少覆盖好几个校验小块」；追加写的校验和增量更新；空闲时后台扫描不常读的块（L141） | 论文 §5.2（`most of our reads span at least a few blocks` / `incrementally update` / `During idle periods, chunkservers can scan and verify the contents of inactive chunks`） | ✅ 三条全对 |
| 「不是所有副本在几分钟内一起消失就能恢复；全丢了是"不可用"而不是"读到坏数据"」（L149） | 论文 §2.7.1 `A chunk is lost irreversibly only if all its replicas are lost before GFS can react, typically within minutes. Even in this case, it becomes unavailable, not corrupted` | ✅ 连"几分钟"都是论文原话 |
| 主节点恢复两条策略（重启读盘／备份协调者）（讲义 236–243 行）（L151） | 讲义 L236–243 | ✅ 行号指得准 |
| 重启后必须先等一个租约时长才能指定新主副本（讲义 250–251 行）（L151） | 讲义 L250–251 | ✅ |
| 影子主节点：读操作日志副本、应用同样改动、滞后零点几秒、提高只读可用性、只提供读（L151） | 论文 §5.1.3 `shadow masters provide read-only access… may lag the primary slightly, typically fractions of a second… enhance read availability for files that are not being actively mutated…` | ✅ |
| 「主节点那一路的接管，论文交给 GFS 之外的监控设施另起一个新主进程」（L151） | 论文 §5.1.3 `monitoring infrastructure outside GFS starts a new master process elsewhere with the replicated operation log` | ✅ **核对重点：讲义 L253–254 写"论文没说"，指的是"谁判定协调者已死"；论文确实说了"谁起新主进程"。页面没有把两件事混起来。** |
| 「真实可能滞后的是目录内容、访问控制这类元数据」（L151） | 论文 §5.1.3 `since file content is read from chunkservers, applications do not observe stale file content. What could be stale… is file metadata, like directory contents or access control information` | ✅ |
| 「一致」＝所有客户端读哪个副本都一样；「已定义」＝一致且能看到整次修改（L157–L158） | 论文 §2.7.1 定义原文 | ✅ |
| 三档：串行成功＝已定义；并发成功＝一致但未定义；失败＝不一致也未定义（L160） | 论文 §2.7.1（含 "mingled fragments from multiple mutations"） | ✅ |
| 命名空间操作原子：只由主节点处理、加锁、操作日志给出全局全序（L160） | 论文 §2.7.1 `handled exclusively by the master: namespace locking guarantees atomicity… the master's operation log defines a global total order` | ✅ |
| 失败写的形态：可能已在主副本与任意子集次副本成功；若在主副本就失败则不会被分配序号（论文 §3.1）（L162） | 论文 §3.1 `the write may have succeeded at the primary and an arbitrary subset of the secondary replicas. (If it had failed at the primary, it would not have been assigned a serial number and forwarded.)` | ✅ §号与内容都对（原文是 serial number，页面写"序号"） |
| 普通写丢数据的 [a y] 例子、客户端只收到一次成功（L170） | 讲义 L121–128（C1 写 x/y、C2 写 a/b ⇒ `[a y]`，x 与 b 丢失） | ✅ 与讲义同（这是讲义的例子，不是论文的例子） |
| 记录追加：客户端只给数据、GFS 自选偏移、至少一次原子追加、返回偏移（L178） | 论文 §3.3 `appends it to the file at least once atomically… at an offset of GFS's choosing and returns that offset… O_APPEND… without the race conditions` | ✅ |
| 某副本失败客户端重试 ⇒ 不同副本可能不同、可能整条或部分重复；不保证逐字节相同、只保证至少写一次（L180） | 论文 §3.3 | ✅ |
| 返回的偏移标记已定义区域起点；两次追加之间的填充与重复落在未定义区域；**论文指出这些字节相对用户数据量可以忽略**（L184） | 论文 §2.7.1 `They occupy regions considered to be inconsistent and are typically dwarfed by the amount of user data` | ✅ |
| 块满 64MB 的边界：主副本填满到上限、次副本照做、让客户端换下一个块重试（L184） | 论文 §3.3 | ✅ |
| 单条记录限制在**块的四分之一**以内（L184） | 论文 §3.3 `restricted to be at most one-fourth of the maximum chunk size to keep worst-case fragmentation at an acceptable level` | ✅ |
| 应用三条约定（只追加／写检查点／自校验自识别）；写者写完原子改名（L194） | 论文 §2.7.2 | ✅ |
| 「主节点不必在一次写里为几十个客户端反复同步（论文没有这样写）」（L198） | 论文无 | ✅ 已标为我们的推论 |
| Kafka 对比（L200） | 源无 | ✅ 已标为我们的补充 |
| 修改的定义；每次修改在所有副本执行；租约 → 主副本定序（L204） | 论文 §3.1 首段 | ✅ |
| 全局修改顺序＝租约授予先后 + 租约内序号（L204/L208） | 论文 §3.1 `the global mutation order is defined first by the lease grant order chosen by the master, and within a lease by the serial numbers assigned by the primary` | ✅ |
| 不变量：同一块任一时刻最多一个有效租约 ⇒ 最多一个主副本；租约承担的是安全性而非省通信（L210） | 论文 §3.1 机制 + 讲义 L17 / L340 | ✅ 方向正确；**但缺一个边界条件，见 P1-1** |
| 租约初值 60 秒；一直被修改就可续期；续期搭在 heartbeat 上（L218） | 论文 §3.1 `A lease has an initial timeout of 60 seconds… extension requests and grants are piggybacked on the HeartBeat messages` | ✅ |
| 主节点可提前撤销租约（例如要改名时冻结修改）；失联就等过期再发（L218） | 论文 §3.1 `may sometimes try to revoke a lease before it expires (e.g., when the master wants to disable mutations on a file that is being renamed)` | ✅ |
| 七步写流程（L228–L234） | 论文 §3.1 Figure 2 的 7 步 | ✅ 逐步对应（数据先进 LRU 缓冲、全部 ack 后才发写请求、主副本分配连续序号并本地应用、转发次副本、次副本按同一序号、任何副本出错客户端重试） |
| 「如果没有人持有租约，主节点会挑一个副本授予租约（**这一步论文的图里没有画**）」（L228） | 论文 §3.1 第 1 步原文就写着 `If no one has a lease, the master grants one to a replica it chooses (not shown).` | ✅ **页面的括注与论文的 "(not shown)" 完全一致** |
| 链式而不用树形：每台上行带宽服务单一接收方而非切分（L244） | 论文 §3.2 `each machine's full outbound bandwidth is used to transfer the data as fast as possible rather than divided among multiple recipients` | ✅ |
| 「最近」是拿 IP 估出的拓扑距离（L244） | 论文 §3.2 `"distances" can be accurately estimated from IP addresses` | ✅ |
| 流水线：收到一部分就立刻转发，谁都不等谁（L242） | 论文 §3.2 `Once a chunkserver receives some data, it starts forwarding immediately` | ✅ |
| 理想耗时 B/T + R×L；论文链路 100Mbps、L 远小于 1ms、1MB≈80ms（L246） | 论文 §3.2 `is B/T + RL where T is the network throughput and L is latency to transfer bytes between two machines. Our network links are typically 100 Mbps (T), and L is far below 1 ms. Therefore, 1 MB can ideally be distributed in about 80 ms` | ✅ 逐句对应 |
| 「量纲是每跳的链路时延，不是"传一个字节"的时延」（L246） | 同上（B/T 已是推送 B 字节的耗时，R×L 只能是每跳固定时延 × 跳数） | ✅ 这是我们的澄清，模型上站得住 |
| 「不做流水线的对照式 R×B/T + R×L **是我们推的**，论文只给了流水线之后的式子」（L246/L250） | 论文无对照式 | ✅ 已标为我们的推断，**且落进了 `gfs-15` 图内可见文字**（"约 R×B/T 加 R×L（我们推的）"） |
| 读写实测：读聚合 94 MB/s≈125 MB/s 链路上限的 75%；单客户端读 6；写单客户端 6.3、16 客户端聚合 35、理论上限 67（因为每字节写 3/16 台、每台入向 12.5 MB/s）（L258–L264） | 论文 §6.1.1/§6.1.2 原文（94/6/125/75%、6.3/35/67/12.5 逐字命中）；`The main culprit for this is our network stack` | ✅ **七个数字全对**，连"归因给当时的网络栈"都是论文原话 |
| 表 3 集群 A 读速率 583 MB/s（§6.2.3）；正文写它过去一周维持 580 MB/s（L264） | 论文 §6.2.3 Table 3 `Read rate (last minute) 583 MB/s`；正文 `A had been sustaining a read rate of 580 MB/s for the preceding week` | ✅ **§号与两个数字都对** |
| 「论文表 2 数字的上千倍（讲义 320 行）」「协调者内存装不下、GC 扫描很慢（讲义 321–322 行）」（L275） | 讲义 L320–L322 | ✅ 行号指得准 |
| 「论文说为了让启动时间短，必须把日志控制得小（§2.6.3）」；「把这两句接成一条链是我们的推断」（L275） | 论文 §2.6.3（检查点 + 只重放最近的日志）+ §6.2.2 `only a few seconds to read this metadata from disk` | ✅ 归属已标；链条确是我们的 |
| 「早期主节点会因线性扫描几十万个文件的大目录而成为瓶颈，改成可二分查找才解决（§6.2.4）」（L283） | 论文 §6.2.4 Master Load `spent most of its time sequentially scanning through large directories (which contained hundreds of thousands of files)… We have since changed the master data structures to allow efficient binary searches through the namespace` | ✅ **§号正确**（§6.2.4 = Master Load） |
| 单点代价：上千客户端会把协调节点 CPU 压得过重（讲义）；总结那一节写内存与 CPU 都耗尽（L268） | 讲义 L323 / L342–343 | ✅ |
| Dynamo 对比（L291） | 源无 | ✅ 已标为我们的补充 |

**事实核对小结**：与源**冲突**的声明 **0 条**（下表的 P2-1 是措辞层面的重述，不算冲突）；
**否定的声明我做了反向检索**（"论文没有给块大小的倍数"⇒ 搜 `4 KB`/`4KB` 无块大小对比）。
本讲是七讲里事实层最干净的一页。

---

### 陌生读者测试（8 题）

**执行方式变更（需记录在案）**：审校人是队友、深度受限（`subagent` 报 `depth 2 exceeds maxDepth 1`），
**无法自己 spawn 陌生读者**。按 Lead 的指示，本讲的透镜 3 交 **Lead 在 depth 0 spawn 的全新子代理**执行
（只给 `content/03-gfs/index.md` 一个路径 + 8 个机制问题，禁止读 `_fc/`、`docs/`、联网、禁止用自身背景补）。

**答卷结果（Lead 在 depth 0 spawn 的全新子代理，自证只读了 `content\03-gfs\index.md`）：✅ 8 　⚠️ 0 　❌ 0 —— 零缺口。**

| 题 | 判定 | 读者引的页面原句（原样摘录） |
| --- | --- | --- |
| Q1 为什么不持久化块位置 | ✅ | L65「第三类刻意不持久化：主节点在启动时…直接问它「你有哪些块」」+ L67「块的位置不是权威数据，而是块服务器自己磁盘状态的缓存视图」 |
| Q2 64MB 买到哪三样、链通向什么 | ✅ | L97–L99 三条 + 「块大，块数就少；块数少，元数据总量就小；元数据少，就能全放进内存；全放进内存之后…既响应得快，又腾得出余力做后台整理」 |
| Q3 为什么先推数据后发写请求 | ✅ | L254「全部数据都要流经主副本这一台机器，它的上行带宽会立刻成为瓶颈」 |
| Q4 链式 vs 树形、摊掉哪一项 | ✅ | L244「链式能让每台机器的上行带宽被单一接收方吃满」+ L246「摊掉的正是这个被重复支付的 B/T，而 R×L 摊不掉」 |
| Q5 租约是省通信还是安全性 | ✅ | L210「租约在 GFS 里不只是省通信的优化，它承担的是安全性」 |
| Q6 普通写为什么静默丢数据 | ✅ | L170「它收到的只是一次成功。数据是这样静默丢掉的，没有报错」 |
| Q7 落后副本与版本号更大怎么办 | ✅ | L137 两处 |
| Q8 块大的代价哪条是论文的、哪两条是我们的 | ✅ | L111「论文在这一节只记下热点这一条代价；下面另外两条是我们顺着机制补的」——读者明确写「页面用「论文……」与「我们补的」明确标出了出处，**能分辨**」 |

⇒ **Q8 是对本项目归属做法的直接检验，读者说能分辨**。这与 01 的 `intro-5`/`intro-2` 形成正反两面：
**同一门课的两页在附录二上做法不一致**（本页达标、01 那两处不达标）⇒ 支持 `01-introduction-factcheck.md` 的 P1-4 判断。

---

### 附录二 / 附录十 专项

**（一）附录二（标记必须落到图内可见文字 + alt）—— 本页做得最好，逐图核过**

| 属于"我们的"内容 | 正文标记 | 图内可见文字 | `desc` | `alt` | 判定 |
| --- | --- | --- | --- | --- | --- |
| 块大的另外两条代价 | L111/L117/L296 | ✅ `gfs-8`「（这两条是我们的补充）」 | ✅ | ✅ L113 | ✅ |
| 不做流水线的对照式 R×B/T+R×L | L246 | ✅ `gfs-15`「（我们推的）」 | ✅ | ✅ L250 | ✅ |
| 文件数→内存/GC 与日志→重放的因果链 | L275 | ✅ `gfs-28`「这条因果链是我们的推断」 | ✅ | ✅ L281 | ✅ |
| 4KB 那一栏的对比假设 | L91 | ✅ `gfs-30`「（对比假设，我们加的）」 | ✅ | ✅ L89 | ✅ |
| HDFS/Ceph/Kafka/Dynamo 三处外部对比 | L83/L200/L291 | 未画图（无对应图） | — | — | ✅ 不适用 |
| 实测数字的出处 | L264 | ✅ `gfs-29`「数字出自论文测量一节」；`gfs-31`「（讲义 340 行）」 | ✅ | ✅ | ✅ |

⇒ **本页可作为 01 那种「标记没落进图」的正面样板**：同一门课的两页做法不一致，说明这是可做到的。
（对照：`01-introduction` 的 `intro-5`/`intro-2` 未标 ⇒ 见 `01-introduction-factcheck.md` P1-4。）

**（二）附录十（文字没说的事，图不许说）—— 逐张核过，无缺陷；两处"看着像问题其实不是"**

- ✅ **已核不出问题（请勿来改）**：`gfs-10` 上排三格（放置的三条考虑）与下排三格（掉线后的三段动作）**逐列对齐**（`x=38 / 275 / 512`，两排同列），
  这正是 `附录十` 里 `zoo-5` 那一族（列对齐断言一一对应）的形状。**但它不构成缺陷**，因为两排各自被一条虚线面板**显式分组**、并各带行标题。属性原文：
  ```xml
  <rect x="22" y="56" width="716" height="110" rx="10" fill="#f8fafc" stroke="#94a3b8" stroke-dasharray="6,4"/>   <!-- 上排面板 -->
  <rect x="22" y="190" width="716" height="110" rx="10" fill="#f8fafc" stroke="#94a3b8" stroke-dasharray="6,4"/>  <!-- 下排面板 -->
  <text x="380" y="70" ...>放置时挑机器的三条考虑，各治一个毛病</text>
  <text x="380" y="204" ...>副本数掉到目标以下之后：等多久、先救谁</text>
  ```
  `附录十` 的判据 3 要求的正是"**显式断开（圈成一个归属组、加标题说明）**"，本图两条都做了。
- ✅ `gfs-31` 的"没有租约"与"有租约"两格是上下并列的两个**反事实情形**，不是同一对象的两个状态，图内文字已各自标明（`没有租约` / `有租约`），无歧义。
- ✅ `gfs-29` 的横轴刻度（0/25/50/75/100/125）与两条数值标注（读 94、写 35）同轴可比；未发现"两个量画在同一尺度却含义不同"的问题。

**（三）几何类（附录十一：读属性）**

- ✅ 19 张图里我未发现任何"看起来偏了/更宽/没对齐"类的**主张**（页面 `alt` 与 `desc` 都没有下这类断言），
  因此按 `附录十一` 的第三类判据（"文件里有没有某元素"读属性即可、'看起来'类才需渲染），本次**未做渲染量墨迹**。
  例外一处见 P2-3。

---

### 一致性 / 可读性 / 诚实性

- **一致性（透镜 4）**：
  - 与 01 讲的口径：01 说「GFS 把文件切成 **64MB** 的块、每份数据存 **2 到 3 份**」，本页说「默认三份、用户可指定不同区域不同副本级别」。
    **两处不一致**：01 的「2 到 3 份」是 l01 讲义 L204 的说法（`replicates data on 2 or 3 servers`），本页的「默认三份」是论文 §2.3 的说法。
    两个源各自都对，**但同一门课的两页会给读者两个不同数字**。→ P2-2（建议在 01 处标注"讲义的说法"，或统一口径）。
  - 与 09-zookeeper 的「一致性」术语：两页都区分「一致/已定义」与「线性一致」，未见冲突（09 页的核对见其自己的记录）。
  - 与 02 讲的「超时只是猜测」：本页 L135 的失效检测正是同一缺口的应用，口径一致 ✅。
- **可读性（透镜 5）**：本次**没有重跑** `audit_content.py`（句长/密度/配图密度机检不在本记录范围）。
  人读一遍：结构清楚、每节都有"这一节在说什么"的引子。**这一维属"未验"。**
- **诚实性（透镜 6）**：**本页是七讲里做得最规范的一页**。三处主动标注（L81 的 consensus 推断、L111/L117 的两条代价、L275 的因果链）、
  两处"论文没有这样写"、一处把「讲义 vs 论文」两个源分别标注（L135、L151）。
  **唯一的缺口是把一条"依赖时钟同步才成立"的设计意图写成了无条件的不变量**（P1-1）。

### 本次覆盖面（附录十二）

- 已验：**全部具体数字**（64MB／三副本／64 字节／80GB-10MB/s／B/T+R×L-100Mbps-80ms／94-6-125-75%／6.3-35-67-12.5／583-580／六条假设）；
  全部 `§`/行号指认（§2.1/§2.3/§2.5/§2.6.1/§2.6.2/§2.6.3/§2.7.1/§2.7.2/§3.1/§3.2/§3.3/§4.3/§4.5/§5.1.3/§5.2/§6.1.1/§6.1.2/§6.2.3/§6.2.4，以及讲义 17/195–198/202/213–215/236–243/250–251/303–307/310/320–322/340）；
  19 张图的 `title`/`desc`/图内文字与正文 `alt` 逐张比对；`gfs-10` 的列对齐按属性原文核。
- **未验**：① 机检指标；② 渲染量墨迹（本页无"看起来"类主张）；
  ③ **论文抽文本身的准确性**（我用的是 `_chk/gfs.txt`，不是 PDF 原件；若它与 PDF 有出入，错会落在"论文"那一列）。

---

### 结论

**P0 0 项、P1 1 项、P2 3 项 → 修完 P1 后可提 `reviewed`。**

#### P0 · 0 项

#### P1 · 1 项

1. **P1-1（透镜 2+6 · 把有条件的写成无条件：漏掉租约失效的边界条件）**
   页面 L210 把「同一块在任一时刻最多只有一个有效租约，因此最多只有一个主副本」写成一条**不变量**，并在 L218 用它推出"不用担心两个主副本"。
   但**讲义 L297–299 明确把相反的情况列进「GFS 什么时候会破坏自己的保证」**：
   > `Time is not properly synchronized, so leases don't work out. So multiple primaries, maybe write goes to one, read to the other. Again, read may yield "success" but wrong data -- byzantine failure.`
   ⇒ 租约的安全性**依赖时钟同步**；时间不同步时会出现两个主副本，而且读会"成功但读到错数据"，属 byzantine 失效。
   这正是 `quality-audit.md` §2 的第 2 类错误（把"通常如此"写成"一定如此"）与 §6 的"边界条件写清楚了"。
   → **修在**：L210 的不变量句后面加一句边界条件（一句话即可）：
   「这条不变量的前提是**时钟基本同步**：讲义指出，如果时间不同步，租约就会失效，可能出现两个主副本，
   读还可能"成功"却拿到错数据 —— 这属于 byzantine 失效，而不是 fail-stop。」
   **不必**改图（`gfs-31` 画的是机制本身，不是这条边界条件）。

#### P2 · 3 项（记录在案，不阻塞）

1. **P2-1**：L23「搜索索引、爬虫抓下来的网页、日志，加起来已经是几百 TB」—— 论文说的是**集群提供几百 TB 存储**（摘要），
   页面把"集群容量"改述成"数据量"。数量级一致、方向无碍，但归属不同。建议改成「集群提供几百 TB 存储」。
2. **P2-2（跨页数字）**：01 讲写「每份数据存 **2 到 3 份**」（依据 l01 L204），本页写「默认三份」（依据论文 §2.3）。
   两个源各自都对，但同一门课两页给读者两个数字。建议其中一处标注出处（"讲义的说法"／"论文的默认值"）。
3. **P2-3（alt 里有图内没有的数字）**：L260 的 `alt` 与 `gfs-29` 的 `desc` 都写了「单客户端读 6 MB/s、写 6.3 MB/s」，
   但 `gfs-29` 的**图内可见文字**只有聚合值（读 94、写 35）与两条上限（125／67）。
   图单独传播时（截图、PNG），读者拿不到那两个单客户端数字。建议把 6／6.3 标进图内，或从 `alt` 里去掉。

#### 已核不出问题（记录在案，供下一个复核者直接关闭）

- 论文 §号指认**全部正确**，包括最容易错的 `§6.2.3`（Read and Write Rates，表 3 就在这一节）与
  `§6.2.4`（Master Load，线性扫描大目录→二分查找就在这一节）—— 这两处如果错，就是 `附录二` 类别 A 的"编号归属"错误。
- L228 的括注「（这一步论文的图里没有画）」与论文 §3.1 第 1 步原文的 `(not shown)` **逐字对应**。
- L151 的「论文交给 GFS 之外的监控设施另起一个新主进程」有论文 §5.1.3 原文支撑；而讲义 L253–254 的
  「Paper does not say」说的是另一个问题（**谁判定**协调者已死）。页面没有把这两件事混起来 —— 这是一处做对了的细节。
- `gfs-10` 的列对齐**不是** `附录十` 的缺陷（两排各有虚线面板 + 行标题，判据 3 要求的"显式断开"两条都做了）。

---

**审校人声明**：本记录只覆盖上表列出的基线版本（哈希见开头）。按附录五，对其它版本的结论不成立；
页面若再次改动，至少重跑陌生读者测试（本讲的透镜 3 答卷已回：✅8/⚠️0/❌0）。本记录不修改任何正文或图，`status` 字段由 Lead 处理。
