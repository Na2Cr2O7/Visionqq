
import requests
import configparser
# url = "http://localhost:8000/v1/chat/completions"

parser=configparser.ConfigParser()
parser.read('config.ini',encoding='utf8')
url=parser['general']['server_url']
model=parser['general']['modelname']
print(url)
print(model)

messages=[{"role": "user", "content": input("请输入：")}]
while True:
    payload = {
        "model": model,
        "messages": messages
    }
    

    response = requests.post(url, json=payload)


    if response.status_code == 200:
        data = response.json()
        reply = data["choices"][0]["message"]["content"]
        print("模型回复：")
        print(reply)
        messages.append({"role": "assistant", "content": reply})
        messages.append({"role": "user", "content": input("请输入：")})
    else:
        print(f"请求失败，状态码: {response.status_code}")
        print(response.text)