"""
generate_sample_data.py
-----------------------
Creates realistic sample CSVs in data/sample/ for dev & testing.
Run: python generate_sample_data.py
"""

import os
import random
import pandas as pd
from faker import Faker
from datetime import datetime, timedelta
from config import SAMPLE_DATA_DIR, SAMPLE_ROW_COUNT

fake = Faker()
random.seed(42)
Faker.seed(42)

CATEGORIES = ["Electronics", "Clothing", "Home & Garden", "Sports", "Books", "Toys", "Beauty"]
REGIONS    = ["North", "South", "East", "West", "Central"]
COUNTRIES  = ["USA", "Canada", "UK", "Germany", "Australia"]
STATUSES   = ["completed", "returned", "pending", "cancelled"]


def generate_customers(n: int = 500) -> pd.DataFrame:
    rows = []
    for i in range(1, n + 1):
        rows.append({
            "customer_id":    f"CUST{i:05d}",
            "first_name":     fake.first_name(),
            "last_name":      fake.last_name(),
            "email":          fake.email(),
            "country":        random.choice(COUNTRIES),
            "region":         random.choice(REGIONS),
            "signup_date":    fake.date_between(start_date="-5y", end_date="-6m"),
            "customer_segment": random.choice(["Bronze", "Silver", "Gold", "Platinum"]),
        })
    return pd.DataFrame(rows)


def generate_products(n: int = 200) -> pd.DataFrame:
    rows = []
    for i in range(1, n + 1):
        category = random.choice(CATEGORIES)
        rows.append({
            "product_id":   f"PROD{i:05d}",
            "product_name": fake.bs().title()[:50],
            "category":     category,
            "sub_category": fake.word().title(),
            "unit_price":   round(random.uniform(5.0, 500.0), 2),
            "cost_price":   round(random.uniform(2.0, 300.0), 2),
            "supplier":     fake.company(),
            "in_stock":     random.choice([True, False]),
        })
    return pd.DataFrame(rows)


def generate_orders(customers: pd.DataFrame, products: pd.DataFrame, n: int = SAMPLE_ROW_COUNT) -> pd.DataFrame:
    rows = []
    start_date = datetime(2022, 1, 1)
    end_date   = datetime(2024, 12, 31)
    delta_days = (end_date - start_date).days

    for i in range(1, n + 1):
        order_date  = start_date + timedelta(days=random.randint(0, delta_days))
        quantity    = random.randint(1, 10)
        product     = products.sample(1).iloc[0]
        customer    = customers.sample(1).iloc[0]
        unit_price  = product["unit_price"]
        discount    = round(random.choice([0, 0, 0, 0.05, 0.10, 0.15, 0.20]), 2)
        revenue     = round(unit_price * quantity * (1 - discount), 2)

        rows.append({
            "order_id":       f"ORD{i:07d}",
            "order_date":     order_date.strftime("%Y-%m-%d"),
            "customer_id":    customer["customer_id"],
            "product_id":     product["product_id"],
            "quantity":       quantity,
            "unit_price":     unit_price,
            "discount":       discount,
            "revenue":        revenue,
            "shipping_cost":  round(random.uniform(0, 25), 2),
            "order_status":   random.choices(STATUSES, weights=[70, 10, 15, 5])[0],
            "payment_method": random.choice(["Credit Card", "PayPal", "Debit Card", "Bank Transfer"]),
        })
    return pd.DataFrame(rows)


def main():
    os.makedirs(SAMPLE_DATA_DIR, exist_ok=True)

    print("Generating customers...")
    customers = generate_customers(500)
    customers.to_csv(f"{SAMPLE_DATA_DIR}/customers.csv", index=False)
    print(f"  ✓ {len(customers)} customers → data/sample/customers.csv")

    print("Generating products...")
    products = generate_products(200)
    products.to_csv(f"{SAMPLE_DATA_DIR}/products.csv", index=False)
    print(f"  ✓ {len(products)} products → data/sample/products.csv")

    print(f"Generating {SAMPLE_ROW_COUNT:,} orders...")
    orders = generate_orders(customers, products)
    orders.to_csv(f"{SAMPLE_DATA_DIR}/orders.csv", index=False)
    print(f"  ✓ {len(orders):,} orders → data/sample/orders.csv")

    print("\nSample data generation complete.")


if __name__ == "__main__":
    main()
