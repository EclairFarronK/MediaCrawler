import os

from playwright.sync_api import Playwright, sync_playwright, expect

USER_DATA_DIR = "%s_user_data_dir"


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch_persistent_context(headless=False,
                                                           user_data_dir=os.path.join(os.getcwd(), "browser_data",
                                                                                      USER_DATA_DIR % 'bili'))
    page = browser.new_page()
    page.goto("https://www.bilibili.com/video/BV1Tx421k7tU/")
    with page.expect_popup() as page3_info:
        page.get_by_role("link",
                         name="如何使内心强大？解析当代年轻人的九大心理防御机制！【围炉夜话】 哔哩哔哩播放器 32.9万 2272 29:42").click()
    page3 = page3_info.value
    page3.close()
    page.get_by_role("link",
                     name="如何使内心强大？解析当代年轻人的九大心理防御机制！【围炉夜话】 哔哩哔哩播放器 32.9万 2272 29:42").press(
        "Insert")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
