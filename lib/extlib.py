import os

## 获取文件的扩展名，不带点
def get_ext_no_dot(filename: str) -> str:
    return os.path.splitext(filename)[1][1:]

## 获取文件的类型.可包括路径
def get_file_type(filename: str) -> str:
    if os.path.isdir(filename):
        return "folder"
    ext_no_dot = get_ext_no_dot(filename)
    if ext_no_dot in ["jpg", "jpeg", "png", "gif", "webp", "svg"]:
        return "image"
    elif ext_no_dot in ["mp4", "mkv", "webm"]:
        return "video"
    elif ext_no_dot in ["mp3", "wav", "ogg", "flac"]:
        return "audio"
    elif ext_no_dot in ["txt", "md", "html", "css", "js", "py", "cpp", "c", "h", "java", "go", "php", "ass", "vtt", "srt"]:
        return "text"
    elif ext_no_dot in ["pdf"]:
        return "pdf"
    else:
        return "other"