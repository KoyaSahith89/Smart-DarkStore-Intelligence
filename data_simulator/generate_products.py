import pandas as pd
import random
from faker import Faker

fake = Faker()

CATEGORIES = [
    "Dairy", "Beverages", "Snacks", "Bakery", "Fruits",
    "Vegetables", "Personal Care", "Cleaning", "Frozen",
    "Meat", "Seafood", "Pharmacy", "Baby Care", "Pet Care",
    "Stationery", "Electronics", "Home Essentials",
    "Spices", "Grains", "Ready to Eat"
]

def generate_products(skus_per_category=12):
    products = []
    sku_id = 1

    for category in CATEGORIES:
        for _ in range(skus_per_category):
            cost = random.randint(10, 300)
            margin = random.uniform(0.1, 0.4)
            price = round(cost * (1 + margin), 2)

            product = {
                "sku_id": sku_id,
                "product_name": fake.word().capitalize() + " " + category,
                "category": category,
                "cost_price": cost,
                "selling_price": price,
                "margin_percent": round(margin * 100, 2),
                "shelf_life_days": random.choice([3, 7, 15, 30, 90, 180]),
                "is_perishable": random.choice([0, 1])
            }

            products.append(product)
            sku_id += 1

    df = pd.DataFrame(products)
    return df


if __name__ == "__main__":
    df = generate_products()
    print(df.head())
