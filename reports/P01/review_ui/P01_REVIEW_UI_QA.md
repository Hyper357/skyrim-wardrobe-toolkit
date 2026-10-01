# P01_REVIEW_UI_QA.md

**ZLJ Wardrobe Collection — P01 Wardrobe Review 工具验收报告**

验收对象：`reports/P01/review_ui/P01_WARDROBE_REVIEW.html`（1,388,061 B，单文件）
验收日期：2026-09-30
结论：**通过，可交付用户使用。**

---

## 1. 验收方式

没有靠"看起来没问题"。本次验收用 Node 把**线上那份 HTML 里的真实 `<script>`**
抽出来，在一个最小 DOM stub 里跑起来（`tools/P01/p01_ui_test.js`），
逐条断言交互行为。也就是说测的是**发布出去的那份代码本身**，不是副本。

```
python tools\P01\p01_review_ui.py          # 重新生成
node   tools\P01\p01_ui_test.js            # 49 项功能断言
```

结果：**49 / 49 PASS**（exit 0）

---

## 2. 规格逐条对照

| # | 要求 | 结论 | 证据 |
|---|---|---|---|
| 1 | 只读冻结数据、结果内嵌、双击即开 | **PASS** | 0 个 `http(s)` 引用、0 个 CDN、单个 `<script>`；1 张预览图以 base64 内嵌 |
| 2 | 深色现代 UI、桌面优先 | **PASS** | 1920/2K 优先，`minmax(392px,1fr)` 自适应栅格；非报表风 |
| 3 | 顶部进度 + 四类计数 + 进度条 | **PASS** | 启动实测 `{"KEEP":0,"PARTIAL":0,"DROP":0,"UNDECIDED":56}` |
| 4 | 卡片只显示用户要看的字段 | **PASS** | Card 事实区仅 Body/Size/Parts/Material/Physics/BodySlide/Cost/UBE/Deps/Unresolved；FormID/NIF 明细全部收进默认折叠的 Technical Details |
| 5 | KEEP/PARTIAL/DROP 三大按钮 + UNDECIDED、互斥、状态明显 | **PASS** | 连续点 KEEP→DROP→PARTIAL，最终为 PARTIAL（后者胜）；DROP 卡片降至 `opacity .44` + 去饱和 |
| 6 | PARTIAL 展开该套专属 Visual Parts，逐件 KEEP/DROP，默认未定 | **PASS** | 展开面板的零件集合与该 outfit 零件集合**完全一致**（0 泄漏）；逐件 KEEP/DROP/↺ 与「全部 KEEP PART」「全部重置」均生效；其余零件保持 UNDECIDED |
| 7 | Notes 多行文本框 | **PASS** | 重渲染后内容不丢（实测 "XP 核心必留 / 只要靴子" 保留） |
| 8 | Priority 弱化、默认 UNSET | **PASS** | 位于决策按钮下方、`opacity .75`，启动全为 UNSET |
| 9 | 筛选 + 搜索 | **PASS** | 决策筛选返回数与实际一致；Cost=HIGH→17 套；UBE=A→仅含 A 零件的套装；Body=UNKNOWN→13 套；按 outfit 名搜 "MiscMods"→2 套，按零件名搜 "Nyes"→4 套，清空后恢复 56 |
| 10 | 六种排序，默认原始顺序 | **PASS** | 按名严格字典序；按体积严格降序；orig 返回全部 56 |
| 11 | NEXT UNDECIDED | **PASS** | 会跳过已决定的套装并滚动定位 |
| 12 | Preview 缩略图 + 点击放大 / 无图占位 | **PASS** | 1 套有图（内嵌 PNG），其余 55 显示 `No Preview Available`；DDS 被构建脚本显式排除，不会当预览图 |
| 13 | Technical Details 默认折叠 | **PASS** | `<details>` 默认 closed |
| 14 | localStorage 仅作暂存，Export 常驻 | **PASS** | localStorage 异常被 try/catch 包住；四个导出按钮常驻工具栏 |
| 15 | 三个导出 + 两个 CSV | **PASS** | 产出 `P01_USER_DECISIONS.json`、`.csv`、`P01_USER_PART_DECISIONS.csv`、`P01_WARDROBE_REVIEW_STATE.json`；CSV 表头逐字符匹配规格 |
| 16 | Import 校验 outfit_id | **PASS** | 导入合法 id 恢复 decision/priority/note/零件；导入伪造 id 被忽略并提示"忽略 1 条无法匹配的 outfit_id" |
| 17 | Undo / Reset Current / RESET ALL 二次确认 | **PASS** | RESET ALL 实测触发 **2 次** confirm，措辞含"56" |
| 18 | Sticky header 计数 + 进度条 | **PASS** | `position:sticky` |
| 19 | 完成提示不得误报 | **PASS** | 全部决定后显示 Complete；把某套设为 PARTIAL 且留 42 个零件未定 → 改为"Outfit selection complete，PARTIAL 零件尚未处理: 42"；零件处理完 → 恢复 Complete |
| 20 | .bat 只开浏览器 | **PASS** | 仅一行 `start "" "%~dp0P01_WARDROBE_REVIEW.html"`；不启服务、不改环境 |
| 21 | README 简洁 7 步 | **PASS** | 见 `README.md` |
| 22 | 本 QA 文档 | **PASS** | — |

---

## 3. 测试中发现并修复的真实缺陷

这两个是**功能测试真正抓出来的**，不是复述规格：

| # | 缺陷 | 影响 | 状态 |
|---|---|---|---|
| D-1 | PARTIAL 面板「全部重置」按钮声明 `data-pnone`，事件处理器却读 `t.dataset.pall`，于是 `S.parts[undefined]` 抛异常 | 用户点这个按钮**完全没反应**，控制台报错 | **已修复** |
| D-2 | 灯箱点击处理存在一个不可达的第二分支（`t.hasAttribute("data-img")` 恒为假，因为已被前一分支拦截） | 死代码；灯箱仍能工作，但留着会误导 | **已移除** |

D-1 如果只靠肉眼看代码几乎必然漏掉——按钮渲染正常、样式正常，只有真正点它才会暴露。

---

## 4. 诚实说明与已知限制

1. **自动测试不覆盖视觉呈现。** 49 项断言验证的是状态、筛选、排序、导出、
   导入、完成判定这些**逻辑**。像素级排版、响应式断点、动画观感需要在真实
   浏览器里看一次。**建议你第一次打开时随便点两下确认观感。**
2. **DOM stub 不是真浏览器。** 它忠实覆盖了本工具用到的 API 面，但没有
   真实布局引擎。少数纯视觉行为（如 `scrollIntoView` 的平滑滚动、
   `position:sticky` 的实际表现）无法在此断言。
3. **预览图只有 1 套 / 3 张，且很可能是你自己截的游戏内图**（文件名是 Windows
   默认截图格式 `屏幕截图 …png`），不是作者官方预览。**没有做任何渲染。**
4. **localStorage 在 `file://` 下行为不保证一致**，所以页面把 Export 放在
   显眼位置、README 也反复强调。localStorage 只作便捷暂存。
5. `localStorage` 恢复只校验了 decision / priority / note / 零件决策，
   未校验 schema 版本号；跨版本导入以 `outfit_id` 为准做尽力匹配。

---

## 5. 边界自证

| 项 | 结果 |
|---|---|
| 56 套 Outfit 全部显示、ID 唯一 | ✅ |
| 启动时全部 UNDECIDED，无任何预填 | ✅ 启动实测 56/56 |
| KEEP/PARTIAL/DROP 互斥 | ✅ |
| PARTIAL 只显示本套零件 | ✅ 0 泄漏 |
| 原始 P01 CSV 是否被修改 | ❌ 未修改（只读，mtime 仍停在 14:17–14:21） |
| P00 冻结数据是否被修改 | ❌ 未修改 |
| 本工具是否改动过 mod / ESP / NIF / DDS | ❌ 否 |

构建脚本唯一会碰的源文件是**复制** 3 张 PNG 到 `assets/previews/` 作为参照，
**原 mod 目录内的文件只读不写、只复制不移动**。

---

## 6. ⚠ 验收期间发现的环境漂移（与本工具无关，但必须报告）

验收时（16:42）扫描 `E:\SkyrimAE\mo2` 发现 **2 个 mod 文件 + 1 个日志**
在 P01 开始（14:14）之后被改写。逐个追查后确认**全部由 MO2 自身造成**，
不是本工具链写的：

| 时间 | 文件 | 归属 |
|---|---|---|
| 16:20:30 | — | **MO2 被重新启动**（新 pid 38520，取代早先的 18372）|
| 16:20:32 | `mo2\plugins\logs\DownloadManager.log` | MO2 启动日志 |
| 16:26:53 | `mods\Raven语音包 - DBReV\meta.ini` | MO2 刷新 mod 元数据 |
| 16:27:12 | `mods\OutfitGallery 1.0.4\meta.ini` | MO2 刷新 mod 元数据 |

两个被改写的 mod（`OutfitGallery`、`Raven语音包`）**都不在 09 范围内**。

### 更重要的一点：modlist.txt 的 SHA 变了

MO2 退出时会原子重写 `modlist.txt`，本次发生在 **16:20:40**：

| | SHA256 |
|---|---|
| P00 冻结基线 | `5f03db69…cab4f` |
| 当前 | `6805184a…c03e2a` |

P00 当初就记录过「modlist mtime 不可靠，判定一律以 SHA256 为准」。
SHA 确实变了，按项目自己的规则这属于漂移，必须查清——所以我写了
`tools/P01/p01_drift_check.py`，用**与 P00 相同的规则**重新推导 09 范围
（分隔符是名字以 `_separator` 结尾的**被禁用 mod**，不是 `#` 注释行）：

```
frozen scope lines : L883..L938
live    scope lines : L883..L938     ← 完全相同
frozen member count : 56
live    member count : 56
ADDED   : 0
REMOVED : 0

VERDICT: the 56-mod scope is INTACT - P00 conclusions still hold
```

**结论：09 范围的 56 个 Mod 成员集合完全没有变化，位置也没变。**
整个文件的 SHA 变化来自 09 范围之外的其它内容。**P00 的全部结论依然成立，
P01 的 56 套 outfit 依然对应同一批 Mod。**

### 建议

1. **进入任何会改写 modlist / loadorder 的阶段之前，请先关闭 MO2。**
   这次漂移无害，但同样的事情如果发生在 P02 就不好说了。
2. 冻结基线里建议补记一条：**modlist SHA 变化时，先跑
   `p01_drift_check.py` 确认范围成员集合，再决定是否需要重扫。**
   单看 SHA 变化会误报成"范围变了"。

