from typing import Any, Generator, Literal
from PIL import ImageGrab, Image,ImageDraw

from colorama import Fore



import logging
logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s',datefmt='%Y-%m-%d %H:%M:%S')


import positions

from PIL.ImageFile import ImageFile

import pyautogui
import pytweening
import pyperclip
# import getWindowScale
# getWindowScale.setInIWindowScale()

import time
import configparser
# logging.debug("importing easyocr")

import numpy as np

import answer
import enhance
logging.info("importing ocr")
import ocr

# import subprocess
# subprocess.run("FocusqqWindow.exe")

# logging.debug("initializing reader")

def click(x: int, y: int):
    print(x,y)
    pyautogui.moveTo(x, y,duration=1, tween=pytweening.easeInOutQuad)
    pyautogui.click()
def goto(x: int, y: int):
    pyautogui.moveTo(x, y,duration=1, tween=pytweening.easeInOutQuad)
def scrollUp(length: int = 120):
    for i in range(4):
        pyautogui.scroll(length)
        time.sleep(.1)
def scrollDown(length: int = 120):
    for i in range(4):
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
        
        
    


def containsRedDot(image: Image.Image):
    size=image.size
    RED_DOT_COLOR=(247,76,48)
    # newImage=Image.new("RGB",size,(255,255,255))
    for x in range(size[0]):
        for y in range(size[1]):
            pixel=image.getpixel((x,y))
            if pixel==RED_DOT_COLOR:
                return (x,y)
                newImage.putpixel((x,y),(0,0,0))
    # return newImage
    return False
def screenshot(positionRect: tuple[int, int, int, int]) -> Image.Image:
    logging.debug(f"screenshotting {ImageGrab.grab(bbox=positionRect)}")
    return ImageGrab.grab(bbox=positionRect)
logging.info("Successfully imported all modules")
if __name__ == '__main__':

    config=configparser.ConfigParser()
    config.read('config.ini',encoding='utf-8')
    size: tuple[int, int]=int(config.get('general','width')),int(config.get('general','height'))
    scale=float(config.get('general','scale'))
    scrollTries=int(config.get('general','scroll'))
    size=(int(size[0]*scale),int(size[1]*scale))

    logging.debug(f"size with scale: {size}, scale: {scale}")



    positionRect: tuple[Literal[0], Literal[0], int, int]=(0,0,*size)


    logging.debug(f"positionRect: {positionRect}")

    chatListActualSize: tuple[int, int, int, int]=positions.toActualSize(positions.CHAT_LIST_BBOX_RELATIVE_SIZE,size)
    logging.debug(f"chatListActualSize: {chatListActualSize}")

    conversationActualSize: tuple[int, int, int, int]=positions.toActualSize(positions.CONVERSATION_BBOX_RELATIVE_SIZE,size)
    logging.debug(f"conversationActualSize: {conversationActualSize}")

    commentSectionActualSize: tuple[int, int, int, int]=positions.toActualSize(positions.COMMENT_SECTION_BBOX_RELATIVE_SIZE,size)
    logging.debug(f"commentSectionActualSize: {commentSectionActualSize}")

    sendButtonActualSize: tuple[int, int, int, int]=positions.toActualSize(positions.SEND_BUTTON_BBOX_RELATIVE_SIZE,size)
    logging.debug(f"sendButtonActualSize: {sendButtonActualSize}")

    exitConversationActualSize: tuple[int, int, int, int]=positions.toActualSize(positions.EXIT_CONVERSATION_BBOX_RELATIVE_SIZE,size)
    logging.debug(f"exitConversationActualSize: {exitConversationActualSize}")

    while True:
        im=screenshot(positionRect)
        im.save("screenshot.png")
        chatList: Image.Image=im.crop(chatListActualSize)
        del im

        contain: tuple[int, int] | Literal[False]=containsRedDot(chatList)
        if contain :
            click(contain[0]+chatListActualSize[0],contain[1]+chatListActualSize[1])
            time.sleep(2)
            

            # conversation
            goto(conversationActualSize[0]+((conversationActualSize[2]-conversationActualSize[0])//2),conversationActualSize[1]+((conversationActualSize[3]-conversationActualSize[1])//2))
            for _ in range(scrollTries):
                scrollUp()
            conversationText=set()
            for scrollTry in range(scrollTries):
                
                im=screenshot(positionRect)
                

                conversation=im.crop(conversationActualSize)
                del im

                # conversationTexts=getAllTextWithBoxesDrawn("conversation.png")
                # print(conversationTexts)
                fn=f"conversation{scrollTry}.png"
                conversation.save(fn)


                conversation=enhance.getConversation(fn)


                for i in ocr.getAllTextWithBoxesDrawn(conversation):
                    conversationText.add(i)
                scrollDown()

            
            #send answer
            click(commentSectionActualSize[0]+((commentSectionActualSize[2]-commentSectionActualSize[0])//2),commentSectionActualSize[1]+((commentSectionActualSize[3]-commentSectionActualSize[1])//2))


            logging.info(f"{Fore.CYAN}{conversationText}{Fore.RESET}")

            result=answer.getAnswer('\n'.join(list(conversationText)))
            print(Fore.CYAN)
            if type(result)==str:
                print(result)
                sendTextWithoutClick(result)
            print(Fore.RESET)


            # click "send" button
            click(sendButtonActualSize[0]+((sendButtonActualSize[2]-sendButtonActualSize[0])//2)
                      ,sendButtonActualSize[1]+((sendButtonActualSize[3]-sendButtonActualSize[1])//2))
            
            time.sleep(.1)

            # exit conversation
            click(exitConversationActualSize[0],exitConversationActualSize[1])

            

    im.save("screenshot_result.png")

    conversationTexts=getAllTextWithBoxesDrawn("conversation.png")



# im=py



# im.save("screenshot.png")
# result=reader.readtext("screenshot.png")
# draw0: ImageFile=Image.open("screenshot.png")
# draw: ImageDraw.ImageDraw=ImageDraw.Draw(draw0)
# for r in result:
#     pos1,pos2,pos3,pos4=r[0] # type: ignore
#     x=[pos1[0],pos2[0],pos3[0],pos4[0]]
#     y=[pos1[1],pos2[1],pos3[1],pos4[1]]
#     minX=int(min(x))
#     maxX=int(max(x))
#     minY=int(min(y))
#     maxY=int(max(y))
#     print((minX,minY),(maxX,maxY))


#     draw.rectangle(((minX,minY),(maxX,maxY)),outline="red")
    
    
#     # print(r[1]) 

# draw0.save("screenshot_result2.png")

# im.save("screenshot_result.png")
