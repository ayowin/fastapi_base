import os
import shutil
from pathlib import Path

# 项目清理脚本

def clean_project():
    """
    删除项目中的所有 __pycache__ 目录和根目录下的 logs 目录
    """
    project_root = Path(__file__).parent
    print(f"开始清理项目目录: {project_root}")
    
    # 删除所有 __pycache__ 目录
    pycache_count = 0
    for pycache_dir in project_root.rglob("__pycache__"):
        if pycache_dir.is_dir():
            try:
                shutil.rmtree(pycache_dir)
                print(f"已删除 __pycache__ 目录: {pycache_dir}")
                pycache_count += 1
            except Exception as e:
                print(f"删除 {pycache_dir} 时出错: {e}")
    
    # 删除根目录下的 logs 目录
    logs_dir = project_root / "logs"
    if logs_dir.is_dir():
        try:
            shutil.rmtree(logs_dir)
            print(f"已删除 logs 目录: {logs_dir}")
        except Exception as e:
            print(f"删除 {logs_dir} 时出错: {e}")
    
    print(f"\n清理完成!")
    print(f"删除了 {pycache_count} 个 __pycache__ 目录")
    if logs_dir.is_dir():
        print("logs 目录不存在或已被删除")
    else:
        print("已删除 logs 目录")


if __name__ == "__main__":
    clean_project()