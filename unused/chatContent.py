import os
from typing import List



class ChatContent:

    username='' # 用户名
    imagePaths=[] # 图片路径
    text=''  #聊天内容
    time='' #时间
    ownByMyself=False #是否为AI发送
    def __init__(self, username: str, imagePaths: List[str], text: str, time: str,ownByMyself: bool):
        self.username = username
        self.imagePaths = imagePaths
        self.text = text
        self.time = time
        self.ownByMyself = ownByMyself
    def report(self) -> str:
        return f'{'[你]' if self.ownByMyself else ''}{self.username}: {self.text if self.text else "【空】"}\n{self.time}\n 图片：{[image for image in self.imagePaths if os.path.exists(image)] if [image for image in self.imagePaths if os.path.exists(image)] != [] else "无" }'
    # 
    def __str__(self) -> str:
        if not self.ownByMyself:
            return f'{self.username}:{self.text if self.text else "【空】"}'
        #[{self.time}]
        else:
            return f'{self.text if self.text else "【空】"}'