# 菜名 --> “下厨房”链接 --> notion note

https://www.notion.so/226ffb188c6d801f8b1ee2b714b273e9?v=226ffb188c6d81b6bc29000c397f1d1a&source=copy_link

## 使用方法
1. 清空 `src/toolings/dish_names.txt` 文件，输入菜名，每行一个。
2. 运行 `python src/toolings/xiachufang_search.py`。

## 运行过程
1. 读取 `src/toolings/dish_names.txt` 文件中的菜名。
2. 使用 `requests` 库向下厨房搜索菜名。
3. 解析返回的 HTML 内容，提取菜名和对应的链接。
4. 将菜名和链接输出到控制台。
5. 将菜名和链接的字典格式的数据写入 `src/config/dishes_settings.py` 文件。
6. 检查 `src/config/dishes_settings.py` 的大字典中是否有重复，如有重复则删除。
7. 运行 `python src/app/recipe_scraper.py`，将菜品链接转换为 notion 中的内容。
8. 查看 notion 中的新增内容。

## 注意事项
1. 由于“下厨房”有建议的防爬策略，失败后只需重试即可
