from extensionAPIs import *



def after_receiving_messages(messages: List[ChatContent]):
    # 信息被处理后调用
    # 参数
    # messages : 收到的信息
    # print(f'after_receiving_messages({messages})')
    text=''
    for i in messages:
        text+=i.report()+'\n'
    summary=get_answer_as_string(f'总结消息:{text}',False)
    notify(str(summary),"消息总结")
    return messages




description=\
'''自动总结消息扩展：收到消息后，使用消息框显示总结的消息
'''