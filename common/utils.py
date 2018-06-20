# -*- coding: utf-8 -*-
# @Time    : 5/28/18 5:06 PM
# @Author  : Zhu Junwei
# @File    : utils.py
import os
import zipfile
from unrar import rarfile

banner_color = {
    '红': (255, 0, 0),
    '橙': (255, 165, 0),
    '黄': (255, 255, 0),
    '绿': (0, 128, 0),
    '蓝': (0, 0, 255),
    '紫': (128, 0, 128),
    '粉': (255, 192, 203),
    '棕': (165, 42, 42),
    '灰': (128, 128, 128),
    '黑': (0, 0, 0),
    '白': (255, 255, 255)
}

def uncompress(file_name, dst_path):
    """
    解压文件，仅支持rar和zip
    :param file_name: 压缩文件的全路径
    :param dst_path: 解压目录
    :return:
    """
    pos = file_name.rfind('.')
    if not os.path.exists(dst_path):
        os.makedirs(dst_path)
    if pos > -1:
        post_fix = file_name[pos:]
        if post_fix == '.rar':
            rar = rarfile.RarFile(file_name)
            rar.extractall(path=dst_path)
        elif post_fix == '.zip':
            zip = zipfile.ZipFile(file_name)
            zip.extractall(path=dst_path)
        else:
            print('only support rar and zip files!')
