# -*- coding: utf-8 -*-
# @Time    : 5/22/18 3:58 PM
# @Author  : Zhu Junwei
# @File    : gen_item.py

import requests
import json
# aa = {"params": "{"imgs":["jfs/t17359/342/2660587710/254717/3d2452b6/5b052c76Nd20c2e78.jpg"]}"}
#
# print(len(json.dumps(aa)))
# matting_url = 'http://drawbot-matting.jd.com/api/matting'
#
# param = {"imgs": ["jfs/t18763/226/2704177119/605537/1c6efd8e/5b0237d0Nfe8662f0.jpg", "jfs/t16771/274/2603187129/206160/b3c685a2/5b023802Nd54b1452.jpg"]}
# len = len(json.dumps(param))+16
# # print(len(json.dumps(param)))
#
# my_headers = {"Host": "drawbot-matting.jd.com", "Content-Length": len, "Authorization": "eyJjb2RlIjoyMDAsInBpbiI6ImpkX3dyaXRlcjAxIn0="}
# res = requests.post(matting_url, data=param)
# print(res)

import os
import random
from PIL import Image
item_path = '/data1/banner/demo/item/'
elem_path = '/data1/banner/demo/elements/'

def gen_item(sku, box, bg_im):
    items = os.listdir(item_path)
    elements = os.listdir(elem_path)
    if random.randint(0, 1) == 1:
        elem_full_path = os.path.join(elem_path, elements[random.randint(0, len(elements) - 1)])
        element = Image.open(elem_full_path).convert('RGBA')
        element_bbox = element.split()[3].getbbox()
        element = element.crop(element_bbox)
        elem_w, elem_h = element.size

        ratio = (box[2]*1.05) / max(elem_w, elem_h)
        dst_w = int(ratio * elem_w)
        dst_h = int(ratio * elem_h)
        element = element.resize((dst_w, dst_h), resample=Image.BILINEAR)
        bg_im.paste(element, (box[0] + (box[2] - dst_w) // 2, box[1] + (box[3] - dst_h) // 2), element)

    item_full_path = os.path.join(item_path, items[random.randint(0, len(items)-1)])
    item = Image.open(item_full_path).convert('RGBA')
    # print(item.size)
    # item.show()
    bbox = item.split()[3].getbbox()
    # print(box)
    item = item.crop(bbox)
    w, h = item.size
    offset = random.randint(box[2]//20, box[2]//10+1)
    ratio = (box[2]-2*offset)/max(w, h)
    dst_w = int(ratio*w)
    dst_h = int(ratio*h)
    item = item.resize((dst_w, dst_h), resample=Image.BILINEAR)
    bg_im.paste(item, (box[0]+(box[2]-dst_w)//2, box[1]+(box[3]-dst_h)//2), item)





    return bg_im