import os
from playwright.sync_api import Playwright, sync_playwright

USER_DATA_DIR = '%s_user_data_dir'
str = '1340190821'
url = 'https://space.bilibili.com/' + str + '/video?tid=0'


def run(playwright: Playwright) -> None:
    print(os.getcwd())
    browser = playwright.firefox.launch_persistent_context(headless=False,
                                                           user_data_dir=os.path.join(os.getcwd(), "browser_data",
                                                                                      USER_DATA_DIR % 'bili'))
    page = browser.new_page()
    page.goto(url)

    method_name(page)

    total = int(page.locator('.be-pager-total').inner_text().split()[1])
    print(total)
    for i in range(total - 1):
        if i == total - 1:
            page.get_by_role("listitem", name="最后一页:").click()
        else:
            s = str(i + 2)
            page.get_by_role("listitem", name=s).click()

        method_name(page)

    page.wait_for_timeout(3000)
    browser.close()


def method_name(page):
    page.wait_for_timeout(3000)
    for i in page.locator('.list-list li').all():
        with open('output.txt', 'a') as file:
            file.write(i.get_attribute('data-aid') + '\n')


with sync_playwright() as playwright:
    run(playwright)
