
import ctypes
import os
from ctypes import wintypes
from typing import Optional
import time
import configparser
import pyperclip
import time

import logging

config = configparser.ConfigParser()
config.read('config.ini',encoding='utf-8')
scroll=config.getint('general','scroll')


# === 常量 ===
WHEEL_DELTA = 120
DLL_NAME = "InputEvent.dll"

# === 全局变量 ===
_lib = None

def _load_dll():
    
    global _lib
    if _lib is not None:
        return _lib
    logging.debug(f"加载 DLL:{DLL_NAME}")
    # 查找 DLL（当前目录或 PATH）
    dll_path = None
    for path in [os.getcwd(), os.path.dirname(__file__)]:
        candidate = os.path.join(path, DLL_NAME)
        if os.path.exists(candidate):
            dll_path = candidate
            break

    if not dll_path:
        raise FileNotFoundError(f"找不到 {DLL_NAME}，请确保它在当前目录或系统 PATH 中")

    try:
        lib = ctypes.CDLL(dll_path)
    except OSError as e:
        raise RuntimeError(f"无法加载 DLL: {e}")

    # === 函数签名定义 ===
    lib.Mousegoto.argtypes = [ctypes.c_uint, ctypes.c_uint]
    lib.Mousegoto.restype = ctypes.c_bool

    lib.Lclick.argtypes = [ctypes.c_uint, ctypes.c_uint]
    lib.Lclick.restype = ctypes.c_bool

    lib.dragFromTo.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_uint, ctypes.c_float]
    lib.dragFromTo.restype = ctypes.c_bool

    lib.scrollUp.argtypes = [ctypes.c_int]
    lib.scrollUp.restype = ctypes.c_bool

    lib.scrollDown.argtypes = [ctypes.c_int]
    lib.scrollDown.restype = ctypes.c_bool

    lib.scrollLeft.argtypes = [ctypes.c_int]
    lib.scrollLeft.restype = ctypes.c_bool

    lib.scrollRight.argtypes = [ctypes.c_int]
    lib.scrollRight.restype = ctypes.c_bool

    lib.getVkKey.argtypes = [ctypes.c_char_p]
    lib.getVkKey.restype = wintypes.WORD

    lib.copy.restype = ctypes.c_bool
    lib.paste.restype = ctypes.c_bool
    lib.selectAll.restype = ctypes.c_bool
    lib.undo.restype = ctypes.c_bool

    lib.hotKey.argtypes = [wintypes.WORD, wintypes.WORD]
    lib.hotKey.restype = ctypes.c_bool

    lib.press.argtypes = [wintypes.WORD]
    lib.press.restype = ctypes.c_bool

    lib.DPIAwarenessPrologue.restype = ctypes.c_bool

    _lib = lib
    return lib

# === 高级封装函数 ===

def init():
    """初始化：设置 DPI 感知（建议最先调用）"""
    lib = _load_dll()
    success = lib.DPIAwarenessPrologue()
    if not success:
        logging.error("⚠️ 警告: DPI 感知设置失败（可能影响高分屏坐标精度）")
    return success

def mouse_move(x: int, y: int) -> bool:
    """移动鼠标到屏幕绝对坐标 (x, y)"""
    lib = _load_dll()
    return lib.Mousegoto(ctypes.c_uint(x), ctypes.c_uint(y))

# extern "C" __declspec(dllexport)
# bool LmouseDown();
# extern "C" __declspec(dllexport)
# bool LmouseUp();

def mouse_down():
    """按下鼠标左键"""
    lib = _load_dll()
    return lib.LmouseDown()

def mouse_up():
    """抬起鼠标左键"""
    lib = _load_dll()
    return lib.LmouseUp()


def click(x: int, y: int) -> bool:
    """在 (x, y) 处执行左键点击"""
    lib = _load_dll()
    return lib.Lclick(ctypes.c_uint(x), ctypes.c_uint(y))

def dragFromTo0(x1: int, y1: int, x2: int, y2: int, duration: float = 0.1) -> bool:
    """从 (x1,y1) 拖拽到 (x2,y2)，耗时 duration 秒"""
    lib = _load_dll()
    return lib.dragFromTo(
        ctypes.c_uint(x1), ctypes.c_uint(y1),
        ctypes.c_uint(x2), ctypes.c_uint(y2),
        ctypes.c_float(duration)
    )

def scroll_up(delta: int = WHEEL_DELTA) -> bool:
    """垂直向上滚动（delta 默认为 1 格）"""
    lib = _load_dll()
    return lib.scrollUp(delta)


def scroll_down(delta: int = WHEEL_DELTA) -> bool:
    """垂直向下滚动"""
    lib = _load_dll()
    return lib.scrollDown(delta)

def scroll_left(delta: int = WHEEL_DELTA) -> bool:
    """水平向左滚动"""
    lib = _load_dll()
    return lib.scrollLeft(delta)

def scroll_right(delta: int = WHEEL_DELTA) -> bool:
    """水平向右滚动"""
    lib = _load_dll()
    return lib.scrollRight(delta)

def copy() -> bool:
    """Ctrl + C"""
    lib = _load_dll()
    return lib.copy()

def paste() -> bool:
    """Ctrl + V"""
    lib = _load_dll()
    return lib.paste()

def select_all() -> bool:
    """Ctrl + A"""
    lib = _load_dll()
    return lib.selectAll()

def undo() -> bool:
    """Ctrl + Z"""
    lib = _load_dll()
    return lib.undo()

def press_key(key_name: str) -> bool:
    """
    按下单个键（支持字母、数字、功能键名）
    示例: press_key('A'), press_key('ENTER'), press_key('F1')
    """
    lib = _load_dll()
    vk = lib.getVkKey(key_name.encode('ascii'))
    if vk == 0:
        raise ValueError(f"未知键名: {key_name}")
    return lib.press(vk)

def hotkey(modifier: str, key: str) -> bool:
    """
    按下组合键（modifier + key）
    
    Args:
        modifier (str): 修饰键，如 'ctrl', 'alt', 'shift'（大小写不敏感）
        key (str): 主键，如 'c', 'v', 'f1', 'enter'（大小写不敏感）
    
    Returns:
        bool: 是否成功发送输入事件
    
    Examples:
        hotkey('ctrl', 'c')   # 复制
        hotkey('alt', 'f4')   # 关闭窗口
    """
    modifier = modifier.upper().strip()
    key = key.upper().strip()
    
    lib = _load_dll()
    mod_vk = lib.getVkKey(modifier.encode('ascii'))
    key_vk = lib.getVkKey(key.encode('ascii'))
    
    if mod_vk == 0:
        raise ValueError(f"未知修饰键: {modifier}")
    if key_vk == 0:
        raise ValueError(f"未知按键: {key}")
        
    return lib.hotKey(mod_vk, key_vk)

# === 可选：便捷别名 ===
press = press_key

# === 可选：主动初始化 ===
init()

def tab():
    """按下 Tab 键"""
    return press_key('TAB')


def uploadFile():
    dll=ctypes.CDLL(os.path.abspath('uploadFile.dll'))
    # extern "C" int __declspec(dllexport) upload()
    success=dll.upload()
    if success!=0:
        print('Upload failed')
        time.sleep(.5)
        press('ESC')
    print('\n')
import focus as fc
autoFocusing=config.getboolean('general','autoFocusing')
def focus():
    fc.focus_func(autoFocusing)

def scrollUp(length: int = 120):
    for i in range(scroll):
        scroll_up(length)
        time.sleep(.1)
def scrollDown(length: int = 240):
    for i in range(scroll):
        scroll_down(length)
        time.sleep(.1)

def goto(x: int, y: int):
    mouse_move(x, y)

def sendTextWithoutClick(text:str):
    temp=''
    for i in text:
        if i=='\n':
            pyperclip.copy(temp)
            time.sleep(.2)
            temp=''
            hotkey('ctrl', 'v')
            press('enter')
            continue
        temp+=i
    pyperclip.copy(temp)
    time.sleep(.2)
    hotkey('ctrl', 'v')
def dragFromTo(x1: int, y1: int, x2: int, y2: int):
    mouse_move(x1, y1)
    mouse_down()
    mouse_move(x2, y2)
    time.sleep(scroll)
    mouse_up()

if __name__ == '__main__':
    while True: 
        input("Press Enter to continue...")
        focus() 