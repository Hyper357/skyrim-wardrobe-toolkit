# P01 Wardrobe Review — 使用说明

这是一个**单文件、离线**的人工筛选工具。它只读取已冻结的 P00 / P01 数据，
不修改任何 Skyrim / MO2 资产。

## 怎么用

1. 双击 `OPEN_P01_REVIEW.bat`
   （或直接双击 `P01_WARDROBE_REVIEW.html`）
2. 浏览 56 套 Outfit，点 **KEEP** / **PARTIAL** / **DROP**
   想取消就点 **UNDECIDED**。同一套永远只有一个 decision。
3. 点 **PARTIAL** 时会自动展开该套的 Visual Parts，
   逐个勾 **KEEP**（保留零件）或 **DROP**（丢弃零件）。
   默认全部 UNDECIDED，**不必一次勾完**。
4. **Notes** 随手写，例如「只要靴子和面罩」「XP 核心必留」「以后转 UBE」。
   Priority（S/A/B/C）是次要信息，留空也行。
5. 随时点 **Export Backup** 存一份完整进度。
6. 全部完成后点 **Export CSV** 和 **Export JSON**。
7. 把导出的三个文件交回项目：

   - `P01_USER_DECISIONS.csv`
   - `P01_USER_PART_DECISIONS.csv`
   - `P01_USER_DECISIONS.json`
     （可选）`P01_WARDROBE_REVIEW_STATE.json`

## 顺手的几个功能

- **▶ NEXT UNDECIDED** — 滚到下一套还没决定的，形成
  「看衣服 → 点决定 → NEXT」的快速流程
- 顶部筛选：Decision / Body / Cost / UBE / Material + 搜索框
- 排序：原始顺序 / 名称 / 体积 / Cost / UBE / Decision
- **Undo Last Decision**、**Reset Current Outfit**、**RESET ALL**（需两次确认）
- 关闭页面会**自动暂存**到浏览器 localStorage，但 localStorage 在
  `file://` 下不保证可靠，所以**务必用 Export Backup 落盘**

## 想换个时间继续

点 **Import Previous State** 选回 `P01_WARDROBE_REVIEW_STATE.json` 即可恢复
KEEP / PARTIAL / DROP、Priority、Notes 和所有零件勾选。导入时会校验
`outfit_id`，不匹配的行会被忽略并提示。

## 说明

- 预览图：56 套里只有 1 套带图（共 3 张 PNG），已内嵌进 HTML。
  其余显示 `No Preview Available`。这是真实情况，**没有做任何渲染**。
- 页面只做记录，不删除、不合并、不转换任何东西。
