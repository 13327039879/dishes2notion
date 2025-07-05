import os
import json
from notion_client import Client
from config import settings  # 可放 token, db_id 也在 settings.py
from config.settings import RECIPES_DIR

# Notion API 配置
NOTION_TOKEN = settings.NOTION_TOKEN
DATABASE_ID = settings.DATABASE_ID

notion = Client(auth=NOTION_TOKEN)


def load_recipes(json_dir):
    files = [f for f in os.listdir(json_dir) if f.endswith(".json")]
    recipes = []
    for file in files:
        with open(os.path.join(json_dir, file), "r", encoding="utf-8") as f:
            recipes.append(json.load(f))
    return recipes


def create_notion_page(recipe):
    props = {
        "菜名": {"title": [{"text": {"content": recipe["菜名"]}}]},
        "链接": {"url": recipe["链接"]},
        "照片": {"files": [{"name": recipe["菜名"], "external": {"url": recipe["照片"]}}]},
        "食材清单": {"multi_select": [{"name": item} for item in recipe["食材清单"]]},
        "做法": {"rich_text": [{"text": {"content": part}}
        for step in recipe["做法"]
        for part in split_text(step)]},
        "类型": {"multi_select": [{"name": item} for item in recipe["类型"]]},
    }

    try:
        notion.pages.create(
            parent={"database_id": DATABASE_ID},
            properties=props
        )
        print(f"✅ 成功导入：{recipe['菜名']}")

    except Exception as e:
        print(f"❌ 导入失败：{recipe['菜名']}，错误：{e}")


def batch_import_to_notion(recipe_dir):
    existing_titles = fetch_existing_titles()
    recipes = load_recipes(recipe_dir)
    for recipe in recipes:
        if is_recipe_exists(recipe["菜名"], existing_titles):
            print(f"✅ 已存在：{recipe['菜名']}，跳过导入")
            continue
        create_notion_page(recipe)


def fetch_existing_titles():
    titles = set()
    start_cursor = None
    while True:
        response = notion.databases.query(
            database_id=DATABASE_ID,
            start_cursor=start_cursor,
            page_size=100
        )
        for row in response["results"]:
            title_prop = row["properties"].get("菜名", {}).get("title", [])
            if title_prop:
                titles.add(title_prop[0]["plain_text"])

        if not response.get("has_more"):
            break
        start_cursor = response["next_cursor"]
    return titles


def is_recipe_exists(recipe_name, existing_titles):
    if recipe_name in existing_titles:
        return True
    return False


def split_text(text, limit=2000):
    return [text[i:i+limit] for i in range(0, len(text), limit)]


if __name__ == "__main__":
    batch_import_to_notion(RECIPES_DIR)
