#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/1/5 16:34 
# @Author  : xudh
# @File    : main.py 
# @Software: PyCharm
# @Function: 梳理全部自定义OCR数据集程序，第一步生成字符图像，第二步字符图像切割，第三步分割字符图像分类


import os
from produce_base_dataset import produceBaseDataset
from division_ocr import divisionOCR
from classOCR import class_ocr

if __name__ == '__main__':
    folderPath = r'F:\produce_myocr_datasets\pildata9'  # 此文件夹下，需包含字体文件夹，模型文件夹，背景文件夹
    ocrFolder = os.path.join(folderPath, r'datasets')  # 完整数据文件夹
    imageNumber = 10000
    print("制作图像......")
    produceBaseDataset(folderPath, ocrFolder, imageNumber)

    divisionFolder = os.path.join(folderPath, r'division')
    prefix_name = r'artificial_0106_'
    print("分割图像......")
    divisionOCR(ocrFolder, divisionFolder, prefix_name)

    modelPath = os.path.join(folderPath, r'models\model_best.onnx')
    classFolder = os.path.join(folderPath, r'classResults')
    imgSize = (50, 50)  # resize图像尺寸需与训练模型是使用尺寸相同
    print("分类图像......")
    class_ocr(divisionFolder, classFolder, modelPath, imgSize)
