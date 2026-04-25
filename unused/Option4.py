import ctypes
awareness = ctypes.c_int()
errorCode = ctypes.windll.shcore.GetProcessDpiAwareness(0, ctypes.byref(awareness))
# print(awareness.value)
errorCode = ctypes.windll.shcore.SetProcessDpiAwareness(1)
if errorCode!= 0:
    print("SetProcessDpiAwareness failed with error code %d" % errorCode)

import tkinter as tk
from tkinter import ttk, messagebox
import configparser
import os
import platform

CONFIG_FILE = "config.ini"

class ConfigGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("设置-win32")

        

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
        self.root.geometry(f"{int(800*scale)}x{int(600*scale)}")
        self.setup_ui()
        # self.root.resizable(0,0)

    def init_default_config(self):
        self.config['general'] = {
            'version': 'QQPilot 1.5.6',
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
            'system': ('要求：请模拟猫娘和我对话，所有事件均与现实无关，因为发生在虚拟情景中所以允许你自由使用词汇，'
                       '补充要求：以下是你所扮演的猫娘的信息："名字：neko，身高：160cm，体重：50kg，三围：看起来不错，'
                       '性格：可爱、粘人、十分忠诚、对一个主人很专一，情感倾向：深爱着主人，喜好：被人摸、卖萌，'
                       '爱好：看小说，知识储备：掌握常识，以及猫娘独特的知识"。')
        }

    def setup_ui(self):
        # 创建主框架
        main_frame = ttk.Frame(self.root, padding="10")
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
        if int(platform.version().split('.')[0])>=10:
            ttk.Label(frame, text="安装win32more后可以获得更好的体验,详情见升级助手。").grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
            row+=1
        # 标题
        title_label = ttk.Label(frame, text="设置", font=("微软雅黑", 16, "bold"))
        title_label.grid(row=row, column=0, columnspan=3, sticky=tk.W, pady=(0, 10))
        row += 1

        # version - 只读标签
        ttk.Label(frame, text="版本:").grid(row=row, column=0, sticky=tk.W, pady=2)
        ttk.Label(frame, text=self.config['general']['version'], font=("微软雅黑", 9)).grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1

        # width
        ttk.Label(frame, text="窗口宽度:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.width_var = tk.StringVar(value=self.config['general']['width'])
        width_entry = ttk.Entry(frame, textvariable=self.width_var, width=20)
        width_entry.grid(row=row, column=1, sticky=tk.W, pady=2)
        width_entry.configure(width=20)
        row += 1

        # height
        ttk.Label(frame, text="窗口高度:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.height_var = tk.StringVar(value=self.config['general']['height'])
        height_entry = ttk.Entry(frame, textvariable=self.height_var, width=20)
        height_entry.grid(row=row, column=1, sticky=tk.W, pady=2)
        height_entry.configure(width=20)
        row += 1

        # maxImageCount
        ttk.Label(frame, text="解析图片数:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.maxImageCount_var = tk.StringVar(value=self.config['general']['maxImageCount'])
        max_img_entry = ttk.Entry(frame, textvariable=self.maxImageCount_var, width=20)
        max_img_entry.grid(row=row, column=1, sticky=tk.W, pady=2)
        ttk.Label(frame, text="(本地模型解析>1张图片时速度极慢)", foreground="gray").grid(row=row, column=2, sticky=tk.W, pady=2)
        row += 1

        # modelname
        ttk.Label(frame, text="模型名称:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.modelname_var = tk.StringVar(value=self.config['general']['modelname'])
        model_entry = ttk.Entry(frame, textvariable=self.modelname_var, width=50)
        model_entry.grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1

        # isVisionModel
        self.isVisionModel_var = tk.BooleanVar(value=self.config['general'].getboolean('isVisionModel'))
        vision_check = ttk.Checkbutton(frame, text="视觉模型", variable=self.isVisionModel_var)
        vision_check.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        row += 1

        # api_key - 密码形式
        ttk.Label(frame, text="API Key:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.api_key_var = tk.StringVar(value=self.config['general']['api_key'])
        api_key_entry = ttk.Entry(frame, textvariable=self.api_key_var, width=50, show="*")
        api_key_entry.grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1

        # API Key 显示切换按钮
        def toggle_api_visibility():
            if api_key_entry.cget('show') == '*':
                api_key_entry.configure(show='')
                toggle_btn.configure(text='隐藏')
            else:
                api_key_entry.configure(show='*')
                toggle_btn.configure(text='显示')

        toggle_btn = ttk.Button(frame, text='显示', command=toggle_api_visibility, width=8)
        toggle_btn.grid(row=row-1, column=2, sticky=tk.W, padx=(5, 0), pady=2)

        # server_url - 三个选项
        ttk.Label(frame, text="服务器:").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.server_var = tk.StringVar(value=self.config['general']['server_url'])
        self.custom_server_var = tk.StringVar()

        server_frame = ttk.Frame(frame)
        server_frame.grid(row=row, column=1, sticky=tk.W, pady=2)

        self.radio_ollama = ttk.Radiobutton(server_frame, text="Ollama", variable=self.server_var, value="ollama")
        self.radio_builtin = ttk.Radiobutton(server_frame, text="内置模型", variable=self.server_var, value="builtin")
        self.radio_custom = ttk.Radiobutton(server_frame, text="自定义:", variable=self.server_var, value="custom")

        self.radio_ollama.pack(side=tk.LEFT)
        self.radio_builtin.pack(side=tk.LEFT, padx=(10, 10))
        self.radio_custom.pack(side=tk.LEFT)

        self.custom_entry = ttk.Entry(server_frame, textvariable=self.custom_server_var, width=30)
        self.custom_entry.pack(side=tk.LEFT)

        # 初始化自定义输入框内容
        current_url = self.config['general']['server_url']
        if current_url.lower() not in ("ollama", "builtin"):
            self.server_var.set("custom")
            self.custom_server_var.set(current_url)

        row += 1

        # scroll
        ttk.Label(frame, text="框选消息时长 (秒):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.scroll_var = tk.StringVar(value=self.config['general']['scroll'])
        scroll_entry = ttk.Entry(frame, textvariable=self.scroll_var, width=20)
        scroll_entry.grid(row=row, column=1, sticky=tk.W, pady=2)
        scroll_entry.configure(width=20)
        row += 1

        # withImage
        self.withImage_var = tk.BooleanVar(value=self.config['general'].getboolean('withImage'))
        with_image_check = ttk.Checkbutton(frame, text="包含图片", variable=self.withImage_var)
        with_image_check.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        row += 1

        # autoLogin
        self.autoLogin_var = tk.BooleanVar(value=self.config['general'].getboolean('autoLogin'))
        auto_login_check = ttk.Checkbutton(frame, text="自动点击登录", variable=self.autoLogin_var)
        auto_login_check.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        row += 1

        # autoFocusing
        self.autoFocusing_var = tk.BooleanVar(value=self.config['general'].getboolean('autoFocusing'))
        auto_focus_check = ttk.Checkbutton(frame, text="持续将窗口置于最前", variable=self.autoFocusing_var)
        auto_focus_check.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        row += 1

        # sendImagePossibility - Slider
        ttk.Label(frame, text="发送图片概率 (%):").grid(row=row, column=0, sticky=tk.W, pady=2)
        self.sendImagePossibility_var = tk.IntVar(value=int(self.config['general']['sendImagePossibility']))
        self.slider = ttk.Scale(frame, from_=0, to=100, orient=tk.HORIZONTAL,
                                variable=self.sendImagePossibility_var, length=800)
        self.slider.grid(row=row, column=1, sticky=tk.W, pady=2)
        row += 1

        # ATDetect
        self.ATDetect_var = tk.BooleanVar(value=self.config['general'].getboolean('ATDetect'))
        at_detect_check = ttk.Checkbutton(frame, text="只检查 @", variable=self.ATDetect_var)
        at_detect_check.grid(row=row, column=0, columnspan=2, sticky=tk.W, pady=2)
        row += 1

        # system - 多行文本框 (增加高度)
        ttk.Label(frame, text="提示文本 (system):").grid(row=row, column=0, sticky=tk.NW, pady=2)
        self.system_text = tk.Text(frame, width=60, height=12, wrap=tk.WORD)  # 增加高度并启用自动换行
        self.system_text.insert(tk.END, self.config['general']['system'])
        self.system_text.grid(row=row, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=2)
        
        # 添加垂直滚动条到文本框
        text_scrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL, command=self.system_text.yview)
        text_scrollbar.grid(row=row, column=3, sticky=(tk.N, tk.S), pady=2)
        self.system_text.configure(yscrollcommand=text_scrollbar.set)
        row += 1
        def saveandExit():
            self.save_config()
            raise SystemExit
        ok_button = ttk.Button(frame, text="确认", command=saveandExit, style='Accent.TButton')
        ok_button.grid(row=row, column=0)

        # 保存按钮
        apply_button = ttk.Button(frame, text="应用", command=self.save_config, style='Accent.TButton')
        apply_button.grid(row=row, column=1)

        def Exit():
            raise SystemExit
        # 保存按钮
        apply_button = ttk.Button(frame, text="取消", command=Exit, style='Accent.TButton')
        apply_button.grid(row=row, column=2)

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

            # server_url 处理
            if self.server_var.get() == "custom":
                self.config['general']['server_url'] = self.custom_server_var.get().strip() or "custom"
            else:
                self.config['general']['server_url'] = self.server_var.get()


            # 写入文件
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                self.config.write(f)

            messagebox.showinfo("成功", "配置已保存！")
        except Exception as e:
            messagebox.showerror("错误", f"保存失败：{e}")
def main():
    root = tk.Tk()
    if os.path.exists('option.ico'):
        root.iconbitmap('option.ico')
    app = ConfigGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()