import json
import os
import requests
from bs4 import BeautifulSoup

from app.utils.image_utils import safe_filename
from app.utils.notion_utils import batch_import_to_notion
from config.settings import URLS, SCRAPED_PATH, RECIPES_DIR, IMAGES_DIR, CATEGORY_RULES


def fetch_recipe(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')

    title_tag = soup.find('h1', class_='page-title')
    title = title_tag.get_text(strip=True) if title_tag else '未知菜名'

    intro_tag = soup.find('div', class_='desc mt10')
    intro = intro_tag.get_text(strip=True) if intro_tag else '（无简介）'

    # 主图
    img = soup.select_one('div.cover.image.expandable img')
    image_url = img['src'] if img and 'src' in img.attrs else '（无图片）'

    ingredients = []
    ings_wrapper = soup.find('div', class_='ings')
    if ings_wrapper:
        for li in ings_wrapper.find_all('li'):
            name_tag = li.find('span', class_='name')
            amount_tag = li.find('span', class_='unit')
            name = name_tag.get_text(strip=True) if name_tag else ''
            amount = amount_tag.get_text(strip=True) if amount_tag else ''
            if name:
                ingredients.append(f"{name}：{amount}")

    steps = []
    step_tags = soup.select('div.steps > ol > li')
    for i, li in enumerate(step_tags, 1):
        step_text = li.get_text(strip=True)
        if step_text:
            steps.append(f"{i}. {step_text}")

    return {
        '菜名': title,
        '照片': image_url,
        '食材清单': ingredients,
        '做法': steps,
        '链接': url,
        '类型': classify_recipe(title),
    }


def load_scraped(path):
    if not os.path.exists(path):
        return set()
    with open(path, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())


def append_scraped(name, url, path):
    with open(path, "a", encoding="utf-8") as f:
        f.write(name + "\n")
        f.write(url + "\n")


def save_recipe_as_json(data, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    filename = safe_filename(data['菜名']) + ".json"
    filepath = os.path.join(output_dir, filename)
    try:
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"📝 已保存为 JSON：{filepath}")
    except Exception as e:
        print(f"❌ 保存 JSON 失败：{e}")


def classify_recipe(name):
    """
    根据菜名进行五大类分类：荤菜、素菜、点心、主食、汤
    如果都不匹配则返回“其他”
    """
    categories = set()
    for category, keywords in CATEGORY_RULES.items():
        if any(kw in name for kw in keywords):
            categories.add(category)
            return list(categories)
    categories.add("其他")
    return list(categories)


if __name__ == '__main__':
    scraped_urls = load_scraped(SCRAPED_PATH)

    for url in URLS:
        if url in scraped_urls:
            print(f"✅ 已跳过：{url}")
            continue

        print(f"\n🚀 抓取中：{url}")
        data = fetch_recipe(url)
        if not data:
            print(f"❌ 抓取失败：{url}")
            continue

        print(f"🍽️ 菜名：{data['菜名']}")
        print(f"📷 照片：{data['照片']}")
        print(f"🍽️ 类型：{data['类型']}")
        print("🥬 食材清单：")
        for ing in data['食材清单']:
            print(f"  - {ing}")
        print("👣 做法：")
        for step in data['做法']:
            print(f"  {step}")
        # 下载主图到 images/
        # download_image(data['照片'], data['菜名'], IMAGES_DIR)
        save_recipe_as_json(data, RECIPES_DIR)

        append_scraped(data['菜名'], url, SCRAPED_PATH)

    # 批量导入到 Notion
    batch_import_to_notion(RECIPES_DIR)
