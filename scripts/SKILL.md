---
name: bixi-deploy
description: >
  赑屃 · 部署技能 v1.0。交互式部署接口：
  操作模式: 本地同步 / GitHub推送 / 全流程 / 查看状态
  Use when asked to 部署/发布/同步/更新 赑屃技能库网站，或 deploy/sync/publish bixi site.
version: 1.0.0
model: deepseek-v4-flash
tools: terminal,python
---

# 赑屃 · 部署技能 v1.0

## 交互式部署（默认）

无参数运行脚本进入交互菜单：

```bash
python3 /Volumes/Mac1T/墨码/GitHub管理/赑屃/scripts/sync_bixi.py
```

菜单流程：

```
操作模式：
  [1] 本地同步（git add + commit）
  [2] GitHub 推送（本地 → GitHub）
  [3] 全流程（1 + 2）
  [4] 查看仓库状态
```

## 命令行参数（非交互）

| 参数 | 作用 |
|------|------|
| （无参数） | 交互菜单 |
| `--sync` | 仅本地同步（git add + commit） |
| `--push` | 仅 GitHub 推送 |
| `--sync --push` | 本地同步 + 推送 |
| `--rebuild` | 配合 `--sync` 时重建首页统计（注：需手动更新） |
| `--interactive` | 强制交互菜单 |

### 示例

```bash
# 交互菜单
python3 scripts/sync_bixi.py

# 仅提交本地变更
python3 scripts/sync_bixi.py --sync

# 推送至 GitHub
python3 scripts/sync_bixi.py --push

# 提交 + 推送
python3 scripts/sync_bixi.py --sync --push
```

## 核心路径

```
赑屃网站根目录:   /Volumes/Mac1T/墨码/GitHub管理/赑屃/
同步脚本:        赑屃/scripts/sync_bixi.py
技能源目录:      /Volumes/Mac1T/墨码/赑屃/
```

## 网站结构

```
赑屃/
├── index.html              # 门户首页（含浮篆动画）
├── css/
│   └── style.css           # 青金水墨主题
├── public/                  # 公共技能 · 2 项
├── hermes/                  # 墨痕技能 · 4 项
├── pansi-skills/            # 盘丝技能 · 5 项
├── tunzei/                  # 吞贼技能 · 4 项
├── other/                   # 其他技能 · 2 项
    └── scripts/
        └── sync_bixi.py        # 部署脚本
```

## 技能页面添加说明

新增技能页面的步骤：

1. 在对应分类目录下创建 `{技能名称}.html`，使用分类目录下已有页面作为模板
2. 使用本地同步模式部署

### 页面模板参考

每页包含三个板块：
- **功能摘要** — 核心能力 + 亮点 feature grid
- **实现方式** — 技术架构说明
- **为什么做这个** — 博客式分享

共享 CSS 变量（`css/style.css`）：
```
--cyan:    #2a9d8f   （主色）
--gold:    #d4a853   （辅助色）
--bg-page: #080a0c   （底色）
```

---

## 输出确认

```
赑屃技能库部署 v1.0
═══════════════════════════════════
技能总数：17 项

操作模式：
  [1] 本地同步
  [2] GitHub 推送
  [3] 全流程
  [4] 查看仓库状态
```
