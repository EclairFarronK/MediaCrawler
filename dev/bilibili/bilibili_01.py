import os
from playwright.sync_api import Playwright, sync_playwright

# path
file_path = './data/'
# 设置浏览器缓存位置
USER_DATA_DIR = '%s_user_data_dir'


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch_persistent_context(headless=False,
                                                           user_data_dir=os.path.join(os.getcwd(), 'browser_data',
                                                                                      USER_DATA_DIR % 'bili'))
    page = browser.new_page()

    # 从文件中读取信息
    with open('./up', 'r', encoding="utf-8") as file:
        lines = file.readlines()
    # 去掉空格
    lines = [line.strip() for line in lines]
    for line in lines:
        up = line.split(' ')[1]
        url = f'https://space.bilibili.com/{up}/video?tid=0'
        page.goto(url)

        file_name = page.locator('#h-name').inner_text() + '.txt'

        # 目录没有就创建
        os.makedirs(file_path, exist_ok=True)
        file_path_name = file_path + file_name

        # # 删除文件
        # if os.path.exists(file_path_name):
        #     # 如果文件存在，则删除
        #     os.remove(file_path_name)
        #     print(f"文件 '{file_name}' 已删除")
        # else:
        #     # 如果文件不存在，则输出消息
        #     print(f"文件 '{file_name}' 不存在，无需删除")

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

        page.wait_for_timeout(500)
    browser.close()

# todo 插入数据库，如果影响返回为0就break
def method_name(page, file_path_name):
    page.wait_for_timeout(500)
    for i in page.locator('.list-list li').all():
        with open(file_path_name, 'a') as file:
            file.write(i.get_attribute('data-aid') + '\n')


with sync_playwright() as playwright:
    run(playwright)
