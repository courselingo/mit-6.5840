## 16-memcached 质量审核（草稿） · 作者 mit65840-author · 状态 draft

> 本记录是**草稿**：本讲状态为 `draft`，尚未进入 reviewed 流程，也**没有**由第二位审校人独立复核。
> 结论只列已核对项与未核对项，不改正文与图。

### 核对基线（先做行尾归一化再算哈希：`path.read_bytes().replace(b"\r\n", b"\n")`）

| 对象 | 归一化 SHA256（全 64 位） | 字节 |
| --- | --- | --- |
| `content/16-memcached/index.md` | `A3E162986B3BE8BDF0B8477B2B1479A0E1D3D125B40106DD8B4F3F62CBF1365C` | 26311 |
| `content/16-memcached/figures/mc-1.svg` | `BB87A6588E5FBA0B1209B197722695EB893069D81E0AC6A1FCF03DF571227A94` | 2654 |
| `content/16-memcached/figures/mc-2.svg` | `2DC65FA6231D022CE511C9520FBA92E72CA108DB1E9C46E42693D9C02421848B` | 4154 |
| `content/16-memcached/figures/mc-3.svg` | `F0CF162DC015CCFDF654574F4BEEC666E3D6A5E94931C68AA0AA3CE2721D9545` | 4114 |
| `content/16-memcached/figures/mc-4.svg` | `A854D2DF6FF09F986AF859BA796E516C2B02567CF2B27BDEBA23E60A94BE622D` | 4334 |
| `content/16-memcached/figures/mc-5.svg` | `46125A6BF0F3B1701E64A54B887F6BFEFC0FB5EF77EB6AE9FD5ECCAFDE6A7AF5` | 3708 |
| `content/16-memcached/figures/mc-6.svg` | `2DE64AAC786B9A66D86DC3448353ABE7AABAF255C790F10DB4C93FE0887D2F55` | 3898 |

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
