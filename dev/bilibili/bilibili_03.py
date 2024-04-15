import os
import mysql.connector
from playwright.sync_api import Playwright, sync_playwright

# 设置浏览器缓存位置
USER_DATA_DIR = '%s_user_data_dir'


def run(playwright: Playwright) -> None:
    browser = playwright.firefox.launch_persistent_context(headless=False,
                                                           user_data_dir=os.path.join(os.getcwd(), 'browser_data',
                                                                                      USER_DATA_DIR % 'bili'))
    page = browser.new_page()

    # 建立数据库连接
    conn = mysql.connector.connect(
        host="43.156.129.154",
        user="tsp",
        password="199409_ad",
        database="tsp"
    )
    # 获取游标
    cursor = conn.cursor()
    # 执行SQL查询
    cursor.execute("SELECT user_id,name FROM user")
    # 获取查询结果
    user_info = cursor.fetchall()

    for user in user_info:
        user_id = user[0]
        user_name = user[1]
        query = 'SELECT bvid FROM bvid WHERE user_id = %s'
        cursor.execute(query, (user_id,))
        list_bvid_00 = cursor.fetchall()
        list_bvid_01 = []
        for i in list_bvid_00:
            list_bvid_01.append(i[0])
        url = f'https://space.bilibili.com/{user_id}/video?tid=0'
        page.goto(url)
        page.wait_for_timeout(1000)
        list_bvid_02 = method_name(page)
        list_bvid_update = list(set(list_bvid_02) - set(list_bvid_01))
        sql_01(conn, cursor, list_bvid_update, user_id, user_name)
        if (len(list_bvid_update) < len(list_bvid_02)):
            continue

        total = int(page.locator('.be-pager-total').inner_text().split()[1])
        for i in range(total - 1):
            if total == 2:
                page.get_by_role('listitem', name=f'最后一页:{total}', exact=True).click()
            elif i == total - 2:
                page.get_by_role('listitem', name=f'最后一页:{total}', exact=True).click()
            else:
                s = str(i + 2)
                page.get_by_role('listitem', name=s, exact=True).click()
            page.wait_for_timeout(1000)
            list_bvid_03 = method_name(page)
            list_bvid_update = list(set(list_bvid_03) - set(list_bvid_01))
            sql_01(conn, cursor, list_bvid_update, user_id, user_name)
            if (len(list_bvid_update) < len(list_bvid_03)):
                break
    # 关闭游标和连接
    cursor.close()
    conn.close()
    browser.close()


def sql_01(conn, cursor, list_bvid_update, user_id, user_name):
    list_bvid_update_sql = []
    for bvid_update in list_bvid_update:
        list_bvid_update_sql.append((user_id, user_name, bvid_update))
    sql = "INSERT INTO bvid (user_id, name, bvid) VALUES (%s, %s, %s)"
    cursor.executemany(sql, list_bvid_update_sql)
    conn.commit()


def method_name(page):
    list_01 = []
    for i in page.locator('.list-list li').all():
        list_01.append(i.get_attribute('data-aid'))
    return list_01


with sync_playwright() as playwright:
    run(playwright)
