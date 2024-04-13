import os
import requests
import json
import re
from bs4 import BeautifulSoup
import subprocess
# from detail_video import video_bvid

# video_bvid 是一个从外部得到的单个视频ID
video_bvid = 'BV1Gm421E7yW'


class BilibiliVideoAudio:
    def __init__(self, bvid):
        self.bvid = bvid
        self.headers = {
            "referer": "https://search.bilibili.com/all?keyword=%E4%B8%BB%E6%92%AD%E8%AF%B4%E8%81%94%E6%92%AD&from_source=webtop_search&spm_id_from=333.1007&search_source=5&page=4&o=90",
            "origin": "https://search.bilibili.com",
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0',
            'Accept-Encoding': 'gzip, deflate, br'
        }

    def get_video_audio(self):
        # 构造视频链接并发送请求获取页面内容
        url = f'https://www.bilibili.com/video/{self.bvid}/?spm_id_from=333.337.search-card.all.click&vd_source=14378ecd144bed421affe1fe0ddd8981'
        content = requests.get(url, headers=self.headers).content.decode('utf-8')
        soup = BeautifulSoup(content, 'html.parser')

        # 获取视频标题
        meta_tag = soup.head.find('meta', attrs={'name': 'title'})
        title = meta_tag['content']

        # 获取视频和音频链接
        pattern = r'window\.__playinfo__=({.*?})\s*</script>'
        json_data = re.findall(pattern, content)[0]
        data = json.loads(json_data)

        video_url = data['data']['dash']['video'][0]['base_url']
        audio_url = data['data']['dash']['audio'][0]['base_url']

        return {
            'title': title,
            'video_url': video_url,
            'audio_url': audio_url
        }

    def download_video_audio(self, url, filename):
        # 对文件名进行清理，去除不合规字符
        filename = self.sanitize_filename(filename)
        try:
            # 发送请求下载视频或音频文件
            resp = requests.get(url, headers=self.headers).content
            print(filename.__class__)
            print(filename)
            download_path = os.path.join('D:\\video', filename)  # 构造下载路径
            with open(download_path, mode='wb') as file:
                file.write(resp)
            print("{:*^30}".format(f"下载完成：{filename}"))
        except Exception as e:
            print(e)

    def sanitize_filename(self, filename):
        # 定义不合规字符的正则表达式
        invalid_chars_regex = r'[\"*<>?\\|/:,]'

        # 替换不合规字符为空格
        sanitized_filename = re.sub(invalid_chars_regex, ' ', filename)

        return sanitized_filename

    def merge_video_audio(self, video_path, audio_path, output_path):
        """
        使用ffmpeg来合并视频和音频。
        """
        try:
            command = [
                'ffmpeg',
                '-y',  # 覆盖输出文件如果它已经存在
                '-i', video_path,  # 输入视频路径
                '-i', audio_path,  # 输入音频路径
                '-c', 'copy',  # 复制原始数据，不进行转码
                output_path  # 输出视频路径
            ]
            subprocess.run(command, check=True)
            print(f"视频和音频合并完成：{output_path}")
        except subprocess.CalledProcessError as e:
            print(f"合并失败: {e}")


def main():
    try:
        # 只处理一个 bvid
        bilibili = BilibiliVideoAudio(video_bvid)
        video_audio_info = bilibili.get_video_audio()

        title = video_audio_info['title']
        video_url = video_audio_info['video_url']
        audio_url = video_audio_info['audio_url']

        processed_videos_path = 'D:\\processed_videos'
        if not os.path.exists(processed_videos_path):
            os.makedirs(processed_videos_path)

        video_filename = f"{title}.mp4"
        audio_filename = f"{title}.mp3"
        output_filename = f"{title} - combined.mp4"

        video_file_path = os.path.join('D:\\video', video_filename)
        audio_file_path = os.path.join('D:\\video', audio_filename)
        output_file_path = os.path.join(processed_videos_path, output_filename)

        bilibili.download_video_audio(video_url, video_filename)  # 下载视频
        bilibili.download_video_audio(audio_url, audio_filename)  # 下载音频
        bilibili.merge_video_audio(video_file_path, audio_file_path, output_file_path)  # 合并视频和音频

        # Optional: Delete the separate files after merge
        # os.remove(video_file_path)
        # os.remove(audio_file_path)

    except Exception as ex:
        print(f"Failed to process video/audio for {video_bvid}: {ex}")


main()