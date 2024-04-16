import os
import json
import requests
import subprocess
from dev.tool.database import conn
from dev.tool.tools import sanitize_filename
from playwright.sync_api import Playwright, sync_playwright

# todo 从数据库查询根据bvid直接去下载
path = 'G:/bilibili'
USER_DATA_DIR = '%s_user_data_dir'
url = 'https://www.bilibili.com/video/'
headers = {
    'referer': 'https://www.bilibili.com/video/BV1A3411b7gm',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36',
}
cursor = conn.cursor()


def start(playwright: Playwright) -> None:
    cursor.execute('SELECT name,bvid FROM bvid WHERE is_download = 0 AND can_download =0')
    list_01 = cursor.fetchall()
    print(f'下载总数：{len(list_01)} {list_01}')

    context = playwright.firefox.launch_persistent_context(headless=True,
                                                           user_data_dir=os.path.join(os.getcwd(), 'browser_data',
                                                                                      USER_DATA_DIR % 'bili'))
    page = context.new_page()
    # todo 这一段怎么异步来提高效率？
    remain = 0
    for line in list_01:
        name = line[0]
        bvid = line[1]
        try:
            file_download_path = f'{path}/{name}/'
            os.makedirs(file_download_path, exist_ok=True)
            # todo 打印url
            print(url + bvid)
            page.goto(url + bvid)
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
            print('{:*^30}'.format(f'剩余：{len(list_01) - remain}'))
            remain = remain + 1

            # 合并，将之前的删除
            # todo 第三步
            commond = f'ffmpeg -i {file_download_path}{data_title}.mp4 -i {file_download_path}{data_title}.mp3 -c:v copy -c:a aac -strict experimental {file_download_path}{data_title}_{line[1]}.mp4'
            subprocess.run(commond, shell=True)
            os.remove(f'{file_download_path}{data_title}.mp3')
            os.remove(f'{file_download_path}{data_title}.mp4')
            # todo 还没有测试
            cursor.execute('UPDATE bvid SET is_download = 1 WHERE bvid = %s', (bvid,))
            conn.commit()
        except Exception as e:
            print(str(e))
            # todo 还没有测试
            cursor.execute('UPDATE bvid SET can_download = 1, comment = %s WHERE bvid = %s', (str(e), bvid,))
            conn.commit()
    context.close()


def method_name(commond):
    subprocess.run(commond, shell=True)


with sync_playwright() as playwright:
    start(playwright)
