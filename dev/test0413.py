import os
import re

import requests

headers = {
    "referer": "https://search.bilibili.com/all?keyword=%E4%B8%BB%E6%92%AD%E8%AF%B4%E8%81%94%E6%92%AD&from_source=webtop_search&spm_id_from=333.1007&search_source=5&page=4&o=90",
    "origin": "https://search.bilibili.com",
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
    'Accept-Encoding': 'gzip, deflate, br'
}
url = 'https://cn-hncs-cu-01-01.bilivideo.com/upgcxcode/52/13/1502851352/1502851352-1-16.mp4?e=ig8euxZM2rNcNbRVhwdVhwdlhWdVhwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&uipk=5&nbs=1&deadline=1713018971&gen=playurlv2&os=bcache&oi=3704285647&trid=0000f0859819a9574243a36fc99a6bc3cc24h&mid=28444445&platform=html5&upsig=c6e93943b94996c646c4e2610ef396a8&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,mid,platform&cdnid=3290&bvc=vod&nettype=0&f=h_0_0&bw=60145&logo=80000000'
filename = 'a.mp4'


def sanitize_filename( filename):
    # 定义不合规字符的正则表达式
    invalid_chars_regex = r'[\"*<>?\\|/:,]'
    # 替换不合规字符为空格
    sanitized_filename = re.sub(invalid_chars_regex, ' ', filename)
    return sanitized_filename


def download_video_audio(url, filename):
    # 对文件名进行清理，去除不合规字符
    filename = sanitize_filename(filename)
    try:
        # 发送请求下载视频或音频文件
        resp = requests.get(url, headers=headers).content
        print(filename.__class__)
        print(filename)
        download_path = os.path.join('D:\\video', filename)  # 构造下载路径
        with open(download_path, mode='wb') as file:
            file.write(resp)
        print("{:*^30}".format(f"下载完成：{filename}"))
    except Exception as e:
        print(e)


download_video_audio(url, filename)
