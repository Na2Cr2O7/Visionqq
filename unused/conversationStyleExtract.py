indentificationString='⨋'

import re
from dataclasses import dataclass
from typing import List
import os
from urllib.parse import unquote

from chatContent import ChatContent





def extract_image_paths(text: str) -> tuple[List[str], str]:
    """
    从文本中提取所有 <img src="..."> 的本地路径，并返回：
    - 提取到的图片路径列表（已处理为 os.path 可用格式）
    - 剩余的纯文本内容（不含 img 标签）
    """
    img_paths = []
    # 匹配 <img ... src="...">，支持单引号或双引号，忽略大小写
    img_tag_pattern = re.compile(r'<img\s+[^>]*?src\s*=\s*[\'"]([^\'"]+)[\'"][^>]*>', re.IGNORECASE)
    
    # 查找所有匹配的 src
    matches = list(img_tag_pattern.finditer(text))
    
    for match in matches:
        src = match.group(1)
        # 如果是 file:// 开头，去掉协议头
        if src.startswith('file://'):
            path = src[7:]  # 移除 'file://'
            # Windows 路径可能是 /D:/... 或 D:\...，统一处理
            if path.startswith('/') and len(path) >= 3 and path[2] == ':':
                # 例如：/D:/folder/file.jpg → D:/folder/file.jpg
                path = path[1:]
            # URL 解码（处理 %20 等）
            path = unquote(path)
            # 转换为系统路径分隔符（Windows 用 \，但 Python 接受 / 和 \）
            # 为了 os.path 兼容性，我们保留原样或标准化
            normalized_path = os.path.normpath(path)
            img_paths.append(normalized_path)
    
    # 移除所有 <img ...> 标签，只保留纯文本
    clean_text = img_tag_pattern.sub('', text).strip()
    
    return img_paths, clean_text


def parse_chat_log(chat_str: str) -> List[ChatContent]:
    # 匹配消息头：任意非空字符直到 ": MM-dd HH:mm:ss"
    header_pattern = re.compile(r'^(.+?):\s+(\d{2}-\d{2}\s+\d{2}:\d{2}:\d{2})$')
    lines = chat_str.splitlines()
    messages = []
    i = 0

    while i < len(lines):
        line = lines[i].rstrip()
        if not line:
            i += 1
            continue

        header_match = header_pattern.match(line)
        if header_match:
            username = header_match.group(1)
            time_str = header_match.group(2)
            i += 1
            content_lines = []

            # 收集后续非头部行
            while i < len(lines):
                next_line = lines[i].rstrip()
                if not next_line:
                    i += 1
                    continue
                if header_pattern.match(next_line):
                    break
                content_lines.append(lines[i])
                i += 1

            raw_text = '\n'.join(content_lines)
            # 提取图片路径并清理文本
            image_paths, clean_text = extract_image_paths(raw_text)


            messages.append(ChatContent(
                username=username,
                imagePaths=image_paths,
                text=clean_text,
                time=time_str,
                ownByMyself=( indentificationString in raw_text)
            ))
        else:
            i += 1

    return messages

extract=parse_chat_log

# ===== 示例测试 =====
if __name__ == "__main__":
    test_log = '''Na₂IrCl₆•6H₂O: 11-01 08:12:19
<img src="file://D:\\Documents\\Tencent Files\\435345435\\nt_qq\\nt_data\\Emoji\\emoji-recv\\2025-11\\Ori\\eef841f590c5d7b664566c97e62c429a.jpg" />
内容内容内容内容内容内容内容

3454345: 11-25 08:10:36
普通文字，没有图片

2435435646: 11-25 08:11:00
<img src="file:///C:/Users/Admin/Pictures/test%20image.png" />
还有这张图！'''

    parsed = parse_chat_log(test_log)
    for msg in parsed:
        print("=== 消息 ===")
        print(str(msg))
        print("图片路径:", msg.imagePaths)
        print("Report:\n", msg.report())
        print()

