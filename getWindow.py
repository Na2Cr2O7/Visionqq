import win32gui
import win32con
import configparser

config=configparser.ConfigParser()
config.read('config.ini',encoding='utf-8')
size=int(config.get('general','width')),int(config.get('general','height'))

desktop=win32gui.GetDesktopWindow()
# dpi=win32gui.GetDpiForWindow(desktop)

hwnd: int=win32gui.FindWindow(None,"QQ")

qqlist=[]
def isQQ(hwnd,param):
    if 'QQ' in win32gui.GetWindowText(hwnd):
        print(hwnd,win32gui.GetWindowText(hwnd),param)
        qqlist.append(hwnd)
    
win32gui.EnumWindows(isQQ,None)
for hwnd in qqlist:
    win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,0,0,0,0,win32con.SWP_NOSIZE)
    win32gui.SetWindowPos(hwnd,win32con.HWND_TOPMOST,0,0,*size,win32con.SWP_NOMOVE)
    get_rect: tuple[int, int, int, int]=win32gui.GetWindowRect(hwnd)
    print(win32gui.GetWindowText(hwnd),get_rect)


    

