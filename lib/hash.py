import hashlib


def get_file_hash(file_abs_path, algo="md5", BUF_SIZE=1024 * 512):
    """
    获取一个文件的哈希值. 可用于对付大文件.
    BUF_SIZE 完全是任意的,这里选取512KB
    目前支持blake2b 和 md5
    """
    match algo:
        case "blake2b":
            cur_hash = hashlib.blake2b()
        case "md5":
            cur_hash = hashlib.md5()
        case _:
            raise Exception("算法选择错误!不存在指定的方法!")

    with open(file_abs_path, "rb") as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            cur_hash.update(data)

    return cur_hash.hexdigest()
