import os
import shutil
import configparser
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from pathlib import Path

class UpgradeHelperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("升级助手")
        self.root.geometry("600x400")
        self.root.resizable(True, True)

        self.script_dir = Path(__file__).parent.resolve()

        # 源目录显示
        tk.Label(root, text="源目录（程序所在位置）:", font=("Arial", 10)).pack(anchor="w", padx=10, pady=(10, 0))
        self.src_var = tk.StringVar(value=str(self.script_dir))
        tk.Entry(root, textvariable=self.src_var, state="readonly", width=80).pack(padx=10, pady=5, fill="x")

        # 目标目录选择
        tk.Label(root, text="目标目录（升级到的位置）:", font=("Arial", 10)).pack(anchor="w", padx=10, pady=(10, 0))
        self.dest_var = tk.StringVar()
        dest_frame = tk.Frame(root)
        dest_frame.pack(padx=10, pady=5, fill="x")
        tk.Entry(dest_frame, textvariable=self.dest_var, width=70).pack(side="left", fill="x", expand=True)
        tk.Button(dest_frame, text="浏览...", command=self.select_destination).pack(side="right", padx=(5, 0))

        # 开始按钮
        tk.Button(root, text="开始升级", command=self.start_upgrade, bg="#4CAF50", fg="white", height=2).pack(pady=10)

        # 日志输出框
        tk.Label(root, text="操作日志:", font=("Arial", 10)).pack(anchor="w", padx=10)
        self.log_text = scrolledtext.ScrolledText(root, height=12, state="disabled", wrap="word")
        self.log_text.pack(padx=10, pady=5, fill="both", expand=True)

    def log(self, message):
        self.log_text.config(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")
        self.root.update()

    def select_destination(self):
        folder = filedialog.askdirectory(title="请选择目标文件夹")
        if folder:
            self.dest_var.set(folder)

    def merge_config_files(self, src_ini, dst_ini):
        """合并 config.ini，保留目标中用户已修改的值"""
        src_ini = Path(src_ini)
        dst_ini = Path(dst_ini)

        if not dst_ini.exists():
            shutil.copy2(src_ini, dst_ini)
            self.log(f"复制 config.ini: {dst_ini}")
            return

        src_config = configparser.ConfigParser()
        src_config.read(src_ini, encoding='utf-8')

        dst_config = configparser.ConfigParser()
        dst_config.read(dst_ini, encoding='utf-8')

        for section in src_config.sections():
            if not dst_config.has_section(section):
                dst_config.add_section(section)
            for key, value in src_config.items(section):
                if not dst_config.has_option(section, key):
                    dst_config.set(section, key, value)

        with open(dst_ini, 'w', encoding='utf-8') as f:
            dst_config.write(f)
        self.log(f"合并 config.ini: {dst_ini}")

    def copy_files_with_config_merge(self, src_dir, dst_dir):
        src_path = Path(src_dir)
        dst_path = Path(dst_dir)
        dst_path.mkdir(parents=True, exist_ok=True)

        for src_file in src_path.rglob('*'):
            if src_file.is_file():
                rel_path = src_file.relative_to(src_path)
                dst_file = dst_path / rel_path
                dst_file.parent.mkdir(parents=True, exist_ok=True)

                if rel_path.name.lower() == 'config.ini':
                    self.merge_config_files(src_file, dst_file)
                else:
                    shutil.copy2(src_file, dst_file)
                    self.log(f"复制文件: {dst_file}")

    def start_upgrade(self):
        dest = self.dest_var.get().strip()
        if not dest:
            messagebox.showwarning("输入错误", "请先选择目标文件夹！")
            return

        dest_path = Path(dest)
        if not dest_path.parent.exists():
            messagebox.showerror("路径错误", f"父目录不存在:\n{dest_path.parent}")
            return

        try:
            self.log("开始升级...")
            self.copy_files_with_config_merge(self.script_dir, dest_path)
            self.log("✅ 升级完成！")
            messagebox.showinfo("成功", "升级已完成！")
        except Exception as e:
            self.log(f"❌ 升级失败: {e}")
            messagebox.showerror("错误", f"升级过程中出错:\n{str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = UpgradeHelperApp(root)
    root.mainloop()