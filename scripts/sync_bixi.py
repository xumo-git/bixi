#!/usr/bin/env python3
"""
赑屃技能库 → GitHub Pages 自动同步脚本

用法:
  python3 scripts/sync_bixi.py                    # 交互菜单
  python3 scripts/sync_bixi.py --sync             # 仅同步（git add + commit）
  python3 scripts/sync_bixi.py --sync --rebuild   # 同步 + 重建技能库首页统计
  python3 scripts/sync_bixi.py --push             # 仅推送至 GitHub
  python3 scripts/sync_bixi.py --sync --push      # 同步 + 推送
"""

import os, sys, subprocess
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

CATEGORIES = {
    "public": "public",
    "hermes": "hermes",
    "pansi-skills": "pansi-skills",
    "tunzei": "tunzei",
    "other": "other",
}
CAT_NAMES = ["公共技能", "墨痕技能", "盘丝技能", "吞贼技能", "其他技能"]


def count_skills():
    """统计各分类技能数，返回 (总技能数, 分类映射)"""
    cats = {}
    total = 0
    for cat_dir in CATEGORIES.values():
        cat_path = REPO / cat_dir
        if not cat_path.exists():
            cats[cat_dir] = 0
            continue
        count = len([f for f in cat_path.iterdir() if f.suffix == ".html"])
        cats[cat_dir] = count
        total += count
    return total, cats


def interactive_menu():
    print("=" * 50)
    print("  赑屃技能库部署 v1.0")
    print("=" * 50)
    print()
    total, _ = count_skills()
    print(f"  技能总数：{total} 项")
    print()
    print("操作模式：")
    print("  [1] 本地同步（git add + commit）")
    print("  [2] GitHub 推送（本地 → GitHub）")
    print("  [3] 全流程（1 + 2）")
    print("  [4] 查看仓库状态")
    mode = input("请输入 [1/2/3/4]: ").strip()
    while mode not in ("1", "2", "3", "4"):
        mode = input("请重新输入 [1/2/3/4]: ").strip()
    mode = int(mode)

    rebuild = False
    if mode in (1, 3):
        r = input("重建技能库首页统计？[y/N]: ").strip().lower()
        rebuild = r == "y"

    print()
    return mode, rebuild


def git_status():
    r = subprocess.run(
        ["git", "-C", str(REPO), "status", "--porcelain"],
        capture_output=True, text=True
    )
    return r.stdout.strip()


def git_add_commit():
    status = git_status()
    if not status:
        print("无变更，无需提交")
        return False

    print("变更文件：")
    for line in status.split("\n"):
        print(f"  {line}")

    total, cats = count_skills()
    detail = " · ".join(f"{n}: {c}" for n, c in zip(CAT_NAMES, cats.values()))

    subprocess.run(["git", "-C", str(REPO), "add", "-A"])
    r = subprocess.run(
        ["git", "-C", str(REPO), "commit", "-m", f"sync: 赑屃技能库更新（{total} 技能 · {detail}）"],
        capture_output=True, text=True
    )
    if r.returncode != 0:
        if "nothing to commit" in r.stderr:
            print("无变更，无需提交")
            return False
        print(f"[!] commit 失败: {r.stderr}")
        return False
    print("✓ 已提交")
    return True


def git_push():
    status = git_status()
    if not status:
        r = subprocess.run(
            ["git", "-C", str(REPO), "log", "--oneline", "-1"],
            capture_output=True, text=True
        )
        last_commit = r.stdout.strip()
        print(f"上次提交: {last_commit}")

    r = subprocess.run(
        ["git", "-C", str(REPO), "push"],
        capture_output=True, text=True, timeout=120
    )
    if r.returncode != 0:
        print(f"[!] push 失败: {r.stderr}")
        return False
    print("✓ 已推送至 GitHub")
    return True


def show_status():
    status = git_status()
    if status:
        print("未提交变更：")
        for line in status.split("\n"):
            print(f"  {line}")
    else:
        print("✓ 工作区干净，无未提交变更")

    r = subprocess.run(
        ["git", "-C", str(REPO), "log", "--oneline", "-3"],
        capture_output=True, text=True
    )
    print(f"\n最近提交：\n{r.stdout}")

    total, cats = count_skills()
    print(f"\n技能统计：")
    for name, cat_dir in zip(CAT_NAMES, CATEGORIES.values()):
        print(f"  {name}: {cats[cat_dir]} 项")
    print(f"  总计: {total} 项")


def main():
    is_interactive = "--interactive" in sys.argv or not any(
        a in sys.argv for a in ("--sync", "--push", "--rebuild")
    )

    if is_interactive:
        mode, rebuild = interactive_menu()
        do_sync = mode in (1, 3)
        do_push = mode in (2, 3)
        do_status = mode == 4
    else:
        do_sync = "--sync" in sys.argv
        do_push = "--push" in sys.argv
        rebuild = "--rebuild" in sys.argv
        do_status = False

    if do_status:
        show_status()
        return

    if do_sync:
        print("=" * 50)
        print("  本地同步：赑屃技能库 → Git")
        print("=" * 50)
        print()
        committed = git_add_commit()
        if rebuild and committed:
            print("\nℹ 如需重建首页统计，请手动更新 index.html 中的技能数")
        elif not committed:
            print("\n无需同步")

    if do_push:
        if do_sync:
            print()
        print("=" * 50)
        print("  GitHub 推送")
        print("=" * 50)
        print()
        git_push()


if __name__ == "__main__":
    main()
