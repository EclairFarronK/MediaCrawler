import os
from playwright.sync_api import Playwright, sync_playwright

# todo 输入up主的这个号就行了
up = '94215602'
USER_DATA_DIR = '%s_user_data_dir'
url = f'https://space.bilibili.com/{up}/video?tid=0'
file_path = './data/'


# todo 对比下载量和实际总数，是是否一样，
# todo 需要一个去重的脚本，如果发现有重复的给提示
# todo 自动拉取，看是否更新，如果更新就下载新的
def run(playwright: Playwright) -> None:
    print(os.getcwd())
    browser = playwright.firefox.launch_persistent_context(headless=False,
                                                           user_data_dir=os.path.join(os.getcwd(), 'browser_data',
                                                                                      USER_DATA_DIR % 'bili'))
    page = browser.new_page()
    page.goto(url)

    file_name = page.locator('#h-name').inner_text() + '.txt'

    # 目录没有就创建
    os.makedirs(file_path, exist_ok=True)

    file_path_name = file_path + file_name

    # 删除文件
    if os.path.exists(file_path_name):
        # 如果文件存在，则删除
        os.remove(file_path_name)
        print(f"文件 '{file_name}' 已删除")
    else:
        # 如果文件不存在，则输出消息
        print(f"文件 '{file_name}' 不存在，无需删除")

    method_name(page, file_path_name)

    total = int(page.locator('.be-pager-total').inner_text().split()[1])
    for i in range(total - 1):
        if total == 2:
            page.get_by_role('listitem', name=f'最后一页:{total}', exact=True).click()
        elif i == total - 2:
            page.get_by_role('listitem', name=f'最后一页:{total}', exact=True).click()
        else:
            s = str(i + 2)
            page.get_by_role('listitem', name=s, exact=True).click()

        method_name(page, file_path_name)

    page.wait_for_timeout(1000)
    browser.close()


def method_name(page, file_path_name):
    page.wait_for_timeout(1000)
    for i in page.locator('.list-list li').all():
        with open(file_path_name, 'a') as file:
            file.write(i.get_attribute('data-aid') + '\n')


# todo 这里为什么要用异步？
with sync_playwright() as playwright:
    run(playwright)
