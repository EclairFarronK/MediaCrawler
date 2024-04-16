import mysql.connector

# 建立数据库连接
conn = mysql.connector.connect(
    host="43.156.129.154",
    user="tsp",
    password="199409_ad",
    database="tsp"
)

# 获取游标
cursor = conn.cursor()
cursor.execute('SELECT bvid FROM bvid')
results = cursor.fetchall()
list_01=[]
for i in results:
    list_01.append(i[0])
# 关闭游标和连接
cursor.close()
conn.close()

import os


def scan_files(directory):
    file_list = []
    for root, directories, files in os.walk(directory):
        for filename in files:
            file_list.append(os.path.join(root, filename))
    return file_list


def get_file_names(directory):
    files = scan_files(directory)
    file_names = [os.path.basename(file) for file in files]
    return file_names


directory = 'G:/bilibili'
file_names = get_file_names(directory)
list_02 = []
for filename in file_names:
    last_underscore_index = filename.rfind("_")
    mp4_index = filename.rfind(".mp4")
    # 获取两者之间的内容
    content_between = filename[last_underscore_index + 1:mp4_index]
    list_02.append(content_between)
print(len(list_01))
print(len(list_02))
print(set(list_01)-set(list_02))
print(set(list_02)-set(list_01))