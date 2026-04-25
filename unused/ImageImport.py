import tkinter as tk
from tkinter import filedialog, messagebox
import os
import shutil
from pathlib import Path

# 支持的图片格式
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.tiff', '.svg'}

def select_folder():
    root = tk.Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="请选择包含图片的文件夹")
    root.destroy()
    return folder_selected

def copy_images(source_folder, target_folder, status_callback):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    success = 0
    failure = 0

    files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]
    image_files = [f for f in files if os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS]

    if not image_files:
        status_callback("未找到任何支持的图片文件。")
        return 0, 0

    for file in image_files:
        src_path = os.path.join(source_folder, file)
        dst_path = os.path.join(target_folder, file)
        status_callback(f"正在复制: {file}")
        
        try:
            shutil.copy2(src_path, dst_path)
            success += 1
        except Exception as e:
            print(f"复制失败: {file} - {e}")
            failure += 1

    return success, failure

def main():
    root = tk.Tk()
    root.title("导入图片")  # ✅ 标题要求
    root.geometry("600x340")
    root.resizable(False, False)

    # === 尊贵金配色 ===
    BG_COLOR = "#F5F5F5"
    BUTTON_COLOR = "#FFE038"
    BUTTON_TEXT_COLOR = "#222222"
    LABEL_COLOR = "#333333"
    STATUS_BG = "#FFFFFF"

    root.configure(bg=BG_COLOR)

    # 说明文字
    label_info = tk.Label(
        root,
        text="选择一个包含图片的文件夹，所有图片将被复制到当前目录下的 Images 文件夹中",
        bg=BG_COLOR,
        fg=LABEL_COLOR,
        wraplength=550,
        justify="center"
    )
    label_info.pack(pady=12)

    # 文件夹选择
    folder_var = tk.StringVar()
    folder_frame = tk.Frame(root, bg=BG_COLOR)
    folder_frame.pack(pady=5)

    folder_entry = tk.Entry(folder_frame, textvariable=folder_var, width=50, relief="solid", bd=1)
    folder_entry.pack(side=tk.LEFT, padx=(0, 8))

    def browse_folder():
        folder = select_folder()
        if folder:
            folder_var.set(folder)

    browse_btn = tk.Button(
        folder_frame,
        text="选择文件夹",
        bg=BUTTON_COLOR,
        fg=BUTTON_TEXT_COLOR,
        activebackground="#FFD000",
        relief="flat",
        command=browse_folder
    )
    browse_btn.pack(side=tk.RIGHT)

    # 目标路径提示
    target_folder = Path("./Images")
    target_label = tk.Label(
        root,
        text=f"目标文件夹：{target_folder}",
        bg=BG_COLOR,
        fg="#555555",
        font=("TkDefaultFont", 9)
    )
    target_label.pack(pady=5)

    # 状态栏
    status_var = tk.StringVar()
    status_var.set("就绪")
    status_label = tk.Label(
        root,
        textvariable=status_var,
        bg=STATUS_BG,
        fg=LABEL_COLOR,
        relief="solid",
        bd=1,
        padx=10,
        pady=10,
        wraplength=500,
        justify="center",
        height=3
    )
    status_label.pack(pady=12, padx=30, fill=tk.X)

    # 按钮区域
    button_frame = tk.Frame(root, bg=BG_COLOR)
    button_frame.pack(pady=10)

    def start_copy():
        source = folder_var.get().strip()
        if not source:
            messagebox.showwarning("警告", "请先选择源文件夹！")
            return
        if not os.path.isdir(source):
            messagebox.showerror("错误", "选择的路径不是有效文件夹！")
            return

        # 禁用按钮防止重复点击
        start_btn.config(state="disabled")
        browse_btn.config(state="disabled")

        status_var.set("开始扫描图片...")
        root.update()

        try:
            success, failure = copy_images(source, str(target_folder), lambda msg: (status_var.set(msg), root.update()))
            final_msg = f"完成！成功 {success} 张，失败 {failure} 张。"
            status_var.set(final_msg)
            messagebox.showinfo("完成", final_msg)
        except Exception as e:
            error_msg = f"发生未知错误：{str(e)}"
            status_var.set(error_msg)
            messagebox.showerror("错误", error_msg)
        finally:
            # 恢复按钮
            start_btn.config(state="normal")
            browse_btn.config(state="normal")

    start_btn = tk.Button(
        button_frame,
        text="开始",
        bg=BUTTON_COLOR,
        fg=BUTTON_TEXT_COLOR,
        activebackground="#FFD000",
        relief="flat",
        font=("TkDefaultFont", 10, "bold"),
        padx=20,
        command=start_copy
    )
    start_btn.pack(side=tk.LEFT, padx=10)

    finish_btn = tk.Button(
        button_frame,
        text="关闭",
        bg="#E0E0E0",
        fg="#333333",
        activebackground="#CCCCCC",
        relief="flat",
        padx=20,
        command=root.destroy
    )
    finish_btn.pack(side=tk.LEFT, padx=10)

    root.mainloop()

if __name__ == "__main__":
    main()