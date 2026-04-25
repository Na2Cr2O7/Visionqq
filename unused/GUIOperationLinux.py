import pyautogui
import pytweening
import pyperclip
import configparser
import time
import os
import subprocess
config = configparser.ConfigParser()
config.read('config.ini',encoding='utf-8')
scroll=config.getint('general','scroll')
autoFocusing=config.getboolean('general','autoFocusing')
width=config.getint('general','width')
height=config.getint('general','height')
wmctrlsh='''#!/bin/bash

while IFS= read -r line; do
    [[ -n "$line" ]] || continue
    win_id=${line%% *}
    wmctrl -i -r "$win_id" -e 0,0,0,WIDTH,HEIGHT
done < <(wmctrl -l | grep -i 'qq')
'''
sh=wmctrlsh.replace('WIDTH',str(width))
sh=sh.replace('HEIGHT',str(height))
with open('left.sh', 'w',encoding='utf8') as f:
    f.write(sh)
subprocess.run(['chmod','+x','left.sh'])

def focus():
    global wmctrlsh
    if autoFocusing:
        subprocess.run(['sh','focus.sh'])
    subprocess.run(['sh','left.sh'])

def mouse_move(x: int, y: int) -> bool:
    pyautogui.moveTo(x, y)
    return True
def mouse_down() -> bool:
    pyautogui.mouseDown()
    return True

def mouse_up() -> bool:
    pyautogui.mouseUp()
    return True

def click(x: int, y: int) -> bool:
    pyautogui.click(x, y)
    return True

def dragFromTo0(x1: int, y1: int, x2: int, y2: int) -> bool:
    pyautogui.drag(x2 - x1, y2 - y1)
    return True

def scroll_up(delta: int =120) -> bool:
    pyautogui.scroll(delta)
    return True

def scroll_down(delta: int =120) -> bool:
    pyautogui.scroll(-delta)
    return True

def scroll_left(delta: int =120) -> bool:
    pyautogui.scroll(-delta)
    return True

def scroll_right(delta: int =120) -> bool:
    pyautogui.scroll(delta)
    return True


def press_key(key_name: str) -> bool:
    """
    按下单个键（支持字母、数字、功能键名）
    示例: press_key('A'), press_key('ENTER'), press_key('F1')
    """
    pyautogui.press(key_name)
    return True
def hotkey(modifier: str, key: str) -> bool:
    """
    按下组合键（支持字母、数字、功能键名）
    示例: hotkey('ctrl', 'c'), hotkey('alt', 'F4')
    """
    pyautogui.hotkey(modifier, key)
    return True

def tab() -> bool:
    """
    按下Tab键
    """
    pyautogui.press('tab')
    return True

def scrollUp(length: int = 120) -> bool:
    """
    向上滚动
    """
    for i in range(scroll):
        scroll_up(length)
        time.sleep(.1)
    return True
def scrollDown(length: int = 240) -> bool:
    """
    向下滚动
    """
    for i in range(scroll):
        scroll_down(length)
        time.sleep(.1)
    return True

def goto(x: int, y: int)-> bool:
    """
    移动鼠标到指定位置
    """
    mouse_move(x, y)
    return True

press=press_key
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



    