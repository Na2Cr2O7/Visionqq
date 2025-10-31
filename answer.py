import importlib
import configparser
import requests

config = configparser.ConfigParser()
config.read('config.ini', encoding='utf-8')
modelName: str = config['general']['modelName']
server_url: str=config['general']['server_url']
API_KEY=config['general']['API_KEY']
if API_KEY=='None':
    API_KEY=None
useOllama=False
ollama=None
if server_url=='Ollama':
    ollama=importlib.import_module('ollama')
    useOllama=True

# check the model is exist or not
print('Model:',modelName)
if useOllama:
    try:
        ollama.chat(modelName) # type: ignore
    except ollama.ResponseError as e:  # type: ignore
        print('Error:', e.error)
        if e.status_code == 404:
            ollama.pull(modelName)  # type: ignore



import re

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
def getAnswer(text: str):
    if useOllama:
        # Ollama 部分保持不变
        response = ollama.chat( # type: ignore
            model=modelName,
            messages=[
                {
                    'role': 'system',
                    'content': config.get('general', 'system') if config.get('general', 'system') != 'None' else ''
                },
                {
                    'role': 'user',
                    'content': text
                }
            ],
            stream=True
        )
        result = ''
        for chunk in response:
            result += chunk['message']['content']
            print(chunk['message']['content'], end='')
        return result
    else:
        # 兼容 OpenAI 及类 OpenAI API 的通用调用
        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json"
        }

        # 构建消息
        messages = [
            {
                "role": "system",
                "content": config.get('general', 'system') if config.get('general', 'system') != 'None' else ""
            },
            {
                "role": "user",
                "content": text
            }
        ]

        data = {
            "model": modelName,
            "messages": messages
        }

        try:
            response = requests.post(server_url, headers=headers, json=data, timeout=30)

            if response.status_code == 200:
                json_resp = response.json()
                # 大多数类 OpenAI 接口都返回 choices[0].message.content
                content = json_resp["choices"][0]["message"]["content"]
                return content
            else:
                print(f"API Error: {response.status_code} - {response.text}")
                return None
        except Exception as e:
            print(f"Request failed: {e}")
            return None
        
def yieldAnswer(text:str):
    if not useOllama:
        yield getAnswer(text)
    
    response=ollama.chat(model=modelName,messages=[{ # type: ignore
            'role':'system',
            'text':config.get('general','system') if config.get('general','system') != 'None' else ''
            
        },
        {
            'role':'user',
            'content':text
        }

        
        ],stream=True)
    for trunk in response:
        # print(trunk['message']['content'], end='')
        yield trunk['message']['content']
