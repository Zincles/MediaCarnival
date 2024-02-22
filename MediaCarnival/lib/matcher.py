import os
import re

## 这是一个在媒体库中用于匹配并识别 Episode / Season 的库。
## 该库有多种匹配模式，会尝试自适应找到最合适的（也就是变数最多的）匹配模式。
## 不过，前提是输入的字符串们的模式是一致的————变数不能太多。
## 另外，Season的上限是99.

## 目前代码写的很野，这完全取决于作者精神状态（现在是半夜4:46AM）。
## TODO 这个库远远没有编写完毕。还有很多路要走！

EPISODE_PATTERN_JELLYFIN = r"(?<=E)\d{1,}"  # S01E01
EPISODE_PATTERN_BRACKET = r"(?<=\[)\d{1,}(?=\])"  # [01]
EPISODE_PATTERN_EVERYNUMBER = r"\d{1,}"  # 01

SEASON_PATTERN_JELLYFIN = r"(?<=S)\d{1,}"  # S01E01
SEASON_PATTERN_EVERYNUMBER = r"\d{1,2}"  # 01


def regex_get_all(raw_str: str, pattern: str) -> list[str]:
    "获取匹配到正则表达式的所有字符串。"
    return re.findall(pattern, raw_str)


def regex_get_at(raw_str: str, pattern: str, n: int = 0) -> str:
    "获取第n个匹配到正则表达式的字符串。如果没有匹配到或者越界，则返回空字符串。"
    r_str = re.findall(pattern, raw_str)
    if n <= len(r_str) - 1:
        return r_str[n]
    else:
        return ""


def regex_get_num(raw_str: str, pattern: str):
    "获取有多少个匹配到的字符串。"
    return len(re.findall(pattern, raw_str))


def regex_get_diff(raw_strs: list[str], pattern: str):
    """
    获取匹配到的字符串的变数。仅限相似的字符串使用。
    例如，对于 ['S01E01_1080p','S01E02_1080p','S01E03_1080p'], 匹配其EVERYNUMBER的变数为[1,3,1]。
    """
    index: list[set] = [set() for i in range(regex_get_num(raw_strs[0], pattern))]

    if not regex_is_similar(raw_strs, pattern):
        return []

    # 遍历每个字符串。将每个字符串对应位置的匹配结果加入到index中。
    for i in range(len(raw_strs)):
        for j in range(regex_get_num(raw_strs[i], pattern)):
            index[j].add(regex_get_at(raw_strs[i], pattern, j))

    return [len(i) for i in index]  # 返回变数数组。


def regex_is_similar(raw_strs: list[str], pattern: str) -> bool:
    "判断字符串们是否相似。不相似的字符串没有可比性。需要检验匹配结果长度是否一致。空数组视为True"
    if len(raw_strs) == 0:
        return True
    length = regex_get_num(raw_strs[0], pattern)
    for i in raw_strs:
        if regex_get_num(i, pattern) != length:
            return False
    return True


def get_episode_mapping(raw_strs: list[str]) -> dict:
    """
    输入一组文件名, 依次通过上述匹配模式, 计算episode
    JELLYFIN和BRACKET模式如果匹配成功则会直接认为是最终结果。
    EVERYNUMBER模式会尝试匹配所有的数字, 并返回变数最大的一个,也就是尝试尽可能忽略掉不是episode的数字(它们大概率是相同的)。
    如果文件过乱，则返回空字典。
    """
    is_similar = True
    is_similar = is_similar and regex_is_similar(raw_strs, EPISODE_PATTERN_JELLYFIN)
    is_similar = is_similar and regex_is_similar(raw_strs, EPISODE_PATTERN_BRACKET)
    is_similar = is_similar and regex_is_similar(raw_strs, EPISODE_PATTERN_EVERYNUMBER)
    if not is_similar:  # 关联性太差，无法匹配
        print("文件名关联性太差, 无法匹配Episode。")
        return {}
    if raw_strs == []:  # 空数组
        print("空数组，无法匹配Episode。")
        return {}

    result = {}

    # 尝试JELLYFIN模式 匹配Episode
    if regex_get_all(raw_strs[0], EPISODE_PATTERN_JELLYFIN):
        for s in raw_strs:
            if regex_get_all(s, EPISODE_PATTERN_JELLYFIN):
                result[s] = int(regex_get_at(s, EPISODE_PATTERN_JELLYFIN))
        print("JELLYFIN模式匹配Episode成功")
        return result

    # 尝试BRACKET模式 匹配Episode
    elif regex_get_all(raw_strs[0], EPISODE_PATTERN_BRACKET):
        for s in raw_strs:
            if regex_get_all(s, EPISODE_PATTERN_BRACKET):
                result[s] = int(regex_get_at(s, EPISODE_PATTERN_BRACKET))
        print("BRACKET模式匹配Episode成功")
        return result
    else:
        print("JELLYFIN和BRACKET模式匹配Episode均失败。尝试寻找最优EVERYNUMBER模式。")

    # 尝试EVERYNUMBER模式 匹配Episode。返回变数最大的一个。如果最大变数小于输入字符串的数量的一半，则认为匹配失败。
    for i in range(regex_get_num(raw_strs[0], EPISODE_PATTERN_EVERYNUMBER)):
        if regex_get_diff(raw_strs, EPISODE_PATTERN_EVERYNUMBER)[i] > len(raw_strs) / 2:
            for s in raw_strs:
                result[s] = int(regex_get_at(s, EPISODE_PATTERN_EVERYNUMBER, i))
            print("EVERYNUMBER模式匹配Episode成功")
            return result

    print("EVERYNUMBER模式匹配Episode失败。")
    return {}


def get_season_mapping(raw_strs: list[str]) -> dict:
    """
    输入一组文件名, 依次通过上述匹配模式, 计算season
    JELLYFIN模式如果匹配成功则会直接认为是最终结果。
    EVERYNUMBER模式会尝试匹配所有的数字, 并返回变数第二大的一个,也就是尝试尽可能忽略掉不是season的数字(它们大概率是相同的)。
    如果文件过乱，则返回空字典。
    """

    is_similar = True
    is_similar = is_similar and regex_is_similar(raw_strs, SEASON_PATTERN_JELLYFIN)
    is_similar = is_similar and regex_is_similar(raw_strs, SEASON_PATTERN_EVERYNUMBER)
    if not is_similar:  # 关联性太差，无法匹配
        print("文件名关联性太差, 无法匹配Season。")
        return {}
    if raw_strs == []:  # 空数组
        print("空数组，无法匹配Season。")
        return {}

    result = {}

    # 尝试JELLYFIN模式 匹配Season
    if regex_get_all(raw_strs[0], SEASON_PATTERN_JELLYFIN):
        for s in raw_strs:
            if regex_get_all(s, SEASON_PATTERN_JELLYFIN):
                result[s] = int(regex_get_at(s, SEASON_PATTERN_JELLYFIN))
        print("JELLYFIN模式匹配Season成功")
        return result

    # # TODO 进行优化，增加识别准确度

    # # 尝试EVERYNUMBER模式 匹配Season。返回变数第二大的一个。如果第二大变数大于100，则认为匹配失败。
    # diffs = regex_get_diff(raw_strs, SEASON_PATTERN_EVERYNUMBER)
    # diffs.sort(reverse=True)
    # for i in range(regex_get_num(raw_strs[0], SEASON_PATTERN_EVERYNUMBER)):
    #     if diffs[i] <= 100:
    #         for s in raw_strs:
    #             result[s] = int(regex_get_at(s, SEASON_PATTERN_EVERYNUMBER, i))
    #         print("EVERYNUMBER模式匹配Season成功")
    #         return result
    # print("EVERYNUMBER模式匹配Season失败。")

    # 直接返回1.
    for s in raw_strs:
        result[s] = 1
    print("Jellyfin模式匹配失败。所有剧集视为第一季。")
    return result


# RAW_ARR = [
#     "[Sakurato] Mahou Shoujo ni Akogarete1 [01][AVC-8bit 1080P AAC][CHS]",
#     "[Sakurato] Mahou Shoujo ni Akogarete1 [02][AVC-8bit 1080P AAC][CHS]",
#     "[Sakurato] Mahou Shoujo ni Akogarete1 [03][AVC-8bit 1080P AAC][CHS]",
# ]

# JEL_ARR = [
#     "SOME_SHOW - S02E01 - SOME_EPISODE 01 [1080p]",
#     "SOME_SHOW - S03E02 - SOME_EPISODE 02 [1080p]",
#     "SOME_SHOW - S04E03 - SOME_EPISODE 03 [1080p]",
# ]

# BAD_ARR = [
#     "Channel 6 - SOME_EPISODE 01 [1080p]",
#     "Channel 6 - SOME_EPISODE 02 [1080p]",
#     "Channel 6 - SOME_EPISODE 03 [1080p]",
#     "Channel 6 - SOME_EPISODE 04 [1080p]",
# ]

# RAW = "[Sakurato] Mahou Shoujo ni Akogarete [05][AVC-8bit 1080P AAC][CHS]"


# os.system("clear")
# v = get_episode_mapping(BAD_ARR)
# for i in v:
#     print(i, "\t", v[i])
