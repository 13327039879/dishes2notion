"""Search for recipe links on 下厨房 (xiachufang.com) based on dish names."""
import os
import time

import requests
from bs4 import BeautifulSoup

from config import settings


def get_dish_names():
    """Read dish names from a text file."""
    with open(os.path.join(settings.BASE_DIR, "toolings", "dish_names.txt"), "r") as f:
        return f.readlines()


def search_recipe_link(dish_name):
    """Search for a recipe link on 下厨房 based on the dish name."""
    search_url = f"https://www.xiachufang.com/search/?keyword={requests.utils.quote(dish_name)}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    try:
        response = requests.get(search_url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None
        soup = BeautifulSoup(response.text, 'html.parser')
        link_tag = soup.select_one('div.normal-recipe-list ul li a')
        if link_tag and link_tag['href']:
            return "https://www.xiachufang.com" + link_tag['href']
    except Exception:
        return None
    return None


if __name__ == '__main__':
    # main process
    url_dict = {}
    for name in get_dish_names():
        url = search_recipe_link(name)
        if url:
            url_dict[name] = url
            print(f"# ✅ 找到：{name} -> {url}")
        else:
            print(f"# ❌ 未找到：{name}")
        time.sleep(1)  # 防止请求过快被封

    for name, link in url_dict.items():
        print(f'"{name.strip()}": "{link}",')
