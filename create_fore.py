#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/12/22 20:02 
# @Author  : xudh
# @File    : create_fore1.py 
# @Software: PyCharm
# @Function:


import random
import os
from PIL import ImageFont, Image, ImageDraw

# 将一些随机参数直接写死在这，太多了，不好传
char_range = 'ABCDEF'
font_range = [25, 50]
color_range = [160, 240]
begin_point = (20, 20)
int_range = [2, 5]      #不算起始的字符，剩下整数的随机长度范围
bsave_txt = False


def produceForeImage(fore_bi_path, font_path, ImageNum=10000):
    if not os.path.exists(fore_bi_path):
        os.mkdir(fore_bi_path)

    font_list = []
    for sub in os.listdir(font_path):
        rangeNumber = 1
        if sub == 'boston-1.ttf' or sub == 'OmbudsmanStencil-1.ttf':
            rangeNumber = 4
        for i in range(rangeNumber):
            font_list.append(os.path.join(font_path, sub))

    for pic_num in range(ImageNum):
        img = Image.new("RGB", (500, 500), 'black')
        write_char = ""
        randomint = random.randint(int_range[0], int_range[1])
        addchar = random.randint(0, 9)

        for i in range(randomint):
            if i == 0 and addchar != 0:
                char_index = random.randint(0, 5)
                write_char += char_range[char_index] + "-"
            ranv = random.randint(0, 9)
            write_char += str(ranv)

        draw = ImageDraw.Draw(img)
        font_size = random.randint(font_range[0], font_range[1])
        font_index = random.randint(0, len(font_list) - 1)
        font_name = font_list[font_index]
        font = ImageFont.truetype(font_name, font_size)
        ran_rgb = random.randint(color_range[0], color_range[1])
        # ran_g = random.randint(color_range[0], color_range[1])
        # ran_b = random.randint(color_range[0], color_range[1])
        draw.text(begin_point, write_char, (ran_rgb, ran_rgb, ran_rgb), font=font)
        w, h = draw.textsize(write_char, font)
        #print(write_char)

        xRight = begin_point[0] * 2 + w
        yLower = begin_point[1] * 2 + h

        region = img.crop((0, 0, xRight, yLower))

        if bsave_txt:
            txt_name = os.path.join(fore_bi_path, str(pic_num) + '.txt')
            txt_str = str(begin_point[0]) + "," + str(begin_point[1]) + "," + str(w) + "," + str(
                h) + "," + write_char + "," + font_name
            with open(txt_name, "w") as f:
                f.writelines(txt_str)

        file_name = str(pic_num) + '.jpg'
        img_name = os.path.join(fore_bi_path, file_name)
        region.save(img_name)


if __name__ == '__main__':
    # test()
    font_path = r'F:\produce_myocr_datasets\pildata5\font'
    fore_bi_path = r'F:\produce_myocr_datasets\pildata5\fore_bi'
    produceForeImage(fore_bi_path, font_path, 100)
