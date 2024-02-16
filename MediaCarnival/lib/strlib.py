def truncate_middle(string, keep_start=20, keep_end=20, separator=" ... "):
    """缩减字符串的中间部分，保留开头和结尾部分"""
    if len(string) <= keep_start + keep_end:
        return string
    else:
        return string[:keep_start] + separator + string[-keep_end:]
