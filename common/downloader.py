# -*- coding: utf-8 -*-
# @Time    : 5/22/18 4:44 PM
# @Author  : Zhu Junwei
# @File    : downloader.py
import os
import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

#
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--disable-gpu')
#
# driver = webdriver.Chrome(chrome_options=chrome_options)
# driver.set_window_size(1920, 1080)
#
# driver.get("http://www.baidu.com/")
# driver.save_screenshot(driver.title+".png")


def download_image(image_url, dst_dir, file_name, timeout=20):

    response = None
    file_path = os.path.join(dst_dir, file_name)
    if os.path.exists(file_path):
        # print('exists!')
        return
    try_times = 0
    while True:
        try:
            try_times += 1
            # print('begin')
            response = requests.get(image_url, timeout=timeout)
            # print('response')
            # print(file_path)
            with open(file_path, 'wb') as f:
                f.write(response.content)
            response.close()

            break
        except Exception as e:
            if try_times < 3:
                continue
            if response:
                response.close()
            print("## Fail:  {}  {}".format(image_url, e.args))
            break

