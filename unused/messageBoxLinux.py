import tkinter as tk
from tkinter import messagebox
MB_OK = 0x0
MB_OKCANCEL = 0x1
MB_YESNO = 0x4
MB_ICONINFO = 0x40
MB_ICONWARN = 0x30
MB_ICONERROR = 0x10
MB_ICONQUESTION = 0x20
IDABORT = 3
IDCANCEL = 2
IDCONTINUE = 11
IDIGNORE = 5
IDNO = 7
IDOK = 1
IDRETRY = 4
IDTRYAGAIN = 10
IDYES = 6
import subprocess
import os
import sysDetect

def MessageBox(text, title="提示", style=MB_OK | MB_ICONINFO):
    # """
    # 跨平台消息框函数，根据平台和可用库显示消息框
    # """
    # return _show_tk_message_box(text, title, style)
    dir=os.path.dirname(os.path.abspath(__file__))
    fn=os.path.basename(os.path.abspath(__file__))
    os.chdir(dir)
    if sysDetect.isLinux():
        return subprocess.run(['./PythonPath.sh',fn,text,title,str(style)])
    else:
        return subprocess.run(['PythonPath.cmd',fn,text,title,str(style)])
    
def _show_tk_message_box(text, title, style):
    """
    当没有wxPython时，使用tkinter作为备选方案（主要在Linux上）
    """
    try:

        
        # 隐藏主窗口
        root = tk.Tk()
        root.withdraw()
        root.focus_force()  # 确保消息框出现在前台
        
        # 解析样式并调用相应的tkinter消息框函数
        if style & MB_YESNO == MB_YESNO:
            if style & MB_ICONQUESTION:
                result = messagebox.askyesno(title, text)
                root.destroy()
                return IDYES if result else IDNO
            elif style & MB_ICONWARN:
                result = messagebox.askyesno(title, text)
                root.destroy()
                return IDYES if result else IDNO
            elif style & MB_ICONERROR:
                result = messagebox.askyesno(title, text)
                root.destroy()
                return IDYES if result else IDNO
            else:  # 默认情况
                result = messagebox.askyesno(title, text)
                root.destroy()
                return IDYES if result else IDNO
        elif style & MB_OKCANCEL == MB_OKCANCEL:
            result = messagebox.askokcancel(title, text)
            root.destroy()
            return IDOK if result else IDCANCEL
        else:  # MB_OK
            if style & MB_ICONERROR:
                messagebox.showerror(title, text)
                root.destroy()
                return IDOK
            elif style & MB_ICONWARN:
                messagebox.showwarning(title, text)
                root.destroy()
                return IDOK
            elif style & MB_ICONQUESTION:
                messagebox.showinfo(title, text)  # tkinter没有专门的问题图标
                root.destroy()
                return IDOK
            else:  # MB_ICONINFO 或默认
                messagebox.showinfo(title, text)
                root.destroy()
                return IDOK
    except ImportError:
        # 如果连tkinter都没有，则打印到控制台
        print(f"{title}: {text}")
        return IDOK
import sys
def main():
    if len(sys.argv) > 1:  # 运行时指定参数
        text = sys.argv[1]
        title = "提示"
        style = MB_OK | MB_ICONINFO
        if len(sys.argv) > 2:
            title = sys.argv[2]
        if len(sys.argv) > 3:
            style = int(sys.argv[3])
        result = _show_tk_message_box(text, title, style)
        sys.exit(result)
    sys.exit( _show_tk_message_box("这是一个测试消息框",'',''))

if __name__ == "__main__":
    main()
    
