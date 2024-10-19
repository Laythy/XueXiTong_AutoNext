# pyautogui库截取屏幕截图和模拟鼠标点击, datetime库获取时间戳, time库sleep, Image和imagehash库用于图片hash比较, myocr是我自己的.py文件
import pyautogui
import datetime
import time
from PIL import Image
import imagehash
import myocr
print("【注意】必须将浏览器全屏,视频不全屏,分辨率2k(2560*1440),windows显示设置缩放150%,在下面输入章节号后,请在10秒内切到视频播放页并播放视频.")
words = input("打开并播放你要看的章节, 并输入当前的章节号(如3.1, 4.5等):")  # 开始的章节

# 获取屏幕尺寸  
screen_width, screen_height = pyautogui.size()
# 计算每个部分的尺寸(此处截取整个屏幕1/9, x, y各1/3)
part_width = screen_width // 3
part_height = screen_height // 3
# 计算中间部分的坐标  
middle_left = part_width  # 中间左边框的x坐标  
middle_top = part_height  # 中间顶部的y坐标  
middle_right = middle_left + part_width  # 中间右边框的x坐标  
middle_bottom = middle_top + part_height  # 中间底部的y坐标

filepath = r"C:\Users\Laythy\Desktop\py_auto_next_video\shots\\"

def compare_images(image_path1, image_path2):
    # 打开图片
    image1 = Image.open(image_path1)
    image2 = Image.open(image_path2)
    # 生成图片的哈希值
    hash1 = imagehash.average_hash(image1)
    hash2 = imagehash.average_hash(image2)
    # 计算哈希值之间的差异
    difference = hash1 - hash2
    # 打印哈希值和差异
    # print(f"Hash1: {hash1}")
    # print(f"Hash2: {hash2}")
    # print(f"Difference: {difference}")
    # 计算相似度百分比并返回
    similarity_percent = (1 - (difference / 64)) * 100
    # similarity_percent = (1 - (difference / len(hash1.hash.bits) ** 0.5)) * 100  # 这句报错 没有.bits attribution(属性)
    return similarity_percent

def ocr(timestamp, keyword):
    if keyword != "视频":
        keyword = str('%.1f' % (float(keyword)+0.1))
    print("keyword:" + keyword + "\n")
    # 下面3个print是做测试用的
    # print("ocr - 1")
    screen = pyautogui.screenshot(region=(0, 0, 2560, 1440))    # region四个参数依次是: 起点x 起点y 宽(delta x) 高(delta y)
    # print("ocr - 2")
    time.sleep(1)
    screen.save(filepath + str(timestamp) + "-OCR.png")
    # print("ocr - 3")
    x, y = myocr.coordinate(filepath + str(timestamp) + "-OCR.png", keyword)     # 调用
    return x, y

count = 1  # 截图第一张就是count 1
while True:
    stamp = int(datetime.datetime.now().timestamp())
    while stamp % 20 == 0:      # 这里是检测间隔, 60秒. 如要修改, 下面的 stamp - 60 的 60 也要一同修改.
        # 返回上一张图片, 并截取新屏幕
        stamp_before = stamp - 20
        screenshot = pyautogui.screenshot(region=(middle_left, middle_top, part_width, part_height))
        # 保存图片
        screenshot.save(filepath+str(stamp)+".png")
        print("检测计数: " + str(count) + "\n时间戳:" + str(stamp))
        # 比较图片
        if count != 1:
            sim_percent = compare_images(filepath+str(stamp_before)+".png", filepath+str(stamp)+".png")
            print("相似性: " + str(sim_percent) + "\n")
            if sim_percent > 95:
                words = str('%.1f' % (float(words)+0.1))
                coordinate_x, coordinate_y = ocr(stamp, words)
                # 此处截全屏, 使用OCR识别出"x.x xxxxx章节", 获取这几个字的中心坐标, 然后模拟鼠标左键点击
                if coordinate_x == 0 or coordinate_y == 0:
                    # 注意这一步, 在末章跳下一首章时, 不用+".1", 因为在下一个coordinate x y = ocr()中 ocr()函数会自动+1
                    # words = str('%.1f' % float(str(int(str(words).split(".")[0])+1)+".1"))    # 若对应章节如2.6没找到, 则换下一章节第一课3.1.
                    words = str('%.1f' % float(int(str(words).split(".")[0]) + 1))
                    print("新的章节号是:"+str(words)+"\n")
                coordinate_x, coordinate_y = ocr(stamp, words)
                # count = 0  # 无奈之举,此bug以后再修

                pyautogui.click(coordinate_x, coordinate_y)     # 点击进入下一节课
                # 下面再截图, 识别"视频"二字. 点击.
                time.sleep(2)  # sleep 2秒 让网页加载 防止无法识别到"视频"字样
                coordinate_x, coordinate_y = ocr(stamp, "视频")
                pyautogui.click(coordinate_x, coordinate_y)  # 点击进入视频页
                # 下面点击视频画面中间的播放按钮, 播放按钮位置是固定的(对于2k屏150%是x 949, y 957)
                time.sleep(5)       # sleep 5秒 让视频加载 防止又识别到相似度大于98.
                pyautogui.click(949, 957)
        else:
            print("这是第一次截屏检测, 不存在与上一张的相似性.\n")
            words = str('%.1f' % (float(words)-0.1))    # 修复未知bug: 第一次会跳转两章
        # sleep3秒, 防止重复检测. count计数+1. 更新新的时间戳.
        count += 1
        time.sleep(3)
        stamp = int(datetime.datetime.now().timestamp())
    time.sleep(0.1)
