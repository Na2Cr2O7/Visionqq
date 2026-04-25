import ctypes
from ctypes import Structure, c_int, c_uint, c_void_p, POINTER,c_char_p
import os
import configparser
config = configparser.ConfigParser()
config.read('config.ini',encoding='utf-8')
width=config.getint('general', 'width')
height=config.getint('general', 'height')
scale=config.getfloat('general', 'scale')
# 定义 Point 结构体
class Point(Structure):
    _fields_ = [
        ("x", c_uint),
        ("y", c_uint)
    ]

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

    def is_null(self):
        return self.x == 0 and self.y == 0


# 定义 RECT 结构体（注意：Windows API 中 RECT 是 left/top/right/bottom）
class RECT(Structure):
    _fields_ = [
        ("left", c_uint),
        ("top", c_uint),
        ("right", c_uint),
        ("bottom", c_uint)
    ]

    def __repr__(self):
        return f"RECT(left={self.left}, top={self.top}, right={self.right}, bottom={self.bottom})"


visionDLL = ctypes.CDLL(os.path.abspath('Vision.dll'))
screenshotDLL = ctypes.CDLL(os.path.abspath('ScreenCapture.dll'))

# 函数1: screenshot
screenshotDLL.screenshot.argtypes = [c_int, c_int, c_int, c_int]
screenshotDLL.screenshot.restype = c_int  # 返回 1 表示失败

screenshotDLL.fullScreenshot.argtypes = []
screenshotDLL.fullScreenshot.restype = c_int

# 函数2: containsRedDot
visionDLL.containsRedDot.argtypes = [RECT,c_char_p]
visionDLL.containsRedDot.restype = Point

# 函数3: containsBlue
visionDLL.containsBlue.argtypes = [c_char_p]
visionDLL.containsBlue.restype = Point

# 函数4: point（构造 Point）
visionDLL.point.argtypes = [c_uint, c_uint]
visionDLL.point.restype = Point

# 函数5: rect（构造 RECT）
visionDLL.rect.argtypes = [c_uint, c_uint, c_uint, c_uint]
visionDLL.rect.restype = RECT

def rect(x, y, width, height):
    return visionDLL.rect(x, y, width, height)
def point(x, y):
    return visionDLL.point(x, y)
def screenshot(x, y, width, height):
    result = screenshotDLL.screenshot(x, y, width, height)
    return not result == 1
def fullScreenShot():
    result = screenshotDLL.fullScreenshot()
    return not result == 1
def containsRedDot(rect):
    point=visionDLL.containsRedDot(rect,'screenshot.png'.encode())
    return [point.x, point.y]


def containsBlue():
    point=visionDLL.containsBlue('screenshot.png'.encode())

    return [point.x, point.y]




visionDLL.matchTemplatesBegin.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
visionDLL.matchTemplatesBegin.restype = ctypes.c_int

visionDLL.matchTemplatesMultiScaleBegin.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_int]
visionDLL.matchTemplatesMultiScaleBegin.restype = ctypes.c_int

visionDLL.matchTemplateNext.argtypes = [ctypes.c_int]
visionDLL.matchTemplateNext.restype = Point

visionDLL.matchTemplateEnd.argtypes = []
visionDLL.matchTemplateEnd.restype = None

def find_templates(image_path: str, template_path: str, tolerance: int = 30,max_count=1):
    """
    在图像中查找模板匹配的位置。
    
    参数:
        image_path: 大图路径
        template_path: 模板图路径
        tolerance: 容忍度 (平均每个通道的绝对误差)。越小越严格，越大越宽松。
                   通常范围: 10 (非常严格) ~ 50 (较宽松). 默认 30.
    
    返回:
        包含所有匹配点坐标 (x, y) 的列表。如果没有找到，返回空列表。
        如果发生错误 (如文件不存在)，抛出 RuntimeError。
    """
    # 转换路径为 bytes (C 字符串)
    img_bytes = image_path.encode('utf-8')
    tpl_bytes = template_path.encode('utf-8')
    
    # 调用开始匹配
    count = visionDLL.matchTemplatesMultiScaleBegin(img_bytes, tpl_bytes, tolerance,max_count)
    
    if count < 0:
        visionDLL.matchTemplateEnd() # 清理资源
        error_map = {
            -1: "大图尺寸小于模板图尺寸 (图像太小，放不下模板)",
            -2: f"无法加载大图: {image_path} (文件不存在或格式损坏)",
            -3: f"无法加载模板图: {template_path} (文件不存在或格式损坏)"
        }
        msg = error_map.get(count, f"未知错误代码: {count}")
        raise RuntimeError(msg)
    
    results = []
    for i in range(count):
        pt = visionDLL.matchTemplateNext(i)
        results.append((pt.x, pt.y))
    
    # 清理资源
    visionDLL.matchTemplateEnd()
    
    return results
if __name__ == '__main__':
    print(fullScreenShot())
    print(visionDLL.rect(0, 0, int(width*scale),int(height*scale)))
    print(containsRedDot(visionDLL.rect(0, 0, int(width*scale),int(height*scale))))
    print(containsBlue())
    print(screenshot(0, 0, int(1920*scale),int(1080*scale)))