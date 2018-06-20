# -*- coding: utf-8 -*-
# @Time    : 6/5/18 3:23 PM
# @Author  : Zhu Junwei
# @File    : banner_factory.py
import random
from PIL import Image, ImageColor, ImageDraw, ImageFilter
import gen_background
import gen_item
import gen_text
import optimize_banner
import common.config as config
import cv2
import numpy as np

"""
本工程中的矩形框坐标均为 left，top，width，height。而PIL中一般为left，top，right，bottom。要进行转化。
"""

class GenBanner(object):
    """

    """
    def __init__(self, size=(1200, 600), layout=config.HORIZONTAL_LEFT, style='科技', color='蓝', reserve=None):

        #目标图像宽， 高
        self.size = size

        #banner布局，左右、上下、居中
        self.layout = layout

        #整体风格
        self.style = style

        #色系
        self.color = color

        #留白设置，左右上下的空余比例
        self.reserve = reserve

    def set_param(self, size=(1200, 600), layout=config.HORIZONTAL_LEFT, style='科技', color='蓝', reserve=None):
        self.size = size
        self.layout = layout
        self.style = style
        self.color = color
        self.reserve = reserve

    def generate(self, sku):

        #边界保留比例，即此部分不画图
        if self.reserve is None:
            right_ratio = left_ratio = random.randint(2, 10) / 100
            bottom_ratio = top_ratio = random.randint(2, 10) / 100
            self.reserve = (left_ratio, right_ratio, top_ratio, bottom_ratio)

        w, h = self.size
        left_gap = int(w * self.reserve[0])
        right_gap = int(w * self.reserve[1])
        top_gap = int(h * self.reserve[2])
        bottom_gap = int(h * self.reserve[3])

        valid_w = w - left_gap - right_gap
        valid_h = h - top_gap - bottom_gap

        #根据布局和banner尺寸获得主体区域和文案区域，此部分后期由序列模型生成
        #这里人工设定5个布局，默认主体区域为正方形
        if self.layout == config.HORIZONTAL_LEFT:
            item_size = min(valid_h, random.randint(valid_w//3, valid_w//2)) - 1

            text_w = random.randint(item_size, valid_w - item_size)
            text_h = item_size

            x_offset = (valid_w - text_w - item_size)//2

            item_x = w - right_gap - item_size - x_offset
            item_y = top_gap + (valid_h - item_size) // 2
            text_x = left_gap + x_offset
            text_y = item_y

        elif self.layout == config.HORIZONTAL_RIGHT:
            item_size = min(valid_h, random.randint(valid_w // 3, valid_w // 2)) - 1

            text_w = random.randint(item_size, valid_w - item_size)
            text_h = item_size

            x_offset = (valid_w - text_w - item_size) // 2

            item_x = left_gap + x_offset
            item_y = top_gap + (valid_h - item_size) // 2
            text_x = w - right_gap - text_w - x_offset
            text_y = item_y

        elif self.layout == config.VERTICAL_TOP:
            item_size = min(valid_w, random.randint(valid_h // 3, valid_h // 2)) - 1

            text_w = random.randint(item_size, valid_w)
            text_h = random.randint(item_size, valid_h - item_size)

            y_offset = (valid_h - text_h - item_size)//2

            item_x = left_gap + (valid_w - item_size) // 2
            item_y = h - bottom_gap - item_size-y_offset
            text_x = left_gap + (valid_w-text_w)//2
            text_y = top_gap+y_offset
        elif self.layout == config.VERTICAL_BOTTOM:
            item_size = min(valid_w, random.randint(valid_h // 3, valid_h // 2)) - 1

            text_w = random.randint(item_size, valid_w)
            text_h = random.randint(item_size, valid_h - item_size)

            y_offset = (valid_h - text_h - item_size) // 2

            item_x = left_gap + (valid_w - item_size) // 2
            item_y = top_gap + y_offset
            text_x = left_gap + (valid_w - text_w) // 2
            text_y = h - bottom_gap - text_h - y_offset
        elif self.layout == config.CENTER:
            item_size = min(random.randint(valid_w//3, valid_w//2), random.randint(valid_h // 3, valid_h // 2))
            item_x = left_gap + (valid_w-item_size)//2
            item_y = top_gap + (valid_h-item_size)//2
            text_w = random.randint(item_size, item_size*2)
            text_h = random.randint(item_size, item_size*2)
            text_x = left_gap + (valid_w-text_w)//2
            text_y = top_gap + (valid_h-text_h)//2
        else:
            print('use default layout!')
            item_size = min(valid_h, random.randint(valid_w // 4, valid_w // 2)) - 1
            item_x = w - right_gap - item_size
            item_y = top_gap + (valid_h - item_size) // 2

            text_w = random.randint(item_size, valid_w - item_size)
            text_h = item_size
            text_x = left_gap
            text_y = item_y


        #平铺区域位置（如果有）
        sub_bg_x = left_gap
        sub_bg_y = top_gap
        sub_bg_w = w - left_gap - right_gap
        sub_bg_h = h - top_gap - bottom_gap

        # alpha_rect = Image.open('./resources/rectangle.png').convert('RGBA').split()[3]
        # alpha_rect = alpha_rect.crop(alpha_rect.getbbox())
        # alpha_circle = Image.open('./resources/circle.png').convert('RGBA').split()[3]
        # alpha_circle = alpha_circle.crop(alpha_circle.getbbox())

        #平铺区域颜色及透明度
        R = min(255, random.randint(0, 300))
        G = min(255, random.randint(0, 300))
        B = min(255, random.randint(0, 300))
        A = min(255, random.randint(150, 300))
        I = (R + G + B) / 3

        # 在RGB模式下，第四个参数失效，默认255，在RGBA模式下，也可只传入前三个值，A值默认255
        #只保留亮的结果
        # sub_bg = None if I < 128 else Image.new('RGBA', (sub_bg_w, sub_bg_h), (R, G, B, A))


        dst_color = config.banner_color[self.color]
        if I < 128 or (abs(R-dst_color[0])>30 and abs(G-dst_color[1])>30 and abs(B-dst_color[2])>30):
            sub_bg = None
        else:
            sub_bg = Image.new('RGB', self.size, (R, G, B))
            alpha_layer = Image.new('L', self.size, 0)
            alpha_draw = ImageDraw.Draw(alpha_layer)
            alpha_draw.rectangle((sub_bg_x, sub_bg_y, sub_bg_x+sub_bg_w, sub_bg_y+sub_bg_h), fill=A)

            #主体区域镂空
            # offset = item_size//20
            # alpha_draw.ellipse((item_x+offset, item_y+offset, item_x+item_size-offset, item_y+item_size-offset), fill=0)
            # alpha_layer = alpha_layer.filter(ImageFilter.BLUR())

            # alpha_layer_np = np.asarray(alpha_layer)
            # cv2.circle(alpha_layer_np, (item_x, item_y), item_size//2, 0)
            # alpha_layer = Image.fromarray(alpha_layer_np)

            sub_bg.putalpha(alpha_layer)

        #获得背景
        bg_im = gen_background.gen_bg((w, h), self.style, self.color)
        # bg_im = bg_im.convert('RGBA')
        # bg_im.show()

        #添加平铺区域
        if sub_bg is not None:
            bg_im.paste(sub_bg, (0, 0), sub_bg)
        # bg_im.show()

        #添加主体区域
        # item_size = min(w - left_gap - right_gap, h - top_gap - bottom_gap)
        # item_x = w - right_gap - item_size
        # item_y = h -bottom_gap - item_size
        bg_im = gen_item.gen_item(sku, (item_x, item_y, item_size, item_size), bg_im)
        # bg_im.show()

        #添加文案区域
        # text_x = left_gap
        # text_y = top_gap
        # text_w = w - left_gap - right_gap - item_size
        # text_h = h - top_gap - bottom_gap
        lines = ['夏日手机抢鲜购', '你值得购买']
        action_line = '立即抢购'
        bg_im = gen_text.gen_text(lines, '清新', (text_x, text_y, text_w, text_h), bg_im, action=action_line, layout=self.layout)

        #整图优化
        banner = optimize_banner.opt_banner(bg_im)

        return banner

