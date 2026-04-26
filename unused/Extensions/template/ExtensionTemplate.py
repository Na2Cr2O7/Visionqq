from typing import List
from chatContent import ChatContent
from extensionAPIs import *

###################
# Vision QQ 扩展
# 在这里编写自定义的代码
###################

def after_receiving_messages(messages: List[ChatContent])  -> None:
    # 信息被处理后调用
    # 参数
    # messages : 收到的信息
    print(f'after_receiving_messages({messages})')

def before_sending_the_message_by_AI_generated(answer:str) -> str:
    # 信息被发送前调用
    # 参数
    # answer : 获取的答案
    # 返回值
    # 对答案的修改,直接返回答案则无修改
    # 必须有返回值
    print(f'before_sending_the_message_by_AI_generated({answer})')
    return answer

def after_screenshot() -> None:
    # 截图后调用
    # 截图保存在当前目录下的screenshot.bmp
    print('after_screenshot()')
    pass


description=\
'''在这里填写扩展的描述


'''