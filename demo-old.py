# -*- coding: utf-8 -*-
# @Time    : 5/22/18 4:08 PM
# @Author  : Zhu Junwei
# @File    : demo-old.py


############百度nlp sdk##########################
# from aip import AipNlp
#
# """ 你的 APPID AK SK """
# APP_ID = '11281365'
# API_KEY = 'I8Da8Om8gGCuoLA8ns49gFTl'
# SECRET_KEY = 'ke5dFWWLQjyFhlbTS1VhoGhjdGMM4Df1'
#
# client = AipNlp(APP_ID, API_KEY, SECRET_KEY)
#
# res = client.lexer('大限将至，这些外航还在抗拒“台湾属于中国”')
# res2 = client.dnnlm('大限将至，这些外航还在抗拒“台湾属于中国”')
# print(res.items())
# print(res2.items())
############百度nlp sdk##########################
############baidu nlp api#######################

# url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=I8Da8Om8gGCuoLA8ns49gFTl&client_secret=ke5dFWWLQjyFhlbTS1VhoGhjdGMM4Df1'
#
# response = requests.post(url)
#
# response_text = json.loads(response.text)
#
# print(response_text['access_token'])

# my_headers = {"Content-Type": "application/json"}
# my_token = '24.7118db5cdbe15d3886fa7af85f4219c6.2592000.1529584273.282335-11281365'
#
# sentence = "增高鞋全民疯抢"
#
# my_data = {"text": sentence}
# my_json = json.dumps(my_data)
#
# fenci_url = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/lexer?charset=UTF-8&access_token={}'.format(my_token)
# res = requests.post(fenci_url, data=my_json, headers=my_headers)
#
# my_res = json.loads(res.text)
# print(my_res)
############baidu nlp api#######################

#########解压文件################################
# import os
# import common.utils as utils
#
# src = '/home/zjw/projects/gen_banner/resources/fonts/FZ'
# files = os.listdir(src)
# for file in files:
#     file_path = os.path.join(src, file)
#     utils.uncompress(file_path, src)
###############################################


# from PIL import Image, ImageDraw, ImageFont
# bg_im = Image.open('/data1/banner/demo/background/ec12a047b311b6a74779048c48cd5ba8.jpg')
# w, h = bg_im.size
#
# #item
# item_im = Image.open('/data1/banner/demo/item/ba2716e19fef04a7c95d55c1ed93e9de.png')
# item_w, item_h = item_im.size
# dh = int(h*2/3)
# dw = int(item_w * dh/item_h)
# item_im = item_im.resize((dw, dh), resample=Image.BILINEAR)
#
# item_im2 = Image.open('/data1/banner/demo/item/f42b1ea86a193598d65522888dc7bb5a.png')
# item_w2, item_h2 = item_im2.size
# dh2 = h//2
# dw2 = int(item_w2 * dh2/item_h2)
# item_im2 = item_im2.resize((dw2, dh2), resample=Image.BILINEAR)
#
# #放置商品
# bg_im.paste(item_im, (w-dw-200, h//6), item_im)
# # bg_im.paste(item_im2, (w-dw-150-dw2, h//4), item_im2)
#
# #处理文字
# font_size = h//10
# myfont = ImageFont.truetype('./resources/fonts/HY/HYXiXiuTiJ.ttf', size=font_size)
# myfont2 = ImageFont.truetype('./resources/fonts/HY/HYCuJianHeiJ.ttf', size=int(2*font_size/3))
# draw = ImageDraw.Draw(bg_im)
# fillcolor = 'white'
# draw.text((200, h//3), "夏日手机抢鲜购", font=myfont, fill=fillcolor)
# draw.text((200, h//3 + font_size), "你值得购买", font=myfont, fill='purple')
#
# #处理热点标签
# tag = Image.new('RGB', (font_size*4, font_size), 'white')
# draw_tag = ImageDraw.Draw(tag)
# draw_tag.text((int(font_size*2/3), font_size//6), "立即抢购", font=myfont2, fill='black')
# bg_im.paste(tag, (200, h//3 + font_size*2+20))
#
# #元素
# # element_im = Image.open('/data1/banner/demo/elements/dd7d61e8403f016bb80963da79a53156.png')
# # element_w, element_h = element_im.size
# # eh = min(element_h, 3*font_size)
# # ew = int(eh * element_w / element_h)
# # element_im = element_im.resize((ew, eh), resample=Image.BILINEAR)
# # bg_im.paste(element_im, (200, h//3 + font_size), element_im)
#
#
#
# bg_im.show()


