"""Settings for the recipe scraper project."""
import os

from config.dishes_settings import URL_DICT

# set up base directories and paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRAPED_PATH = os.path.join(BASE_DIR, "db", "scraped.txt")
os.makedirs(os.path.join(BASE_DIR, "db"), exist_ok=True)
RECIPES_DIR = os.path.join(BASE_DIR, "recipes")
IMAGES_DIR = os.path.join(BASE_DIR, "images")

URLS = URL_DICT.values()

NOTION_TOKEN = os.getenv("NOTION_TOKEN")
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")

CATEGORY_RULES = {
    "荤菜": ["鸡", "鸭", "牛", "猪", "肉", "虾", "蟹", "排骨", "鱼", "培根", "腊肠", "三文鱼", "鱿鱼"],
    "素菜": ["豆腐", "青菜", "白菜", "西红柿", "土豆", "茄子", "黄瓜", "菜花", "西兰花", "金针菇", "木耳"],
    "点心": ["饼", "糕", "糯米", "馅", "包", "汤圆", "酥", "卷", "蛋挞", "饺子"],
    "主食": ["饭", "面", "米", "粉", "米线", "粥", "卷饼", "炒饭", "煲仔饭"],
    "汤": ["汤", "炖", "羹", "盅", "煲"]
}
