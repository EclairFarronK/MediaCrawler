import os
import json
import requests
from playwright.sync_api import Playwright, sync_playwright

# bvid
str = 'BV1k64y1D7hy'
USER_DATA_DIR = '%s_user_data_dir'
url = 'https://www.bilibili.com/video/' + str
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
    page.goto(url)
    list = page.locator('head script').all()
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
    download_path = os.path.join('D:\\video', 'filename.mp4')  # 构造下载路径
    with open(download_path, mode='wb') as file:
        file.write(resp)
    print("{:*^30}".format(f"下载完成：{'filename'}"))

    resp = requests.get(url_audio_download, headers=headers).content
    download_path = os.path.join('D:\\video', 'filename.mp3')  # 构造下载路径
    with open(download_path, mode='wb') as file:
        file.write(resp)
    print("{:*^30}".format(f"下载完成：{'filename'}"))
    context.close()


with sync_playwright() as playwright:
    run(playwright)
