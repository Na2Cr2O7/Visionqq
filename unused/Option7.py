import sysDetect
import platform
import tkinter as tk
from tkinter import ttk, messagebox
import configparser
import os
import platform

CONFIG_FILE = "config.ini"
def isnumeric(text:str):
    try:
        float(text)
        return True
    except:
        return False
class ConfigGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("设置")

        

        # 加载配置
        self.config = configparser.ConfigParser()
        if os.path.exists(CONFIG_FILE):
            self.config.read(CONFIG_FILE, encoding='utf-8')
        else:
            self.init_default_config()

        # 确保 [general] 存在
        if 'general' not in self.config:
            self.init_default_config()
        scale=self.config.getfloat('general','scale')
        self.root.geometry(f"{int(1000*scale)}x{int(600*scale)}")
        self.setup_ui()
        # self.root.resizable(0,0)

    def init_default_config(self):
        self.config['general'] = {
            'version': 'QQPilot 1.5.8',
            'width': '1285',
            'height': '720',
            'scale': '1.75',
            'maxImageCount': '1',
            'modelname': 'huihui_ai/deepseek-r1-abliterated:8b',
            'isVisionModel': 'False',
            'api_key': 'abcd',
            'server_url': 'builtin',
            'scroll': '4',
            'withImage': 'True',
            'autoLogin': 'False',
            'autoFocusing': 'True',
            'sendImagePossibility': '40',
            'nt_data': 'None',
            'ATDetect': 'False',
            'remote_server_timeout': '300',
            'tab_times':'8',
            'system': 'NULL'
        }

    def setup_ui(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10", relief='groove')
        # main_frame=tk.Frame(self.root, bg=BG, relief='groove', bd=2)
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        # 创建画布和滚动条
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # 配置网格权重
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)

        frame = scrollable_frame
        frame.columnconfigure(1, weight=1)

        row = 0
        # 标题
        title_label = ttk.Label(frame, text="设置", font=("微软雅黑", 16, "bold"))
        title_label.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        row += 1
        BG='white'
        def createFrame(row):
            f=tk.Frame(frame, relief='groove', bd=4,bg=BG)
            f.grid(row=row,column=0,padx=20,pady=10,sticky=(tk.W,tk.E),columnspan=3,)
            return f
        
        # version - 只读标签

        frame0=createFrame(row)
        tk.Label(frame0, text="版本:",bg=BG).grid(row=0, column=0, sticky=tk.W, pady=40,padx=40)
        tk.Label(frame0, text=self.config['general']['version']+f' {platform.system()}',bg=BG).grid(row=0, column=1, sticky=tk.W, pady=40,padx=40)
        row += 1

        # width
        frame0=createFrame(row)
        tk.Label(frame0, text="窗口宽度:",bg=BG).grid(row=0, column=0, sticky=tk.W, pady=40,padx=40)
        self.width_var = tk.StringVar(value=self.config['general']['width'])
        width_entry = ttk.Entry(frame0, textvariable=self.width_var, width=20)
        width_entry.grid(row=0, column=1, sticky=tk.E, pady=40,padx=40)
        width_entry.configure(width=20)
        row += 1

        
        
        # height
        f=createFrame(row)
        tk.Label(f, text="窗口高度:",bg=BG).grid(row=row, column=0, sticky=tk.W, pady=40,padx=40)
        self.height_var = tk.StringVar(value=self.config['general']['height'])
        height_entry = ttk.Entry(f, textvariable=self.height_var, width=20)
        height_entry.grid(row=row, column=1, sticky=tk.W, pady=40,padx=40)
        height_entry.configure(width=20)
        row += 1

        # maxImageCount
        f=createFrame(row)
        tk.Label(f, text="解析图片数:",bg=BG).grid(row=row, column=0, sticky=tk.W, pady=40,padx=40)
        self.maxImageCount_var = tk.StringVar(value=self.config['general']['maxImageCount'])
        max_img_entry = ttk.Entry(f, textvariable=self.maxImageCount_var, width=20)
        max_img_entry.grid(row=row, column=1, sticky=tk.W, pady=40,padx=40)
        tk.Label(f, text="(本地模型解析>1张图片时速度极慢)", foreground="gray",bg=BG).grid(row=row, column=2, sticky=tk.W, pady=40,padx=40)
        row += 1

        # modelname
        frame0=createFrame(row)
        tk.Label(frame0, text="模型名称:",bg=BG).grid(row=0, column=0, sticky=tk.W, pady=40,padx=40)
        self.modelname_var = tk.StringVar(value=self.config['general']['modelname'])
        model_entry = ttk.Entry(frame0, textvariable=self.modelname_var, width=50)
        model_entry.grid(row=0, column=1, sticky=tk.W, pady=40,padx=40)
        # isVisionModel
        # frame0=createFrame(row)
        self.isVisionModel_var = tk.BooleanVar(value=self.config['general'].getboolean('isVisionModel'))
        vision_check = tk.Checkbutton(frame0, text="视觉模型", variable=self.isVisionModel_var,bg=BG)
        vision_check.grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=40,padx=40)
        row += 1

        frame0=createFrame(row)
        # api_key - 密码形式
        tk.Label(frame0, text="API Key:",bg=BG).grid(row=row, column=0, sticky=tk.W, pady=40,padx=40)
        self.api_key_var = tk.StringVar(value=self.config['general']['api_key'])
        api_key_entry = ttk.Entry(frame0, textvariable=self.api_key_var, width=50, show="*")
        api_key_entry.grid(row=row, column=1, sticky=tk.W, pady=40,padx=40)
        row += 1
        # API Key 显示切换按钮
        def toggle_api_visibility():
            if api_key_entry.cget('show') == '*':
                api_key_entry.configure(show='')
                toggle_btn.configure(text='隐藏')
            else:
                api_key_entry.configure(show='*')
                toggle_btn.configure(text='显示')

        toggle_btn = tk.Button(frame0, text='显示', command=toggle_api_visibility, width=8,bg="#39833D", fg=BG)
        toggle_btn.grid(row=row-1, column=2, sticky=tk.W, pady=40,padx=40)


        frame0=createFrame(row)
        # server_url - 三个选项
        tk.Label(frame0, text="服务器:",bg=BG).grid(row=row, column=0, sticky=tk.W, pady=40,padx=40)
        self.server_var = tk.StringVar(value=self.config['general']['server_url'])
        self.custom_server_var = tk.StringVar()

        server_frame = tk.Frame(frame0,bg=BG)
        server_frame.grid(row=row, column=1, sticky=tk.W)

        self.radio_ollama = tk.Radiobutton(server_frame,bg=BG, text="Ollama", variable=self.server_var, value="ollama")
        self.radio_builtin = tk.Radiobutton(server_frame,bg=BG, text="内置模型", variable=self.server_var, value="builtin")
        self.radio_custom = tk.Radiobutton(server_frame,bg=BG, text="自定义:", variable=self.server_var, value="custom")

        self.radio_ollama.pack(side=tk.LEFT, pady=40,padx=40)
        self.radio_builtin.pack(side=tk.LEFT, pady=40,padx=40)
        self.radio_custom.pack(side=tk.LEFT, pady=40,padx=40)

        self.custom_entry = ttk.Entry(server_frame, textvariable=self.custom_server_var, width=30)
        self.custom_entry.pack(side=tk.LEFT, pady=40,padx=40)

        # 初始化自定义输入框内容
        current_url = self.config['general']['server_url']
        if current_url.lower() not in ("ollama", "builtin"):
            self.server_var.set("custom")
            self.custom_server_var.set(current_url)

        row += 1


        # scroll
        frame0=createFrame(row)
        tk.Label(frame0, text="框选消息时长 (秒):",bg=BG).grid(row=row, column=0, sticky=tk.W, pady=40,padx=40)
        self.scroll_var = tk.StringVar(value=self.config['general']['scroll'])
        scroll_entry = tk.Entry(frame0, textvariable=self.scroll_var, width=20)
        scroll_entry.grid(row=row, column=1, sticky=tk.W, pady=40,padx=40)
        scroll_entry.configure(width=20)
        row += 1

        # withImage
        frame0=createFrame(row)
        self.withImage_var = tk.BooleanVar(value=self.config['general'].getboolean('withImage'))
        with_image_check = tk.Checkbutton(frame0,bg=BG, text="包含图片", variable=self.withImage_var)
        with_image_check.grid(row=row, column=0, sticky=tk.W, pady=40,padx=40)

        # autoLogin
        self.autoLogin_var = tk.BooleanVar(value=self.config['general'].getboolean('autoLogin'))
        auto_login_check = tk.Checkbutton(frame0,bg=BG, text="自动点击登录", variable=self.autoLogin_var)
        auto_login_check.grid(row=row, column=1, sticky=tk.W, pady=40,padx=40)

        # autoFocusing

        self.autoFocusing_var = tk.BooleanVar(value=self.config['general'].getboolean('autoFocusing'))
        auto_focus_check = tk.Checkbutton(frame0,bg=BG, text="持续将窗口置于最前", variable=self.autoFocusing_var)
        auto_focus_check.grid(row=row, column=2, sticky=tk.W, pady=40,padx=40)
        row += 1
        self.sendImagePossibility_var = tk.IntVar(value=int(self.config['general']['sendImagePossibility']))
        if not sysDetect.isLinux():
            # sendImagePossibility - Slider
            frame0=createFrame(row)
            tk.Label(frame0, text="发送图片概率 (%):",bg=BG).grid(row=row, column=0, sticky=tk.W, pady=40,padx=40)
            self.slider = ttk.Scale(frame0, from_=0, to=100, orient=tk.HORIZONTAL,
                                    variable=self.sendImagePossibility_var, length=800)
            self.slider.grid(row=row, column=1, sticky=tk.W,pady=40,padx=40)
            row += 1

        # ATDetect
        frame0=createFrame(row)
        self.ATDetect_var = tk.BooleanVar(value=self.config['general'].getboolean('ATDetect'))
        at_detect_check = tk.Checkbutton(frame0, text="只检查 @",bg=BG,variable=self.ATDetect_var)
        at_detect_check.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=40,padx=40)
        row += 1

        #remoteServerTimeout
        frame0=createFrame(row)
        tk.Label(frame0,bg=BG, text="远程服务器超时 (秒):").grid(row=row, column=0, sticky=tk.W, pady=40,padx=40)
        self.remoteServerTimeout_var = tk.StringVar(value=self.config['general']['remote_server_timeout'])
        remote_server_timeout_entry = ttk.Entry(frame0, textvariable=self.remoteServerTimeout_var, width=20)
        remote_server_timeout_entry.grid(row=row, column=1, sticky=tk.W, pady=40,padx=40)
        remote_server_timeout_entry.configure(width=20)
        row += 1

        #tab_times 使用下拉菜单
        frame0=createFrame(row)
        tk.Label(frame0,bg=BG, text="tab按下次数").grid(row=row, column=0, sticky=tk.W, pady=40,padx=40)
        self.tab_times_var = tk.StringVar(value=self.config['general']['tab_times'])
        tab_times_menu = ttk.OptionMenu(frame0, self.tab_times_var, self.tab_times_var.get(), '7','8')
        tab_times_menu.grid(row=row, column=1, sticky=tk.W, pady=40,padx=40)
        tk.Label(frame0, text="若框选消息时总是点击到删除或其他的按键时可以调整", foreground="gray",bg=BG).grid(row=row, column=2, sticky=tk.W, pady=40,padx=40)

        row += 1

        # system - 多行文本框 (增加高度)
        frame0=createFrame(row)
        tk.Label(frame0,bg=BG, text="提示文本 (system):").grid(row=row, column=0, sticky=tk.NW, pady=40,padx=40)
        self.system_text = tk.Text(frame0, width=60, height=12, wrap=tk.WORD)  # 增加高度并启用自动换行
        self.system_text.insert(tk.END, self.config['general']['system'])
        self.system_text.grid(row=row, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=40,padx=40)

        frame0=tk.Frame(frame)
        frame0.grid(row=row+1,column=0,sticky=(tk.W,tk.E),columnspan=3,)
        
        # 添加垂直滚动条到文本框
        text_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.system_text.yview)
        text_scrollbar.grid(row=row, column=3, sticky=(tk.N, tk.S), pady=2)
        self.system_text.configure(yscrollcommand=text_scrollbar.set)
        row += 1
        def saveandExit():
            self.save_config()
            raise SystemExit
        
        ok_button = tk.Button(frame0, text="确认", command=saveandExit,bg="#2A772D", fg=BG,width=10)
        ok_button.grid(row=row, column=0,sticky=tk.W,pady=40,padx=40)

        # 保存按钮
        apply_button = tk.Button(frame0, text="应用", command=self.save_config,bg="#0B310C", fg=BG,width=10)
        apply_button.grid(row=row, column=1,pady=40,padx=40)

        def Exit():
            raise SystemExit
        
        cancel_button = tk.Button(frame0, text="取消", command=Exit,bg="#AF4C4C", fg=BG ,width=10)
        cancel_button.grid(row=row, column=2,pady=40,padx=40)

        # 将canvas和滚动条放置在主框架中
        canvas.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # 绑定鼠标滚轮事件
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)

        # 绑定 radio 按钮切换逻辑
        self.server_var.trace_add("write", self.on_server_radio_change)
        self.on_server_radio_change()

    def on_server_radio_change(self, *args):
        if self.server_var.get() == "custom":
            self.custom_entry.config(state='normal')
        else:
            self.custom_entry.config(state='disabled')

    def save_config(self):
        try:
            # 基础字段
            if not isnumeric(self.width_var.get()):
                raise Exception("宽度不是数字")
            if not isnumeric(self.height_var.get()):
                raise Exception("高度不是数字")
            if not isnumeric(self.maxImageCount_var.get()):
                raise Exception("解析图片数不是数字")
            if not isnumeric(self.scroll_var.get()):
                raise Exception("框选消息时长不是数字")
            if not isnumeric(self.remoteServerTimeout_var.get()):
                raise Exception("远程服务器超时不是数字")
            self.config['general']['width'] = self.width_var.get()

            self.config['general']['height'] = self.height_var.get()
            self.config['general']['maxImageCount'] = self.maxImageCount_var.get()
            self.config['general']['modelname'] = self.modelname_var.get()
            self.config['general']['isVisionModel'] = str(self.isVisionModel_var.get())

            self.config['general']['api_key'] = self.api_key_var.get()

            self.config['general']['scroll'] = self.scroll_var.get()

        
            self.config['general']['withImage'] = str(self.withImage_var.get())
            self.config['general']['autoLogin'] = str(self.autoLogin_var.get())
            self.config['general']['autoFocusing'] = str(self.autoFocusing_var.get())
            self.config['general']['sendImagePossibility'] = str(self.sendImagePossibility_var.get())
            self.config['general']['ATDetect'] = str(self.ATDetect_var.get())
            self.config['general']['system'] = self.system_text.get("1.0", tk.END).strip()
            self.config['general']['remote_server_timeout'] = self.remoteServerTimeout_var.get()
            self.config['general']['tab_times'] = self.tab_times_var.get()

            # server_url 处理
            if self.server_var.get() == "custom":
                self.config['general']['server_url'] = self.custom_server_var.get().strip() or "custom"
            else:
                self.config['general']['server_url'] = self.server_var.get()


            # 写入文件
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                self.config.write(f)

            # messagebox.showinfo("成功", "配置已保存！")
        except Exception as e:
            messagebox.showerror("错误", f"保存失败：{e}")
def main():
    root = tk.Tk()
    if os.path.exists('option.ico'):
        try:
            root.iconbitmap('option.ico')
        except:
            pass
    app = ConfigGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()