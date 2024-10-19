from cnocr import CnOcr

def coordinate(image_path, keyword):
    center_x, center_y = 0, 0
    ocr = CnOcr()
    file = image_path
    res = ocr.ocr(file)
    for item in res:
        # print(item)  # item 外层是列表, 内层是字典, 字典中position是array
        if keyword in item.get("text", ""):
            print(item.get("text"))
            # 获取位置数组（我们只需要前三个点来计算中心）
            position_array = item['position']
            # 计算矩形的中心（注意：这里我们计算的是基于前三个点的矩形的几何中心）
            # 左上角 (x1, y1), 右上角 (x2, y2), 右下角 (x3, y3)
            x1, y1 = position_array[0]
            # x2, y2 = position_array[1]
            x3, y3 = position_array[2]
            # 矩形的中心可以通过计算对角线的中点来得到
            # 但由于我们有一个额外的点（闭合多边形的第四个点），我们忽略它
            center_x = (x1 + x3) / 2.0  # 或者使用 (x1 + x2 + x3 - x1 (因为x4=x1)) / 3.0，但这里x2和x1的x坐标相同，所以简化为(x1 + x3) / 2
            center_y = (y1 + y3) / 2.0  # 同理，y2和y1的y坐标也相同
            print(center_x, center_y)
    return center_x, center_y

#
# 以下供测试用
# path = r"C:\Users\Laythy\Desktop\py_auto_ocr_coordinates\xxt-shots\382.png"
# coordinate(path, "4.1")
# 4.1《战舰波将金号》赏机
# 2073.5 1334.0
#
