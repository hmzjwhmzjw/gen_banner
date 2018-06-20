# -*- coding: utf-8 -*-
# @Time    : 5/22/18 3:58 PM
# @Author  : Zhu Junwei
# @File    : gen_background.py
import os
from PIL import Image,ImageColor
import random
import common.config as config
import requests

bg_path = '/data1/banner/demo/background/'
bg_list = './resources/background.txt'


def transform_bg(org_bg, size, style, color):
    pass

def gen_bg(size, style, color):

    #获取背景图列表
    bg_dict = {}
    with open(bg_list, 'r', encoding='utf-8') as bg:
        for line in bg.readlines():
            newline = line.strip().split()
            if len(newline) < 2:
                continue
            bg_dict[newline[0]] = newline[1:]


    #查看是否有合适的背景
    res = []
    for key, value in bg_dict.items():
        description = ''.join(value)
        if description.find(style) > -1 and description.find(color) > -1:
            res.append(key)

    if len(res) == 0:
        print('no suitable background!')
        return Image.new('RGB', size, config.banner_color[color])
    else:
        idx = random.randint(0, len(res) - 1)
        bg_full_path = os.path.join(bg_path, res[idx])
        bg_im = Image.open(bg_full_path).convert('RGB')
        w, h = bg_im.size
        if w/h > size[0]/size[1]:
            bg_im = bg_im.resize((int(w*size[1]/h), size[1]), resample=Image.BILINEAR)
        else:
            bg_im = bg_im.resize((size[0], int(h*size[0]/w)), resample=Image.BILINEAR)

        #裁切
        new_w, new_h = bg_im.size
        x = (new_w-size[0])//2
        y = (new_h-size[1])//2
        return bg_im.crop((x, y, new_w-x, new_h-y))




