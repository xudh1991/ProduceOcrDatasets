#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/20 15:27 
# @Author  : xudh
# @File    : main.py 
# @Software: PyCharm
# @Function: 制作分割前数据分成三大步，第一步读取不同的字体文件生成字符图像，
# 第二步对字符图像进行数据增强，正常包括旋转和仿射变换，当前未使用仿射变换
# 第三步将旋转后的图像与背景图像融合

import os
import cv2
import random
import numpy as np
from create_fore import produceForeImage
from do_change import foreImageAugment


def get_back_paths(back_folder):
    back_paths = []
    for back_pic in os.listdir(back_folder):
        back_name = os.path.join(back_folder, back_pic)
        back_paths.append(back_name)
    return back_paths


def test():
    fore_name = r'D:\txtTest\my_data\fore_ground\0AMEBP9XXTJDEP2CD.jpg'
    back_name = r'D:\txtTest\my_data\back_ground\IMG_20191113_165357.jpg'
    fore_img = cv2.imread(fore_name)
    back_img = cv2.imread(back_name)
    reshape_fore_img = np.reshape(fore_img, (-1, 3))
    np.savetxt(r'D:\txtTest\fore_img.txt', reshape_fore_img, fmt='%0.8f')
    # cv2.imshow("fore_img", fore_img)
    cv2.imwrite(r"D:\txtTest\fore_img.jpg", fore_img)

    fore_shape = fore_img.shape
    back_shape = back_img.shape
    begin_x = random.randint(0, (back_shape[1] - fore_shape[1]))
    begin_y = random.randint(0, (back_shape[0] - fore_shape[0]))
    end_y = begin_y + fore_shape[0]
    end_x = begin_x + fore_shape[1]
    roi_back = back_img[begin_y:end_y, begin_x:end_x]
    # np.savetxt('roi_back.txt', roi_back, fmt='%0.8f')
    # cv2.imshow("roi_back", roi_back)
    cv2.imwrite(r"D:\txtTest\roi_back.jpg", roi_back)
    roi_back[fore_img > 200] = 255
    # np.savetxt('roi_back_no.txt', roi_back, fmt='%0.8f')
    # cv2.imshow("roi_back_no", roi_back)
    reshape_roi_back = np.reshape(roi_back, (-1, 3))
    np.savetxt(r'D:\txtTest\roi_back.txt', reshape_roi_back, fmt='%0.8f')
    cv2.imwrite(r"D:\txtTest\roi_back_no.jpg", roi_back)
    new_img = fore_img + roi_back
    # np.savetxt('roi_back_no.txt', roi_back, fmt='%0.8f')
    # cv2.imshow("img", new_img)
    cv2.imwrite(r"D:\txtTest\new_img.jpg", new_img)
    cv2.waitKey()


def createDatasets(fore_img, back_img):
    fore_shape = fore_img.shape
    back_shape = back_img.shape
    begin_x = random.randint(0, (back_shape[1] - fore_shape[1]))
    begin_y = random.randint(0, (back_shape[0] - fore_shape[0]))
    end_y = begin_y + fore_shape[0]
    end_x = begin_x + fore_shape[1]
    roi_back = back_img[begin_y:end_y, begin_x:end_x]
    # roi_back[fore_img > 50] = 0
    new_img = np.zeros_like(fore_img)
    for i in range(fore_shape[1]):
        for j in range(fore_shape[0]):
            new_img[j, i] = (fore_img[j, i] / 255) * fore_img[j, i] + (1 - (fore_img[j, i] / 255)) * roi_back[j, i]

    return new_img


def produceBaseDataset(folder_path, data_folder, image_number):
    fore_folder = os.path.join(folder_path, r'fore_bi')  # 前景文件夹
    fore_ground_folder = os.path.join(folder_path, r'fore_ground_bi')  # 前景增强后的文件夹
    back_folder = os.path.join(folder_path, r'back_ground')  # 背景文件夹
    font_folder = os.path.join(folder_path, r'font')

    print("制作前景图像......")
    produceForeImage(fore_folder, font_folder, image_number)
    print("前景图像数据增强......")
    foreImageAugment(fore_folder, fore_ground_folder, True, 5, False, False)

    if not os.path.exists(fore_folder):
        print(f'还没有生成前景文件夹{fore_folder}')
        return 0
    if not os.path.exists(back_folder):
        print(f'没有生成背景文件夹{back_folder}，需向总{folder_path}文件夹下添加背景文件夹和文件')
        return 0

    if not os.path.exists(data_folder):
        os.mkdir(data_folder)
    back_paths = get_back_paths(back_folder)
    print("前景、背景图像融合......")
    for fore_pic in os.listdir(fore_folder):
        if not fore_pic.endswith('.jpg'):
            continue
        fore_name = os.path.join(fore_folder, fore_pic)
        fore_img = cv2.imread(fore_name)
        for i in range(100):
            back_index = random.randint(0, len(back_paths) - 1)
            back_img = cv2.imread(back_paths[back_index])
            fore_shape = fore_img.shape
            back_shape = back_img.shape
            if (back_shape[1] - fore_shape[1]) < 0 or (back_shape[0] - fore_shape[0]) < 0:
                continue
            else:
                break
        # back_index = random.randint(0, len(back_paths)-1)
        # back_img = cv2.imread(back_paths[back_index])
        new_img = createDatasets(fore_img, back_img)
        new_name = os.path.join(data_folder, fore_pic)
        #print(f"fore_name:{fore_name}")
        #print(f"back_name:{back_paths[back_index]}")
        cv2.imwrite(new_name, new_img)


if __name__ == '__main__':
    # test()
    produceBaseDataset()
