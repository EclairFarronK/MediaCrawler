import os
import json
import subprocess
import requests
from dev.tool.tools import sanitize_filename
from playwright.sync_api import Playwright, sync_playwright

# todo 文件夹名字
# todo 输入文件名，提取bvid，然后下载
name = '孬子妹'
file_download_path = f'G:/bilibili/{name}/'
# 目录没有就创建
os.makedirs(file_download_path, exist_ok=True)

file_name = f'./data/{name}.txt'
USER_DATA_DIR = '%s_user_data_dir'
url = 'https://www.bilibili.com/video/'
headers = {
    'referer': 'https://www.bilibili.com/video/BV1A3411b7gm',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
}


def start(playwright: Playwright) -> None:
    # 读取文件内容，并将每行作为列表的一个元素
    with open(file_name, 'r') as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]

    # 获取视频的bv号，去重
    lists = []
    files = os.listdir(file_download_path)
    for file in files:
        start_index = file.rfind('_') + 1
        end_index = file.rfind('.mp4')
        if start_index != -1 and end_index != -1:
            video_id = file[start_index:end_index]
            lists.append(video_id)
        else:
            print('没有找到符合条件的字符串')

    difference = set(lines) - set(lists)
    lines = list(difference)
    print(lines)
    print(f'下载总数：{len(lines)} {lines}')

    context = playwright.firefox.launch_persistent_context(headless=True,
                                                           user_data_dir=os.path.join(os.getcwd(), 'browser_data',
                                                                                      USER_DATA_DIR % 'bili'))
    page = context.new_page()
    # todo 这一段怎么异步来提高效率？
    remain = 0
    for line in lines:
        try:
            # todo 打印url
            page.goto(url + line)
            print(url + line)
            url_list = page.locator('head script').all()
            data_title = page.locator('[data-title]').get_attribute('data-title')
            data_title = sanitize_filename(data_title)

            flag = 0
            for i in url_list:
                if flag == 3:
                    original = i.inner_text()
                    result = original.replace('window.__playinfo__=', '')
                    data = json.loads(result)
                    url_video_download = data["data"]['dash']['video'][0]['baseUrl']
                    url_audio_download = data["data"]['dash']['audio'][0]['baseUrl']
                    break
                flag = flag + 1
            #     todo 不去研究了
            # resp = page.request.get(url=url_download, headers=headers)
            # todo 第二步
            resp = requests.get(url_video_download, headers=headers).content
            download_path = os.path.join(file_download_path, data_title + '.mp4')  # 构造下载路径
            with open(download_path, mode='wb') as file:
                file.write(resp)
            print('{:*^30}'.format(f'下载完成：{data_title}'))

            resp = requests.get(url_audio_download, headers=headers).content
            download_path = os.path.join(file_download_path, data_title + '.mp3')  # 构造下载路径
            with open(download_path, mode='wb') as file:
                file.write(resp)
            print('{:*^30}'.format(f'下载完成：{data_title}'))
            print('{:*^30}'.format(f'剩余：{len(lines) - remain}'))
            remain = remain + 1

            # 合并，将之前的删除
            # todo 第三步
            commond = f'ffmpeg -i {file_download_path}{data_title}.mp4 -i {file_download_path}{data_title}.mp3 -c:v copy -c:a aac -strict experimental {file_download_path}{data_title}_{line}.mp4'
            subprocess.run(commond, shell=True)
            os.remove(f'{file_download_path}{data_title}.mp3')
            os.remove(f'{file_download_path}{data_title}.mp4')
        except Exception as e:
            print(e)
    context.close()


def method_name(commond):
    subprocess.run(commond, shell=True)


with sync_playwright() as playwright:
    start(playwright)
