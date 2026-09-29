## 16-memcached 质量审核（草稿） · 作者 mit65840-author · 状态 draft

> 本记录是**草稿**：本讲状态为 `draft`，尚未进入 reviewed 流程，也**没有**由第二位审校人独立复核。
> 结论只列已核对项与未核对项，不改正文与图。

### 核对基线（先做行尾归一化再算哈希：`path.read_bytes().replace(b"\r\n", b"\n")`）

| 对象 | 归一化 SHA256（全 64 位） | 字节 |
| --- | --- | --- |
| `content/16-memcached/index.md` | `7A5E796BBCBB8D5DB8D507C4D07F521CFA6BF2DB081B077E7506EC676B5D26D4` | 24087 |
| `content/16-memcached/figures/mc-1.svg` | `3FE1E049D931DAB98FAA73887A3DD23BE900901D942E82162967EBC4F1782586` | 2654 |
| `content/16-memcached/figures/mc-10.svg` | `F7F28102024E330BF2345306DE0E30404AC22CA08C287DF298E60B52784B4702` | 3847 |
| `content/16-memcached/figures/mc-11.svg` | `3BDD592B1D46529B7C6093CC256ACAA7EB9948829F7F4D583836F740CBBFBB7F` | 3057 |
| `content/16-memcached/figures/mc-2.svg` | `B869A20F250DE49B942149797264DC22FFDA1B4BBF85DC8629738D6512A11639` | 4157 |
| `content/16-memcached/figures/mc-3.svg` | `6A199DAEE2D1900DE4669F765EA6AC18C4F815D49AFF4D1D3647F00C667D751B` | 4618 |
| `content/16-memcached/figures/mc-4.svg` | `6D26CB0C058DE7CD2B20728E881243D0D8EB96B22C65F810BED9CEE029464EA4` | 4844 |
| `content/16-memcached/figures/mc-5.svg` | `71BAF62F12E79245332B3734FB474DB86F73B71B54EC22CD94DAFACE2555D28E` | 4226 |
| `content/16-memcached/figures/mc-6.svg` | `E8DCD9994E0B68440822AD07856CDD765D52A9BB8FC5903AF73AF79E26095269` | 3900 |
| `content/16-memcached/figures/mc-7.svg` | `013B03DE3ABB6D55522890D04D78A86FA0378ACFA7C061298DC72248ECDECBD8` | 3291 |
| `content/16-memcached/figures/mc-8.svg` | `B0E7DFEB8FAB451B3E72FB29FA639A1642F971504B3ECFFE679064CDCB35806C` | 3641 |
| `content/16-memcached/figures/mc-9.svg` | `1BAD36ACD7EE6393CFF618E0AD168C5187F388C51850383D4EDA24FDCED09C39` | 2401 |

### 源

| 对象 | 值 |
| --- | --- |
| 抓取副本 | `_fc/l-memcached.txt`（291 行 / 11,735 字节） |
| SHA256（归一化） | `0D477E2E74B3B2B1873CF779DAC2C78D0EEDCA7064C251365EB2B556CAB64BBA` |
| 清单出处 | `docs/lecture-manifest.md` 第 16 行（源可用、11,735 B、本仓状态「待做」） |

### 已核对

- 清单第 16 行的标题、源文件名与字节数与抓取副本一致。
- 本页为原创讲解：无逐字稿、无双语原文对照、未转载源笔记图表；`[diagram]` 处均未取图。
- 页内每一处「N 项」都与随后的列表条数逐一对过（三条价值、三条 region 作用、三条大簇理由、两条数据库写入理由）。
- 命中率那笔账自洽（99% 对应约百分之一；99% 降到 98% 时未命中率翻倍）。

### 未核对 / 待办（本页仍是草稿的原因）

- 源笔记转述的论文数字（例如 Table 2 的 99% 命中率）没有回到 NSDI 2013 论文原文核对。
- 没有第二位审校人独立复核（本仓 reviewed 讲次要求有独立审校记录）。
- 视觉复核记录（`docs/audit/visual-review/`）尚未产出。
