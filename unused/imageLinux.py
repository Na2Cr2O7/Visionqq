
import configparser
config = configparser.ConfigParser()
config.read('config.ini',encoding='utf-8')
width=config.getint('general', 'width')
height=config.getint('general', 'height')
scale=config.getfloat('general', 'scale')
from PIL import Image
from PIL import ImageGrab
SCREENSHOT_NAME='screenshot.png'
class RECT(object):
    left = 0
    top = 0
    right = 0
    bottom = 0
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom
def rect(x, y, width, height):
    return RECT(x,y,width+x,height+y)
def screenshot(x, y, width, height):
    img =  ImageGrab.grab()
    img = img.crop((x, y, x + width, y + height))
    img.save(SCREENSHOT_NAME)
    return img
def fullScreenShot():
    img = ImageGrab.grab()
    img.save(SCREENSHOT_NAME)
    return img

def containsRedDot(rect):
    RED_DOT=(247,76,48)
    image=Image.open(SCREENSHOT_NAME)
    width=image.width
    height=image.height
    for x in range(rect.left,rect.right):
        for y in range(rect.top,rect.bottom):
            pixel=image.getpixel((x,y))
            if pixel==RED_DOT:
                return [x,y]
    return [0,0]

def containsBlue():
    BLUE=(0,153,255)
    fullScreenShot()
    image=Image.open(SCREENSHOT_NAME)
    width=image.width
    height=image.height
    for x in range(width):
        for y in range(height):
            pixel=image.getpixel((x,y))
            if pixel==BLUE:
                return [x,y]
    return [0,0]


import cv2
import numpy as np
from typing import List, Tuple

import cv2
import numpy as np
from typing import List, Tuple

def find_templates(image_path: str, template_path: str, tolerance: int = 30, max_count: int = 5) -> List[Tuple[int, int]]:
    """
    基于 OpenCV 底层加速的多尺度模板匹配。
    
    核心逻辑：
    1. 使用 cv2.matchTemplate (C++ 底层，极速)。
    2. 将 'tolerance' (平均绝对误差) 转换为 TM_SQDIFF 或 TM_CCORR 的阈值。
       这里我们使用 TM_SQDIFF (平方差)，因为它直接对应误差概念。
       关系推导：MAE = Sum(|I-T|) / N. 
       SQDIFF = Sum((I-T)^2). 
       虽然数学上不严格等价，但在工程上，设定一个 SQDIFF 的阈值效果非常接近。
       或者，为了严格符合 '平均绝对误差'，我们可以使用 TM_SAD (Sum of Absolute Differences)，
       但 OpenCV 的 matchTemplate 不直接支持 TM_SAD 作为方法标识符用于多通道？
       实际上 OpenCV 支持 TM_SQDIFF, TM_CCORR, TM_CCOEFF 等。
       
       【修正策略】：为了严格匹配 "平均绝对误差" 的定义，且保持高速：
       我们依然使用 cv2.matchTemplate 获取候选区，然后用 numpy 向量化操作快速验证 MAE。
       或者，直接使用 TM_SQDIFF 并估算阈值。
       
       为了最快速度且符合直觉，本函数使用 TM_SQDIFF (值越小越好)。
       阈值换算经验公式：Threshold_SQDIFF ≈ (Tolerance_MAE ^ 2) * PixelCount * Channels
    """
    
    # 1. 读取图像
    img = cv2.imread(image_path)
    tpl = cv2.imread(template_path)
    
    if img is None or tpl is None:
        raise RuntimeError("无法加载图片")

    # 确保通道一致 (转为 BGRA 或 BGR)
    if img.shape[2] != tpl.shape[2]:
        # 简单处理：都转为 3 通道 BGR
        if img.shape[2] == 4: img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
        if tpl.shape[2] == 4: tpl = cv2.cvtColor(tpl, cv2.COLOR_BGRA2BGR)
        # 如果还有不一致，强制转换
        if img.shape[2] != tpl.shape[2]:
             if img.shape[2] > tpl.shape[2]: img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
             else: tpl = cv2.cvtColor(tpl, cv2.COLOR_BGR2GRAY)
    
    img_h, img_w = img.shape[:2]
    tpl_h, tpl_w = tpl.shape[:2]
    channels = img.shape[2] if len(img.shape) > 2 else 1
    
    final_results = []
    
    # 多尺度因子 (照搬 C++ 顺序)
    factors = [1.0, 1.5, 0.5, 0.6, 0.7, 0.8, 0.9, 1.1, 1.2, 1.3, 1.4, 1.6, 1.7, 1.8, 1.9, 2.0]
    
    # 预计算全局阈值 (基于平方差估算)
    # MAE = Sum(|diff|) / N  => Sum(|diff|) = MAE * N
    # SQDIFF = Sum(diff^2). 假设 diff 分布均匀，SQDIFF ≈ N * (MAE^2) * k (k为系数，通常取1-2作为保守估计)
    # 这里我们做一个宽松的转换，稍后可以用 numpy 二次筛选
    pixel_count = tpl_h * tpl_w * channels
    # 经验阈值：如果 tolerance=30, 则单个像素误差 30。平方后 900。
    # 总误差阈值 = 900 * pixel_count. 
    # 为了防止误杀，我们稍微放大一点，或者在后续步骤用 numpy 精确计算 MAE 过滤。
    # 策略：先用 matchTemplate 找出所有“可能”的低分点，再用 numpy 精确计算 MAE 过滤。
    

    for factor in factors:
        cur_w = int(tpl_w * factor)
        cur_h = int(tpl_h * factor)
        
        if cur_w > img_w or cur_h > img_h:
            continue
            
        # 缩放模板
        resized_tpl = cv2.resize(tpl, (cur_w, cur_h))
        
        # 使用 TM_SQDIFF (值越小匹配度越高，0 表示完全相同)
        res = cv2.matchTemplate(img, resized_tpl, cv2.TM_SQDIFF)
        
        # 计算当前尺度下的最大允许平方差阈值
        # 为了严谨，我们先不设死阈值，而是提取所有局部最小值，然后排序，最后用 numpy 算 MAE 过滤
        # 但为了速度，我们设定一个宽松的上限，避免处理全图
        max_sqdiff_threshold = (tolerance * 1.5) ** 2 * pixel_count * (factor ** 2) # 粗略估算
        
        # 查找所有小于阈值的位置
        # np.where 返回的是数组
        loc = np.where(res <= max_sqdiff_threshold)
        
        candidates = []
        for pt in zip(*loc[::-1]): # pt = (x, y)
            score_sqdiff = res[pt[1], pt[0]]
            candidates.append((pt[0], pt[1], score_sqdiff, cur_w, cur_h))
        
        # 如果没有候选点，跳过
        if not candidates:
            continue
            
        # 【关键优化】按分数排序，先处理最好的点
        candidates.sort(key=lambda x: x[2])
        
        # 对当前尺度的候选点进行精确 MAE 验证和去重
        for x, y, sq_score, w, h in candidates:
            if len(final_results) >= max_count:
                break
                
            # 1. 精确计算 MAE (使用 Numpy 向量化，极快)
            # 提取 ROI
            roi = img[y:y+h, x:x+w]
            # 计算绝对差之和
            diff = cv2.absdiff(roi, resized_tpl)
            mae = np.mean(diff)
            
            if mae > tolerance:
                continue # 精确验证失败，跳过
            
            # 2. 去重检查 (复用之前的逻辑)
            is_dup = False
            dedup_dist = int(w * 0.2)
            if dedup_dist < 5: dedup_dist = 5
            
            for exist_x, exist_y in final_results:
                if abs(x - exist_x) < dedup_dist and abs(y - exist_y) < dedup_dist:
                    is_dup = True
                    break
            
            if not is_dup:
                final_results.append((x, y))
        
        if len(final_results) >= max_count:
            break

    return final_results


# ================= 使用示例与测试 =================
if __name__ == "__main__":
    import os

    # 生成测试数据
    src_file = "VisionQQ_C/x64/Release/gb.png"
    tpl_file = "VisionQQ_C/x64/Release/copy.png"

    print("生成测试图片...")
    # 创建背景 (蓝色)
    bg = np.zeros((400, 600, 3), dtype=np.uint8)
    bg[:] = [255, 0, 0] 
    
    # 创建一个红色方块目标 (会有轻微噪点)
    target_area = bg[100:150, 200:250]
    target_area[:] = [0, 0, 255] 
    # 加一点噪点模拟真实场景
    noise = np.random.randint(-10, 10, target_area.shape, dtype=np.int16)
    target_area = np.clip(target_area.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    bg[100:150, 200:250] = target_area
    
    # 再创建一个放大的目标
    target_area2 = bg[250:350, 400:500]
    # 手动绘制一个放大的红色块
    cv2.rectangle(bg, (400, 250), (500, 350), (0, 0, 255), -1)
    
    cv2.imwrite(src_file, bg)
    
    # 创建标准模板 (50x50 红色)
    tpl = np.zeros((50, 50, 3), dtype=np.uint8)
    tpl[:] = [0, 0, 255]
    cv2.imwrite(tpl_file, tpl)

    try:
        print(f"\n开始搜索 (Tolerance=30)...")
        # 调用函数
        points = find_templates(
            image_path=src_file, 
            template_path=tpl_file, 
            tolerance=30,  # 允许平均每个通道 30 的误差
            max_count=5
        )
        
        print(f"找到 {len(points)} 个点: {points}")
        
        # 可视化验证
        res_img = cv2.imread(src_file)
        for i, (x, y) in enumerate(points):
            # 由于不知道具体尺度，这里画一个估计的框 (假设是原模板大小，实际可能不准，仅作位置标记)
            # 在实际应用中，find_templates 返回了坐标，通常配合其他逻辑使用
            cv2.circle(res_img, (x + 25, y + 25), 5, (0, 255, 0), -1)
            cv2.putText(res_img, f"#{i}", (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        
        cv2.imshow("Result", res_img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    except RuntimeError as e:
        print(f"错误: {e}")
    finally:
        # 清理测试文件
        if os.path.exists(src_file): os.remove(src_file)
        if os.path.exists(tpl_file): os.remove(tpl_file)