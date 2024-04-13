import subprocess

commond = f'ffmpeg -i ./data/邹小荃/Daily vlog.mp4 -i ./data/邹小荃/Daily vlog.mp4.mp3 -c:v copy -c:a aac -strict experimental ./data/邹小荃/Daily vlog.mp4_xxxxx.mp4'
subprocess.run(commond, shell=True)