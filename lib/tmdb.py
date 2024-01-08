from urllib.parse import quote
from requests import Response
import requests

## TODO 编写用于进行查询的实例。 以下调用API的代码是底层的。
## 这代表它们相当不完善，甚至没有异常处理，这意味着它们只能被包装在其他更完善的类里，而不是直接用于业务逻辑。
## 除此之外，我大概还得做好缓存工作，防止针对TMDB的大量查询导致自己IP被ban...
## 我不太能把自己的API明文编写到这里，很抱歉。你需要自行申请API。反正也是免费的。


def request_movie_detail(authorization: str, movie_id: int, append_to_response="", language="zh-CN") -> Response:
    """查询电影的信息。"""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?append_to_response={append_to_response}&language={language}"
    headers = {"accept": "application/json", "Authorization": authorization}
    response: Response = requests.get(url, headers=headers)
    return response


def request_tv_series_detail(authorization: str, series_id: int, append_to_response="", language="zh-CN") -> Response:
    """查询电视剧的总信息。"""
    url = f"https://api.themoviedb.org/3/tv/{series_id}?append_to_response={append_to_response}&language={language}"
    headers = {"accept": "application/json", "Authorization": authorization}
    response: Response = requests.get(url, headers=headers)
    return response


def request_tv_season_detail(
    authorization: str, series_id: int, season_number: int, append_to_response="", language="zh-CN"
) -> Response:
    """查询电视剧节目的某季的信息。"""
    url = f"https://api.themoviedb.org/3/tv/{series_id}/season/{season_number}?append_to_response={append_to_response}&language={language}"
    headers = {"accept": "application/json", "Authorization": authorization}
    response: Response = requests.get(url, headers=headers)
    return response


def request_tv_episode_detail(
    authorization: str, series_id: int, season_number: int, episode_number: int, append_to_response="", language="zh-CN"
) -> Response:
    """查询电视剧节目的某季的信息。"""
    url = f"https://api.themoviedb.org/3/tv/{series_id}/season/{season_number}/episode/{episode_number}?append_to_response={append_to_response}&language={language}"
    headers = {"accept": "application/json", "Authorization": authorization}
    response: Response = requests.get(url, headers=headers)
    return response


def request_search_multi(
    authorization: str,
    query: str,
    include_adult: bool = True,
    language: str = "zh-CN",
    page: int = 1,
):
    """使用字符串搜索媒体的信息"""
    url = f"https://api.themoviedb.org/3/search/multi?query={quote(query)}&include_adult={str(include_adult).lower()}&language={language}&page={page}"
    headers = {"accept": "application/json", "Authorization": authorization}
    response = requests.get(url, headers=headers)
    return response


def request_image(img_path: str, size="original"):
    """根据api中获取的相对url,获取图像信息。"""
    url = f"https://image.tmdb.org/t/p/{size}/{img_path}"  # 完整 URL
    response = requests.get(url)  # 下载图片资源
    return response
