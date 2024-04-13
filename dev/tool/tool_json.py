# 从json中提取数据
import json

with open('json.json', 'r', encoding='utf-8') as file:
    data = json.load(file)
print(data)
name = data["data"]['list']['vlist']
print(len(name))
for item in name:
    print(item['title'] + '_T_' + item['bvid'])
