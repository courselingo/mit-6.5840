## 21-bft 质量审核（草稿） · 作者 mit65840-author · 状态 draft

> 本记录是**草稿**：本讲状态为 `draft`，尚未进入 reviewed 流程，也没有由第二位审校人独立复核。

### 一、核对基线（先归一化行尾再算哈希）

| 对象 | 归一化 SHA256（全 64 位） | 字节 |
| --- | --- | --- |
| `content/21-bft/index.md` | `43EE7C73704230CF4D2351EC1771D8765E5E2F8A249C0914C75F3F5515D14C8F` | 28891 |
| `content/21-bft/figures/bft-1.svg` | `732EDEFE00ABE2FD9DF51B679BB384E5D64A9FF703AA38C2C9EE5351FB3BD056` | 2941 |
| `content/21-bft/figures/bft-2.svg` | `0449BCF6A12C29398D3B339373D9254E24DF07499C307938E90CE0CDAD808ABB` | 3673 |
| `content/21-bft/figures/bft-3.svg` | `CC28BD252C36D75ECAC1476B2BFD25DD78E94A0B614CDC23657B9947382FE83C` | 3801 |
| `content/21-bft/figures/bft-4.svg` | `65D9D94F992442DEC8D4662D6564929544B3F499F9DC0AFACCB2F5BF843E1B6A` | 3314 |
| `content/21-bft/figures/bft-5.svg` | `0F45F8F30F9FE56970C83799B63D96CFE283C8AAA008A846E1792BA7B4942CE2` | 4110 |
| `content/21-bft/figures/bft-6.svg` | `20D4AC744EAB11A9E4B807F9177F55977A2DF5A618BE59519B6AE6BFE1DC35E6` | 5450 |
| `content/21-bft/figures/bft-7.svg` | `159998E071F75940FECC0C734E5131FDC07584BF31056760997EAD78E5EFB45F` | 2921 |
| `content/21-bft/figures/bft-8.svg` | `82B01C26CD3E4C7C4E88865868D36B2DC3087619BAD10562FDDD879CDAD05116` | 2968 |
| `content/21-bft/figures/bft-9.svg` | `2C382E5CCAF167F27244F7383C19CF3AC22CD34DAAFEDBF90D87EA6D791547E1` | 2743 |
| `content/21-bft/figures/bft-10.svg` | `D78635A13A2D549B2E10655CDC352E4AABBFC60E0728CA700F6C0D5FEC09B325` | 3437 |
| `content/21-bft/figures/bft-11.svg` | `3E0047975D54DD6EB1D19799CEA1B557CFF36A1A78CD44549B3F130EF7E02436` | 3754 |
| `content/21-bft/figures/bft-12.svg` | `E54ADCDA662C4A32AE75A9FEE2CFFEBB4B948AE11FC86732E0034D5EE09C26B1` | 4138 |

### 二、事实核对

| 项 | 结论 |
| --- | --- |
| 清单第 21 行的标题与源文件 | `Byzantine Fault Tolerance` / `notes/l-bft.txt`（13,785 B）——与抓取副本一致 |
| 抓取副本 | `_fc/l-bft.txt`，342 行，归一化 SHA256 `8BA9633DFFA0E8A64277D97E45B9F2E436720F9715FA6E10C1F1401EEE4D7767` |
| 源内图片 | **0 张**（无 `.png`/`.jpg`，也无 `[diagram]` 占位）；源里的两幅 ASCII 时序示意**未转载** |
| 参数自洽 | 3f+1 里至多 f 坏；2×(2f+1)−(3f+1) = f+1 > f ⇒ 任意两个 2f+1 集合至少重叠一台好节点 |

### 三、陌生读者测试（8 题）

1. 「失败即停止」假设了什么？
2. 拜占庭失败比它多了哪几种可能？
3. 攻击者能做哪四件事、哪三件事不会发生？
4. 为什么只有一台被攻陷就能卡死第一版设计？
5. 2f+1 台里等 f+1 个匹配为什么不够？
6. 3f+1 台里等 2f+1 个匹配为什么够？
7. 为什么必须加 COMMIT 这个第三阶段？
8. 视图切换里 NEW-VIEW 为什么必须带完整的 VIEW-CHANGE 消息？

（上述 8 题的答案都能在本页正文对应小节里找到；本记录只列题，不写答案。）

### 四、附录二·附录十专项

- 附录二（不逐字翻译）：本页无逐字稿、无双语对照，全部为原创讲解。
- 附录十（术语与跨页去重）：本页未新增词条；与 `papers/raft`（崩溃容错）、`19-sundr`（不可信但不合谋）的分工已写在正文与溯源。

### 五、一致性·可读性·诚实性

- 一致性：同一概念全篇同名（主、副本、视图号、三阶段名）。
- 可读性：每节先给结论再给依据；公式只用两处（3f+1 与 2×(2f+1)−(3f+1)）。
- 诚实性：未读论文全文这一点已写在溯源「我没做的事」里。

### 六、本次覆盖面

已核对：清单行、源文件行数与哈希、源内图片数、参数自洽、跨页分工。未核对：论文原文的检查点与密码学优化细节、参考文献条目。

### 七、结论

**draft 阶段可用**；进入 reviewed 需要：论文原文回核 + 第二位审校人独立复核 + 每张图的视觉复核记录。
