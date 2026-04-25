import ast
import os
from pathlib import Path
import tkinter as tk
from tkinter import ttk, font, messagebox
import sysDetect
if not sysDetect.isLinux():
    import download.HighDPIPrologue  as HighDPIPrologue
    
import configparser
parser=configparser.ConfigParser()
parser.read("config.ini",encoding="utf-8")
scale=parser.getfloat("general", "scale")
class ExtensionViewer:
    def __init__(self, root):
        self.root = root
        self.root.title("扩展管理器")
        self.root.geometry(f"{int(650*scale)}x{int(450*scale)}")
        self.extensions_dir = Path("Extensions")
        self.setup_ui()
        self.load_extensions()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)

        style = ttk.Style()
        default_font = font.nametofont("TkDefaultFont")
        row_height = int((default_font.metrics("linespace") + 6) * scale)
        style.configure("Treeview", rowheight=row_height)

        columns = ('名称', '描述', '状态')
        self.tree = ttk.Treeview(main_frame, columns=columns, show='headings', height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=int((180 if col == '描述' else 120) * scale)) 

        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=1, column=1, sticky=(tk.N, tk.S))

        # 右键菜单...
        self.context_menu = tk.Menu(self.tree, tearoff=0)
        self.context_menu.add_command(label="启用", command=self.enable_extension)
        self.context_menu.add_command(label="禁用", command=self.disable_extension)
        self.tree.bind("<Button-3>", self.show_context_menu)
        self.tree.bind("<Button-2>", self.show_context_menu)

        self.status_var = tk.StringVar(value="就绪")
        status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=(10, 0))

    def show_context_menu(self, event):
        item = self.tree.identify_row(event.y)
        if not item:
            return
        self.tree.selection_set(item)
        self.context_menu.post(event.x_root, event.y_root)

    def extract_description(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                tree = ast.parse(f.read(), filename=str(file_path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Assign):
                    for target in node.targets:
                        if isinstance(target, ast.Name) and target.id == 'description':
                            if isinstance(node.value, ast.Constant):
                                return str(node.value.value).replace('\n', ' ')
            return "无描述"
        except Exception as e:
            return f"解析错误: {str(e)}"

    def load_extensions(self):
        if not self.extensions_dir.exists():
            self.extensions_dir.mkdir(exist_ok=True)
            self.status_var.set("已创建 extensions 文件夹")

        for item in self.tree.get_children():
            self.tree.delete(item)

        count = 0

        # 启用的扩展 (.py)
        for py_file in self.extensions_dir.glob("*.py"):
            if py_file.name.startswith("__"):
                continue
            desc = self.extract_description(py_file)
            self.tree.insert('', tk.END, values=(py_file.stem, desc, "启用"), tags=('enabled',))
            count += 1

        # 禁用的扩展 (.disabled)
        for disabled_file in self.extensions_dir.glob("*.disabled"):
            base_name = disabled_file.stem.replace('.disabled', '')
            self.tree.insert('', tk.END, values=(base_name, "该扩展当前被禁用", "禁用"), tags=('disabled',))
            count += 1
        if count !=2:
            self.status_var.set(f"已加载{count}个扩展 - 请右键点击扩展进行操作")
        else:
            self.status_var.set(f"已加载两个扩展 - 请右键点击扩展进行操作")


    def get_selected_item(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("提示", "请先选择一个扩展")
            return None
        item = selection[0]
        name, desc, status = self.tree.item(item, 'values')
        return item, name, status

    def enable_extension(self):
        result = self.get_selected_item()
        if not result:
            return
        item, name, status = result
        if status == "启用":
            messagebox.showinfo("提示", "该扩展已是启用状态")
            return

        disabled_path = self.extensions_dir / f"{name}.disabled"
        enabled_path = self.extensions_dir / f"{name}.py"

        if not disabled_path.exists():
            messagebox.showerror("错误", f"找不到禁用文件：{disabled_path}")
            return

        try:
            disabled_path.rename(enabled_path)
            self.tree.set(item, column='状态', value='启用')
            self.tree.set(item, column='描述', value=self.extract_description(enabled_path))
            self.tree.item(item, tags=('enabled',))
            self.status_var.set(f"已启用扩展：{name}")
        except Exception as e:
            messagebox.showerror("错误", f"启用失败：{e}")

    def disable_extension(self):
        result = self.get_selected_item()
        if not result:
            return
        item, name, status = result
        if status == "禁用":
            messagebox.showinfo("提示", "该扩展已是禁用状态")
            return

        enabled_path = self.extensions_dir / f"{name}.py"
        disabled_path = self.extensions_dir / f"{name}.disabled"

        if not enabled_path.exists():
            messagebox.showerror("错误", f"找不到启用文件：{enabled_path}")
            return

        try:
            enabled_path.rename(disabled_path)
            self.tree.set(item, column='状态', value='禁用')
            self.tree.set(item, column='描述', value="该扩展当前被禁用")
            self.tree.item(item, tags=('disabled',))
            self.status_var.set(f"已禁用扩展：{name}")
        except Exception as e:
            messagebox.showerror("错误", f"禁用失败：{e}")

if __name__ == "__main__":
    root = tk.Tk()
    if os.path.exists("extension.ico"):
        try:
            root.iconbitmap("extension.ico")
        except:
            pass
    app = ExtensionViewer(root)
    root.mainloop()