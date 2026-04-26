from typing import List
from chatContent import ChatContent
from extensionAPIs import *

MessageBox("awsddsfdgsdfg")


def after_receiving_messages(messages: List[ChatContent])  -> List[ChatContent]:
    # 信息被处理后调用
    # 参数
    # messages : 收到的信息
    # 返回值
    # 消息列表
    MessageBox("WDAEFDSFDGFsedff")
    for message in messages:
        MessageBox(message.report())
    return messages

def before_sending_the_message_by_AI_generated(answer:str) -> str:
    # 信息被发送前调用
    # 参数
    # answer : 获取的答案
    # 返回值
    # 对答案的修改,直接返回答案则无修改
    # 必须有返回值

    MessageBox(answer)
    return answer



description=\
'''在这里填写扩展的描述


'''