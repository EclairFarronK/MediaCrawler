import os
import re

import requests

keyword = '奶贝'
file_name = '00111'
file_path = 'E:\project\python\MediaCrawler'
video_url = 'https://v3-web.douyinvod.com/1cd07637a451b12890995d6d12d068bb/660c1417/video/tos/cn/tos-cn-ve-0015c800/3accc747e9484a4d90b3be1511994a57/?a=6383&amp;ch=26&amp;cr=3&amp;dr=0&amp;lr=all&amp;cd=0%7C0%7C0%7C3&amp;cv=1&amp;br=1836&amp;bt=1836&amp;cs=0&amp;ds=3&amp;ft=I~D7TISS9cZxiTBUuRfKp5De4fkaD6WicO7T6x659~_CSzZZONP5zxK5l4JwUx&amp;mime_type=video_mp4&amp;qs=0&amp;rc=NTVnaTszZGkzNmZoPGRkO0BpM3BsZThzdXg7NDMzOmkzM0AxYDJeMmAzNWMxM14uLzJfYSNmai5gMGY2LmJgLS1gLWFzcw%3D%3D&amp;btag=e00010000&amp;cquery=100a&amp;dy_q=1712063992&amp;l=202404022119528920ECD5B765A31B3106'


def filter_filename(filename):
    filtered_filename = re.sub(r'[\\/:*?"<>| ]+', '', filename)
    return filtered_filename


def save_douyin_videos(keyword, file_name, video_url):
    print(video_url)
    folder_name = keyword  # 使用关键词命名文件夹

    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    file_path = os.path.join(folder_name, filter_filename(file_name).replace("...展开", "") + ".mp4")
    if os.path.exists(file_path):
        print(f"文件已存在，跳过保存: {file_path}")
        return
    with open(file_path, 'wb') as f:
        response = requests.get(video_url, stream=True)
        for chunk in response.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)


save_douyin_videos(keyword, file_name, video_url)
