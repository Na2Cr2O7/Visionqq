from configparser import ConfigParser
import threading
from onebotcore import *
def useOneBot():
    i=ConfigParser()
    i.read("config.ini",encoding="utf-8")
    if i['general']['server_url'].lower()=='onebot':
        return True
    return False
# 启动服务器
def start_server():
    if not useOneBot():
         return 
    try:
        with ReusableTCPServer(("", PORT), OneBotAPIHandler) as httpd:
                logger.info(f"🤖 OneBot API Server running on port {PORT}")
                logger.info(f"📡 Access Token: {'Enabled' if ACCESS_TOKEN else 'Disabled'}")
                httpd.serve_forever()
    except KeyboardInterrupt:
        logger.info("Server stopped by user.")
    except Exception as e:
        logger.error(f"Failed to start server: {e}")

threading.Thread(target=start_server, daemon=True).start()
logger.info("启动服务器")
