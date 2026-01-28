#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Interactive setup tool for YouTube access in video-to-notes-skill
Helps user choose and configure the best method to download YouTube videos
"""

import os
import sys
from pathlib import Path

# Fix Windows encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 60)
    print(f"  {text}")
    print("=" * 60)

def check_cookies_file():
    """Check if cookies.txt already exists"""
    return Path("cookies.txt").exists()

def option_1_manual_cookie():
    """Guide user through manual cookie export"""
    print("\n[OPTION 1] 手动导出 YouTube Cookie")
    print("-" * 60)
    print("""
这是最可靠的方法。YouTube 会识别你的浏览器身份。

步骤（5 分钟）:
  1. 打开 YouTube.com（必须登录）
  2. 按 F12 打开开发者工具
  3. 找到 Application 标签（Chrome/Edge）或 Storage（Firefox）
  4. 左侧菜单 → Cookies → https://www.youtube.com
  5. 右键任意 Cookie → Export All As HAR / Export Cookies
  6. 保存为 cookies.txt 到当前目录（与此脚本同级）
  7. 再次运行此脚本确认

浏览器：
  [A] Chrome / Microsoft Edge
  [B] Firefox
  [C] Safari (macOS)

如果成功，你会看到 cookies.txt 文件出现在当前目录。
依赖: 无（只需浏览器）
成功率: 99%
    """)
    return "manual_cookie"

def option_2_browser_extension():
    """Guide user through browser extension"""
    print("\n[OPTION 2] 使用浏览器扩展")
    print("-" * 60)
    print("""
自动化导出 Cookie 的更简单方法。

步骤（3 分钟）:
  1. 打开浏览器扩展商店
  2. 搜索并安装 Cookie 导出扩展：
     - Chrome: "Get cookies.txt" (By Rahul Patil)
     - Firefox: "Export Cookies" (By Rotem Dan)
     - Edge: "Get cookies.txt"
  3. 点击扩展图标
  4. 点击 "Export" 或 "Download"
  5. 保存为 cookies.txt 到当前目录
  6. 再次运行此脚本确认

优势: 一键导出，不需要手动操作
依赖: 浏览器扩展
成功率: 95%
    """)
    return "browser_extension"

def option_3_local_video():
    """Guide user through local video file"""
    print("\n[OPTION 3] 使用本地视频文件")
    print("-" * 60)
    print("""
如果无法导出 Cookie，可以手动下载视频。

下载方法：
  A. 浏览器扩展:
     - Chrome: "Video Downloader" 或 "Downie"
     - 在 YouTube 页面右键 → 下载视频

  B. 在线工具:
     - y2mate.com
     - ssyoutube.com
     - savefrom.net

  C. 本地工具:
     - ffmpeg: ffmpeg -i "https://youtu.be/..." output.mp4

保存后，使用此命令处理：
  python process_video.py \\
    --local-video "path/to/video.mp4" \\
    --video-title "GitHub Spec Kit" \\
    --language zh \\
    --save-to-file \\
    --output-path "E:\\YU_Files_E\\YU_Notes\\NOTES\\技术"

优势: 无需 Cookie，完全控制
依赖: 视频文件
成功率: 100%
    """)
    return "local_video"

def option_4_bilibili():
    """Alternative platform - Bilibili"""
    print("\n[OPTION 4] 使用 Bilibili（如果视频在那里）")
    print("-" * 60)
    print("""
GitHub Spec Kit 视频可能也在 Bilibili 上。

搜索方法:
  1. 打开 bilibili.com
  2. 搜索 "GitHub Spec Kit" 或 "Spec Kit"
  3. 如果找到，使用 URL 运行脚本：

  python process_video.py \\
    --url "https://www.bilibili.com/video/BV1..." \\
    --language zh \\
    --save-to-file \\
    --output-path "E:\\YU_Files_E\\YU_Notes\\NOTES\\技术"

优势: 某些内容在 Bilibili 更容易访问
依赖: 视频必须存在于 Bilibili
成功率: 取决于可用性
    """)
    return "bilibili"

def show_current_status():
    """Show current setup status"""
    print("\n[当前状态]")
    print("-" * 60)

    if check_cookies_file():
        print("✓ 已找到 cookies.txt 文件")
        print("  你可以立即运行脚本处理 YouTube 视频")
        return True
    else:
        print("✗ 未找到 cookies.txt 文件")
        print("  需要先导出 Cookie 或准备本地视频")
        return False

def main():
    """Main interactive menu"""
    print_header("YouTube Video 下载配置工具")

    print("\nYouTube 目前要求 Cookie 认证来验证合法用户。")
    print("这个工具会帮你选择最合适的方法。")

    has_cookies = show_current_status()

    if has_cookies:
        print("\n[准备完成！]")
        print("你可以开始处理 YouTube 视频了：")
        print("""
  cd scripts
  python process_video.py --url "https://www.youtube.com/watch?v=..." --language zh
        """)
        return 0

    print("\n请选择下面的方案之一:")
    print("\n[1] 手动导出 Cookie（最可靠）")
    print("[2] 使用浏览器扩展（最快）")
    print("[3] 使用本地视频文件（100% 成功）")
    print("[4] 查看 Bilibili 替代方案")
    print("[0] 退出")

    print_header("选择你的方案")

    choice = input("\n请输入选项 [0-4]: ").strip()

    if choice == "1":
        option_1_manual_cookie()
        print("\n[下一步]")
        print("导出 Cookie 后，运行此脚本：")
        print("  python setup_youtube_access.py")
        print("脚本会自动检测 cookies.txt 并确认设置成功。")

    elif choice == "2":
        option_2_browser_extension()
        print("\n[下一步]")
        print("扩展安装并导出后，检查 cookies.txt 是否出现。")

    elif choice == "3":
        option_3_local_video()
        print("\n[下一步]")
        print("使用提供的命令处理本地视频文件。")

    elif choice == "4":
        option_4_bilibili()
        print("\n[下一步]")
        print("如果在 Bilibili 找到视频，运行脚本处理即可。")

    elif choice == "0":
        print("退出。")
        return 0
    else:
        print("无效选项。")
        return 1

    # Final info
    print("\n" + "=" * 60)
    print("需要帮助？")
    print("  - 查看 README.md 获取详细说明")
    print("  - 运行 python export_youtube_cookies.py 自动检查浏览器")
    print("=" * 60 + "\n")

    return 0

if __name__ == "__main__":
    sys.exit(main())
