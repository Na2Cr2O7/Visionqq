import importlib
import os
from colorama import Fore
from typing import List,Any
from chatContent import ChatContent
import logging
extensions=[]
extension_names=[]
warn=False
os.makedirs('Extensions',exist_ok=True)

print()
print()
print()
print()
for mod in os.listdir('Extensions'):
    if mod.endswith('.py'):
        if not warn:
            warn=True
            print(f"{Fore.YELLOW}随意加载扩展可能导致运行缓慢，程序故障，甚至有可能破坏文件{Fore.RESET}")
        print(f"正在加载\t{mod}",end='\r')
        try:
            extension_names.append(mod[:-3])
            extensions.append(importlib.import_module('Extensions.'+mod[:-3]))
            print(f"{Fore.GREEN}_已加载\t\t{mod}{Fore.RESET}\t{extensions[-1].description.replace('\n','')}")
        except Exception as e:
            print(f'{Fore.YELLOW}加载错误\t{mod}\t{e}{Fore.RESET}')
print()
print()
print()
print()



def callEveryExtension(func_name,*args,**kwargs)->Any:
    result=args
    for mod_name,mod in zip(extension_names,extensions):
        try:
            func=getattr(mod,func_name)
            # 检查获取的对象是否为可调用函数
            if callable(func):
                # 判断result是否可以解包
                if isinstance(result, (list, tuple)):
                    result2=func(*result,**kwargs)
                else:
                    result2=func(result,**kwargs)
                if result2 is not None:
                    result=result2
                logging.debug(f'{mod_name}.{func_name} called successfully')
            else:
                logging.warning(f'{mod_name}.{func_name} is not callable')
        except AttributeError as e:
            # 忽略没有该函数的模块，这不是错误情况
            logging.debug(f'Function {func_name} not found in {mod_name}, skipping')
        except Exception as e:
            logging.error(f'Error calling {mod_name}.{func_name}: {e}',exc_info=True)
    return result



if __name__=='__main__':
    callEveryExtension('after_receiving_messages',[ChatContent('',[],'','',True)])
    callEveryExtension('after_screenshot')
    callEveryExtension('before_sending_the_message_by_AI_generated','1')
    callEveryExtension('after_screenshot')

# def after_receiving_messages(messages: List[ChatContent]) -> None:
#     # 信息被处理后调用
#     # 参数
#     # messages : 收到的信息
#     pass

# def before_sending_the_message_by_AI_generated(answer:str) -> str:
#     # 信息被发送前调用
#     # 参数
#     # answer : 获取的答案
#     # 返回值
#     # 对答案的修改,直接返回答案则无修改
#     # 必须有返回值
#     return answer

# def after_screenshot() -> None:
#     # 截图后调用
#     # 截图保存在当前目录下的screenshot.bmp
#     pass


# for mod_name,mod in zip(mod_names,mods):
#     print(mod_name)
#     print(mod.description)
#     mod.after_receiving_messages(None)
#     mod.after_screenshot()
#     mod.before_sending_the_message_by_AI_generated('')
    

