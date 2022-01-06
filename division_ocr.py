#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/28 14:59 
# @Author  : xudh
# @File    : main2.py 
# @Software: PyCharm
# @Function: 使用波峰波谷的方法，分割字符


import cv2 as cv
import os


def divisionOCR(ocr_folder, division_folder, prefix_name):
    #add_number由于图像的命名都是以数字 counterfeit
    if not os.path.exists(division_folder):
        os.mkdir(division_folder)
    for sub in os.listdir(ocr_folder):
        img_path = os.path.join(ocr_folder, sub)
        save_path = os.path.join(division_folder, prefix_name + sub[:-4])
        #print(img_path)
        image = cv.imread(img_path)
        gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
        ret, binary = cv.threshold(gray, 0, 255, cv.THRESH_BINARY + cv.THRESH_OTSU)

        element = cv.getStructuringElement(cv.MORPH_RECT, (5, 5))
        closeimg = cv.morphologyEx(binary, cv.MORPH_CLOSE, element)

        rows = closeimg.shape[0]
        cols = closeimg.shape[1]

        rowsSum = []
        for row in range(rows):
            rsum = 0
            for col in range(cols):
                value = closeimg[row, col]
                rsum += value
            rowsSum.append(rsum)

        colsSum = []
        for col in range(cols):
            csum = 0
            for row in range(rows):
                value = closeimg[row, col]
                csum += value
            colsSum.append(csum)

        rowbegin = 0
        rowend = 0
        brow = False

        for row in range(rows):
            if rowsSum[row] == 0:  # rowsSum[row]是numpy.int類型因此不能用is
                continue
            if brow is False:
                rowbegin = row  # 行起始
                brow = True
            rowend = row

        colarray2 = []
        colarray = []
        bcol = False
        colnum = 0
        for col in range(cols):
            if bcol is False and colsSum[col] > 1000:
                colarray2.append(col)
                bcol = True
                # print(f"第{colnum}个起始点：{col}")

            if bcol is True and colsSum[col] < 1000:
                colarray2.append(col)
                colarray.append(colarray2)
                colarray2 = []
                bcol = False
                # print(f"第{colnum}个结束点：{col}")
                colnum += 1

            if (col == (cols - 1)) and (bcol is True) and (colsSum[col] > 1000):
                colarray2.append(col)
                colarray.append(colarray2)
                colarray2 = []
                bcol = False
                # print(f"最后一个结束点{colnum}：{col}")

        rectimage = image.copy()
        rowbegin = max(rowbegin - 2, 0)
        rowend = min(rowend + 2, rows)
        for i in range(colnum):
            colarray[i][0] = max(colarray[i][0] - 2, 0)
            colarray[i][1] = min(colarray[i][1] + 2, cols)
            if (colarray[i][1] - colarray[i][0] < 10) or (rowend - rowbegin < 10):
                continue

            imageROI = image[rowbegin:rowend, colarray[i][0]:colarray[i][1]]
            save_name = save_path + "_" + str(i) + ".jpg"
            cv.imwrite(save_name, imageROI)
            #cv.rectangle(rectimage, (colarray[i][0], rowbegin), (colarray[i][1], rowend), (255, 0, 0), 1, cv.LINE_8, 0)
        #
        # cv.imshow("image", image)
        # cv.imshow("gray", gray)
        # cv.imshow("binary", binary)
        # cv.imshow("closeimg", closeimg)
        # cv.imshow("rectimage", rectimage)
        # cv.waitKey()


if __name__ == '__main__':
    ocr_folder = r'F:\produce_myocr_datasets\pildata7\datasets'
    division_folder = r'F:\produce_myocr_datasets\pildata7\division'
    prefix_name = r'counterfeit_0106_'
    divisionOCR(ocr_folder, division_folder, prefix_name)