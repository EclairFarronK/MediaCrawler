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
print(len(file_names))
list_01 = []
for filename in file_names:
    last_underscore_index = filename.rfind("_")
    mp4_index = filename.rfind(".mp4")
    # 获取两者之间的内容
    content_between = filename[last_underscore_index + 1:mp4_index]
    list_01.append(content_between)
print(len(list_01))
