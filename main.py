import sys
import os

import xlwt
import datetime
import cv2
from pyzbar import pyzbar
import csv
import time

def read_invoice_txt(path="invoice.txt"):
    with open(path) as f:
        invocies = f.readlines()
        f.close()
        return invocies

def handle_invoice(invocie_list):
    invocie_list = [iv.strip(',\n').split(",") for iv in invocie_list ]
    # invocie_list = [iv[-2][-6:] for iv in invocie_list]
    return invocie_list

def excel(iv_list):
    workbook = xlwt.Workbook(encoding='utf-8')  # 新建工作簿
    sheet1 = workbook.add_sheet("增值税普票")  # 新建sheet
    for index, iv in  enumerate(iv_list):
        sheet1.write(index, 0, index+1)  # 第一行第一列序号
        sheet1.write(index, 1, iv[1])  # 第一行第2列 发票类型
        sheet1.write(index, 2, iv[2])  # 第一行第3列 发票代码
        sheet1.write(index, 3, iv[3])  # 第一行第3列 发票号码
        sheet1.write(index, 4, 1)  # 第一行第3列 发票页码
        sheet1.write(index, 5, datetime.datetime.strptime(iv[5], "%Y%m%d").strftime("%Y/%m/%d"))  # 第一行第3列 开票时间
        sheet1.write(index, 6, iv[6][-6:])  # 第一行第3列 后六位
        sheet1.write(index, 7, "91310115MA1K470G91")  # 第一行第3列 后六位
        # sheet1.write(index, 8, iv[4])  # 第一行第8列 金额
    workbook.save(r'增值税普票.xls')  # 保存

def image_read():
    image_list = []
    info_list = []
    for filepath, dirnames, filenames in os.walk(r'image'):
        for filename in filenames:
            image_list.append(os.path.join(filepath, filename))
    for i in image_list:
        img = cv2.imread(i)  # 打开二维码图片
        det = cv2.QRCodeDetector()  # 创建二维码识别器
        val, pts, st_code = det.detectAndDecode(img)  # 识别二维码
        info_list.append(val)
    return info_list
    # img = cv2.imread("test.PNG")  # 打开二维码图片
    # det = cv2.QRCodeDetector()  # 创建二维码识别器
    # val, pts, st_code = det.detectAndDecode(img)  # 识别二维码
    # print(val)  # 打印识别出的链接

def camera_read():
    found = set()
    capture = cv2.VideoCapture(0)
    PATH = "test.csv"
    while(1):
        ret,frame = capture.read()
        test = pyzbar.decode(frame)
        for tests in test:
            testdate = tests.data.decode('utf-8')
            if testdate not in found:
                print(testdate)
                with open(PATH,'a+') as f:
                    csv_write = csv.writer(f)
                    date = [testdate]
                    csv_write.writerow(date)
                found.add(testdate)
                time.sleep(1)
            else:
                print("请扫描下一张")
                # time.sleep(5)
        cv2.imshow('Test',frame)
        if cv2.waitKey(1) == ord('q'):
            break
    return found


if __name__ == '__main__':
    info_list = camera_read()
    print("found", info_list)
    # ivstr = read_invoice_txt()
    iv_list = handle_invoice(info_list)
    print(iv_list)
    excel(iv_list)
