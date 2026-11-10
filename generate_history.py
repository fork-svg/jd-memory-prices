#!/usr/bin/env python3
"""
生成历史测试数据
"""

import json
import random
from datetime import datetime, timedelta
from pathlib import Path

# 基础价格数据
BASE_PRICES = {
    "100012345001": {"base": 329, "variance": 30, "name": "金士顿 FURY 16GB DDR4", "category": "DDR4内存", "brand": "金士顿", "capacity": "16GB", "type": "DDR4"},
    "100012345002": {"base": 599, "variance": 50, "name": "金士顿 FURY 32GB DDR4", "category": "DDR4内存", "brand": "金士顿", "capacity": "32GB", "type": "DDR4"},
    "100012345003": {"base": 449, "variance": 40, "name": "芝奇幻光戟 16GB DDR4", "category": "DDR4内存", "brand": "芝奇", "capacity": "16GB", "type": "DDR4"},
    "100012345004": {"base": 799, "variance": 70, "name": "芝奇幻光戟 32GB DDR4", "category": "DDR4内存", "brand": "芝奇", "capacity": "32GB", "type": "DDR4"},
    "100012345005": {"base": 399, "variance": 35, "name": "海盗船复仇者 16GB DDR4", "category": "DDR4内存", "brand": "海盗船", "capacity": "16GB", "type": "DDR4"},
    "100012345006": {"base": 699, "variance": 60, "name": "海盗船复仇者 32GB DDR4", "category": "DDR4内存", "brand": "海盗船", "capacity": "32GB", "type": "DDR4"},
    "100012345007": {"base": 279, "variance": 25, "name": "英睿达 16GB DDR4", "category": "DDR4内存", "brand": "英睿达", "capacity": "16GB", "type": "DDR4"},
    "100012345008": {"base": 499, "variance": 45, "name": "英睿达 32GB DDR4", "category": "DDR4内存", "brand": "英睿达", "capacity": "32GB", "type": "DDR4"},
    "100012345009": {"base": 399, "variance": 35, "name": "金百达银爵 16GB DDR5", "category": "DDR5内存", "brand": "金百达", "capacity": "16GB", "type": "DDR5"},
    "100012345010": {"base": 749, "variance": 65, "name": "金百达银爵 32GB DDR5", "category": "DDR5内存", "brand": "金百达", "capacity": "32GB", "type": "DDR5"},
    "100012345011": {"base": 999, "variance": 90, "name": "芝奇焰锋戟 32GB DDR5", "category": "DDR5内存", "brand": "芝奇", "capacity": "32GB", "type": "DDR5"},
    "100012345012": {"base": 1899, "variance": 150, "name": "芝奇焰锋戟 64GB DDR5", "category": "DDR5内存", "brand": "芝奇", "capacity": "64GB", "type": "DDR5"},
}


def generate_day_data(date_str: str) -> dict:
    """生成某一天的价格数据"""
    products = []

    for product_id, info in BASE_PRICES.items():
        price = info["base"] + random.uniform(-info["variance"], info["variance"])
        price = round(price, 2)
        in_stock = random.random() > 0.1

        product_data = {
            "id": product_id,
            "name": info["name"],
            "category": info["category"],
            "brand": info["brand"],
            "capacity": info["capacity"],
            "type": info["type"],
            "url": f"https://item.jd.com/{product_id}.html",
            "price": price if in_stock else None,
            "original_price": round(price * 1.15, 2) if random.random() > 0.6 and in_stock else None,
            "in_stock": in_stock,
            "coupon": round(random.uniform(10, 30), 2) if random.random() > 0.7 and in_stock else None,
        }
        products.append(product_data)

    return {
        "date": date_str,
        "timestamp": f"{date_str}T10:00:00.000000",
        "source": "simulated",
        "products": products
    }


def main():
    """生成过去30天的历史数据"""
    data_dir = Path(__file__).parent / "data"
    data_dir.mkdir(exist_ok=True)

    today = datetime.now()

    for i in range(30, -1, -1):
        date = today - timedelta(days=i)
        date_str = date.strftime("%Y-%m-%d")
        data_file = data_dir / f"{date_str}.json"

        if not data_file.exists():
            data = generate_day_data(date_str)
            with open(data_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"生成数据: {date_str}")

    print("✅ 历史数据生成完成")


if __name__ == "__main__":
    main()
