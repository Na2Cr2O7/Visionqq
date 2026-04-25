import pyautogui
import pytweening
import pyperclip
import configparser
import time


config = configparser.ConfigParser()
config.read('config.ini',encoding='utf-8')
scroll=config.getint('general','scroll')
def click(x: int, y: int):
    print(x,y)
    pyautogui.moveTo(x, y,duration=.1, tween=pytweening.easeInOutQuad)
    pyautogui.click()
def goto(x: int, y: int):
    pyautogui.moveTo(x, y,duration=.1, tween=pytweening.easeInOutQuad)
def tab():
    pyautogui.press('tab')
def dragFromTo(x1: int, y1: int, x2: int, y2: int):
    pyautogui.moveTo(x1, y1)
    pyautogui.mouseDown()
    pyautogui.moveTo(x2, y2, duration=.1)
    time.sleep(scroll)
    pyautogui.mouseUp()

def scrollUp(length: int = 120):
    Warning("deprecated")
    for i in range(scroll):
        pyautogui.scroll(length)
        time.sleep(.1)
def scrollDown(length: int = 240):
    for i in range(scroll):
        pyautogui.scroll(-length)
        time.sleep(.1)
def sendTextWithoutClick(text:str):
    temp=''
    for i in text:
        if i=='\n':
            pyperclip.copy(temp)
            time.sleep(.2)
            temp=''
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            continue
        temp+=i
    pyperclip.copy(temp)
    time.sleep(.2)
    pyautogui.hotkey('ctrl', 'v')



import ctypes
import os
def uploadFile():
    dll=ctypes.CDLL(os.path.abspath('uploadFile.dll'))
    # extern "C" int __declspec(dllexport) upload()
    success=dll.upload()
    if success!=0:
        print('Upload failed')
        time.sleep(.5)
        pyautogui.press('esc')
    print('\n')

import subprocess
import ctypes

# def focus():
#     subprocess.run('focusqqwindow.exe')
def focus():
    dll=ctypes.CDLL(os.path.abspath('FocusQQWindow2.dll'))
    # extern "C" int __declspec(dllexport) focus()
    dll.focus()
if __name__ == '__main__':
    while True: 
        input("Press Enter to continue...")
        focus()


