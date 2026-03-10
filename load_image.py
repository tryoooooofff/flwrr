import shutil
from pathlib import Path

# 配置路径
SOURCE_DIR = Path.home() / "Downloads"  # 图片所在目录
TARGET_DIR = Path(__file__).parent / "images"  # PyCharm 项目中的目标文件夹

# 要导入的精确文件名（区分大小写）
TARGET_FILES = [


    "map_ocean.png"







]

# 创建目标文件夹
TARGET_DIR.mkdir(parents=True, exist_ok=True)

copied = 0
for filename in TARGET_FILES:
    src_path = SOURCE_DIR / filename

    if src_path.exists():
        dst_path = TARGET_DIR / filename
        shutil.copy2(src_path, dst_path)
        print(f"✅ 已导入: {filename}")
        copied += 1
    else:
        print(f"❌ 未找到: {filename}（请检查文件是否在 Downloads 中）")

print(f"\n🎉 共成功导入 {copied} 个物品到 images/ 文件夹")