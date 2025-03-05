import os
import shutil
from file_extractor_gui import FileExtractorApp
import tkinter as tk
import ctypes
ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)

def extract_files(source_dirs, dest_dir):
    """
    将多个源文件夹中的所有文件复制到目标文件夹中
    
    参数:
        source_dirs (list): 源文件夹路径列表
        dest_dir (str): 目标文件夹路径
    """
    # 创建目标文件夹（如果不存在）
    os.makedirs(dest_dir, exist_ok=True)
    
    # 遍历每个源文件夹
    for source_dir in source_dirs:
        # 遍历文件夹中的所有文件和子文件夹
        for root, _, files in os.walk(source_dir):
            for file in files:
                # 构造完整文件路径
                src_path = os.path.join(root, file)
                dest_path = os.path.join(dest_dir, file)
                
                # 复制文件（自动覆盖同名文件）
                shutil.copy2(src_path, dest_path)
                print(f"已复制: {src_path} -> {dest_path}")
    extract_files(source_dirs, dest_dir)
    print("文件提取完成！")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileExtractorApp(root)
    root.mainloop()    
    # 执行提取操作
