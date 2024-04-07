import os

from playwright.sync_api import Playwright, sync_playwright, expect

USER_DATA_DIR = "%s_user_data_dir"


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch(headless=False,
                                        user_data_dir=os.path.join(os.getcwd(), "browser_data",
                                                                   USER_DATA_DIR % 'bili'))
    context = browser.new_context()
    page = context.new_page()

    browser.close()


with sync_playwright() as playwright:
    run(playwright)
