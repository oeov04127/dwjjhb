import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

class FileExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("多文件夹内容合并工具")
        self.root.geometry("600x400")

        # 源文件夹列表
        self.source_dirs = []

        # 创建界面组件
        self.create_widgets()

    def create_widgets(self):
        # 源文件夹选择区
        frame_sources = ttk.LabelFrame(self.root, text="源文件夹")
        frame_sources.pack(pady=10, padx=10, fill="x")

        self.listbox = tk.Listbox(frame_sources, height=5)
        self.listbox.pack(side="left", fill="both", expand=True, padx=5)

        scrollbar = tk.Scrollbar(frame_sources)
        scrollbar.pack(side="right", fill="y")
        self.listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox.yview)

        btn_frame = ttk.Frame(frame_sources)
        btn_frame.pack(side="right", padx=5)

        ttk.Button(btn_frame, text="添加文件夹", command=self.add_folder).pack(pady=2)
        ttk.Button(btn_frame, text="移除选中", command=self.remove_folder).pack(pady=2)

        # 目标文件夹选择区
        frame_dest = ttk.LabelFrame(self.root, text="目标文件夹")
        frame_dest.pack(pady=10, padx=10, fill="x")

        self.dest_var = tk.StringVar()
        ttk.Entry(frame_dest, textvariable=self.dest_var, state="readonly").pack(side="left", fill="x", expand=True, padx=5)
        ttk.Button(frame_dest, text="选择目标", command=self.choose_destination).pack(side="right", padx=5)

        # 操作按钮
        ttk.Button(self.root, text="开始收集", command=self.start_extract).pack(pady=20)

        # 日志区
        self.log_text = tk.Text(self.root, height=8, state="disabled")
        self.log_text.pack(padx=10, pady=5, fill="both", expand=True)

    def add_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.source_dirs.append(folder)
            self.listbox.insert("end", folder)
            self.log(f"已添加源文件夹: {folder}")

    def remove_folder(self):
        selection = self.listbox.curselection()
        if selection:
            index = selection[0]
            removed = self.source_dirs.pop(index)
            self.listbox.delete(index)
            self.log(f"已移除源文件夹: {removed}")

    def choose_destination(self):
        folder = filedialog.askdirectory()
        if folder:
            self.dest_var.set(folder)
            self.log(f"已设置目标文件夹: {folder}")

    def start_extract(self):
        if not self.source_dirs:
            messagebox.showwarning("警告", "请至少选择一个源文件夹")
            return

        if not self.dest_var.get():
            messagebox.showwarning("警告", "请选择目标文件夹")
            return

        try:
            os.makedirs(self.dest_var.get(), exist_ok=True)
            for source_dir in self.source_dirs:
                for root, _, files in os.walk(source_dir):
                    for file in files:
                        src_path = os.path.join(root, file)
                        dest_path = os.path.join(self.dest_var.get(), file)
                        shutil.copy2(src_path, dest_path)
                        self.log(f"已复制: {src_path} -> {dest_path}")

            messagebox.showinfo("完成", "文件收集完成！")
        except Exception as e:
            messagebox.showerror("错误", f"操作失败: {str(e)}")

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileExtractorApp(root)
    root.mainloop()