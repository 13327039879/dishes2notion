# 菜名 --> “下厨房”链接 --> notion note

https://www.notion.so/226ffb188c6d801f8b1ee2b714b273e9?v=226ffb188c6d81b6bc29000c397f1d1a&source=copy_link

## Notion Note 示例
### 菜单
![菜单.png](readme_pictures%2F%E8%8F%9C%E5%8D%95.png)

### 分类
![分类.png](readme_pictures%2F%E5%88%86%E7%B1%BB.png)

### 清单
![清单.png](readme_pictures%2F%E6%B8%85%E5%8D%95.png)

### 计划
![计划.png](readme_pictures%2F%E8%AE%A1%E5%88%92.png)

### 备菜
![备菜.png](readme_pictures%2F%E5%A4%87%E8%8F%9C.png)

## 使用方法
1. 开发调试环境基于 Python 3.12.3 环境。其他 Python 版本未经过任何测试。
2. 清空 `src/toolings/dish_names.txt` 文件，输入菜名，每行一个。
3. 运行 `python src/toolings/xiachufang_search.py`。

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
