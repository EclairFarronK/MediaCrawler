import os
import json
import subprocess

import requests
from playwright.sync_api import Playwright, sync_playwright

from dev.tool.tools import sanitize_filename

# todo 输入文件名，提取bvid，然后下载
file_download_path = './data/邹小荃/'
# 目录没有就创建
os.makedirs(file_download_path, exist_ok=True)

file_name = './data/邹小荃.txt'
USER_DATA_DIR = '%s_user_data_dir'
url = 'https://www.bilibili.com/video/'
headers = {
    'referer': 'https://www.bilibili.com/video/BV1A3411b7gm',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
}


def run(playwright: Playwright) -> None:
    print(os.getcwd())
    context = playwright.firefox.launch_persistent_context(headless=False,
                                                           user_data_dir=os.path.join(os.getcwd(), 'browser_data',
                                                                                      USER_DATA_DIR % 'bili'))
    page = context.new_page()
    # todo 读取成字符串
    with open(file_name, 'r') as file:
        # 读取文件内容，并将每行作为列表的一个元素
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    for line in lines:
        page.goto(url + line)
        list = page.locator('head script').all()
        data_title = page.locator('[data-title]').get_attribute('data-title')
        data_title = sanitize_filename(data_title)

        flag = 0
        for i in list:
            if flag == 3:
                original = i.inner_text()
                result = original.replace('window.__playinfo__=', '')
                data = json.loads(result)
                url_video_download = data["data"]['dash']['video'][0]['baseUrl']
                url_audio_download = data["data"]['dash']['audio'][0]['baseUrl']
                break
            flag = flag + 1
        # resp = page.request.get(url=url_download, headers=headers)
        resp = requests.get(url_video_download, headers=headers).content
        download_path = os.path.join(file_download_path, data_title + '.mp4')  # 构造下载路径
        with open(download_path, mode='wb') as file:
            file.write(resp)
        print("{:*^30}".format(f"下载完成：{data_title}"))

        resp = requests.get(url_audio_download, headers=headers).content
        download_path = os.path.join(file_download_path, data_title + '.mp3')  # 构造下载路径
        with open(download_path, mode='wb') as file:
            file.write(resp)
        print("{:*^30}".format(f"下载完成：{data_title}"))

        # 合并，将之前的删除
        commond = f'ffmpeg -i {file_download_path}{data_title}.mp4 -i {file_download_path}{data_title}.mp3 -c:v copy -c:a aac -strict experimental {file_download_path}{data_title}_{line}.mp4'
        subprocess.run(commond, shell=True)
        os.remove(f'{file_download_path}{data_title}.mp3')
        os.remove(f'{file_download_path}{data_title}.mp4')
    context.close()


with sync_playwright() as playwright:
    run(playwright)
