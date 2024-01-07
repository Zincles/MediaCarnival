from urllib.parse import quote
from requests import Response
import requests


def request_movie_detail_by_id(authorization: str, movie_id="", append_to_response="", language="zh-CN") -> Response:
    """通过id,查询电影的信息。"""
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?append_to_response={append_to_response}&language={language}"
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
    """搜索多种媒体，不局限于电影。"""
    url = f"https://api.themoviedb.org/3/search/multi?query={quote(query)}&include_adult={str(include_adult).lower()}&language={language}&page={page}"
    headers = {"accept": "application/json", "Authorization": authorization}
    response = requests.get(url, headers=headers)
    return response
