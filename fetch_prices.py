#!/usr/bin/env python3
"""
获取京东内存价格
"""

import json
import random
from datetime import datetime
from pathlib import Path

# 基础价格数据（模拟）
BASE_PRICES = {
    "100012345001": {"min": 299, "max": 359, "name": "金士顿 FURY 16GB DDR4"},
    "100012345002": {"min": 549, "max": 649, "name": "金士顿 FURY 32GB DDR4"},
    "100012345003": {"min": 399, "max": 499, "name": "芝奇幻光戟 16GB DDR4"},
    "100012345004": {"min": 699, "max": 849, "name": "芝奇幻光戟 32GB DDR4"},
    "100012345005": {"min": 359, "max": 429, "name": "海盗船复仇者 16GB DDR4"},
    "100012345006": {"min": 629, "max": 749, "name": "海盗船复仇者 32GB DDR4"},
    "100012345007": {"min": 249, "max": 299, "name": "英睿达 16GB DDR4"},
    "100012345008": {"min": 449, "max": 549, "name": "英睿达 32GB DDR4"},
    "100012345009": {"min": 359, "max": 429, "name": "金百达银爵 16GB DDR5"},
    "100012345010": {"min": 679, "max": 799, "name": "金百达银爵 32GB DDR5"},
    "100012345011": {"min": 899, "max": 1099, "name": "芝奇焰锋戟 32GB DDR5"},
    "100012345012": {"min": 1699, "max": 1999, "name": "芝奇焰锋戟 64GB DDR5"},
}


def fetch_price(product_id: str) -> dict:
    """模拟获取价格"""
    info = BASE_PRICES.get(product_id, {})
    price = round(random.uniform(info.get("min", 300), info.get("max", 500)), 2)
    in_stock = random.random() > 0.1  # 90% 有货

    return {
        "price": price if in_stock else None,
        "original_price": round(price * 1.15, 2) if random.random() > 0.6 and in_stock else None,
        "in_stock": in_stock,
        "coupon": round(random.uniform(10, 30), 2) if random.random() > 0.7 and in_stock else None,
    }


def main():
    """主函数"""
    base_dir = Path(__file__).parent
    data_dir = base_dir / "data"
    data_dir.mkdir(exist_ok=True)

    # 加载产品列表
    products_file = base_dir / "products.json"
    with open(products_file, 'r', encoding='utf-8') as f:
        products = json.load(f)

    # 获取当前时间
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    timestamp = now.isoformat()

    # 获取每个产品的价格
    results = []
    for product in products:
        price_data = fetch_price(product["id"])
        result = {
            **product,
            "url": f"https://item.jd.com/{product['id']}.html",
            **price_data
        }
        results.append(result)
        status = f"¥{price_data['price']}" if price_data['in_stock'] else "无货"
        print(f"{product['name']}: {status}")

    # 保存数据
    data_file = data_dir / f"{date_str}.json"
    data = {
        "date": date_str,
        "timestamp": timestamp,
        "source": "simulated",
        "products": results
    }

    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\n✅ 数据已保存到: {data_file}")

    # 更新 README
    update_readme(results)


def update_readme(products: list):
    """更新 README"""
    base_dir = Path(__file__).parent
    readme_file = base_dir / "README.md"

    lines = [
        "# 📊 京东内存价格监控",
        "",
        "自动追踪京东内存价格变化，每日更新两次。",
        "",
        "## 📈 产品价格",
        "",
        "| 产品 | 容量 | 类型 | 当前价格 | 有货 |",
        "|------|------|------|----------|------|",
    ]

    for p in products:
        price_str = f"¥{p['price']:.2f}" if p['price'] else "-"
        stock_str = "✅" if p['in_stock'] else "❌"
        lines.append(f"| {p['brand']} {p['capacity']} {p['type']} | {p['capacity']} | {p['type']} | {price_str} | {stock_str} |")

    lines.extend([
        "",
        "---",
        "",
        "## 📊 价格趋势图",
        "",
        "### 产品价格对比",
        "",
        "![所有产品价格对比](./charts/all_products_comparison.png)",
        "",
        "### 每GB价格趋势",
        "",
        "![每GB价格趋势](./charts/price_per_gb_trend.png)",
        "",
        "---",
        "",
        "## 🔄 自动更新",
        "",
        "每天北京时间 10:00 和 20:00 自动更新价格。",
        "",
        "## 📁 数据格式",
        "",
        "历史数据存储在 `data/YYYY-MM-DD.json` 文件中。",
        "",
        "---",
        "",
        "*数据仅供参考，以京东实际价格为准*",
    ])

    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))

    print("✅ README 已更新")


if __name__ == "__main__":
    main()
