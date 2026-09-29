# 讲次清单 · MIT 6.5840 / 6.824 Distributed Systems

> 本文件定义这门课的「**全量**」= 官方日程页上的全部讲授单元，并逐条标明**它能不能做**。
> 依据：**官方日程页快照** `_fc/schedule.html`（17,414 B，2026-09-28 抓取，本仓 `docs/audit/*-factcheck.md` 逐条引用它）。
> 授权：**`course.toml` 的 `[license] verified = false`** ——
> 徽章只出现在课程主页一处，`schedule.html` / `notes/*` / `general.html` 逐页实测**无许可声明**，
> ⇒ 笔记与讲义的授权覆盖范围**未确立**，按 `redistribution = "unknown"` 处理；
> **只发布 CourseLingo 自己的原创讲解**（讲概念、不转载原文），
> **逐字稿与双语原文对照一律不产出**；**Lab 代码与作业答案永久排除**（课程明确要求不得公开）。

## 官方讲次表（22 条，逐条给出「源是否可得」）

| # | 官方标题 | 源文件 | 源状态 | 本仓状态 |
|---|---|---|---|---|
| 1 | Introduction | `notes/l01.txt` | ✅ 10,886 B | ✅ `01-introduction`（reviewed） |
| 2 | RPC and Threads | `notes/l-rpc.txt` | ✅ 11,984 B | ✅ `02-rpc-and-threads`（reviewed） |
| 3 | GFS | `notes/l-gfs.txt` | ✅ 14,912 B | ✅ `03-gfs`（reviewed） |
| 4 | Paxos pseudo-code FAQ | `notes/l-paxos.txt` | ✅ 12,136 B | ✅ `04-paxos`（reviewed） |
| 5 | Go patterns（guest: Russ Cox） | — | ❌ `l-go.txt` 为 404 页 | ⛔ **源不可得**（客座，无讲义） |
| 6 | Fault Tolerance: Raft (1) | `notes/l-raft.txt` | ✅ 8,935 B | ⬜ **待做** |
| 7 | Fault Tolerance: Raft (2) | 同上（同一份讲义） | ✅ | ⬜ **待做**（与 6 合并为一页，见下） |
| 8 | Consistency and Linearizability | — | ❌ `l-consistency.txt` 404 | ⛔ **源不可得** |
| 9 | Zookeeper | `notes/l-zookeeper.txt` | ✅ 11,686 B | ✅ `09-zookeeper`（reviewed） |
| 10 | Q&A Lab 3A+B | — | ❌ 答疑课，无讲义 | ⛔ **无讲授内容** |
| 11 | Distributed Transactions | — | ❌ `l-transactions.txt` 404 | ⛔ **源不可得** |
| 12 | Spanner | `notes/l-spanner.txt` | ✅ 13,500 B | ⬜ **待做** |
| 13 | Chain Replication | — | ❌ `l-chain.txt` 404 | ⛔ **源不可得** |
| 14 | Optimistic Concurrency Control | — | ❌ `l-occ.txt` 404 | ⛔ **源不可得** |
| 15 | Verification of distributed systems（guest） | — | ❌ 客座，无讲义 | ⛔ **源不可得** |
| 16 | Cache Consistency: Memcached at Facebook | `notes/l-memcached.txt` | ✅ 11,735 B | ⬜ **待做** |
| 17 | AWS Lambda（guest: Marc Brooker） | — | ❌ 客座，无讲义 | ⛔ **源不可得** |
| 18 | Ray | `notes/l-ray.txt` | ✅ 6,926 B | ⬜ **待做** |
| 19 | Fork Consistency, SUNDR | `notes/l-sundr.txt` | ✅ 11,200 B | ⬜ **待做** |
| 20 | Peer-to-peer: Bitcoin | `notes/l-bitcoin.txt` | ✅ 11,510 B | ⬜ **待做** |
| 21 | Byzantine Fault Tolerance | `notes/l-bft.txt` | ✅ 13,785 B | ⬜ **待做** |
| 22 | Project demos | — | ❌ 演示课，无讲义 | ⛔ **无讲授内容** |

## 计数（本文件是这条判据的唯一台账）

```
官方讲次            22
源不可得／无讲授内容  15   （5、8、10、11、13、14、15、17、22 等）
**源可得 ⇒ 应产出**  **12** （1、2、3、4、6/7、9、12、16、18、19、20、21）
已产出（内容全部落盘）  **12**  （全部 12 条：1、2、3、4、6、9、12、16、18、19、20、21）
  其中 `status = "reviewed"`  5  （1、2、3、4、9 —— 本仓原有的那五讲）
  其中 `status = "draft"`     **7**（6、12、16、18、19、20、21 —— 2026-09-29 这一批新产出）
⇒ 待产出（内容）        **0**  ✅
⇒ **待产出（收尾记录）**  **34 份** —— 本仓标准是每讲两份记录：`<页>-factcheck.md` + 逐图
  `visual-review/mit-6.5840__<页>-<n>.md`。实测缺口：
  · `19-sundr` 缺 1 份 factcheck + 12 份逐图复核
  · `20-bitcoin` 缺 1 份 factcheck + 11 份逐图复核
  · `16-memcached` 缺 10 份逐图复核（已有 1 份，而它用了**带讲次号**的口径 `__16-memcached-1`，
    与其余各页的 `__<slug>-<n>` 不一致 ⇒ 新的那 10 份按**多数口径**写 `__memcached-<n>`）
```

★ **「完成」的两个层次**（这一栏是为了让「完善」可核）：
**内容层**已满（12/12 落盘 + nav 一致 + 五仓六道全绿）；
**记录层**还差 34 份，而那一层是**本仓比另外四门高的地方**（另外四门没有逐图复核记录）。

## 与此表绑定的三条不变式

1. **导航与台账一致**：`websrc/mkdocs.yml` 的 `nav:` 讲座列表必须与「已产出」一栏逐条对应；
   新增一讲 ⇒ **在页面落盘之后**把 nav 加上（否则站点上看不到，而台账已记录）。
   ★ 而「同一轮」这种写法不够 —— 它会被理解成「写作那一轮」，于是 nav 里会出现指向尚未落盘页面的条目。
   ⇒ **要写成一个可观测的事件**：「在 `content/<slug>/index.md` 落盘之后」。
2. **源不可得的不做，而不是用别的东西凑**：`⛔` 的那 10 条**不代补**
   ——上游没有讲义，就意味着**没有可核的依据**；而本课程的 `explanation` 口径要求每条内容可追到源。
3. **图名前缀在本仓内唯一**（见 `docs/figure-spec.md`）——
   因为逐图复核记录的文件名只用「前缀 + 序号」，**把两个目录压成了同一个命名空间**。

## 抓取口径（写在这里，免得下一个人重推）

```
· 讲义路径形如 https://pdos.csail.mit.edu/6.824/notes/<name>.txt，
  而 <name> 不是 l01/l02 那种连号 —— 实测存在的有 l01 / l-rpc / l-gfs / l-paxos /
  l-zookeeper / l-raft / l-spanner / l-memcached / l-ray / l-sundr / l-bitcoin / l-bft。
· **404 页固定 236 字节** ⇒ 「236 B」不是内容，是 404 页（`l-go.txt`、`lab-rpc.html`、`l-chain.txt` 都是这个大小）。
· **000 是瞬时失败、不是 404**（`l-spanner` / `l-bft` / `l-rpc` 首抓都是 000，重试即 200）⇒ 必须重试再判。
· 快照一律落 `_fc/`，并与 `docs/audit/<page>-factcheck.md` 里的 SHA256 对得上。
```
