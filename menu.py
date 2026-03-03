import tkinter as tk
import subprocess
import sys
import os

def run_script(script_name):
    """运行指定的 shell 脚本"""
    if os.name == 'nt':  # Windows
        subprocess.Popen(['bash', script_name])
    else:  # Unix-like (Linux/macOS)
        subprocess.Popen(['./' + script_name])
def script(fn,c):
    with open(fn if '.sh' in fn else f'{fn}.sh', 'w', encoding='utf-8') as f:
        f.write(c)
    f.close()
    os.system(f'chmod +x {fn if ".sh" in fn else f"{fn}.sh"}')
    run_script(fn if '.sh' in fn else f'{fn}.sh')
def on_launch():
    run_script('run.sh')

def on_settings():
    run_script('option.sh')

def on_extension_manager():
    run_script('ExtensionViewer.sh')

def on_lupgrade():
    run_script("LUpgrade.sh")
def on_download():

    run_script('download.sh')
def on_exit():
    root.destroy()
    sys.exit()


# 创建主窗口
root = tk.Tk()
root.title("启动台")
root.geometry("300x400")
root.resizable(False, False)

# 配色
button_bg = "#ffe038"
button_fg = "black"
button_font = ("Arial", 12, "bold")

# 创建按钮
btn_launch = tk.Button(root, text="启动", command=on_launch,
                       bg=button_bg, fg=button_fg, font=button_font, width=20, height=1)
btn_settings = tk.Button(root, text="设置", command=on_settings,
                         bg=button_bg, fg=button_fg, font=button_font, width=20, height=1)
btn_ext_mgr = tk.Button(root, text="扩展管理器", command=on_extension_manager,
                        bg=button_bg, fg=button_fg, font=button_font, width=20, height=1)
tk.Button(root, text="下载助手", command=on_download, bg=button_bg, fg=button_fg, font=button_font, width=20, height=1).pack(pady=10)
btn_exit = tk.Button(root, text="关闭", command=on_exit,
                     bg=button_bg, fg=button_fg, font=button_font, width=20, height=1)

# 布局按钮（垂直居中）
btn_launch.pack(pady=10)
btn_settings.pack(pady=10)
btn_ext_mgr.pack(pady=10)
tk.Button(root, text="升级助手", command=on_lupgrade, bg=button_bg, fg=button_fg, font=button_font, width=20, height=1).pack(pady=10)
btn_exit.pack(pady=10)

# 启动 GUI 主循环
root.mainloop()