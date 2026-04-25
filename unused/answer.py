import importlib
import configparser
import load
from colorama import Fore
import base64
import os
from typing import List, Optional
import time
from openai import OpenAI
import httpx
from chatContent import ChatContent
config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
modelName: str = config['general']['modelName']
server_url: str=config['general']['server_url']
isVisionModel: bool=config.getboolean('general', 'isVisionModel')
maxImageCount=config.getint('general', 'maxImageCount')
remoteServerTimeout=config.getint('general', 'remote_server_timeout')

API_KEY=config['general']['API_KEY']


if API_KEY=='None':
    API_KEY=None
useOllama=False
builtInLanguageModel=False
ollama=None

MAX_LENGTH=5000

if server_url.lower()=='ollama':
    ollama=importlib.import_module('ollama')
    useOllama=True
if server_url=='builtin':
    builtInLanguageModel=True
    tinylm=importlib.import_module('TinyLangJaccard')

# check the model is exist or not
print('Model:',modelName)
if useOllama:
    try:
        ollama.chat(modelName) # type: ignore
    except ollama.ResponseError as e:  # type: ignore
        print('错误：', e.error)
        if e.status_code == 404:
            print('模型未找到，正在下载...')
            load.startLoading(Fore.YELLOW,'正在下载模型...')
            ollama.pull(modelName)  # type: ignore
            load.stopLoading()

import base64
import os

def _imageToBase64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

import re
from pathlib import Path

def isTime(text):
    # 正则表达式匹配 HH:MM 格式，括号可选
    pattern = r'\(?([0-2]?[0-9]):([0-5][0-9])\)?'
    pattern2 = r'\(?([0-2]?[0-9]).([0-5][0-9])\)?'
    
    matches = re.findall(pattern, text)
    matches.extend(re.findall(pattern2, text))
    valid_times = []
    for hour_str, minute_str in matches:
        # 补全为两位数并转换为整数
        hour = int(hour_str)
        minute = int(minute_str)
        
        # 验证时间有效性：小时 0-23，分钟 0-59（minute 已由正则保证）
        if 0 <= hour <= 23:
            valid_times.append(f"{hour:02d}:{minute:02d}")
    
    return len(valid_times) > 0, valid_times


def concatenateText(text:list[ChatContent],images):
    message=[]
    textList=text
    for t in textList[:-1]:
        if str(t)=='':
            continue
        if not t.ownByMyself:
            message.append({"role": "user", "content": str(t)})
        else:
            message.append({"role": "assistant", "content": str(t)})
    if len(textList)<1:
        textList=['']
    if isVisionModel and images:
        message.append({"role": "user", "content":str(textList[-1]), "images": [p for p in images if os.path.exists(p)]})
    else:
        message.append({"role": "user", "content":str(textList[-1])})
    if len(message)<1:
        message.append({"role": "user", "content":"_"})
    return message
def getAnswer(text:list[ChatContent],systemPrompt:str='auto') -> Optional[str]:
    """
    调用 AI 模型获取回答（支持纯文本或图文输入）。
    
    Args:
        text: 用户问题文本
        imageList: 本地图像路径列表（仅 vision 模型有效）
    
    Returns:
        模型返回的文本，或 None（出错时）
    """
    if len(text)==0:
        return ""
    
    if builtInLanguageModel:
        for t in text[::-1]:
            if t.text == '':
                continue
            if t.ownByMyself:
                continue
            return tinylm.answer(t.text)
        return ''
    


    # 获取系统提示
    system_prompt = config.get('general', 'system')
    if systemPrompt!='auto':
        if system_prompt == 'None' or systemPrompt=='':
            system_prompt = ''
        else:
            system_prompt = systemPrompt

        
    imageList=[]
    imageCount=0
    for t in text:
        if not t.ownByMyself:
            for i in t.imagePaths:
                if os.path.exists(i):
                   imageList.append(i)
                   imageCount+=1
                   if imageCount>=maxImageCount:
                       break
                else:
                   print(f"× 没有找到图片 {i}")
            if imageCount>=maxImageCount:
                break
        if imageCount>=maxImageCount:
            break
    # 构建消息

    
    if useOllama:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages+=concatenateText(text,imageList)
        print(f"Ollama request: {messages}")
        try:
            response = ollama.chat( # type: ignore
                    model=modelName,
                    messages=messages,
                    
                    
                    stream=True
                )

            result = ''
            length = 0
            for chunk in response:
                token = chunk['message']['content']
                result += token
                length += len(token)
                if length >= MAX_LENGTH:
                    break
                print(token, end='', flush=True)
            print()  # 换行
            return result
        except Exception as e:
            print(f"Ollama request failed: {e}")
            return None
            
    else:
        try:
            client = OpenAI(
                api_key=API_KEY,
                base_url=server_url,
                timeout=httpx.Timeout(remoteServerTimeout),
                max_retries=2
            )
            if not (isVisionModel and imageList):
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})

                for t in text:
                    role = "assistant" if t.ownByMyself else "user"
                    messages.append({"role": role, "content": str(t)})

                # 确保最后一条是 user 消息
                if messages and messages[-1]["role"] == "assistant":
                    messages.append({"role": "user", "content": ""})  # 或者 raise ValueError("对话不能以助手消息结尾")
                print(f"openAI request{messages}")
                startTime=time.time()
 
                response = client.chat.completions.create(
                    model=modelName,
                    messages=messages,
                    max_tokens=MAX_LENGTH,
                    temperature=0.7,
                )
                print(f'用时{time.time()-startTime:.2f}s')
                answer: str = response.choices[0].message.content.strip()
                print(answer)
                return answer
            else:
                messages = []
                if system_prompt:
                    messages.append({"role": "system", "content": system_prompt})

                # 所有历史消息（包括倒数第二条及之前）
                for t in text[:-1]:
                    role = "assistant" if t.ownByMyself else "user"
                    messages.append({"role": role, "content": str(t)})

                last_t = text[-1]

                # 最后一条必须是用户输入（如果不是，强行视为用户输入可能有风险）
                # 你可以选择报错，或自动转换（这里按你的逻辑转换）
                # 但不要重复添加！

                # 构建多模态 content
                final_content:List = [{"type": "text", "text": str(last_t)}]

                for img_path in imageList:
                    if not os.path.isfile(img_path):
                        print(f"[ERROR] Image file not found: {img_path}")
                        continue
                    b64_image = _imageToBase64(img_path)
                    mime_type = "image/jpeg" if img_path.lower().endswith(('.jpg', '.jpeg')) else "image/png"
                    final_content.append({
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime_type};base64,{b64_image}"}
                    })

                messages.append({"role": "user", "content": final_content})
                print(f"openAI request{messages}")
                startTime=time.time()
                response = client.chat.completions.create(
                    model=modelName,
                    messages=messages,
                    max_tokens=MAX_LENGTH,
                    temperature=0.7,
                )
                answer: str = response.choices[0].message.content.strip() #type: ignore
                print(f'用时{time.time()-startTime:.2f}s')

                print(answer)
                return answer

        except Exception as e:
            print(f"[ERROR] Failed to get answer: {e}")
            # raise e
            return None
                
def get_answer_as_string(text:str,system_prompt):
    return getAnswer([ChatContent(username='',imagePaths=[],text=text,time='',ownByMyself=False)],system_prompt)
if __name__ == '__main__':
    ollama=importlib.import_module('ollama')
    tinylm=importlib.import_module('TinyLangJaccard')
    c=ChatContent(
        username='',
        imagePaths=[],
        text='解释图片\n2\n3\n4\n5',
        time=f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}',
        ownByMyself=False
    )
    c2=ChatContent(
        username='',
        imagePaths=[r"D:\Pictures\111.PNG"],
        text='12345',
       time=f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}',
        ownByMyself=True
    )
    c3=ChatContent(
        username='',
        imagePaths=[],
        text='678910',
        time=f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}',
        ownByMyself=False
    )


    useOllama=True
    modelName='jingyaogong/minimind2:latest'
    answer=getAnswer([c,c2,c3] )
    print(answer)
    isVisionModel=True
    answer=getAnswer([c,c2,c3] )
    print(answer)
    useOllama=False
    builtInLanguageModel=True
    answer=getAnswer([c,c2,c3] )
    print(answer)
    builtInLanguageModel=False
    server_url = 'http://localhost:8000/v1'
    API_KEY='21r234242'
    answer=getAnswer([c,c2,c3] )
    print(answer)

