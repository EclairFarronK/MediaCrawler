import re
import os
import asyncio
import requests
from playwright.async_api import async_playwright


def save_douyin_videos(keyword, file_name, video_url):
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


def filter_filename(filename):
    filtered_filename = re.sub(r'[\\/:*?"<>| ]+', '', filename)
    return filtered_filename


async def search_douyin_videos(keyword, scroll_count):
    async with async_playwright() as p:
        browser = await p.firefox.launch(headless=False)
        # browser = await p.chromium.launch(headless=False,
        #                                   executable_path='C:\Program Files (x86)\Google\Chrome\Application\chrone.exe')
        page = await browser.new_page()
        await page.set_viewport_size({"width": 1280, "height": 800})
        await page.goto('https://www.douyin.com/search/搜索')
        await page.time
        await asyncio.sleep(3)
        # 在输入框中输入“python”
        await page.fill('input', keyword + "视频")
        # 点击搜索按钮
        await page.click('.rB8dMXOc')
        await asyncio.sleep(3)

        links = await page.query_selector_all('.BL9IYM4m')
        arr = []
        titles = []
        for _ in range(scroll_count):
            xgplayers = await page.query_selector_all('.xgplayer')
            for player in xgplayers:
                video_src = await player.inner_html()
                arr.append(video_src)

            await page.evaluate('window.scrollBy(0, window.innerHeight)')
            await asyncio.sleep(3)

        await asyncio.sleep(2)
        titles = await page.query_selector_all('.KxCuain0')
        print(len(arr))
        print(len(titles))
        for i in range(len(arr)):
            if i < len(titles):
                get_title = await titles[i].evaluate('(element) => element.textContent')
                video_src_list = re.findall(r'<video.*?src=["\'](.*?)["\']', arr[i])
                for video_src in video_src_list:
                    print(f"标题: {get_title}")
                    print(f"视频源: https:{video_src}")
                    save_douyin_videos(keyword, get_title, "https:" + video_src)
                    print("-----------")

        await browser.close()


# 调用函数进行搜索
asyncio.run(search_douyin_videos('奶贝', 20))
