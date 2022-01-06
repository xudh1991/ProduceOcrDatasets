#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2022/1/5 14:57 
# @Author  : xudh
# @File    : main.py 
# @Software: PyCharm
# @Function: 使用训练好的模型，对分割后的字符图像进行分类

import os
import cv2
import numpy as np
import shutil


def class_ocr(image_folder, save_path, model_path, imgsize):
    if not os.path.exists(image_folder):
        raise ValueError("没有用于分类的文件夹")

    if not os.path.exists(model_path):
        raise ValueError("没有用于分类的模型文件")

    if not os.path.exists(save_path):
        os.mkdir(save_path)

    net = cv2.dnn.readNetFromONNX(model_path)
    for sub in os.listdir(image_folder):
        src_name = os.path.join(image_folder, sub)
        image = cv2.imread(src_name)
        resizeimg = cv2.resize(image, imgsize)
        blob = cv2.dnn.blobFromImage(resizeimg)
        net.setInput(blob)
        out = net.forward()
        cls = np.argmax(np.array(out[0]))
        save_sub_path = os.path.join(save_path, str(cls))
        if not os.path.exists(save_sub_path):
            os.mkdir(save_sub_path)
        dst_name = os.path.join(save_sub_path, sub)
        #print(f'src_name:{src_name}')
        #print(f'dst_name:{dst_name}')
        shutil.move(src_name, dst_name)


if __name__ == '__main__':
    modelPath = r'D:\2021-12-27_14-26-09_ocr_classification_ocr_net_learningrate0.0001\training\model_best.onnx'
    imageFolder = r'F:\produce_myocr_datasets\pildata7\division'
    savePath = r'F:\produce_myocr_datasets\pildata7\class_results'
    imgsize = (50, 50)
    class_ocr(imageFolder, savePath, modelPath, imgsize)
