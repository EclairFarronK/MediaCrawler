import os
from playwright.sync_api import Playwright, sync_playwright

# todo 输入up主的这个号就行了
str = '3546595161278780'
USER_DATA_DIR = '%s_user_data_dir'
url = 'https://space.bilibili.com/' + str + '/video?tid=0'


# todo 根据bvid下载视频
# todo 对比下载量和实际总数，是是否一样，
# todo playwright有没有检测http请求的方法？
# todo 需要一个去重的脚本，如果发现有重复的给提示
# todo 自动拉取，看是否更新，如果更新就下载新的
# todo playwright可以主动发起http请求吗？
def run(playwright: Playwright) -> None:
    print(os.getcwd())
    browser = playwright.firefox.launch_persistent_context(headless=False,
                                                           user_data_dir=os.path.join(os.getcwd(), 'browser_data',
                                                                                      USER_DATA_DIR % 'bili'))
    page = browser.new_page()
    page.goto(url)

    method_name(page)

    total = int(page.locator('.be-pager-total').inner_text().split()[1])
    print(total)
    for i in range(total - 1):
        if total == 2:
            page.get_by_role('listitem', name='最后一页:').click()
        elif i == total - 1:
            page.get_by_role('listitem', name='最后一页:').click()
        else:
            s = str(i + 2)
            page.get_by_role('listitem', name=s).click()

        method_name(page)

    page.wait_for_timeout(3000)
    browser.close()


def method_name(page):
    page.wait_for_timeout(3000)
    for i in page.locator('.list-list li').all():
        with open('output.txt', 'a') as file:
            file.write(i.get_attribute('data-aid') + '\n')


# todo 这里为什么要用异步？
with sync_playwright() as playwright:
    run(playwright)
