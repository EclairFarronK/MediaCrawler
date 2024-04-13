import os

from playwright.sync_api import Playwright, sync_playwright, expect

USER_DATA_DIR = "%s_user_data_dir"


def run(playwright: Playwright) -> None:
    context = playwright.firefox.launch_persistent_context(headless=False,
                                                           user_data_dir=os.path.join(os.getcwd(), "browser_data",
                                                                                      USER_DATA_DIR % 'bili'))
    # todo 创建7个线程
    page = context.new_page()

    # browser.pages[1]
    page.goto("https://www.douyin.com/follow")
    page.get_by_role("listitem").filter(has_text="きっと").click()
    page.wait_for_timeout(7000)
    # 根据多个条件去搜索
    locators = page.locator('xg-video-container video source:nth-child(3)').all()
    print(len(locators))
    print(locators[2].get_attribute('src'))
    page.wait_for_timeout(7000)
    list = page.locator('.XWJRuUYW #').all()
    print(len(list))
    for count in range(len(list)):
        page.locator("a").filter(has_text=list[count + 1].inner_text()).click()
        # 第三个的第三个
        page.wait_for_timeout(2000)
        locators = page.locator('xg-video-container video source:nth-child(3)').all()
        print(len(locators))
        print(locators[2].get_attribute('src'))
        # list有了新的变化
        list = page.locator('.XWJRuUYW .ztA3qIFr').all()
    #     根据链接下载的方法
    # ---------------------
    context.close()


with sync_playwright() as playwright:
    run(playwright)

