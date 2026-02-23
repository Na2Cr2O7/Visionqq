import http.server
import socketserver
import json
import logging
import threading
import time
import uuid
import requests
from urllib.parse import urlparse, parse_qs
import enum
import configparser

# 配置读取优化：增加异常处理
try:
    i = configparser.ConfigParser()
    i.read("config.ini", encoding="utf-8")
except Exception as e:
    raise RuntimeError(f"Failed to load config.ini: {e}")

# 常量定义
PORT = 5700
ACCESS_TOKEN = i.get("general", "access_token", fallback="").strip()
GENERAL_REQUIRED_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": f"{i['general']['version'].replace(' ', '')}",
    "X-OneBot-Version": "12",
    "X-Impl": "OneBot-12-QQ",
}
GENERAL_RETURN_HEADERS = {
    "status": "ok",
    "retcode": 0,
    "data": {},
    "message": ""
}

# 日志配置增强
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class ReusableTCPServer(socketserver.TCPServer):
    """重用 TCP 服务器类"""
    allow_reuse_address = True

class OneBotAPIHandler(http.server.BaseHTTPRequestHandler):
    """OneBot API 处理类"""
    def send_general_headers(self):
        """发送通用响应头"""
        for k, v in GENERAL_REQUIRED_HEADERS.items():
            self.send_header(k, v)

    def do_POST(self):
        """处理 POST 请求"""
        try:
            # 内容类型校验
            content_type = self.headers.get("Content-Type")
            if content_type != "application/json":
                self.send_response(400)
                self.send_general_headers()
                self.end_headers()
                self.wfile.write(b"Invalid Content-Type")
                return

            # 访问令牌校验（修复空白字符问题）
            auth_header = self.headers.get("Authorization", "").strip()
            if ACCESS_TOKEN and not auth_header.startswith(f"Bearer {ACCESS_TOKEN}"):
                self.send_response(401)
                self.send_general_headers()
                self.end_headers()
                self.wfile.write(b"Unauthorized")
                return

            # 解析请求体
            content_length = int(self.headers.get("Content-Length", 0))
            request_body = self.rfile.read(content_length)
            try:
                request_data = json.loads(request_body)
            except json.JSONDecodeError:
                self.send_response(400)
                self.send_general_headers()
                self.end_headers()
                self.wfile.write(b"Invalid JSON")
                return
            
            # 匹配动作
            action = request_data.get("action")
            logger.info(f"Received action: {action}, params: {request_data.get('params', {})}")
            
            return_data = GENERAL_RETURN_HEADERS.copy()
            
            match action:
                case "get_version":
                    return_data['data'] = {
                        "impl": "OneBot-12-QQ",
                        "version": "1.0.0",
                        "onebot_version": "12"
                    }
                case "send_message":
                    params = request_data.get("params", {})
                    detail_type = params.get("detail_type")
                    message = params.get("message")
                    
                    # 根据 detail_type 正确获取 detail_id
                    if detail_type == "group":
                        detail_id = params.get("group_id")
                    elif detail_type == "private":
                        detail_id = params.get("user_id")
                    else:
                        detail_id = None
                    
                    # send_message 直接返回完整响应结构
                    return_data = send_message(detail_type, detail_id, message)
                    
                case "get_self_info":
                    return_data['data'] = {
                        "user_id": uuid.uuid4().int >> 64,
                        "user_name": i.get('general', 'version', fallback='1.0.0'),
                        "user_displayname": ""
                    }
                case "get_friend_list":
                    return_data = get_friend_list()
                case "get_user_info":
                    params = request_data.get("params", {})
                    user_id = params.get("user_id")
                    return_data = get_user_info(user_id)
                case "get_group_info":
                    params = request_data.get("params", {})
                    group_id = params.get("group_id")
                    return_data = get_group_info(group_id)
                case "get_group_list":
                    return_data = get_group_list()
                case "upload_file":
                    params = request_data.get("params", {})
                    return_data = upload_file(params)
                case _:
                    return_data.update({
                        "status": "failed", 
                        "retcode": 10004, 
                        "message": "未知动作"
                    })
            
            # ✅ 先发送响应头，再发送响应体
            self.send_response(200)
            self.send_general_headers()
            self.end_headers()
            self.wfile.write(json.dumps(return_data).encode("utf-8"))

        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            self.send_response(500)
            self.send_general_headers()
            self.end_headers()
            self.wfile.write(b"Internal Server Error")
class DetailType(enum.Enum):
    PRIVATE = "private"
    GROUP = "group"

def send_message(detail_type: str, detail_id: str, message: str):
    """发送消息"""
    try:
        if detail_type not in ["private", "group"]:
            return basic_return(10004, "failed", message="Unsupported detail_type")
        
        if not detail_id or not message:
            return basic_return(10004, "failed", message="Missing required params")
        
        # TODO: 实现实际发送逻辑
        message_id = str(uuid.uuid4())
        
        return basic_return(
            0, 
            "ok", 
            data={"message_id": message_id, "time": time.time()},
            message=""
        )
    except Exception as e:
        logger.error(f"Error in send_message: {e}")
        return basic_return(500, "failed", message="Internal Error")


def basic_return(retcode: int, status: str, data: dict = None, message: str = ""): # type: ignore
    """构建标准返回结构"""
    return {
        "status": status,
        "retcode": retcode,
        "data": data or {},
        "message": message
    }

def get_friend_list():
    """
    获取好友列表
    返回 OneBot 12 标准格式
    """
    try:
        # TODO: 从实际数据源获取好友列表
        # 这里返回示例数据，实际使用时需要对接 QQ API 或数据库
        friend_list = [
            {
                "user_id": "123456",
                "user_name": "我是大笨蛋",
                "user_displayname": "",
                "user_remark": "一个自称大笨蛋的人"
            },
            {
                "user_id": "654321",
                "user_name": "我是小笨蛋",
                "user_displayname": "",
                "user_remark": "一个自称小笨蛋的人"
            }
        ]
        
        return {
            "status": "ok",
            "retcode": 0,
            "data": friend_list,
            "message": ""
        }
        
    except Exception as e:
        logger.error(f"Error in get_friend_list: {e}")
        return {
            "status": "failed",
            "retcode": 500,
            "data": [],
            "message": "Internal Error"
        }
def get_user_info(user_id: str):
    """获取用户信息"""
    try:
        if not user_id:
            return {
                "status": "failed",
                "retcode": 10004,
                "data": {},
                "message": "Missing user_id"
            }
        
        # TODO: 从实际数据源获取，这里返回示例数据
        return {
            "status": "ok",
            "retcode": 0,
            "data": {
                "user_id": user_id,
                "user_name": "我是大笨蛋",
                "user_displayname": "",
                "user_remark": "一个自称大笨蛋的人"
            },
            "message": ""
        }
    except Exception as e:
        logger.error(f"Error in get_user_info: {e}")
        return {
            "status": "failed",
            "retcode": 500,
            "data": {},
            "message": "Internal Error"
        }
def get_group_info(group_id: str):
    """获取群信息"""
    try:
        if not group_id:
            return {
                "status": "failed",
                "retcode": 10004,
                "data": {},
                "message": "Missing group_id"
            }
        
        # TODO: 从实际数据源获取，这里返回示例数据
        return {
            "status": "ok",
            "retcode": 0,
            "data": {
                "group_id": group_id,
                "group_name": "一群大笨蛋"
            },
            "message": ""
        }
    except Exception as e:
        logger.error(f"Error in get_group_info: {e}")
        return {
            "status": "failed",
            "retcode": 500,
            "data": {},
            "message": "Internal Error"
        }
    
def get_group_list():
    """获取群列表"""
    try:
        # TODO: 从实际数据源获取，这里返回示例数据
        group_list = [
            {
                "group_id": "123456",
                "group_name": "一群大笨蛋"
            },
            {
                "group_id": "654321",
                "group_name": "一群大笨蛋2群"
            }
        ]
        
        return {
            "status": "ok",
            "retcode": 0,
            "data": group_list,
            "message": ""
        }
    except Exception as e:
        logger.error(f"Error in get_group_list: {e}")
        return {
            "status": "failed",
            "retcode": 500,
            "data": [],
            "message": "Internal Error"
        }
    
def upload_file(params: dict):
    """上传文件"""
    try:
        file_type = params.get("type")
        file_name = params.get("name")
        
        if not file_type or not file_name:
            return {
                "status": "failed",
                "retcode": 10004,
                "data": {},
                "message": "Missing type or name"
            }
        
        # 根据 type 处理不同上传方式
        if file_type == "url":
            url = params.get("url")
            headers = params.get("headers", {})
            if not url:
                return {
                    "status": "failed",
                    "retcode": 10004,
                    "data": {},
                    "message": "Missing url for type=url"
                }
            # TODO: 从 URL 下载文件
            logger.info(f"Downloading file from URL: {url}")
            
        elif file_type == "path":
            path = params.get("path")
            if not path:
                return {
                    "status": "failed",
                    "retcode": 10004,
                    "data": {},
                    "message": "Missing path for type=path"
                }
            # TODO: 从路径读取文件
            logger.info(f"Reading file from path: {path}")
            
        elif file_type == "data":
            data = params.get("data")
            sha256 = params.get("sha256")
            if not data:
                return {
                    "status": "failed",
                    "retcode": 10004,
                    "data": {},
                    "message": "Missing data for type=data"
                }
            # TODO: 处理二进制数据
            logger.info(f"Processing file data, sha256: {sha256}")
            
        else:
            return {
                "status": "failed",
                "retcode": 10004,
                "data": {},
                "message": f"Unsupported file type: {file_type}"
            }
        
        # 生成 file_id
        file_id = str(uuid.uuid4())
        
        # TODO: 实际存储文件逻辑
        
        return {
            "status": "ok",
            "retcode": 0,
            "data": {
                "file_id": file_id
            },
            "message": ""
        }
        
    except Exception as e:
        logger.error(f"Error in upload_file: {e}")
        return {
            "status": "failed",
            "retcode": 500,
            "data": {},
            "message": "Internal Error"
        }
