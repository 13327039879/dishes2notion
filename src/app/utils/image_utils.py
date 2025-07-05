"""Image utility functions."""
import os
import re

import requests


def safe_filename(name):
    """Sanitize a string to be used as a filename."""
    return re.sub(r'[\\/:*?"<>|]', "_", name)


def download_image(image_url, name, image_dir):
    """Download an image from a URL and save it to a directory."""
    if not image_url or image_url.startswith("（无图片）"):
        print("⚠️ 无主图，跳过下载")
        return
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            os.makedirs(image_dir, exist_ok=True)
            filename = safe_filename(name) + ".jpg"
            filepath = os.path.join(image_dir, filename)
            with open(filepath, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
            print(f"📥 主图已保存：{filepath}")
        else:
            print(f"❌ 下载失败：{image_url}")
    except Exception as e:
        print(f"❌ 图片下载异常：{e}")
