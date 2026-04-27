"""Unit tests for transform.py"""

import pytest
import pandas as pd
from etl.transform import (
    build_dim_date,
    build_dim_product,
    build_dim_customer,
    build_dim_region,
    build_fact_sales,
)

# ── Fixtures ──────────────────────────────────────────────────

@pytest.fixture
def sample_orders():
    return pd.DataFrame({
        "order_id":     ["ORD001", "ORD002", "ORD003"],
        "order_date":   ["2023-01-15", "2023-03-20", "2023-06-01"],
        "customer_id":  ["CUST001", "CUST002", "CUST001"],
        "product_id":   ["PROD001", "PROD002", "PROD001"],
        "quantity":     [2, 1, 3],
        "unit_price":   [50.0, 120.0, 50.0],
        "discount":     [0.0, 0.1, 0.05],
        "revenue":      [100.0, 108.0, 142.50],
        "shipping_cost":[5.0, 8.0, 5.0],
        "order_status": ["completed", "completed", "returned"],
        "payment_method": ["Credit Card", "PayPal", "Credit Card"],
    })

@pytest.fixture
def sample_products():
    return pd.DataFrame({
        "product_id":   ["PROD001", "PROD002"],
        "product_name": ["Widget A", "Gadget B"],
        "category":     ["Electronics", "Toys"],
        "sub_category": ["Accessories", "Action Figures"],
        "unit_price":   [50.0, 120.0],
        "cost_price":   [30.0, 80.0],
        "supplier":     ["Supplier X", "Supplier Y"],
        "in_stock":     [True, False],
    })

@pytest.fixture
def sample_customers():
    return pd.DataFrame({
        "customer_id":       ["CUST001", "CUST002"],
        "first_name":        ["Alice", "Bob"],
        "last_name":         ["Smith", "Jones"],
        "email":             ["alice@example.com", "bob@example.com"],
        "country":           ["USA", "Canada"],
        "region":            ["North", "East"],
        "customer_segment":  ["Gold", "Silver"],
        "signup_date":       ["2020-06-01", "2021-01-15"],
    })


# ── Tests: dim_date ───────────────────────────────────────────

def test_dim_date_row_count(sample_orders):
    df = build_dim_date(sample_orders)
    assert len(df) == 3

def test_dim_date_columns(sample_orders):
    df = build_dim_date(sample_orders)
    for col in ["date_key", "full_date", "year", "quarter", "month", "is_weekend"]:
        assert col in df.columns

def test_dim_date_key_is_int(sample_orders):
    df = build_dim_date(sample_orders)
    assert df["date_key"].dtype in ["int32", "int64"]

def test_dim_date_no_duplicates(sample_orders):
    df = build_dim_date(sample_orders)
    assert df["date_key"].nunique() == len(df)


# ── Tests: dim_product ────────────────────────────────────────

def test_dim_product_margin(sample_products):
    df = build_dim_product(sample_products)
    # (50-30)/50 * 100 = 40%
    assert df.loc[df["product_id"] == "PROD001", "margin_pct"].values[0] == pytest.approx(40.0)

def test_dim_product_no_nulls_in_key(sample_products):
    df = build_dim_product(sample_products)
    assert df["product_id"].notna().all()


# ── Tests: dim_customer ───────────────────────────────────────

def test_dim_customer_full_name(sample_customers):
    df = build_dim_customer(sample_customers)
    assert "Alice Smith" in df["full_name"].values

def test_dim_customer_email_lowercase(sample_customers):
    df = build_dim_customer(sample_customers)
    assert all(df["email"] == df["email"].str.lower())


# ── Tests: dim_region ─────────────────────────────────────────

def test_dim_region_unique_combos(sample_customers):
    df = build_dim_region(sample_customers)
    assert len(df) == 2

def test_dim_region_has_key(sample_customers):
    df = build_dim_region(sample_customers)
    assert "region_key" in df.columns


# ── Tests: fact_sales ─────────────────────────────────────────

def test_fact_sales_row_count(sample_orders, sample_customers, sample_products):
    dim_date     = build_dim_date(sample_orders)
    dim_customer = build_dim_customer(sample_customers)
    dim_region   = build_dim_region(sample_customers)
    fact         = build_fact_sales(sample_orders, dim_date, dim_customer, dim_region)
    assert len(fact) == 3

def test_fact_sales_gross_profit(sample_orders, sample_customers):
    dim_date     = build_dim_date(sample_orders)
    dim_customer = build_dim_customer(sample_customers)
    dim_region   = build_dim_region(sample_customers)
    fact         = build_fact_sales(sample_orders, dim_date, dim_customer, dim_region)
    row = fact[fact["order_id"] == "ORD001"].iloc[0]
    assert row["gross_profit"] == pytest.approx(100.0 - 5.0)

def test_fact_sales_no_null_order_ids(sample_orders, sample_customers):
    dim_date     = build_dim_date(sample_orders)
    dim_customer = build_dim_customer(sample_customers)
    dim_region   = build_dim_region(sample_customers)
    fact         = build_fact_sales(sample_orders, dim_date, dim_customer, dim_region)
    assert fact["order_id"].notna().all()
