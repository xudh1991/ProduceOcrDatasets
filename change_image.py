#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/20 15:28 
# @Author  : xudh
# @File    : change_image.py.py 
# @Software: PyCharm
# @Function:

import random
import cv2
import numpy as np
import os


def get_change_point(rows, cols):
    move_ratio = 0.3
    pers_dirction = random.randint(0, 3)

    if pers_dirction == 0:  # up
        upleft = int(move_ratio * random.random() * (cols - 1))
        upright = int((1 - move_ratio * random.random()) * (cols - 1))
        dst_points = np.float32([[upleft, 0], [upright, 0], [0, rows - 1], [cols - 1, rows - 1]])
    elif pers_dirction == 1:  # down
        downleft = int(move_ratio * random.random() * (cols - 1))
        downright = int((1 - move_ratio * random.random()) * (cols - 1))
        dst_points = np.float32([[0, 0], [cols - 1, 0], [downleft, rows - 1], [downright, rows - 1]])
    elif pers_dirction == 2:  # left
        leftup = int(move_ratio * random.random() * (rows - 1))
        leftdown = int((1 - move_ratio * random.random()) * (rows - 1))
        dst_points = np.float32([[0, leftup], [cols - 1, 0], [0, leftdown], [cols - 1, rows - 1]])
    elif pers_dirction == 3:  # right
        rightup = int(move_ratio * random.random() * (rows - 1))
        rightdown = int((1 - move_ratio * random.random()) * (rows - 1))
        dst_points = np.float32([[0, 0], [cols - 1, rightup], [0, rows - 1], [cols - 1, rightdown]])
    else:
        ValueError('pers_dirction is wrong')

    return dst_points


def getPerspectivePoint(rows, cols):
    move_ratio = 1
    pers_dirction = random.randint(0, 3)

    if pers_dirction == 0:  # up
        upleft = int(move_ratio * (0.8 + 0.2 * random.random()) * (cols - 1))
        upright = int((1 - move_ratio * (0.8 + 0.2 * random.random())) * (cols - 1))
        dst_points = np.float32([[upleft, 0], [upright, 0], [0, rows - 1], [cols - 1, rows - 1]])
    elif pers_dirction == 1:  # down
        downleft = int(move_ratio * (0.8 + 0.2 * random.random()) * (cols - 1))
        downright = int((1 - move_ratio * (0.8 + 0.2 * random.random())) * (cols - 1))
        dst_points = np.float32([[0, 0], [cols - 1, 0], [downleft, rows - 1], [downright, rows - 1]])
    elif pers_dirction == 2:  # left
        leftup = int(move_ratio * (0.8 + 0.2 * random.random()) * (rows - 1))
        leftdown = int((1 - move_ratio * (0.8 + 0.2 * random.random())) * (rows - 1))
        dst_points = np.float32([[0, leftup], [cols - 1, 0], [0, leftdown], [cols - 1, rows - 1]])
    elif pers_dirction == 3:  # right
        rightup = int(move_ratio * (0.8 + 0.2 * random.random()) * (rows - 1))
        rightdown = int((1 - move_ratio * (0.8 + 0.2 * random.random())) * (rows - 1))
        dst_points = np.float32([[0, 0], [cols - 1, rightup], [0, rows - 1], [cols - 1, rightdown]])
    else:
        ValueError('pers_dirction is wrong')

    return dst_points


def myPerspective(image):
    rows, cols, channel = image.shape
    src_points = np.float32([[0, 0], [cols - 1, 0], [0, rows - 1], [cols - 1, rows - 1]])
    dst_points = get_change_point(rows, cols)
    projective_martix = cv2.getPerspectiveTransform(src_points, dst_points)
    projective_image = cv2.warpPerspective(image, projective_martix, (cols, rows), borderValue=(0, 0, 0))
    return projective_image
    # #picname = save_pic[:-4] + "_" + str(i) + save_pic[-4:]
    # cv2.imshow("img", projective_image)
    # #cv2.imwrite(save_pic, projective_image)
    # cv2.waitKey()


def myRotate(image, center_point, random_angle):
    M = cv2.getRotationMatrix2D(center_point, random_angle, 1)
    rotate_image = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]), borderValue=(0, 0, 0))
    return rotate_image


def main():
    pass


if __name__ == '__main__':
    main()
