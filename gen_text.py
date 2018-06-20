# -*- coding: utf-8 -*-
# @Time    : 5/22/18 4:00 PM
# @Author  : Zhu Junwei
# @File    : gen_text.py

# from PIL import Image, ImageDraw, ImageFont
# im = Image.open('/data1/banner/demo/background/ec12a047b311b6a74779048c48cd5ba8.jpg')
# w, h = im.size
# draw = ImageDraw.Draw(im)
# myfont = ImageFont.truetype('./resources/fonts/HY/HYBaiQiTiJ.ttf', size=60)
# fillcolor = 'white'
# draw.text((700, 140), "夏日手机抢鲜购", font=myfont, fill=fillcolor)
# draw.text((700, 200), "    你值得购买", font=myfont, fill=fillcolor)
# im.show()

#RGB 2 Grey
#L = R * 299/1000 + G * 587/1000 + B * 114/1000
import os
import random
from PIL import Image, ImageFont, ImageDraw
import common.config as config

font_path = './resources/fonts/'
font_dict={
    'FZKTJW.TTF': '方正楷体 优雅 高贵 艺术 复古',
    'FZLTSJW.TTF': '方正兰亭宋 优雅 高贵 艺术 复古',
    'FZLTHJW.TTF': '方正兰亭黑简体 现代 简洁 轻松 低调',
    'FZLTXIHJW.TTF': '方正兰亭细黑简体 现代 简洁 轻松 低调',
    'FZHTJW.TTF': '方正黑体简体 现代 简洁 轻松 低调',
    'FZLanTYJW.ttf': '方正兰亭圆简体 现代 简洁 轻松 低调',
    'FZDHTJW.TTF': '方正大黑简体 男性 阳刚 粗犷 霸气',
    'FZLTCHJW.TTF': '方正兰亭粗黑简体 男性 阳刚 粗犷 霸气',
    'FZCSJW.TTF': '方正粗宋简体 男性 阳刚 粗犷 霸气',
    'FZCKJW.TTF': '方正粗楷简体 男性 阳刚 粗犷 霸气',
    'FZLTCXHJW.TTF': '方正兰亭超细黑简体 女性 优雅 高端 清新',
    'FZLTXHJW.TTF': '方正兰亭纤黑简体 女性 优雅 高端 清新',
    'FZLanTYJW_Xian.ttf': '方正兰亭纤圆简体 女性 优雅 高端 清新',
    'FZYBXSJW.TTF': '方正硬笔行书 中国风',
    'FZSEJW.TTF': '方正少儿简体 可爱',
    'FZQKBYSJW.TTF': '方正清刻本悦宋简体 优雅 高贵 艺术 复古 现代 简洁 轻松 低调'

}

tag_path = '/data1/banner/demo/tag/'

def gen_tag(w, h):
    tags = os.listdir(tag_path)
    tag_num = len(tags)
    idx = random.randint(0, tag_num*2)
    if idx < tag_num:
        tag_file = os.path.join(tag_path, tags[idx])
        tag = Image.open(tag_file).convert('RGBA')
        bbox = tag.split()[3].getbbox()
        # print(box)
        tag = tag.crop(bbox).resize((w,h), resample=Image.BILINEAR)
    else:
        tag = Image.new('RGBA', (w,h), 'white')
    return tag


def gen_text(lines, style, box, bg, action=None, color=None, layout=config.HORIZONTAL_LEFT):
    """
    将文案嵌入banner中，文案包括主文案，辅助文案和行动点，一般有三行
    :param lines: 文案内容，按照主副顺序
    :param style: 文字风格
    :param box: 文案区域
    :param bg: banner背景图
    :param action: 行动点，比如 立即购买>
    :param color: 文字颜色，未指定则根据背景自动调节
    :return: 嵌入文案后的banner图
    """

    #计算文案中最长的一行一共有多少字符
    max_len = 0
    for line in lines:
        if len(line) > max_len:
            max_len = len(line)
    if max_len < 1:
        return bg

    #计算一共有多少行，包括行动点
    line_num = len(lines)
    if action is not None:
        line_num += 1

    # #处理文字
    font_size = min(int(box[3]*0.9/line_num), int(box[2]*0.9/max_len))

    #确定主副文案字体
    candidate_fonts = list()

    #default font
    candidate_fonts.append('FZLTCHJW.TTF')
    for key, value in font_dict.items():
        if value.find(style) > -1:
            candidate_fonts.append(key)

    #选择字体
    idx = random.randint(0, len(candidate_fonts)) - 1
    select_idx = 0 if idx < 0 else idx

    #第一行文案
    main_font = ImageFont.truetype(os.path.join(font_path, candidate_fonts[select_idx]), size=font_size)

    #副文案
    sub_font_size = (2*font_size//3) if random.randint(0, 2) > 0 else font_size
    sub_font = ImageFont.truetype(os.path.join(font_path, candidate_fonts[select_idx]), size=sub_font_size)

    #行动点，默认
    action_font_size = random.randint(font_size//2, (2*font_size//3))
    action_font = ImageFont.truetype('./resources/fonts/FZLTHJW.TTF', size=action_font_size)

    #确定主副文案字体颜色
    crop_box = (box[0], box[1], box[0]+box[2], box[1]+box[3])
    small_crop = bg.crop(crop_box).resize((10, 10), resample=Image.ANTIALIAS)
    text_crop = small_crop.convert('L')
    crop_hist = text_crop.histogram()

    #平均亮度
    avg_L = int(sum([i * crop_hist[i] for i in range(len(crop_hist))]) / 100)

    #文案颜色
    fill_color = 'black' if avg_L > 128 else 'white'
    if color is not None:
        fill_color = color

    #tag字体颜色
    tag_font_color = small_crop.getpixel((2, 8))


    #嵌入文案，有两种对齐方式：左对齐和居中，随机选择
    draw = ImageDraw.Draw(bg)
    if random.randint(0, 2) > 1 and layout in (config.HORIZONTAL_LEFT, config.HORIZONTAL_RIGHT):
        # 左对齐
        draw.text((box[0] + box[2] // 20, box[1] + (box[3] - font_size * line_num) // 2), lines[0], font=main_font,
                  fill=fill_color)
        line_idx = 0
        for line in lines:
            line_idx += 1
            if line_idx == 1:
                continue
            draw.text((box[0] + box[2] // 20,
                       box[1] + (box[3] - font_size * line_num) // 2 + font_size * line_idx - sub_font_size), line,
                      font=sub_font, fill=fill_color)
        # 处理行动点标签
        if action is not None:
            action_len = len(action)
            tag_w = action_font_size * action_len + action_font_size * 2
            tag_h = action_font_size * 3 // 2
            # tag = Image.new('RGB', (tag_w, tag_h), 'white')
            tag = gen_tag(tag_w, tag_h)
            tag_x = box[0] + box[2] // 20
            tag_y = box[1] + (box[3] - font_size * line_num) // 2 + font_size * line_num - action_font_size
            bg.paste(tag, (tag_x, tag_y), tag)
            tag_crop = bg.crop((tag_x, tag_y, tag_x+tag_w, tag_y+tag_h)).convert('L').resize((9, 9))
            tag_L = tag_crop.getpixel((5, 5))
            tag_font_L = tag_font_color[0] * 299 / 1000 + tag_font_color[1] * 587 / 1000 + tag_font_color[2] * 114 / 1000
            if abs(tag_L - tag_font_L) < 50:
                tag_font_color = 'black' if tag_L > 128 else 'white'
            draw_tag = ImageDraw.Draw(bg)
            draw_tag.text((tag_x + action_font_size, tag_y + action_font_size // 5), action, font=action_font, fill=tag_font_color)


    else:
        #居中
        main_text_num = len(lines[0])
        draw.text((box[0] + (box[2] - font_size * main_text_num) // 2, box[1] + (box[3] - font_size * line_num) // 2),
                  lines[0], font=main_font, fill=fill_color)
        line_idx = 0
        for line in lines:
            line_idx += 1
            if line_idx == 1:
                continue
            line_text_num = len(line)
            draw.text((box[0] + (box[2] - sub_font_size * line_text_num) // 2,
                       box[1] + (box[3] - font_size * line_num) // 2 + font_size * line_idx - sub_font_size), line,
                      font=sub_font, fill=fill_color)
        # 处理行动点标签
        if action is not None:
            action_len = len(action)
            tag_w = action_font_size * action_len + action_font_size * 2
            tag_h = action_font_size * 3 // 2
            # tag = Image.new('RGB', (tag_w, tag_h), 'white')
            tag = gen_tag(tag_w, tag_h)

            tag_x = box[0] + (box[2] - tag_w) // 2
            tag_y = box[1] + (box[3] - font_size * line_num) // 2 + font_size * line_num - action_font_size
            bg.paste(tag, (tag_x, tag_y), tag)
            tag_crop = bg.crop((tag_x, tag_y, tag_x + tag_w, tag_y + tag_h)).convert('L').resize((9, 9))
            tag_L = tag_crop.getpixel((5, 5))
            tag_font_L = tag_font_color[0] * 299 / 1000 + tag_font_color[1] * 587 / 1000 + tag_font_color[
                2] * 114 / 1000
            if abs(tag_L - tag_font_L) < 50:
                tag_font_color = 'black' if tag_L > 128 else 'white'
            draw_tag = ImageDraw.Draw(bg)
            draw_tag.text((tag_x + action_font_size, tag_y + action_font_size // 5), action, font=action_font,
                          fill=tag_font_color)

    return bg

