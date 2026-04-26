import tkinter as tk
from tkinter import ttk
import threading
import time
import json
import tkinter.messagebox as messagebox
import os
import subprocess
import sys
import urllib.parse
import urllib.error
import urllib.request
# from ua import generate_headers_based_on_os
import platform
import HighDPIPrologue as HighDPIPrologue
headers = "UL"

headers = {"User-Agent":"NULL"}
print(headers)
os.chdir(os.path.abspath('./download'))
def open_folder(filepath):
    """打开文件所在文件夹"""
    filepath = os.path.abspath(filepath)
    if not os.path.exists(filepath):
        messagebox.showwarning("警告", "文件不存在，无法打开文件夹！")
        return
    try:
        subprocess.run(['explorer', '/select,', filepath], check=True)
    except:
        pass
class DownloadApp:
    def __init__(self, root):
        self.root = root
        self.root.title("下载助手")
        self.root.iconbitmap("downloadHelper.ico")
        self.root.configure(bg="#d5e8f9")
        
        title=tk.Label(self.root, text="下载可能需要的文件",font=("Arial", 16), bg="#d5e8f9",fg="#333333")
        title.pack(pady=10)

        with open('index.json', 'r', encoding='utf-8') as f:
            self.index = json.load(f)
        for i, download in enumerate(self.index):
            description = download.get("description")
            url = download.get("url")
            filename = download.get("filename")
            self.create_download_section(description, url, i, filename)
        self.root.geometry(f"800x{100+int(250 * 3)}")

    def create_download_section(self, name, url, index, filename=None):
        frame = tk.Frame(self.root, bg='white', relief='groove', bd=2)
        frame.pack(pady=15, padx=25, fill='x')

        label = tk.Label(frame, text=name, font=("Arial", 12), bg='white')
        label.pack(anchor='w', padx=15, pady=(15, 10))

        progress = ttk.Progressbar(frame, orient='horizontal', length=600, mode='determinate')
        progress.pack(padx=2, pady=5)
        
        status = tk.Label(frame, text="准备就绪", bg='white', font=("Arial", 9))
        status.pack(anchor='w', padx=15, pady=(0, 10))

        btn_frame = tk.Frame(frame, bg='white')
        btn_frame.pack(pady=5)

        start_btn = tk.Button(btn_frame, text="开始", 
                              command=lambda: self.start_download(url, progress, status, filename, open_btn),
                              bg='#4CAF50', fg='white', font=("Arial", 10), width=12)
        start_btn.pack(side='left', padx=5)

        open_in_browser_btn = tk.Button(btn_frame, text="🌐 在浏览器中打开",
                                         command=lambda: self.open_in_browser(url),
                                         bg="#424566", width=20,fg='white')
        open_in_browser_btn.pack(side='left', padx=5)

        # “打开文件夹”按钮（初始隐藏）
        open_btn = tk.Button(btn_frame, text="📂 打开文件夹",
                             command=lambda f=filename: open_folder(f),
                             state='disabled', width=12)
        open_btn.pack(side='left', padx=5)

        # 存储引用（可选）
        setattr(self, f'progress_{index}', progress)
        setattr(self, f'status_{index}', status)
        setattr(self, f'start_btn_{index}', start_btn)
        setattr(self, f'open_btn_{index}', open_btn)

    def open_in_browser(self, url):
        try:
            subprocess.run(['cmd', '/c', 'start', url], check=True)
        except:
            subprocess.run(['start', url], check=True)
            

    def start_download(self, url, progress_bar, status_label, filename, open_btn):
        if "下载中" in status_label.cget("text"):
            return

        def download():
            try:
                status_label.config(text="📥 连接中...")
                # response = requests.get(url, stream=True, headers=headers)
                request = urllib.request.Request((url),headers=headers)
                try:
                    response = urllib.request.urlopen(request)
                except urllib.error.HTTPError as e:
                    messagebox.showerror("错误", f"无法访问URL:\n{e}")
                    status_label.config(text="❌ 无法访问URL")
                    progress_bar['value'] = 0
                    return                
                except urllib.error.URLError as e:
                    messagebox.showerror("错误", f"无法访问URL:\n{e}")
                    status_label.config(text="❌ 访问URL失败")
                    progress_bar['value'] = 0
                    return
                
          
                
                # response.raise_for_status()

                total_size = int(response.headers.get('content-length', 0))
                if total_size == 0:
                    total_size = 10240

                downloaded = 0
                chunk_size = 8192
                last_update_time = time.time()
                last_downloaded = 0

                status_label.config(text="⬇️ 下载中...")
                progress_bar['maximum'] = 100

                with open(filename, 'wb') as f:
                    while True:
                        chunk = response.read(chunk_size)
                        if chunk:
                            f.write(chunk)
                            downloaded += len(chunk)

                            current_time = time.time()
                            if current_time - last_update_time >= 0.3 or downloaded == total_size:
                                elapsed = current_time - last_update_time
                                speed_kbps = ((downloaded - last_downloaded) / elapsed) / 1024 if elapsed > 0 else 0
                                percent = min((downloaded / total_size) * 100, 100)
                                progress_bar['value'] = percent

                                if speed_kbps < 1024:
                                    speed_str = f"{speed_kbps:.2f} KB/s"
                                else:
                                    speed_str = f"{speed_kbps / 1024:.2f} MB/s"

                                downloaded_mb = downloaded / 1024 / 1024
                                total_mb = total_size / 1024 / 1024
                                status_label.config(
                                    text=f"{percent:.1f}% 已完成, {speed_str} | {downloaded_mb:.2f}MB/{total_mb:.2f}MB"
                                )
                                self.root.update_idletasks()
                                last_update_time = current_time
                                last_downloaded = downloaded
                        else:
                            break   

                # 下载成功！
                messagebox.showinfo("提示", f"{filename} 下载完成！")
                status_label.config(text="✅ 下载完成！")
                # 启用“打开文件夹”按钮
                self.root.after(0, lambda: open_btn.config(state='normal'))

            except Exception as e:
                messagebox.showerror("错误", f"下载失败:\n{e}")
                status_label.config(text="❌ 下载失败")
                progress_bar['value'] = 0

        thread = threading.Thread(target=download, daemon=True)
        thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = DownloadApp(root)
    root.mainloop()