# 从json中提取数据
import json


def json_01():
    with open('json_01.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    print(data)
    name = data["data"]['list']['vlist']
    print(len(name))
    for item in name:
        print(item['title'] + '_T_' + item['bvid'])


def json_02():
    with open('json_02.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
    name = data["data"]['dash']['video'][0]['backupUrl'][0]
    print(name)
    # for item in name:
    #     print(item['title'] + '_T_' + item['bvid'])


json_02()
