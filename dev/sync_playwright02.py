from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # browser = p.chromium.launch(headless=False)
    browser = p.firefox.launch(headless=False,
                                )
    page = browser.new_page()
    page.goto("https://www.byhy.net/_files/stock1.html")
    print(page.title())
    page.locator('#kw').fill('通讯\n')
    page.locator('#go').click()
    # 打印所有搜索内容
    lcs = page.locator(".result-item").all()
    for lc in lcs:
        print(lc.inner_text())
    browser.close()
p.stop()
