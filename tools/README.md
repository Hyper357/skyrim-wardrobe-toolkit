# latex Wardrobe Collection — P00 扫描工具

## 只读保证

本目录下的所有脚本**只读取** `E:\SkyrimAE\mo2\mods\`、`E:\SkyrimAE\Data\` 与
`E:\SkyrimAE\mo2\profiles\Default\modlist.txt`。
所有写操作都被限制在本工程目录内：

```
E:\SkyrimAE\opencode工作目录\5-latex-wardrobe-collection\
├─ tools\        <- 脚本（本目录）
├─ data\         <- 中间 JSON 证据
└─ reports\P00\  <- 交付报告
```

脚本里没有任何 `open(..., "w")` 指向 `mo2\` 或 `Data\`。
P00 阶段禁止做的事（改 Mod / 改插件 / 跑 BodySlide / 跑 PGPatcher /
改 modlist / merge / 删文件）全部未被实现，不是靠约定靠自觉。

## 配置

全部路径集中在 `p00_common.py` 顶部常量里。改机器时只改那一处：

| 常量 | 本机取值 |
|---|---|
| `MO2_INSTANCE` | `E:\SkyrimAE\mo2` |
| `MO2_PROFILE` | `Default` |
| `MODLIST` | `E:\SkyrimAE\mo2\profiles\Default\modlist.txt` |
| `MODS_DIR` | `E:\SkyrimAE\mo2\mods` |
| `GAME_DATA` | `E:\SkyrimAE\Data` |
| `TARGET_SEPARATOR` | `09 特殊服装与NSFW 装备_separator` |

`TARGET_SEPARATOR` **不带**前导 `+` / `-`，因为解析时状态前缀已被剥掉。

## 一键重扫

```powershell
cd E:\SkyrimAE\opencode工作目录\5-latex-wardrobe-collection
python tools\p00_s1_scope.py
```

幂等：重复运行覆盖 `data\p00_scope.json` 与
`reports\P00\{00_SCOPE.md,01_MOD_INVENTORY.csv}`，不产生累积副作用。

## MO2 优先级模型（务必先读）

写在 `p00_common.py` 的模块 docstring 里，这里复述要点：

1. `modlist.txt` 是 MO2 左栏的**倒序**。第 1 行 = 左栏最底一行 = **最高覆盖优先级**。
2. 分隔符是**标题**，成员排在标题**下方**。
3. 两条合起来：**行号 L 的 mod，归属于行号比 L 大、且最接近的那个分隔符**。
4. 因此分隔符所在行 S 拥有的区间是 `(下方最近分隔符行号 + 1) … (S - 1)`。
5. `+` 启用 / `-` 禁用 / `#` 注释。
6. VFS 冲突：启用 mod 从第 1 行往下扫，同一虚拟路径**第一个命中者胜出**。

第 3 条是最容易搞反的一条。搞反会让范围多出 900 个 mod。
`p00_s1_scope.py` 每次运行都会打印解析出的范围与命中数，可自检。

## 已实现 / 未实现

| 阶段 | 脚本 | 状态 |
|---|---|---|
| 00 范围定义 | `p00_s1_scope.py` | ✅ |
| 01 Mod 级盘点 | `p00_s1_scope.py` | ✅ |
| 02–19 插件/NIF/DDS/DIY/材质/PBR/合并风险 | — | 未开始（等 P00 范围审核） |
| P00_MASTER_REPORT.md | — | 未开始 |

## 环境

Python 3.14.6（`python`）。标准库即可跑阶段 1。
`PyNifly` 未安装 —— 阶段 5 做 NIF 几何解析前需要装，或改用自写的 NIF 头解析器。
