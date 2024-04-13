import re


def sanitize_filename(filename):
    # 定义不合规字符的正则表达式
    invalid_chars_regex = r'[\"*<>?\\|/:,]'
    # 替换不合规字符为空格
    sanitized_filename = re.sub(invalid_chars_regex, ' ', filename)
    return sanitized_filename
