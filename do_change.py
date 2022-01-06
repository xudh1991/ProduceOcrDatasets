#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/20 15:34 
# @Author  : xudh
# @File    : do_change.py 
# @Software: PyCharm
# @Function: 前景图像增强，旋转变换和仿射变换

import cv2
import os
from change_image import myRotate, myPerspective
import random


def foreImageAugment(src_folder, dst_folder, use_rotate=True, angle_range=5, use_perspective=False, bsave_txt=False):
    if not os.path.exists(dst_folder):
        os.mkdir(dst_folder)

    for sub in os.listdir(src_folder):
        if not sub.endswith('.jpg'):
            continue
        img_path = os.path.join(src_folder, sub)
        #print(img_path)
        save_path = os.path.join(dst_folder, sub)
        # save_txt = os.path.join(save_folder, txt_path)
        img = cv2.imread(img_path)
        img_shape = img.shape
        if bsave_txt:
            txt_path = img_path[:-4] + ".txt"
            with open(txt_path, "r") as f:
                txtstr = f.readline()
            spiltstr = txtstr.split(",")
            txt_size = [int(spiltstr[0]), int(spiltstr[1]), int(spiltstr[2]), int(spiltstr[3])]
            dst = save_path[:-4] + '.txt'
            newt_txt = spiltstr[4]
            with open(dst, "w") as f:
                f.writelines(newt_txt)
        if use_rotate:
            random_angle = random.randint(-angle_range, angle_range)
            center_point = (int(img_shape[0] / 2.0), int(img_shape[1] / 2.0))
            img = myRotate(img, center_point, random_angle)
        if use_perspective:
            img = myPerspective(img)

        cv2.imwrite(save_path, img)


if __name__ == '__main__':
    src_folder = r"F:\temp_datasets\pildata5\fore_bi"
    dst_folder = r"F:\temp_datasets\pildata5\fore_ground_bi"
    # bsave_txt = False
    # use_rotate = True
    # angle_range = 5
    # use_perspective = False
    foreImageAugment(src_folder, dst_folder, True, 5, False, False)
