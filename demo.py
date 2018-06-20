# -*- coding: utf-8 -*-
# @Time    : 6/6/18 5:30 PM
# @Author  : Zhu Junwei
# @File    : demo.py
import os
import banner_factory
import common.config as config
import time
import numpy as np
from PIL import Image
import cv2


# banner_color = {
#     '红': (255, 0, 0),
#     '橙': (255, 165, 0),
#     '黄': (255, 255, 0),
#     '绿': (0, 128, 0),
#     '蓝': (0, 0, 255),
#     '紫': (128, 0, 128),
#     '粉': (255, 192, 203),
#     '棕': (165, 42, 42),
#     '灰': (128, 128, 128),
#     '黑': (0, 0, 0),
#     '白': (255, 255, 255)
# }

Banner = banner_factory.GenBanner()

t1 = time.time()

for i in range(2):
    Banner.set_param(size=(1125, 762),layout=config.HORIZONTAL_LEFT, style='科技', color='绿', reserve=(0.1, 0.1, 0.28, 0.18))

    # Banner.set_param(size=(1125, 762),layout=config.VERTICAL_BOTTOM, style='科技', color='蓝', reserve=(0.1, 0.1, 0.1, 0.1))
    # Banner.set_param(size=(762, 762),layout=config.CENTER, style='科技', color='蓝', reserve=(0.1, 0.1, 0.1, 0.1))
    res = Banner.generate('123')
    res = res.convert('RGB')
    res.save('./res/{}.png'.format(i))

    res.save('./res/{}.jpg'.format(i), format='JPEG')
    cv_res = cv2.cvtColor(np.asarray(res), cv2.COLOR_RGB2BGR)
    # cv2.circle(cv_res, (300,300), 100, (0,0,0))
    # cv2.rectangle(cv_res,(200,200), (400,400), (0,255,0))
    # cv2.ellipse(cv_res,(500,500),(100,50),0,0, 360,(0,0,0))
    cv2.imwrite('./res/{}_cv2.jpg'.format(i), cv_res)

t2 = time.time()
print(t2-t1)

