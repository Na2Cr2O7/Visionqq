import platform
import sys
import re

def get_windows_version_info():
    if platform.system() != "Windows":
        return None

    release = platform.release()
    version = platform.version()
    arch = platform.architecture()[0]
    
    # 提取构建号 (Build Number)
    # version 字符串格式通常为: "10.0.22631" 或 "6.1.7601"
    build_number = 0
    try:
        parts = version.split('.')
        if len(parts) >= 3:
            build_number = int(parts[2])
    except (ValueError, IndexError):
        pass

    os_name = "Unknown"
    nt_version = release # 默认使用 release 作为 NT 版本

    # 1处理 Windows 10 vs 11 (release 都是 '10')
    if release == '10':
        if build_number >= 22000:
            os_name = "11"
            nt_version = "10.0" # UA 中 Win11 依然显示 NT 10.0
        else:
            os_name = "10"
            nt_version = "10.0"
    elif release == '6.3':
        os_name = "8.1"
        nt_version = "6.3"
    elif release == '6.2':
        os_name = "8"
        nt_version = "6.2"
        
    elif release == '6.1':
        os_name = "7"
        nt_version = "6.1"
    elif release == '6.0':
        os_name = "Vista"
        nt_version = "6.0"
    elif release == '5.1':
        os_name = "XP"
        nt_version = "5.1"
    elif release == '5.0':
        os_name = "2000"
        nt_version = "5.0"
    else:
        os_name = f"Other ({release})"

    return {
        "name": os_name,
        "nt_version": nt_version,
        "build": build_number,
        "arch": arch,
        "full_version": version
    }

def generate_headers_based_on_os():
    sys_name = platform.system()
    
    if sys_name == "Windows":
        info = get_windows_version_info()
        if not info:
            # Fallback
            nt_ver = "10.0"
            arch_str = "Win64; x64"
            win_name = "10"
        else:
            nt_ver = info['nt_version']
            win_name = info['name']
            # 架构处理
            if '64' in info['arch']:
                arch_str = "Win64; x64"
            else:
                arch_str = "WOW64" if info['name'] not in ['XP', '2000'] else ""
        
        # 构建平台字符串
        if arch_str:
            platform_str = f"Windows NT {nt_ver}; {arch_str}"
        else:
            platform_str = f"Windows NT {nt_ver}"
            
        # 根据系统版本推荐合适的 Chrome 版本 (避免版本穿越)
        if win_name in ['XP', '2000', 'Vista']:
            chrome_ver = "49.0.2623.112"
        elif win_name in ['7', '8', '8.1']:
            chrome_ver = "109.0.0.0"
        else:
            chrome_ver = "134.0.0.0" # 最新
            
        ua = f"Mozilla/5.0 ({platform_str}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{chrome_ver} Safari/537.36"
        
    elif sys_name == "Darwin":
        ua = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        win_name = "macOS"
        
    elif sys_name == "Linux":
        ua = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        win_name = "Linux"
    else:
        ua = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        win_name = "Unknown (Fallback Win10)"

    return {
        "detected_os": win_name,
        "headers": {
            "user-agent": ua,
            "sec-ch-ua-platform": '"Windows"' if sys_name == "Windows" else ('"macOS"' if sys_name == "Darwin" else '"Linux"')
        }
    }

# --- 执行测试 ---
if __name__ == "__main__":
    result = generate_headers_based_on_os()
    
    print(f"检测到操作系统: {result['detected_os']}")
    print("-" * 30)
    print("生成的 Headers:")
    print(result)
    for key, value in result['headers'].items():
        print(f"{key}: {value}")
    
    # 额外打印详细调试信息 (仅 Windows)
    if platform.system() == "Windows":
        info = get_windows_version_info()
        print("-" * 30)
        print(f"[Debug] Release: {platform.release()}")
        print(f"[Debug] Version: {platform.version()}")
        print(f"[Debug] Build Number: {info['build']}")
        if info['build'] >= 22000:
            print("[Debug] 判定依据: Build >= 22000 -> Windows 11")
        else:
            print("[Debug] 判定依据: Build < 22000 -> Windows 10")