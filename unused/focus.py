import ctypes
from ctypes import c_bool, c_int
import os

dll = ctypes.CDLL(os.path.abspath('FocusQQWindow2.dll'))  # 或 ctypes.WinDLL，两者在多数情况下可互换

# 获取函数
focus_func = dll.focus

# 设置参数类型和返回类型
focus_func.argtypes = [c_bool]
focus_func.restype = c_int

if __name__ == '__main__':
    ###测试，创建一个名称有QQ的窗口
    import tkinter
    root = tkinter.Tk()
    root.title("QQ")
    root.geometry("400x300")
    # 调用函数
    result = focus_func(False)   # 或 False
    print("Result:", result)


    root.mainloop()