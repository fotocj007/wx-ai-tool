# -*- coding: utf-8 -*-
# Author: iniwap
# Date: 2025-06-03
# Description: 用于热搜话题获取，关注项目 https://github.com/iniwap/ai_write_x

# Copyright (c) 2025 iniwap
#
# This software is licensed under the AIWriteX License.
# Non-commercial, personal profit, non-profit derivative distribution, and non-profit service provision are allowed; profit-making sales and services require authorization.
# See the LICENSE.md file in the project root for full details.
#
# 本软件受 AIWriteX 许可证保护。
# 允许非商业、个人盈利、非盈利衍生分发和非盈利服务；盈利性销售和服务需授权。
# 详情请参阅 LICENSE.md 文件。


import requests
import random
from typing import Optional, List, Dict
from bs4 import BeautifulSoup

from core.logger import get_logger

# 平台名称映射
PLATFORMS = [
    {"name": "微博", "zhiwei_id": "weibo", "tophub_id": "s.weibo.com"},
    {"name": "抖音", "zhiwei_id": "douyin", "tophub_id": "douyin.com"},
    {"name": "哔哩哔哩", "zhiwei_id": "bilibili", "tophub_id": "bilibili.com"},
    {"name": "今日头条", "zhiwei_id": "toutiao", "tophub_id": "toutiao.com"},
    {"name": "百度", "zhiwei_id": "baidu", "tophub_id": "baidu.com"},
    {"name": "小红书", "zhiwei_id": "little-red-book", "tophub_id": None},
    {"name": "快手", "zhiwei_id": "kuaishou", "tophub_id": None},
    {"name": "虎扑", "zhiwei_id": None, "tophub_id": "hupu.com"},
    {"name": "豆瓣小组", "zhiwei_id": None, "tophub_id": "douban.com"},
    {"name": "澎湃新闻", "zhiwei_id": None, "tophub_id": "thepaper.cn"},
    {"name": "知乎", "zhiwei_id": "zhihu", "tophub_id": "zhihu.com"},

    {"name": "微信", "zhiwei_id": None, "tophub_id": "wechat.com"},
    {"name": "实时榜中榜", "zhiwei_id": None, "tophub_id": "tophub.today"},
    {"name": "开源中国", "zhiwei_id": None, "tophub_id": "oschina.net"},
    {"name": "GitHub", "zhiwei_id": None, "tophub_id": "github.com"},
]

# 知微数据支持的平台
ZHIWEI_PLATFORMS = [p["zhiwei_id"] for p in PLATFORMS if p["zhiwei_id"]]

# tophub 支持的平台
TOPHUB_PLATFORMS = [p["tophub_id"] for p in PLATFORMS if p["tophub_id"]]

logger = get_logger()

def get_zhiwei_hotnews(platform: str) -> Optional[List[Dict]]:
    """
    获取知微数据的热点数据
    参数 platform: 平台标识 (weibo, douyin, bilibili, toutiao, baidu, little-red-book, kuaishou, zhihu)
    返回格式: 列表数据，每个元素为热点条目字典，仅包含 name, rank, lastCount, url
    """
    api_url = f"https://trends.zhiweidata.com/hotSearchTrend/search/longTimeInListSearch?type={platform}&sortType=realTime"  # noqa 501
    try:
        logger.info(f"---热点获取url:{api_url}")
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            # noqa 501
            "Referer": "https://trends.zhiweidata.com/",
        }
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()

        data = response.json()
        if data.get("state") and isinstance(data.get("data"), list):
            return [
                {
                    "name": item.get("name", ""),
                    "rank": item.get("rank", 0),
                    "lastCount": item.get("lastCount", 0),
                    "url": item.get("url", ""),
                }
                for item in data["data"]
            ]
        return None
    except Exception as e:  # noqa 841
        return None


def get_tophub_hotnews(platform: str, cnt: int = 10) -> Optional[List[Dict]]:
    """
    获取 tophub.today 的热点数据
    参数 platform: 平台名称（中文，如“微博”）
    参数 tophub_id: tophub.today 的平台标识（如 s.weibo.com, zhihu.com）
    参数 cnt: 返回的新闻数量
    返回格式: 列表数据，每个元素为热点条目字典，包含 name, rank, lastCount
    """
    api_url = "https://tophub.today/"
    try:
        logger.info(f"---热点获取url:{api_url}")

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            # noqa 501
        }
        response = requests.get(api_url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        platform_divs = soup.find_all("div", class_="cc-cd")

        for div in platform_divs:
            platform_span = div.find("div", class_="cc-cd-lb").find("span")
            if platform_span and platform_span.text.strip() == platform:
                news_items = div.find_all("div", class_="cc-cd-cb-ll")[:cnt]
                hotnews = []
                for item in news_items:
                    rank = item.find("span", class_="s").text.strip()
                    title = item.find("span", class_="t").text.strip()
                    engagement = item.find("span", class_="e")
                    last_count = engagement.text.strip() if engagement else "0"
                    hotnews.append(
                            {
                                "name": title,
                                "rank": int(rank),
                                "lastCount": last_count,
                                "url": item.find("a")["href"] if item.find("a") else "",
                            }
                    )
                return hotnews
        return None
    except Exception as e:  # noqa 841
        return None


def get_platform_news(platform: str, cnt: int = 30) -> List[Dict]:
    """
    获取指定平台的新闻数据，优先从知微数据获取，失败则从 tophub.today 获取
    参数 platform: 平台名称（中文，如"微博"）
    参数 cnt: 返回的新闻数量
    返回: 新闻数据列表，包含 name, rank, lastCount, url 字段
    """
    # 查找平台对应的知微数据标识和 tophub 标识
    platform_info = next((p for p in PLATFORMS if p["name"] == platform), None)
    if not platform_info:
        return []

    # 1. 优先尝试知微数据
    if platform_info["zhiwei_id"] in ZHIWEI_PLATFORMS:
        hotnews = get_zhiwei_hotnews(platform_info["zhiwei_id"])
        if hotnews:
            return hotnews[:cnt]

    # 2. 回退到 tophub.today
    if platform_info["tophub_id"] in TOPHUB_PLATFORMS:
        hotnews = get_tophub_hotnews(platform, cnt)
        if hotnews:
            return hotnews[:cnt]

    return []