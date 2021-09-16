import sys
import os

import xlwt
import datetime
import cv2

def image_read(filename):
    img = cv2.imread(filename)  # 打开二维码图片
    det = cv2.QRCodeDetector()  # 创建二维码识别器
    val, pts, st_code = det.detectAndDecode(img)  # 识别二维码
    print(val)


if __name__ == '__main__':
    filename = 'image/7.png'
    image_read(filename)


